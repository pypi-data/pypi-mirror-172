"""Added showOn fields

Peek Plugin Database Migration Script

Revision ID: 931b88db3117
Revises: a423a783700f
Create Date: 2019-07-28 20:15:55.922299

"""

# revision identifiers, used by Alembic.
revision = "931b88db3117"
down_revision = "a423a783700f"
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "DocDbProperty",
        sa.Column("showOnDetail", sa.Boolean(), nullable=True, server_default="1"),
        schema="core_docdb",
    )
    op.execute(""" UPDATE "core_docdb"."DocDbProperty" SET "showOnDetail" = true """)
    op.alter_column(
        "DocDbProperty",
        "showOnDetail",
        type_=sa.Boolean(),
        nullable=False,
        schema="core_docdb",
    )

    op.add_column(
        "DocDbProperty",
        sa.Column("showOnSummary", sa.Boolean(), nullable=True, server_default="0"),
        schema="core_docdb",
    )
    op.execute(""" UPDATE "core_docdb"."DocDbProperty" SET "showOnSummary" = false """)
    op.alter_column(
        "DocDbProperty",
        "showOnSummary",
        type_=sa.Boolean(),
        nullable=False,
        schema="core_docdb",
    )

    op.add_column(
        "DocDbProperty",
        sa.Column("showOnTooltip", sa.Boolean(), nullable=True, server_default="0"),
        schema="core_docdb",
    )
    op.execute(""" UPDATE "core_docdb"."DocDbProperty" SET "showOnTooltip" = false """)
    op.alter_column(
        "DocDbProperty",
        "showOnTooltip",
        type_=sa.Boolean(),
        nullable=False,
        schema="core_docdb",
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("DocDbProperty", "showOnTooltip", schema="core_docdb")
    op.drop_column("DocDbProperty", "showOnSummary", schema="core_docdb")
    op.drop_column("DocDbProperty", "showOnDetail", schema="core_docdb")
    # ### end Alembic commands ###
