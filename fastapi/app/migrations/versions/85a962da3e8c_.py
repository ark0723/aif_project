"""empty message

Revision ID: 85a962da3e8c
Revises: 
Create Date: 2024-05-02 16:36:05.656118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85a962da3e8c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AIF_Member',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('member_email', sa.String(length=100), nullable=False),
    sa.Column('img_generate_count', sa.SmallInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('img_generate_count <=2', name='max_count_constraint'),
    sa.PrimaryKeyConstraint('member_id')
    )
    op.create_index(op.f('ix_AIF_Member_member_email'), 'AIF_Member', ['member_email'], unique=False)
    op.create_index(op.f('ix_AIF_Member_member_id'), 'AIF_Member', ['member_id'], unique=False)
    op.create_table('AI_Image',
    sa.Column('img_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('img_url', sa.String(length=255), nullable=True),
    sa.Column('keyword_input', sa.Text(), nullable=True),
    sa.Column('generating_count', sa.SmallInteger(), nullable=True),
    sa.Column('style_code', sa.String(length=20), nullable=True),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['AIF_Member.member_id'], ),
    sa.PrimaryKeyConstraint('img_id')
    )
    op.create_index(op.f('ix_AI_Image_img_id'), 'AI_Image', ['img_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_AI_Image_img_id'), table_name='AI_Image')
    op.drop_table('AI_Image')
    op.drop_index(op.f('ix_AIF_Member_member_id'), table_name='AIF_Member')
    op.drop_index(op.f('ix_AIF_Member_member_email'), table_name='AIF_Member')
    op.drop_table('AIF_Member')
    # ### end Alembic commands ###
