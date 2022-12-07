import pytest

from typing import Tuple
from opentrons_shared_data.pipette.pipette_definition import (
    SupportedTipsDefinition,
    PipetteTipType,
)
from opentrons_shared_data.pipette.dev_types import PipetteModel, PipetteName
from opentrons.config import ot3_pipette_config as pc


def test_multiple_tip_configurations() -> None:
    loaded_configuration = pc.load_ot3_pipette("p1000", 8, 1.0)
    assert list(loaded_configuration.supported_tips.keys()) == list(PipetteTipType)
    assert isinstance(
        loaded_configuration.supported_tips[PipetteTipType.t50],
        SupportedTipsDefinition,
    )


@pytest.mark.parametrize(
    argnames=["model", "channels", "version"],
    argvalues=[["p50", 8, 1.0], ["p1000", 96, 1.0], ["p50", 1, 1.0]],
)
def test_load_full_pipette_configurations(
    model: str, channels: int, version: float
) -> None:
    loaded_configuration = pc.load_ot3_pipette(model, channels, version)
    assert loaded_configuration.pipette_type.value == model
    assert loaded_configuration.channels.as_int == channels


@pytest.mark.parametrize(
    argnames=["name", "output"],
    argvalues=[["p50_single_v2.0", ("p50", 1, 2.0)], ["p1000_multi", ("p1000", 8, 1.0)], ["p1000_96", ("p1000", 96, 1.0)]],
)
def test_convert_pipette_model(model: PipetteModel, output: Tuple[str, int, float]) -> None:
    assert output == pc.convert_pipette_model(model)

@pytest.mark.parametrize(
    argnames=["name", "output"],
    argvalues=[["p50_single", ("p50", 1, 1.0)], ["p1000_multi_gen3", ("p1000", 8, 3.0)], ["p300_single_gen2", ("p300", 1, 2.0)]],
)
def test_convert_pipette_name(name: PipetteName, output: Tuple[str, int, float]) -> None:
    assert output == pc.convert_pipette_name(name)
