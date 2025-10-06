"""create cars table

Revision ID: 847c9b5ba231
Revises:
Create Date: 2025-10-06 07:53:41.850653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '847c9b5ba231'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cars',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('brand', sa.String, nullable=False),
        sa.Column('model', sa.String, nullable=False),
        sa.Column('make', sa.String, nullable=False),
        sa.Column('fuel_type', sa.String, nullable=False),
        sa.Column('color', sa.String, nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cars')
