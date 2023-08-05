"""Fixed nullable Queue rawValue

Peek Plugin Database Migration Script

Revision ID: 1f014c013f8b
Revises: d4ffb9c5cb27
Create Date: 2020-04-21 18:33:51.189917

"""

# revision identifiers, used by Alembic.
revision = "1f014c013f8b"
down_revision = "d4ffb9c5cb27"
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    schema = "pl_livedb"
    table = "LiveDbRawValueQueue"
    op.execute(
        '''CREATE TEMP TABLE tempqueue AS
                  select * from %s."%s"'''
        % (schema, table)
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("LiveDbRawValueQueue", schema="pl_livedb")

    op.create_table(
        "LiveDbRawValueQueue",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("modelSetId", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("rawValue", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="pl_livedb",
    )
    op.create_index(
        "idx_LiveDbRawValueQueue_all",
        "LiveDbRawValueQueue",
        ["id", "modelSetId", "key", "rawValue"],
        unique=False,
        schema="pl_livedb",
    )
    # ### end Alembic commands ###

    op.execute(
        '''SELECT setval('%s."%s_id_seq"', max(id))
                  FROM %s."%s"'''
        % (schema, table, schema, table)
    )

    op.execute(
        """INSERT INTO %s."%s"
                  select * from tempqueue"""
        % (schema, table)
    )

    op.execute("""DROP TABLE tempqueue""")


def downgrade():
    pass
