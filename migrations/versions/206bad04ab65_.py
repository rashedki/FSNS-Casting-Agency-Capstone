"""empty message

Revision ID: 206bad04ab65
Revises: 
Create Date: 2020-08-25 12:37:07.567478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '206bad04ab65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('actors', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('actors_movie_id_fkey', 'actors', type_='foreignkey')
    op.create_foreign_key(None, 'actors', 'movies', ['movie_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'actors', type_='foreignkey')
    op.create_foreign_key('actors_movie_id_fkey', 'actors', 'movies', ['movie_id'], ['id'])
    op.alter_column('actors', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
