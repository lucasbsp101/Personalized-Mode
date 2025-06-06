import logging
import os
from logging.config import fileConfig

from alembic import context
from flask import current_app
from sqlalchemy import pool, engine_from_config

# --- Configuração do Logging ---
# Interpreta o arquivo .ini para configurar o logging.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# --- DEFINIÇÃO DA URL DO BANCO DE DADOS PARA PRODUÇÃO ---
# Esta é a parte mais importante para o Render.
# Lemos a variável de ambiente DATABASE_URL.
database_url = os.getenv('DATABASE_URL')

# O Render usa "postgres://", mas SQLAlchemy prefere "postgresql://"
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Se a variável não for encontrada (ambiente local, por exemplo),
# tentamos pegar da configuração do Flask.
if not database_url:
    try:
        database_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        logger.info("Usando a URL do banco de dados da configuração do Flask.")
    except Exception:
        logger.error("ERRO: DATABASE_URL não está definida e não foi possível acessar a configuração do Flask.")
        raise ValueError("Não foi possível determinar a URL do banco de dados para o Alembic.")

# Injeta a URL do banco de dados na configuração do Alembic.
config.set_main_option('sqlalchemy.url', database_url)
logger.info(f"Alembic configurado para usar o banco de dados: {database_url[:30]}...") # Log para confirmar

# --- Configuração do Target Metadata para Autogenerate ---
# Pega os metadados do modelo do Flask-SQLAlchemy para que as migrações automáticas funcionem.
target_db = current_app.extensions['migrate'].db
target_metadata = target_db.metadata

def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline'.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações em modo 'online'.
    """
    # Usa a engine_from_config, que lerá a 'sqlalchemy.url' que definimos acima.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()