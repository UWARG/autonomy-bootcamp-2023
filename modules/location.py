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
