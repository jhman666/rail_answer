from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class VehicleBase(BaseModel):
    vehicle_no: str | None = None
    vehicle_model: str | None = None
    line_id: int | None = None
    manufacturer: str | None = None
    manufacture_date: date | None = None
    service_date: date | None = None
    status: str | None = None


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    vehicle_no: str | None = None
    vehicle_model: str | None = None
    line_id: int | None = None
    manufacturer: str | None = None
    manufacture_date: date | None = None
    service_date: date | None = None
    status: str | None = None


class VehicleRead(VehicleBase):
    vehicle_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )