"""Add snippets table for persistent story cards

Revision ID: c7e8f9a0b1d2
Revises: 35c3ce144bee
Create Date: 2025-12-13 03:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7e8f9a0b1d2"
down_revision: Union[str, Sequence[str], None] = "35c3ce144bee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create snippets table for persistent story cards.

    Snippets are AI-generated cards representing memorable moments
    from life story interviews. They include:
    - title: Short catchy title (2-5 words)
    - content: The snippet text (max 300 chars)
    - theme: Category (family, friendship, growth, adventure, etc.)
    - phase: Life phase (CHILDHOOD, YOUNG_ADULT, ADULTHOOD, etc.)
    """
    op.create_table(
        "snippets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("story_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("theme", sa.String(50), nullable=True),
        sa.Column("phase", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["story_id"],
            ["stories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_snippets_id"), "snippets", ["id"], unique=False)
    op.create_index(op.f("ix_snippets_user_id"), "snippets", ["user_id"], unique=False)
    op.create_index(
        op.f("ix_snippets_story_id"), "snippets", ["story_id"], unique=False
    )


def downgrade() -> None:
    """Drop snippets table."""
    op.drop_index(op.f("ix_snippets_story_id"), table_name="snippets")
    op.drop_index(op.f("ix_snippets_user_id"), table_name="snippets")
    op.drop_index(op.f("ix_snippets_id"), table_name="snippets")
    op.drop_table("snippets")
