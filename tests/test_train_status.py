import pytest

from sqlalchemy.orm.exc import NoResultFound
from database.create_database import TrainOrders, TrainStatus

import set_train_orders


def test_engine_sta3(transportation_db):
    """Test Engine to valid station."""
    set_train_orders.create_orders(vehicle="Engine", destination="Station 3", cargo="N/A", turbo=False, speed=30,
                                   session=transportation_db)

    orders = transportation_db.query(TrainOrders).one()
    assert orders.who == "Engine"
    assert orders.where_to == "Station 3"


def test_car1_sta4(transportation_db):
    """Test car to valid station."""
    set_train_orders.create_orders(vehicle="Car 1", destination="Station 4", cargo="Denim", turbo=False, speed=30,
                                   session=transportation_db)

    orders = transportation_db.query(TrainOrders).one()
    assert orders.who == "Car 1"
    assert orders.where_to == "Station 4"
    assert orders.cargo == "Denim"


def test_invalid_car(transportation_db):
    """Test invalid car to valid station."""
    with pytest.raises(NoResultFound):
        set_train_orders.create_orders(vehicle="Car 6", destination="Station 2", cargo="N/A", turbo=False, speed=30,
                                       session=transportation_db)


def test_vehicle_int(transportation_db):
    """Test vehicle entry passed as non-string."""
    with pytest.raises(NoResultFound):
        set_train_orders.create_orders(vehicle=6, destination="Station 2", cargo="N/A", turbo=False, speed=30,
                                       session=transportation_db)


def test_cargo_int(transportation_db):
    """Test cargo entry passed as non-string. Arguments should be converted to string."""
    set_train_orders.create_orders(vehicle="Car 1", destination="Station 4", cargo=8, turbo=False, speed=30,
                                   session=transportation_db)

    orders = transportation_db.query(TrainOrders).one()
    assert orders.cargo == "8"


def test_engine_turbo(transportation_db):
    """Test Engine to valid station with priority flag."""
    set_train_orders.create_orders(vehicle="Engine", destination="Station 3", cargo="N/A", turbo=True, speed=50,
                                   session=transportation_db)

    orders = transportation_db.query(TrainOrders).one()
    assert orders.who == "Engine"
    assert orders.where_to == "Station 3"
    assert orders.priority == True
    assert orders.speed_request == 50


def test_match_speeds(transportation_db):
    """Test current speed matches ordered speed."""
    new_orders = set_train_orders.create_orders(vehicle="Engine", destination="Station 3", cargo="N/A", turbo=False,
                                                speed=45, session=transportation_db)
    set_train_orders.match_speeds(transportation_db, new_orders)
    new_speed = transportation_db.query(TrainStatus).filter(TrainStatus.identification == new_orders.who).one()
    assert new_speed.speed == 45


def test_current_status_update(transportation_db):
    """Test CurrentStatus table is updated to new status after transportation orders made."""
    new_orders = set_train_orders.create_orders(vehicle="Engine", destination="Station 3", cargo="N/A", turbo=False,
                                                speed=30, session=transportation_db)
    set_train_orders.update_curr_location(transportation_db, new_orders)
    new_status = transportation_db.query(TrainStatus).filter(TrainStatus.identification == new_orders.who).one()
    assert new_status.identification == "Engine"
    assert new_status.location == "Station 3"


def test_orders_status_cleared(transportation_db):
    """Test that future orders table is cleared after move performed."""
    new_orders = set_train_orders.create_orders(vehicle="Engine", destination="Station 3", cargo="N/A", turbo=False,
                                                speed=30, session=transportation_db)

    set_train_orders.update_curr_location(transportation_db, new_orders)
    set_train_orders.clear_orders(transportation_db)
    with pytest.raises(NoResultFound):
        transportation_db.query(TrainOrders).one()
