"""empty message

Revision ID: b666a0d3eac1
Revises: 445aeebf4b25
Create Date: 2021-11-15 19:04:56.359929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b666a0d3eac1'
down_revision = '445aeebf4b25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'user_id')
    # ### end Alembic commands ###