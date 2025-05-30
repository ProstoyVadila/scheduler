"""create tasks table

Revision ID: 0ae7f80622ec
Revises: 
Create Date: 2025-04-08 18:06:03.929746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ae7f80622ec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('cron', sa.String(length=255), nullable=False),
    sa.Column('command', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('SCHEDULED', 'CACHED', 'RUNNING', 'SUCCESS', 'FAILED', name='taskstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('last_run', sa.DateTime(timezone=True), nullable=True),
    sa.Column('next_run', sa.DateTime(timezone=True), nullable=True),
    sa.Column('retries', sa.Integer(), nullable=True),
    sa.Column('max_retries', sa.Integer(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###
