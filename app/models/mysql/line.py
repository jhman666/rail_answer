from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class LineMySQL(Base):
    __tablename__ = "line"

    line_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="线路ID"
    )

    line_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="线路编码"
    )

    line_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="线路名称"
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        comment="所属城市"
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        server_default=text("'运营'"),
        comment="线路状态"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        comment="创建时间"
    )