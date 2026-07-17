from __future__ import annotations

import enum
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AuditStatus(str, enum.Enum):
    PENDING = "pending"
    MATCHED = "matched"
    FLAGGED = "flagged"


class BillItem(Base):
    __tablename__ = "bill_items"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    bill_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("medical_bills.id"), nullable=False)
    government_rate_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("government_rates.id"), nullable=True)
    medicine_reference_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("medicine_references.id"), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    total_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    service_code: Mapped[str] = mapped_column(String(100), nullable=True)
    is_medicine: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_procedure: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    matched_reference: Mapped[str] = mapped_column(String(255), nullable=True)
    audit_status: Mapped[AuditStatus] = mapped_column(
        SQLEnum(AuditStatus),
        nullable=True,
        default=AuditStatus.PENDING,
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

    medical_bill: Mapped["MedicalBill"] = relationship("MedicalBill", back_populates="bill_items")
    government_rate: Mapped["GovernmentRate"] = relationship("GovernmentRate", back_populates="bill_items")
    medicine_reference: Mapped["MedicineReference"] = relationship("MedicineReference", back_populates="bill_items")
    audit_findings: Mapped[list["AuditFinding"]] = relationship(
        "AuditFinding",
        back_populates="bill_item",
        cascade="all, delete-orphan",
    )
