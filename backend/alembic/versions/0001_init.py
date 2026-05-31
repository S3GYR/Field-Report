"""Initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2026-05-30 22:02:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("number", sa.String(length=50), nullable=False, unique=True),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("client", sa.String(length=120), nullable=False),
        sa.Column("site", sa.String(length=240), nullable=False),
        sa.Column("weather", sa.String(length=20), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_reports_number", "reports", ["number"], unique=True)
    op.create_index("ix_reports_status", "reports", ["status"], unique=False)

    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("filepath", sa.String(length=500), nullable=False),
        sa.Column("gps_lat", sa.Float(), nullable=True),
        sa.Column("gps_lng", sa.Float(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=False),
    )
    op.create_index("ix_photos_report_id", "photos", ["report_id"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("photo_id", sa.Integer(), sa.ForeignKey("photos.id", ondelete="SET NULL"), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("estimated_cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("estimated_duration", sa.Float(), nullable=True),
    )
    op.create_index("ix_tasks_report_id", "tasks", ["report_id"], unique=False)
    op.create_index("ix_tasks_photo_id", "tasks", ["photo_id"], unique=False)
    op.create_index("ix_tasks_status", "tasks", ["status"], unique=False)

    op.create_table(
        "signatures",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("report_id", sa.Integer(), sa.ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=120), nullable=True),
        sa.Column("signed_on", sa.Date(), nullable=True),
        sa.Column("signature_image", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("signatures")
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_photo_id", table_name="tasks")
    op.drop_index("ix_tasks_report_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_photos_report_id", table_name="photos")
    op.drop_table("photos")
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_number", table_name="reports")
    op.drop_table("reports")
