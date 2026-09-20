from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class VehicleDailyHealthMySQL(Base):
    """
    每日车辆健康度评分表
    """

    __tablename__ = "vehicle_daily_health"

    __table_args__ = (
        UniqueConstraint(
            "vehicle_id",
            "stat_date",
            name="uk_vehicle_health_date"
        ),
    )

    health_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="健康度记录ID"
    )

    vehicle_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("vehicle.vehicle_id"),
        nullable=True,
        index=True,
        comment="车辆ID"
    )

    stat_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True,
        comment="统计日期"
    )

    health_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        index=True,
        comment="综合健康度评分"
    )

    health_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="健康等级"
    )

    device_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment="设备状态评分"
    )

    fault_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment="故障评分"
    )

    alarm_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        comment="报警评分"
    )

    fault_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="当日故障数量"
    )

    alarm_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="当日报警数量"
    )

    critical_fault_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="严重故障数量"
    )

    critical_alarm_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="严重报警数量"
    )

    calculated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="健康度计算时间"
    )