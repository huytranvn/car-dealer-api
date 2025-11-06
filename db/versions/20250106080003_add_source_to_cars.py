"""add source to cars

Revision ID: 20250106080003
Revises: 20250106080002
Create Date: 2025-01-06 08:00:03.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250106080003'
down_revision: Union[str, Sequence[str], None] = '20250106080002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cars', sa.Column('source', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cars', 'source')

