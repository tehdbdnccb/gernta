from alembic import op
import sqlalchemy as sa
revision="0001_decision_journal"; down_revision=None; branch_labels=None; depends_on=None

def upgrade():
    op.create_table("decision_journal",
        sa.Column("id",sa.String(64),primary_key=True),sa.Column("run_id",sa.String(64),nullable=False,unique=True),sa.Column("decision_id",sa.String(64),nullable=False),sa.Column("symbol",sa.String(16),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.Column("approved",sa.Boolean(),nullable=False),sa.Column("executed",sa.Boolean(),nullable=False),sa.Column("order_id",sa.String(128)),sa.Column("regime",sa.String(32),nullable=False),sa.Column("thesis",sa.String(4000),nullable=False),sa.Column("quant_score",sa.Float(),nullable=False),sa.Column("rejection_reasons",sa.JSON(),nullable=False),sa.Column("analysis",sa.JSON(),nullable=False))
    op.create_index("ix_decision_journal_run_id","decision_journal",["run_id"]); op.create_index("ix_decision_journal_symbol","decision_journal",["symbol"]); op.create_index("ix_decision_journal_created_at","decision_journal",["created_at"])

def downgrade(): op.drop_table("decision_journal")
