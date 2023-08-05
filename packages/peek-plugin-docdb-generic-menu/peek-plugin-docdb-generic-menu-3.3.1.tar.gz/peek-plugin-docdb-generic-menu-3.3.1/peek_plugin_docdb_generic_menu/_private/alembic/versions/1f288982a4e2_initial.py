"""initial

Peek Plugin Database Migration Script

Revision ID: 1f288982a4e2
Revises: 
Create Date: 2017-10-05 10:28:00.029716

"""

# revision identifiers, used by Alembic.
revision = "1f288982a4e2"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "GenericDiagramMenu",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("modelSetKey", sa.String(), nullable=True),
        sa.Column("coordSetKey", sa.String(), nullable=True),
        sa.Column("faIcon", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_docdb_generic_menu",
    )
    op.create_table(
        "Setting",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_docdb_generic_menu",
    )
    op.create_table(
        "SettingProperty",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("settingId", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=16), nullable=True),
        sa.Column("int_value", sa.Integer(), nullable=True),
        sa.Column("char_value", sa.String(), nullable=True),
        sa.Column("boolean_value", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["settingId"],
            ["pl_docdb_generic_menu.Setting.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_docdb_generic_menu",
    )
    op.create_index(
        "idx_SettingProperty_settingId",
        "SettingProperty",
        ["settingId"],
        unique=False,
        schema="pl_docdb_generic_menu",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "idx_SettingProperty_settingId",
        table_name="SettingProperty",
        schema="pl_docdb_generic_menu",
    )
    op.drop_table("SettingProperty", schema="pl_docdb_generic_menu")
    op.drop_table("Setting", schema="pl_docdb_generic_menu")
    op.drop_table("GenericDiagramMenu", schema="pl_docdb_generic_menu")
    # ### end Alembic commands ###
