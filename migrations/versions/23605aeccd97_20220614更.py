"""20220614更

Revision ID: 23605aeccd97
Revises: 45a597cb53ae
Create Date: 2022-06-14 22:13:36.898903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23605aeccd97'
down_revision = '45a597cb53ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('LaitGood_UserRegister', sa.Column('county', sa.String(length=5), nullable=True))
    op.add_column('LaitGood_UserRegister', sa.Column('district', sa.String(length=5), nullable=True))
    op.add_column('LaitGood_UserRegister', sa.Column('zipcode', sa.String(length=5), nullable=True))
    op.drop_column('LaitGood_UserRegister', 'twcity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('LaitGood_UserRegister', sa.Column('twcity', sa.VARCHAR(length=20), nullable=True))
    op.drop_column('LaitGood_UserRegister', 'zipcode')
    op.drop_column('LaitGood_UserRegister', 'district')
    op.drop_column('LaitGood_UserRegister', 'county')
    # ### end Alembic commands ###
