# -*- coding: utf-8 -*-
"""Add g4f_chats table for G4FChat content type

Revision ID: 001
Revises: 
Create Date: 2026-04-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'g4f_chats',
        sa.Column('id', sa.Integer(), sa.ForeignKey('contents.id'), primary_key=True),
        sa.Column('system_prompt', sa.Text(), nullable=True),
        sa.Column('welcome_message', sa.Unicode(500), nullable=True),
        sa.Column('model', sa.Unicode(100), nullable=True),
    )


def downgrade():
    op.drop_table('g4f_chats')
