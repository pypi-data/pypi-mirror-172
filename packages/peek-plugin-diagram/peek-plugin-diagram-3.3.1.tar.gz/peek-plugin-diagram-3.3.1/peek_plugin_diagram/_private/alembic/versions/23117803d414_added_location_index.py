"""added location index

Peek Plugin Database Migration Script

Revision ID: 23117803d414
Revises: 1fe753e1f369
Create Date: 2017-09-09 16:10:10.582473

"""

# revision identifiers, used by Alembic.
revision = "23117803d414"
down_revision = "1fe753e1f369"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "LocationIndexCompiled",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("indexBucket", sa.String(length=100), nullable=False),
        sa.Column("blobData", sa.LargeBinary(), nullable=False),
        sa.Column("lastUpdate", sa.String(length=50), nullable=False),
        sa.Column("modelSetId", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["modelSetId"], ["pl_diagram.ModelSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", "indexBucket"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_DKIndexUpdate_coordSetId",
        "LocationIndexCompiled",
        ["modelSetId"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_DKIndexUpdate_gridKey",
        "LocationIndexCompiled",
        ["indexBucket"],
        unique=True,
        schema="pl_diagram",
    )
    op.create_table(
        "LocationIndexCompilerQueue",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("indexBucket", sa.String(length=100), nullable=False),
        sa.Column("modelSetId", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["modelSetId"], ["pl_diagram.ModelSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", "indexBucket", "modelSetId"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_DKCompQueue_coordSetId_gridKey",
        "LocationIndexCompilerQueue",
        ["modelSetId", "indexBucket"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_table(
        "LocationIndex",
        sa.Column("indexBucket", sa.String(length=100), nullable=False),
        sa.Column("dispId", sa.Integer(), nullable=False),
        sa.Column("modelSetId", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dispId"], ["pl_diagram.DispBase.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["modelSetId"],
            ["pl_diagram.ModelSet.id"],
        ),
        sa.PrimaryKeyConstraint("indexBucket", "dispId"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_LocationIndex_dispId",
        "LocationIndex",
        ["dispId"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_LocationIndex_indexBucket",
        "LocationIndex",
        ["indexBucket"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_LocationIndex_modelSetId",
        "LocationIndex",
        ["modelSetId"],
        unique=False,
        schema="pl_diagram",
    )
    op.add_column(
        "DispBase",
        sa.Column("locationJson", sa.String(length=120), nullable=True),
        schema="pl_diagram",
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("DispBase", "locationJson", schema="pl_diagram")
    op.drop_index(
        "idx_LocationIndex_modelSetId", table_name="LocationIndex", schema="pl_diagram"
    )
    op.drop_index(
        "idx_LocationIndex_indexBucket", table_name="LocationIndex", schema="pl_diagram"
    )
    op.drop_index(
        "idx_LocationIndex_dispId", table_name="LocationIndex", schema="pl_diagram"
    )
    op.drop_table("LocationIndex", schema="pl_diagram")
    op.drop_index(
        "idx_DKCompQueue_coordSetId_gridKey",
        table_name="LocationIndexCompilerQueue",
        schema="pl_diagram",
    )
    op.drop_table("LocationIndexCompilerQueue", schema="pl_diagram")
    op.drop_index(
        "idx_DKIndexUpdate_gridKey",
        table_name="LocationIndexCompiled",
        schema="pl_diagram",
    )
    op.drop_index(
        "idx_DKIndexUpdate_coordSetId",
        table_name="LocationIndexCompiled",
        schema="pl_diagram",
    )
    op.drop_table("LocationIndexCompiled", schema="pl_diagram")
    # ### end Alembic command
