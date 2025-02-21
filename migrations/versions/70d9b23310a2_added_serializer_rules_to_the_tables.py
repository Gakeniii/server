"""added serializer rules to the tables

Revision ID: 70d9b23310a2
Revises: 01060817f550
Create Date: 2025-01-29 15:03:04.891086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70d9b23310a2'
down_revision = '01060817f550'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specialty', schema=None) as batch_op:
        batch_op.drop_constraint('fk_doctor_id', type_='foreignkey')
        batch_op.drop_column('doctor_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specialty', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doctor_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_doctor_id', 'doctor', ['doctor_id'], ['id'])

    # ### end Alembic commands ###
