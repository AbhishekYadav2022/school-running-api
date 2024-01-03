"""create other_fees table

Revision ID: 527c0c1caaa3
Revises: 509ba957384f
Create Date: 2024-01-02 19:15:52.535747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '527c0c1caaa3'
down_revision: Union[str, None] = '509ba957384f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('other_fees',
    sa.Column('other_id', sa.Integer(), nullable=False),
    sa.Column('fees_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('other_id')
    )
    op.create_unique_constraint(None, 'exams', ['exam_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exams', type_='unique')
    op.drop_table('other_fees')
    # ### end Alembic commands ###
