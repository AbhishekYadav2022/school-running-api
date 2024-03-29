"""create exams table

Revision ID: e52177d771c8
Revises: c4dac1c643be
Create Date: 2024-01-02 18:48:42.493428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e52177d771c8'
down_revision: Union[str, None] = 'c4dac1c643be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exams',
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('exam_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('exam_id', 'exam_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exams')
    # ### end Alembic commands ###
