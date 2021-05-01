"""empty message

Revision ID: 9cc03814f2de
Revises: 
Create Date: 2021-05-01 11:54:09.021856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cc03814f2de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('mentorship_relations', 'action_user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=False)
    op.alter_column('mentorship_relations', 'mentee_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.alter_column('mentorship_relations', 'mentor_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.alter_column('tasks_comments', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=False)


def downgrade():
    op.alter_column('users', 'id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('tasks_comments', 'user_id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('mentorship_relations', 'mentor_id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('mentorship_relations', 'mentee_id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('mentorship_relations', 'action_user_id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               existing_nullable=False)
