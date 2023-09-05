
You can safely ignore `BOOTCAMPERS DO NOT MODIFY THIS FILE` if you are maintaining the bootcamp. The message is for bootcampers.

TODO: Confluence

TODO: Logging (see all print statements)

TODO: Worker process error handling

TODO: More graceful logging of final state (get the image from Display)

TODO: Remove generate_destination() image exclusion zone when we have a more reliable model

TODO: Unit tests

TODO: Run tests:

```bash
python -m modules.private.tests.test_drone_state_figure_8
python -m modules.private.tests.test_map_render_figure_8
python -m modules.private.tests.test_simulation_worker
python -m modules.private.tests.test_detect_landing_pad_worker
python -m modules.private.tests.test_geolocation_worker
pytest modules/private/tests/test_geolocation.py
python -m modules.private.tests.test_display_worker
python -m modules.private.tests.test_display

# Bootcamp
pytest modules/bootcamp/tests/test_detect_landing_pad.py
python -m modules.bootcamp.tests.run_decision_example
python -m modules.bootcamp.tests.run_decision_simple_waypoint
python -m modules.bootcamp.tests.run_decision_waypoint_landing_pads
```
