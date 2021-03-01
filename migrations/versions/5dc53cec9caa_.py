"""empty message

Revision ID: 5dc53cec9caa
Revises: cab55d22a896
Create Date: 2021-03-02 00:10:39.716468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dc53cec9caa'
down_revision = 'cab55d22a896'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sys_admin', sa.Column('status', sa.SmallInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sys_admin', 'status')
    # ### end Alembic commands ###