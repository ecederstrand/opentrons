import pytest
import importlib
import opentrons
from typing import Any, TYPE_CHECKING

from opentrons.types import Mount, Point
from opentrons.calibration_storage import (
    types as cs_types,
)

if TYPE_CHECKING:
    from opentrons_shared_data.deck.dev_types import RobotModel


@pytest.fixture(autouse=True)
def reload_module(robot_model: "RobotModel") -> None:
    importlib.reload(opentrons.calibration_storage)


@pytest.fixture
def starting_calibration_data(
    robot_model: "RobotModel", ot_config_tempdir: Any
) -> None:
    """
    Starting calibration data fixture.

    Adds dummy data to a temporary directory to test delete commands against.
    """
    from opentrons.calibration_storage import save_pipette_calibration

    if robot_model == "OT-3 Standard":
        save_pipette_calibration(Point(1, 1, 1), "pip1", Mount.LEFT)
        save_pipette_calibration(Point(1, 1, 1), "pip2", Mount.RIGHT)
    else:
        save_pipette_calibration(
            Point(1, 1, 1), "pip1", Mount.LEFT, "mytiprack", "opentrons/tip_rack/1"
        )
        save_pipette_calibration(
            Point(1, 1, 1), "pip2", Mount.RIGHT, "mytiprack", "opentrons/tip_rack/1"
        )


def test_delete_all_pipette_calibration(starting_calibration_data: Any) -> None:
    """
    Test delete all pipette calibrations.
    """
    from opentrons.calibration_storage import (
        get_pipette_offset,
        clear_pipette_offset_calibrations,
    )

    assert get_pipette_offset("pip1", Mount.LEFT) is not None
    assert get_pipette_offset("pip2", Mount.RIGHT) is not None
    clear_pipette_offset_calibrations()
    assert get_pipette_offset("pip1", Mount.LEFT) is None
    assert get_pipette_offset("pip2", Mount.RIGHT) is None


def test_delete_specific_pipette_offset(starting_calibration_data: Any) -> None:
    """
    Test delete a specific pipette calibration.
    """
    from opentrons.calibration_storage import (
        get_pipette_offset,
        delete_pipette_offset_file,
    )

    assert get_pipette_offset("pip1", Mount.LEFT) is not None
    delete_pipette_offset_file("pip1", Mount.LEFT)
    assert get_pipette_offset("pip1", Mount.LEFT) is None


def test_save_pipette_calibration(
    ot_config_tempdir: Any, robot_model: "RobotModel"
) -> None:
    """
    Test saving pipette calibrations.
    """
    from opentrons.calibration_storage import (
        get_pipette_offset,
        save_pipette_calibration,
    )

    assert get_pipette_offset("pip1", Mount.LEFT) is None
    if robot_model == "OT-3 Standard":
        save_pipette_calibration(Point(1, 1, 1), "pip1", Mount.LEFT)
        save_pipette_calibration(Point(1, 1, 1), "pip2", Mount.RIGHT)
    else:
        save_pipette_calibration(
            Point(1, 1, 1), "pip1", Mount.LEFT, "mytiprack", "opentrons/tip_rack/1"
        )
        save_pipette_calibration(
            Point(1, 1, 1), "pip2", Mount.RIGHT, "mytiprack", "opentrons/tip_rack/1"
        )
    assert get_pipette_offset("pip1", Mount.LEFT) is not None
    assert get_pipette_offset("pip2", Mount.RIGHT) is not None
    assert get_pipette_offset("pip1", Mount.LEFT).offset == Point(1, 1, 1)
    assert get_pipette_offset("pip1", Mount.LEFT).offset == Point(1, 1, 1)


def test_get_pipette_calibration(
    starting_calibration_data: Any, robot_model: "RobotModel"
) -> None:
    """
    Test ability to get a pipette calibration model.
    """
    from opentrons.calibration_storage import get_pipette_offset

    # needed for proper type checking unfortunately
    from opentrons.calibration_storage.ot3.models.v1 import (
        InstrumentOffsetModel as OT3InstrModel,
    )
    from opentrons.calibration_storage.ot2.models.v1 import (
        InstrumentOffsetModel as OT2InstrModel,
    )

    pipette_data = get_pipette_offset("pip1", Mount.LEFT)
    if robot_model == "OT-3 Standard":
        assert pipette_data == OT3InstrModel(
            offset=Point(1, 1, 1),
            lastModified=pipette_data.lastModified,
            source=cs_types.SourceType.user,
        )
    else:

        assert pipette_data == OT2InstrModel(
            offset=Point(1, 1, 1),
            tiprack="mytiprack",
            uri="opentrons/tip_rack/1",
            last_modified=pipette_data.last_modified,
            source=cs_types.SourceType.user,
        )
