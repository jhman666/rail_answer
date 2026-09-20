from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DeviceMySQL(Base):
    """
    车辆设备基础信息表
    """

    __tablename__ = "device"

    __table_args__ = (
        UniqueConstraint(
            "vehicle_id",
            "device_code",
            name="uk_device_vehicle_code"
        ),
    )

    device_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="设备ID"
    )

    vehicle_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("vehicle.vehicle_id"),
        nullable=True,
        index=True,
        comment="所属车辆ID"
    )

    device_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="设备编码"
    )

    device_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="设备名称"
    )

    device_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="设备类型"
    )

    system_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="所属系统"
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="设备制造商"
    )

    install_position: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="安装位置"
    )

    install_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="安装日期"
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        server_default=text("'正常'"),
        comment="设备状态"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="创建时间"
    )