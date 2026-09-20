from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FaultRecordMySQL(Base):
    """
    车辆设备故障记录表
    """

    __tablename__ = "fault_record"

    fault_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="故障ID"
    )

    vehicle_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("vehicle.vehicle_id"),
        nullable=True,
        index=True,
        comment="车辆ID"
    )

    device_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("device.device_id"),
        nullable=True,
        index=True,
        comment="设备ID"
    )

    fault_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="故障代码"
    )

    fault_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="故障类型"
    )

    fault_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        comment="故障等级"
    )

    fault_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        comment="故障发生时间"
    )

    recover_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="故障恢复时间"
    )

    fault_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="故障描述"
    )

    fault_cause: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="故障原因"
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        server_default=text("'未恢复'"),
        comment="故障状态"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="创建时间"
    )