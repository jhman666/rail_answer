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


class AlarmRecordMySQL(Base):
    """
    车辆设备报警记录表
    """

    __tablename__ = "alarm_record"

    alarm_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="报警ID"
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

    alarm_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="报警代码"
    )

    alarm_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="报警类型"
    )

    alarm_level: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        comment="报警等级"
    )

    alarm_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        comment="报警发生时间"
    )

    clear_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="报警解除时间"
    )

    alarm_content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="报警内容"
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        server_default=text("'未解除'"),
        comment="报警状态"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="创建时间"
    )