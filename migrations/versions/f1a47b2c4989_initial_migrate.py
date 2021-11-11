"""Initial migrate

Revision ID: f1a47b2c4989
Revises:
Create Date: 2021-10-28 23:51:03.625111

"""
# thirdparty
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f1a47b2c4989"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "basket",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("pickup", sa.Boolean(), nullable=True, comment="Самовывоз"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "basket_item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("basket_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["basket_id"],
            ["basket.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("basket_item")
    op.drop_table("basket")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###