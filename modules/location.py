"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Simple location struct.
"""

# Basically a struct
# pylint: disable-next=too-few-public-methods
class Location:
    """
    Location in world space.
    """
    def __init__(self, location_x: float, location_y: float):
        """
        location is in metres from world origin.
        """
        self.location_x = location_x
        self.location_y = location_y

    def __eq__(self, other: "Location") -> bool:
        """
        Required for comparison.
        """
        if not isinstance(other, Location):
            return False

        return self.location_x == other.location_x and self.location_y == other.location_y

    def __hash__(self) -> int:
        """
        Required for dictionaries and sets.
        """
        return hash((self.location_x, self.location_y))

    def __repr__(self) -> str:
        """
        To string
        """
        return f"({self.location_x},{self.location_y})"
