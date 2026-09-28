"""initial baseline

Revision ID: 0001
Revises:
Create Date: 2026-09-28 06:11:39

"""

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Baseline revision. Real tables come from ``alembic revision --autogenerate``."""


def downgrade() -> None:
    """No-op downgrade for the baseline."""
