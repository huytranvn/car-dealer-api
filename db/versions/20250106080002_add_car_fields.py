"""add car fields

Revision ID: 20250106080002
Revises: 20250106080001
Create Date: 2025-01-06 08:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250106080002'
down_revision: Union[str, Sequence[str], None] = '20250106080001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cars', sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('cars', sa.Column('registered_date', sa.String(), nullable=True))
    op.add_column('cars', sa.Column('registered_year', sa.Integer(), nullable=True))
    op.add_column('cars', sa.Column('mileage', sa.Integer(), nullable=True))
    op.add_column('cars', sa.Column('wheel_drive', sa.String(), nullable=True))
    op.add_column('cars', sa.Column('registration_number', sa.String(), nullable=True))
    op.add_column('cars', sa.Column('variant', sa.String(), nullable=True))

    # Add unique constraint on registration_number
    op.create_unique_constraint('uq_cars_registration_number', 'cars', ['registration_number'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_cars_registration_number', 'cars', type_='unique')
    op.drop_column('cars', 'variant')
    op.drop_column('cars', 'registration_number')
    op.drop_column('cars', 'wheel_drive')
    op.drop_column('cars', 'mileage')
    op.drop_column('cars', 'registered_year')
    op.drop_column('cars', 'registered_date')
    op.drop_column('cars', 'price')

