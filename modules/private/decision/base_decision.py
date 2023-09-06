"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Base decision class.
"""

from ... import commands
from ... import drone_report
from ... import location


# All logic in the run() method
# pylint: disable-next=too-few-public-methods
class BaseDecision:
    """
    Required to enforce different decision behaviour in tests.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Nothing to do.
        """
        raise NotImplementedError

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Virtual method.
        """
        raise NotImplementedError
