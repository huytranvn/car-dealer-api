"""add external_link and display_image_url to cars

Revision ID: 20250106080004
Revises: 20250106080003
Create Date: 2025-01-06 08:00:04.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250106080004'
down_revision: Union[str, Sequence[str], None] = '20250106080003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cars', sa.Column('external_link', sa.String(), nullable=True))
    op.add_column('cars', sa.Column('display_image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cars', 'display_image_url')
    op.drop_column('cars', 'external_link')

