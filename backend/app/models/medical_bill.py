from __future__ import annotations

import enum
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Enum as SQLEnum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BillStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    COMPLETED = "completed"


class MedicalBill(Base):
    __tablename__ = "medical_bills"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    hospital_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("hospitals.id"), nullable=False)
    bill_number: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    patient_name: Mapped[str] = mapped_column(String(255), nullable=True)
    patient_id: Mapped[str] = mapped_column(String(120), nullable=True)
    admission_date: Mapped[date] = mapped_column(Date, nullable=True)
    discharge_date: Mapped[date] = mapped_column(Date, nullable=True)
    hospital_bill_type: Mapped[str] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=True)
    grand_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=True)
    status: Mapped[BillStatus] = mapped_column(
        SQLEnum(BillStatus),
        nullable=False,
        default=BillStatus.PENDING,
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    source_file_path: Mapped[str] = mapped_column(Text, nullable=True)
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

    user: Mapped["User"] = relationship("User", back_populates="medical_bills")
    hospital: Mapped["Hospital"] = relationship("Hospital", back_populates="medical_bills")
    bill_items: Mapped[list["BillItem"]] = relationship(
        "BillItem",
        back_populates="medical_bill",
        cascade="all, delete-orphan",
    )
    audit_findings: Mapped[list["AuditFinding"]] = relationship(
        "AuditFinding",
        back_populates="medical_bill",
        cascade="all, delete-orphan",
    )
    complaints: Mapped[list["Complaint"]] = relationship(
        "Complaint",
        back_populates="medical_bill",
        cascade="all, delete-orphan",
    )
    audit_report: Mapped["AuditReport"] = relationship(
        "AuditReport",
        back_populates="medical_bill",
        cascade="all, delete-orphan",
        uselist=False,
    )
