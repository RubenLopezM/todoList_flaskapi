"""empty message

Revision ID: 445aeebf4b25
Revises: fd12ada04390
Create Date: 2021-11-15 18:58:48.836111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '445aeebf4b25'
down_revision = 'fd12ada04390'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('text', sa.String(length=120), nullable=False))
    op.add_column('task', sa.Column('done', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'done')
    op.drop_column('task', 'text')
    # ### end Alembic commands ###
