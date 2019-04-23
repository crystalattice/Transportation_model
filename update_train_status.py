# from db_setter_procs import set_speed_proc
from db_setter_procs import set_trains_proc
import del_train_row
from db_getter_procs import get_trains_proc
from voltdbclient import *

client = FastSerializer("localhost", 21212)


def update_train_status(car, new_location, new_speed, new_status):
    del_train_row.del_train(car)
    set_trains_proc.call([car, new_location, new_speed, new_status])


if __name__ == "__main__":
    car_id = input("Name of car/engine id: ")
    location = input("Location: ")
    speed = int(input("How fast? "))
    status = input("Train status: ")
    update_train_status(car_id, location, speed, status)

    print("Engine")
    print(get_trains_proc.call(["Engine"]))
    print("*" * 8)
    print("Car 1")
    print(get_trains_proc.call(["Car 1"]))
    print("*" * 8)
    print("Car 2")
    print(get_trains_proc.call(["Car 2"]))
    print("*" * 8)
    print("Car 3")
    print(get_trains_proc.call(["Car 3"]))

    # Get just the speed of car 3
    car3 = str(get_trains_proc.call(["Car 3"]))
    print(car3[-10:-9])