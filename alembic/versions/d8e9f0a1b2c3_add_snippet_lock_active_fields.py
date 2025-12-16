"""Add is_locked and is_active fields to snippets table

Revision ID: d8e9f0a1b2c3
Revises: c7e8f9a0b1d2
Create Date: 2025-12-16 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8e9f0a1b2c3"
down_revision: Union[str, Sequence[str], None] = "c7e8f9a0b1d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_locked and is_active fields to snippets table.

    is_locked: When True, snippet is protected from deletion during regeneration.
               Users can lock cards they want to keep while regenerating others.

    is_active: Soft-delete flag. When False, snippet is archived/deleted but
               can be restored. This allows users to recover accidentally
               deleted cards.
    """
    # Add is_locked column (default False - not locked)
    op.add_column(
        "snippets",
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default="0"),
    )

    # Add is_active column (default True - active/visible)
    op.add_column(
        "snippets",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
    )

    # Add index on is_active for efficient filtering of active vs archived snippets
    op.create_index(
        "ix_snippets_is_active",
        "snippets",
        ["is_active"],
        unique=False,
    )


def downgrade() -> None:
    """Remove is_locked and is_active fields from snippets table."""
    op.drop_index("ix_snippets_is_active", table_name="snippets")
    op.drop_column("snippets", "is_active")
    op.drop_column("snippets", "is_locked")
