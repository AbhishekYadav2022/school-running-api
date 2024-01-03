"""create other_fees_details table

Revision ID: 66b7a3c8e5a5
Revises: b5aed6677aad
Create Date: 2024-01-02 19:18:26.762074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66b7a3c8e5a5'
down_revision: Union[str, None] = 'b5aed6677aad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('other_fees_details',
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('other_fees_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('fees_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['std_classes.class_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['other_fees_id'], ['other_fees.other_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.session_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('session_id', 'other_fees_id', 'class_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('other_fees_details')
    # ### end Alembic commands ###