from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class GovernmentRate(Base):
    __tablename__ = "government_rates"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    jurisdiction: Mapped[str] = mapped_column(String(120), nullable=False)
    scheme_name: Mapped[str] = mapped_column(String(255), nullable=True)
    version: Mapped[str] = mapped_column(String(50), nullable=True)
    procedure_code: Mapped[str] = mapped_column(String(100), nullable=True)
    service_name: Mapped[str] = mapped_column(String(255), nullable=True)
    rate_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=True)
    effective_date: Mapped[date] = mapped_column(Date, nullable=True)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=True)
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

    # Placeholder relationship for future benchmarking logic.
    bill_items: Mapped[list["BillItem"]] = relationship("BillItem", back_populates="government_rate")
