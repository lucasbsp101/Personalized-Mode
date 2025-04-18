"""Added all columns to person

Revision ID: 5b3568043733
Revises: 
Create Date: 2025-04-02 10:35:17.878579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b3568043733'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('learning_preference', sa.String(length=50), nullable=False),
    sa.Column('test_1_score', sa.Integer(), nullable=True),
    sa.Column('test_2_score', sa.Integer(), nullable=True),
    sa.Column('grade_test_1', sa.Integer(), nullable=True),
    sa.Column('grade_test_2', sa.Integer(), nullable=True),
    sa.Column('hobbies', sa.String(length=500), nullable=True),
    sa.Column('work', sa.String(length=500), nullable=True),
    sa.Column('feedback', sa.String(length=500), nullable=True),
    sa.Column('AQ1', sa.String(length=500), nullable=True),
    sa.Column('AQ2', sa.String(length=500), nullable=True),
    sa.Column('AQ3', sa.String(length=500), nullable=True),
    sa.Column('AQ4', sa.String(length=500), nullable=True),
    sa.Column('AQ5', sa.String(length=500), nullable=True),
    sa.Column('AQ6', sa.String(length=500), nullable=True),
    sa.Column('AQ7', sa.String(length=500), nullable=True),
    sa.Column('AQ8', sa.String(length=500), nullable=True),
    sa.Column('AQ9', sa.String(length=500), nullable=True),
    sa.Column('AQ10', sa.String(length=500), nullable=True),
    sa.Column('AQ11', sa.String(length=500), nullable=True),
    sa.Column('AQ12', sa.String(length=500), nullable=True),
    sa.Column('AQ13', sa.String(length=500), nullable=True),
    sa.Column('AQ14', sa.String(length=500), nullable=True),
    sa.Column('AQ15', sa.String(length=500), nullable=True),
    sa.Column('AQ16', sa.String(length=500), nullable=True),
    sa.Column('AQ17', sa.String(length=500), nullable=True),
    sa.Column('AQ18', sa.String(length=500), nullable=True),
    sa.Column('AQ19', sa.String(length=500), nullable=True),
    sa.Column('AQ20', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###
