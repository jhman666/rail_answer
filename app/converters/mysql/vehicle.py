from app.models.mysql.vehicle import VehicleMySQL
from app.schemas.mysql.vehicle import (
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)


class VehicleConverter:

    @staticmethod
    def to_entity(
        vehicle_mysql: VehicleMySQL,
    ) -> VehicleRead:

        return VehicleRead(
            vehicle_id=vehicle_mysql.vehicle_id,
            vehicle_no=vehicle_mysql.vehicle_no,
            vehicle_model=vehicle_mysql.vehicle_model,
            line_id=vehicle_mysql.line_id,
            manufacturer=vehicle_mysql.manufacturer,
            manufacture_date=vehicle_mysql.manufacture_date,
            service_date=vehicle_mysql.service_date,
            status=vehicle_mysql.status,
            created_at=vehicle_mysql.created_at,
        )

    @staticmethod
    def to_mysql(
        vehicle: VehicleCreate,
    ) -> VehicleMySQL:

        return VehicleMySQL(
            vehicle_no=vehicle.vehicle_no,
            vehicle_model=vehicle.vehicle_model,
            line_id=vehicle.line_id,
            manufacturer=vehicle.manufacturer,
            manufacture_date=vehicle.manufacture_date,
            service_date=vehicle.service_date,
            status=vehicle.status,
        )
