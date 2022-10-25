"""Tests for the legacy Protocol API module core implementations."""
from typing import Any, Dict, cast

import pytest
from decoy import Decoy, matchers

from opentrons.hardware_control import SynchronousAdapter
from opentrons.hardware_control.modules import AbstractModule
from opentrons.hardware_control.modules.types import ModuleType, TemperatureModuleModel
from opentrons.protocols.geometry.deck import Deck
from opentrons.protocols.geometry.module_geometry import ModuleGeometry
from opentrons.protocol_api import Labware

from opentrons.protocol_api.core.protocol_api.protocol_context import (
    ProtocolContextImplementation,
)
from opentrons.protocol_api.core.protocol_api.labware import LabwareImplementation
from opentrons.protocol_api.core.protocol_api.legacy_module_core import LegacyModuleCore


@pytest.fixture
def mock_geometry(decoy: Decoy) -> ModuleGeometry:
    """Get a mock module geometry."""
    return decoy.mock(cls=ModuleGeometry)


@pytest.fixture
def mock_sync_module_hardware(decoy: Decoy) -> SynchronousAdapter[AbstractModule]:
    """Get a mock synchronous module hardware."""
    return decoy.mock(name="SynchronousAdapater[AbstractModule]")  # type: ignore[no-any-return]


@pytest.fixture
def mock_deck(decoy: Decoy) -> Deck:
    """Get a mock Deck interface."""

    class _MockDeck(Dict[str, Any]):
        ...

    deck = _MockDeck()
    setattr(deck, "recalculate_high_z", decoy.mock(name="Deck.recalculate_high_z"))

    return cast(Deck, deck)


@pytest.fixture
def mock_protocol_core(decoy: Decoy, mock_deck: Deck) -> ProtocolContextImplementation:
    """Get a mock protocol core."""
    protocol_core = decoy.mock(cls=ProtocolContextImplementation)
    decoy.when(protocol_core.get_deck()).then_return(mock_deck)
    return protocol_core


@pytest.fixture
def mock_labware_core(decoy: Decoy) -> LabwareImplementation:
    """Get a mock labware core."""
    return decoy.mock(cls=LabwareImplementation)


@pytest.fixture
def subject(
    mock_geometry: ModuleGeometry,
    mock_sync_module_hardware: SynchronousAdapter[AbstractModule],
    mock_protocol_core: ProtocolContextImplementation,
) -> LegacyModuleCore:
    """Get a legacy module implementation core with mocked out dependencies."""
    return LegacyModuleCore(
        requested_model=TemperatureModuleModel.TEMPERATURE_V1,
        geometry=mock_geometry,
        sync_module_hardware=mock_sync_module_hardware,
        protocol_core=mock_protocol_core,
    )


def test_get_requested_model(subject: LegacyModuleCore) -> None:
    """It should return the requested model given to the constructor."""
    result = subject.get_requested_model()
    assert result == TemperatureModuleModel.TEMPERATURE_V1


def test_get_geometry(mock_geometry: ModuleGeometry, subject: LegacyModuleCore) -> None:
    """It should return the geometry interface given to the constructor."""
    assert subject.geometry is mock_geometry


def test_get_model(
    decoy: Decoy, mock_geometry: ModuleGeometry, subject: LegacyModuleCore
) -> None:
    """It should get the model from the geometry."""
    decoy.when(mock_geometry.model).then_return(TemperatureModuleModel.TEMPERATURE_V2)
    result = subject.get_model()
    assert result == TemperatureModuleModel.TEMPERATURE_V2


def test_get_type(
    decoy: Decoy, mock_geometry: ModuleGeometry, subject: LegacyModuleCore
) -> None:
    """It should get the model from the geometry."""
    decoy.when(mock_geometry.module_type).then_return(ModuleType.TEMPERATURE)
    result = subject.get_type()
    assert result == ModuleType.TEMPERATURE


def test_get_serial_number(
    decoy: Decoy,
    mock_sync_module_hardware: SynchronousAdapter[AbstractModule],
    subject: LegacyModuleCore,
) -> None:
    """It should return the serial number from the hardware interface."""
    decoy.when(mock_sync_module_hardware.device_info).then_return({"serial": "abc123"})
    result = subject.get_serial_number()
    assert result == "abc123"


def test_add_labware_core(
    decoy: Decoy,
    mock_geometry: ModuleGeometry,
    mock_labware_core: LabwareImplementation,
    mock_deck: Deck,
    subject: LegacyModuleCore,
) -> None:
    """It should add a labware core to the module."""
    mock_labware = decoy.mock(cls=Labware)

    labware_captor = matchers.Captor()

    decoy.when(mock_geometry.add_labware(labware_captor)).then_return(mock_labware)
    decoy.when(mock_labware_core.get_uri()).then_return("a/b/c")

    result = subject.add_labware_core(mock_labware_core)

    assert isinstance(labware_captor.value, Labware)
    assert labware_captor.value.uri == "a/b/c"
    assert result == mock_labware
    assert subject.labware_core == mock_labware_core

    decoy.verify(mock_deck.recalculate_high_z(), times=1)
