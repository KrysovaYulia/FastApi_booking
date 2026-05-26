"""add unique

Revision ID: d9148975e863
Revises:
Create Date: 2026-05-26 17:04:36.837002

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d9148975e863"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_table("users")
 
