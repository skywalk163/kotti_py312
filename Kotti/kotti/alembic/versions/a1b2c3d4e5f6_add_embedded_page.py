"""Add EmbeddedPage content type

Revision ID: a1b2c3d4e5f6
Revises: 814c4ec72f1
Create Date: 2026-04-27 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '814c4ec72f1'


def upgrade():
    # Create embedded_pages table
    op.create_table(
        'embedded_pages',
        sa.Column('id', sa.Integer(), sa.ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('embed_url', sa.String(2000), nullable=True),
        sa.Column('fallback_content', sa.Text(), nullable=True),
        sa.Column('iframe_height', sa.Integer(), nullable=True, server_default='600'),
        sa.Column('allow_fullscreen', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('sandbox_attrs', sa.String(500), nullable=True),
        sa.Column('css_class', sa.String(100), nullable=True),
    )


def downgrade():
    op.drop_table('embedded_pages')
