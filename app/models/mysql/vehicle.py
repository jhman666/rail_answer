from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class VehicleMySQL(Base):
    __tablename__ = "vehicle"

    vehicle_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="车辆ID"
    )

    vehicle_no: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        comment="车辆编号"
    )

    vehicle_model: Mapped[str | None] = mapped_column(
        String(100),
        comment="车辆型号"
    )

    line_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("line.line_id"),
        comment="所属线路ID"
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        comment="车辆制造商"
    )

    manufacture_date: Mapped[date | None] = mapped_column(
        Date,
        comment="生产日期"
    )

    service_date: Mapped[date | None] = mapped_column(
        Date,
        comment="投入运营日期"
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        server_default=text("'运营'"),
        comment="车辆状态"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        comment="创建时间"
    )