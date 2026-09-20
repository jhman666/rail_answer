from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class VehicleDailyHealthBase(BaseModel):
    vehicle_id: int | None = None
    stat_date: date | None = None

    health_score: Decimal | None = None
    health_level: str | None = None

    device_score: Decimal | None = None
    fault_score: Decimal | None = None
    alarm_score: Decimal | None = None

    fault_count: int | None = None
    alarm_count: int | None = None

    critical_fault_count: int | None = None
    critical_alarm_count: int | None = None


class VehicleDailyHealthCreate(
    VehicleDailyHealthBase
):
    pass


class VehicleDailyHealthUpdate(BaseModel):
    vehicle_id: int | None = None
    stat_date: date | None = None

    health_score: Decimal | None = None
    health_level: str | None = None

    device_score: Decimal | None = None
    fault_score: Decimal | None = None
    alarm_score: Decimal | None = None

    fault_count: int | None = None
    alarm_count: int | None = None

    critical_fault_count: int | None = None
    critical_alarm_count: int | None = None


class VehicleDailyHealthRead(
    VehicleDailyHealthBase
):
    health_id: int
    calculated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )