"""category changed to string

Revision ID: 1d2170a0cbc1
Revises: 17cb206b88f2
Create Date: 2024-12-09 23:45:41.907311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d2170a0cbc1'
down_revision: Union[str, None] = '17cb206b88f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category', sa.String(), nullable=False))
    op.drop_column('questions', 'category_id')
    op.add_column('users', sa.Column('reset_password_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reset_password_expires', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'reset_password_expires')
    op.drop_column('users', 'reset_password_token')
    op.add_column('questions', sa.Column('category_id', sa.INTEGER(), nullable=False))
    op.drop_column('questions', 'category')
    # ### end Alembic commands ###