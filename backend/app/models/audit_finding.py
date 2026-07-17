from __future__ import annotations

import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FindingStatus(str, enum.Enum):
    OPEN = "open"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"


class FindingSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditFinding(Base):
    __tablename__ = "audit_findings"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    bill_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("medical_bills.id"), nullable=False)
    item_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("bill_items.id"), nullable=True)
    report_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("audit_reports.id"), nullable=True)
    severity: Mapped[FindingSeverity] = mapped_column(
        SQLEnum(FindingSeverity),
        nullable=True,
    )
    finding_type: Mapped[str] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[FindingStatus] = mapped_column(
        SQLEnum(FindingStatus),
        nullable=False,
        default=FindingStatus.OPEN,
    )
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

    medical_bill: Mapped["MedicalBill"] = relationship("MedicalBill", back_populates="audit_findings")
    bill_item: Mapped["BillItem"] = relationship("BillItem", back_populates="audit_findings")
    audit_report: Mapped["AuditReport"] = relationship("AuditReport", back_populates="audit_findings")
    complaints: Mapped[list["Complaint"]] = relationship(
        "Complaint",
        back_populates="audit_finding",
        cascade="all, delete-orphan",
    )
