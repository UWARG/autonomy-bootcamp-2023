"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Base decision class.
"""

from ... import commands
from ... import drone_report
from ... import location


class BaseDecision:
    """
    Required to enforce different decision behaviour in tests.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Nothing to do.
        """
        raise NotImplementedError

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Virtual method.
        """
        raise NotImplementedError
