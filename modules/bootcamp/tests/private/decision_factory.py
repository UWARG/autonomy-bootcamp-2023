"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Factory pattern for constructing Decision class at runtime.
"""

import enum

from .... import location
from ....bootcamp import decision_example
from ....bootcamp import decision_simple_waypoint
from ....bootcamp import decision_waypoint_landing_pads
from ....private.decision import base_decision


class DecisionEnum(enum.Enum):
    """
    Enumeration for Decision class.
    """

    EXAMPLE = 0
    SIMPLE_WAYPOINT = 1
    WAYPOINT_LANDING_PADS = 2


def create_decision(
    decision_enum: DecisionEnum, waypoint: location.Location, acceptance_radius: float
) -> base_decision.BaseDecision:
    """
    Construct Decision class at runtime.
    """
    match decision_enum:
        case DecisionEnum.EXAMPLE:
            return decision_example.DecisionExample(waypoint, acceptance_radius)
        case DecisionEnum.SIMPLE_WAYPOINT:
            return decision_simple_waypoint.DecisionSimpleWaypoint(waypoint, acceptance_radius)
        case DecisionEnum.WAYPOINT_LANDING_PADS:
            return decision_waypoint_landing_pads.DecisionWaypointLandingPads(
                waypoint, acceptance_radius
            )

    return base_decision.BaseDecision(waypoint, acceptance_radius)
