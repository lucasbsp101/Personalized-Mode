import logging
from logging.config import fileConfig
import os  # << ADICIONE ESTA LINHA

from flask import current_app  # Mantenha para target_metadata

from alembic import context
from sqlalchemy import pool, engine_from_config  # << VERIFIQUE SE engine_from_config ESTÁ IMPORTADO

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:  # Corrigido de fileConfig(config.config_file_name) para a condição correta
    fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# --- INÍCIO DA MODIFICAÇÃO SUGERIDA ---
# Tenta definir sqlalchemy.url diretamente da variável de ambiente DATABASE_URL
# Isso é mais robusto para ambientes de build.
database_url_env = os.getenv('DATABASE_URL')
if database_url_env:
    # Garante compatibilidade com URLs do Heroku/Render (postgres:// -> postgresql://)
    if database_url_env.startswith("postgres://"):
        database_url_env = database_url_env.replace("postgres://", "postgresql://", 1)
    config.set_main_option('sqlalchemy.url', database_url_env)
    logger.info(f"Alembic using DATABASE_URL from environment: {database_url_env[:30]}...")  # Log para verificação
else:
    # Fallback para a lógica original usando current_app (se DATABASE_URL não estiver no env)
    # (Mantenha suas funções get_engine e get_engine_url aqui se esta parte for usada)
    logger.warning("DATABASE_URL not found in environment for Alembic, attempting current_app.")
    # A sua lógica original com get_engine_url() iria aqui
    # Por exemplo (simplificado, adapte se suas funções get_engine/get_engine_url são diferentes):
    try:
        engine_url_from_app = current_app.extensions['migrate'].db.engine.url.render_as_string(
            hide_password=False).replace('%', '%%')
        config.set_main_option('sqlalchemy.url', engine_url_from_app)
    except Exception as e:
        logger.error(f"Could not get engine URL from current_app: {e}")
        # Se falhar, defina um placeholder ou levante um erro para indicar que a URL não foi configurada
        # Exemplo: config.set_main_option('sqlalchemy.url', 'sqlite:///fallback_for_alembic_error.db')
        raise RuntimeError("Alembic could not determine database URL.")

# --- FIM DA MODIFICAÇÃO SUGERIDA ---


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# Esta parte para pegar o target_metadata do current_app geralmente funciona bem
target_db = current_app.extensions['migrate'].db


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


target_metadata = get_metadata()  # Definindo target_metadata aqui


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    # url é pego da configuração já definida (seja do os.getenv ou do current_app)
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True  # Usando target_metadata definido globalmente
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    # engine_from_config usará a 'sqlalchemy.url' que foi definida no início do script
    connectable = engine_from_config(
        config.get_section(config.main_option_name()),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # Usando target_metadata definido globalmente
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()