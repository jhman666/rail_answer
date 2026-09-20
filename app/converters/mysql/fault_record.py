from app.models.mysql.fault_record import FaultRecordMySQL
from app.schemas.mysql.fault_record import (
    FaultRecordCreate,
    FaultRecordRead,
    FaultRecordUpdate,
)


class FaultRecordConverter:

    @staticmethod
    def to_entity(
        fault_mysql: FaultRecordMySQL,
    ) -> FaultRecordRead:

        return FaultRecordRead(
            fault_id=fault_mysql.fault_id,
            vehicle_id=fault_mysql.vehicle_id,
            device_id=fault_mysql.device_id,
            fault_code=fault_mysql.fault_code,
            fault_type=fault_mysql.fault_type,
            fault_level=fault_mysql.fault_level,
            fault_time=fault_mysql.fault_time,
            recover_time=fault_mysql.recover_time,
            fault_description=fault_mysql.fault_description,
            fault_cause=fault_mysql.fault_cause,
            status=fault_mysql.status,
            created_at=fault_mysql.created_at,
        )

    @staticmethod
    def to_mysql(
        fault: FaultRecordCreate,
    ) -> FaultRecordMySQL:

        return FaultRecordMySQL(
            vehicle_id=fault.vehicle_id,
            device_id=fault.device_id,
            fault_code=fault.fault_code,
            fault_type=fault.fault_type,
            fault_level=fault.fault_level,
            fault_time=fault.fault_time,
            recover_time=fault.recover_time,
            fault_description=fault.fault_description,
            fault_cause=fault.fault_cause,
            status=fault.status,
        )

