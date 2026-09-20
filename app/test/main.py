from pathlib import Path
from app.repositories.db.mysql import create_mysql_engine, create_session_factory
from app.repositories.db.mysql_repository import MySQLRepository
from app.core.app_config import load_app_config

def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    config_path = PROJECT_ROOT / "conf" / "app_config.yaml"

    config = load_app_config(config_path)

    engine = create_mysql_engine(config)
    Session = create_session_factory(engine)

    repo = MySQLRepository(Session())

    sql = """
    SELECT
        v.vehicle_no,
        COUNT(fr.fault_id) AS fault_count
    FROM vehicle v
    JOIN fault_record fr
        ON v.vehicle_id = fr.vehicle_id
    WHERE fr.fault_level = '严重'
    GROUP BY v.vehicle_id, v.vehicle_no
    ORDER BY fault_count DESC
    LIMIT 5;
    """

    results = repo.execute_query(sql)

    print(f"{'车辆编号':<20} {'故障数':<10}")
    print("-" * 30)
    for row in results:
        print(f"{row['vehicle_no']:<20} {row['fault_count']:<10}")

    print(f"\n共 {len(results)} 条记录")

if __name__ == "__main__":
    main()