"""books

Revision ID: 5d07b228b962
Revises: 9f95c4759220
Create Date: 2017-05-30 08:59:57.819566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '5d07b228b962'
down_revision = '9f95c4759220'
branch_labels = None
depends_on = None


def upgrade():
    register = table(
        'register',
        column('fund', sa.String),
        column('register', sa.Integer),
    )
    op.bulk_insert(
        register,
        [
            {'fund': "4211", 'register': 2},
        ]
    )

    case = table(
        'case',
        column('register_id', sa.Integer),
        column('book_id', sa.String),
        column('book_num', sa.Integer),
    )
    op.bulk_insert(
        case,
        [
            {
                'register_id': 1,
                'book_id': i + 1,
                'book_num': i + 1,
            } for i in range(20)
        ]
    )


def downgrade():
    op.execute("DELETE FROM `case`")
    op.execute("DELETE FROM register")
