"""Added AQ5 until AQ20 to person

Revision ID: 2045d4eac8a5
Revises: 09101af145b7
Create Date: 2025-04-01 16:37:50.187515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2045d4eac8a5'
down_revision = '09101af145b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('AQ5', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ6', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ7', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ8', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ9', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ10', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ11', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ12', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ13', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ14', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ15', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ16', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ17', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ18', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ19', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('AQ20', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_column('AQ20')
        batch_op.drop_column('AQ19')
        batch_op.drop_column('AQ18')
        batch_op.drop_column('AQ17')
        batch_op.drop_column('AQ16')
        batch_op.drop_column('AQ15')
        batch_op.drop_column('AQ14')
        batch_op.drop_column('AQ13')
        batch_op.drop_column('AQ12')
        batch_op.drop_column('AQ11')
        batch_op.drop_column('AQ10')
        batch_op.drop_column('AQ9')
        batch_op.drop_column('AQ8')
        batch_op.drop_column('AQ7')
        batch_op.drop_column('AQ6')
        batch_op.drop_column('AQ5')

    # ### end Alembic commands ###
