from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    vehicle_id: int | None = None
    device_code: str | None = None
    device_name: str | None = None
    device_type: str | None = None
    system_name: str | None = None
    manufacturer: str | None = None
    install_position: str | None = None
    install_date: date | None = None
    status: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    vehicle_id: int | None = None
    device_code: str | None = None
    device_name: str | None = None
    device_type: str | None = None
    system_name: str | None = None
    manufacturer: str | None = None
    install_position: str | None = None
    install_date: date | None = None
    status: str | None = None


class DeviceRead(DeviceBase):
    device_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )