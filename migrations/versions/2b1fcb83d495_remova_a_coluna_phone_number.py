"""remova a coluna phone_number

Revision ID: 2b1fcb83d495
Revises: d10edffdfe1f
Create Date: 2025-03-17 18:03:44.859472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b1fcb83d495'
down_revision = 'd10edffdfe1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_person_phone_number'), ['phone_number'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_person_phone_number'))

    # ### end Alembic commands ###
