from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class Directions(Enum):
    UP = 1
    DOWN = 2
    STATIONARY = 3

class Request(ABC):
    def __init__(self, floor: int):
        self.floor = floor

    @abstractmethod
    def can_be_fullfilled(self, elevator) :
        raise NotImplementedError

class Lift:
    def __init__(self, no_of_floors):
        self.no_of_floors = no_of_floors
        self.current_floor = 0
        self.direction: Directions = Directions.UP
        self.requests: List[Request] = []

    def move(self):
        if self.requests:
            self.set_direction(Directions.UP if self.requests[0].floor > self.current_floor else Directions.DOWN)
        else:
            self.set_direction(Directions.STATIONARY)
        if self.direction == Directions.UP:
            self.current_floor += 1
            if self.current_floor == self.no_of_floors:
                self.set_direction(Directions.DOWN)
        elif self.direction == Directions.DOWN:
            self.current_floor -= 1
            if self.current_floor == 0:
                self.set_direction(Directions.UP)
                  
        self.check_requests()

        

    def check_requests(self):
        index = 0
        while index < len(self.requests):
            if self.requests[index].can_be_fullfilled(self):
                self.requests.pop(index)
                self.stop()
                return True
            else:
                index += 1

    def stop(self):
        print("Stopped at floor: ", self.current_floor)

    def request(self, floor: Request):
        self.requests.append(floor)

    def get_requests(self):
        return self.requests

    def get_current_floor(self):
        return self.current_floor

    def get_direction(self):
        return self.direction

    def set_direction(self, direction: Directions):
        self.direction = direction
    

class OutsideRequest(Request):
    
    def __init__(self, floor, direction: Directions):
        super().__init__(floor)
        self.direction = direction

    def can_be_fullfilled(self, elevator: Lift):
        
        if self.direction == elevator.direction:
            if self.floor == elevator.get_current_floor():
                return True
        return False

class InsideRequest(Request):
    
    def __init__(self, floor: int):
        super().__init__(floor)

    def can_be_fullfilled(self, elevator: Lift):
        if self.floor == elevator.get_current_floor():
            return True
        return False
  

def main():
    no_of_floors = int(input("Enter the number of floors: "))
    lift = Lift(no_of_floors)
    while True:
        print("1. Request a floor")
        print("2. Request an elevator")
        print("3. Move the lift")
        print("4. Exit")
        choice = int(input("Enter your choice: "),)


        if choice == 1:
            floor = int(input("Enter the floor number: "))
            lift.request(InsideRequest(floor))

        elif choice == 2:
            direction = Directions._member_map_.get(input("Enter the direction: ").upper())
            floor = int(input("Enter the floor number: "))
            lift.request(OutsideRequest(floor, direction))
        elif choice == 3:
            lift.move()
        elif choice == 4:
            break
        else:
            print("Invalid choice")
        print("\n\n")
        print("Current floor: ", lift.get_current_floor())
        print("Direction: ", lift.get_direction())
        print("\n")

main()