"""create emp_payment_record table

Revision ID: 187ea3307c06
Revises: 66b7a3c8e5a5
Create Date: 2024-01-02 19:19:14.662249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '187ea3307c06'
down_revision: Union[str, None] = '66b7a3c8e5a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emp_payment_records',
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('month_id', sa.Integer(), nullable=False),
    sa.Column('is_full_paid', sa.Boolean(), nullable=True),
    sa.Column('payment_amount', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.emp_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['month_id'], ['months.month_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.session_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('employee_id', 'session_id', 'month_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emp_payment_records')
    # ### end Alembic commands ###
