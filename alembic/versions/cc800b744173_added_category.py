"""Added category

Revision ID: cc800b744173
Revises: 1d2170a0cbc1
Create Date: 2024-12-10 00:20:12.318353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc800b744173'
down_revision: Union[str, None] = '1d2170a0cbc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading_materials', sa.Column('category', sa.String(), nullable=False))
    op.add_column('words', sa.Column('category', sa.String(), nullable=False))
    op.add_column('words', sa.Column('pronunciation_category', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('words', 'pronunciation_category')
    op.drop_column('words', 'category')
    op.drop_column('reading_materials', 'category')
    # ### end Alembic commands ###
