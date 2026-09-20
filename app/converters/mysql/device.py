from app.models.mysql.device import DeviceMySQL
from app.schemas.mysql.device import (
    DeviceCreate,
    DeviceRead,
    DeviceUpdate,
)


class DeviceConverter:

    @staticmethod
    def to_entity(
        device_mysql: DeviceMySQL,
    ) -> DeviceRead:

        return DeviceRead(
            device_id=device_mysql.device_id,
            vehicle_id=device_mysql.vehicle_id,
            device_code=device_mysql.device_code,
            device_name=device_mysql.device_name,
            device_type=device_mysql.device_type,
            system_name=device_mysql.system_name,
            manufacturer=device_mysql.manufacturer,
            install_position=device_mysql.install_position,
            install_date=device_mysql.install_date,
            status=device_mysql.status,
            created_at=device_mysql.created_at,
        )

    @staticmethod
    def to_mysql(
        device: DeviceCreate,
    ) -> DeviceMySQL:

        return DeviceMySQL(
            vehicle_id=device.vehicle_id,
            device_code=device.device_code,
            device_name=device.device_name,
            device_type=device.device_type,
            system_name=device.system_name,
            manufacturer=device.manufacturer,
            install_position=device.install_position,
            install_date=device.install_date,
            status=device.status,
        )

