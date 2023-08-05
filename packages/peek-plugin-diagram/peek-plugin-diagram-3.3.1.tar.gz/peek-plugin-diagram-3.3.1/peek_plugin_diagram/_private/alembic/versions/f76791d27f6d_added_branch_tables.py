"""added branch tables

Peek Plugin Database Migration Script

Revision ID: f76791d27f6d
Revises: 5e2f84d757f2
Create Date: 2019-02-04 19:34:07.351930

"""

# revision identifiers, used by Alembic.
revision = "f76791d27f6d"
down_revision = "5e2f84d757f2"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "BranchIndexCompilerQueue",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("modelSetId", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chunkKey", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["modelSetId"], ["pl_diagram.ModelSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", "chunkKey"),
        schema="pl_diagram",
    )
    op.create_table(
        "BranchIndexEncodedChunk",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("modelSetId", sa.Integer(), nullable=False),
        sa.Column("chunkKey", sa.String(), nullable=False),
        sa.Column("encodedData", sa.LargeBinary(), nullable=False),
        sa.Column("encodedHash", sa.String(), nullable=False),
        sa.Column("lastUpdate", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["modelSetId"], ["pl_diagram.ModelSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchIndexEnc_modelSetId_chunkKey",
        "BranchIndexEncodedChunk",
        ["modelSetId", "chunkKey"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_table(
        "BranchIndex",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("coordSetId", sa.Integer(), nullable=False),
        sa.Column("importGroupHash", sa.String(), nullable=True),
        sa.Column("importHash", sa.String(), nullable=True),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("chunkKey", sa.String(), nullable=False),
        sa.Column("packedJson", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["coordSetId"], ["pl_diagram.ModelCoordSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchIndex_chunkKey",
        "BranchIndex",
        ["chunkKey"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchIndex_importGroupHash",
        "BranchIndex",
        ["coordSetId", "importGroupHash"],
        unique=False,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchIndex_importHash",
        "BranchIndex",
        ["coordSetId", "importHash"],
        unique=True,
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchIndex_key",
        "BranchIndex",
        ["coordSetId", "key"],
        unique=True,
        schema="pl_diagram",
    )
    op.create_table(
        "BranchGridIndex",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("branchIndexId", sa.Integer(), nullable=False),
        sa.Column("coordSetId", sa.Integer(), nullable=False),
        sa.Column("gridKey", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["branchIndexId"], ["pl_diagram.BranchIndex.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["coordSetId"], ["pl_diagram.ModelCoordSet.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", "coordSetId"),
        schema="pl_diagram",
    )
    op.create_index(
        "idx_BranchGridIndex_coord_key",
        "BranchGridIndex",
        ["coordSetId", "branchIndexId", "gridKey"],
        unique=True,
        schema="pl_diagram",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "idx_BranchGridIndex_coord_key",
        table_name="BranchGridIndex",
        schema="pl_diagram",
    )
    op.drop_table("BranchGridIndex", schema="pl_diagram")
    op.drop_index("idx_BranchIndex_key", table_name="BranchIndex", schema="pl_diagram")
    op.drop_index(
        "idx_BranchIndex_importGroupHash", table_name="BranchIndex", schema="pl_diagram"
    )
    op.drop_index(
        "idx_BranchIndex_chunkKey", table_name="BranchIndex", schema="pl_diagram"
    )
    op.drop_table("BranchIndex", schema="pl_diagram")
    op.drop_index(
        "idx_BranchIndexEnc_modelSetId_chunkKey",
        table_name="BranchIndexEncodedChunk",
        schema="pl_diagram",
    )
    op.drop_table("BranchIndexEncodedChunk", schema="pl_diagram")
    op.drop_table("BranchIndexCompilerQueue", schema="pl_diagram")
    # ### end Alembic commands ###
