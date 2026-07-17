from __future__ import annotations

import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATED = "generated"
    FAILED = "failed"


class AuditReport(Base):
    __tablename__ = "audit_reports"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    bill_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("medical_bills.id"), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus),
        nullable=False,
        default=ReportStatus.PENDING,
    )
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    medical_bill: Mapped["MedicalBill"] = relationship("MedicalBill", back_populates="audit_report")
    audit_findings: Mapped[list["AuditFinding"]] = relationship(
        "AuditFinding",
        back_populates="audit_report",
        cascade="all, delete-orphan",
    )
