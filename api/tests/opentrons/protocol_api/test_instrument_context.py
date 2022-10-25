"""Tests for the public InstrumentContext class."""
import pytest
from decoy import Decoy

from opentrons.types import Location, Mount, Point
from opentrons.broker import Broker
from opentrons.protocols.api_support.types import APIVersion
from opentrons.protocol_api.core.abstract import InstrumentCore, ProtocolCore

from opentrons.protocol_api import (
    MAX_SUPPORTED_VERSION,
    InstrumentContext,
    Labware,
    Well,
)


@pytest.fixture
def mock_instrument_core(decoy: Decoy) -> InstrumentCore:
    return decoy.mock(cls=InstrumentCore)


@pytest.fixture
def mock_protocol_core(decoy: Decoy) -> ProtocolCore:
    return decoy.mock(cls=ProtocolCore)


@pytest.fixture
def mock_broker(decoy: Decoy) -> Broker:
    return decoy.mock(cls=Broker)


@pytest.fixture
def mock_trash(decoy: Decoy) -> Labware:
    return decoy.mock(cls=Labware)


@pytest.fixture
def api_version() -> APIVersion:
    return MAX_SUPPORTED_VERSION


@pytest.fixture
def subject(
    mock_instrument_core: InstrumentCore,
    mock_protocol_core: ProtocolCore,
    mock_broker: Broker,
    mock_trash: Labware,
    api_version: APIVersion,
) -> InstrumentContext:
    return InstrumentContext(
        core=mock_instrument_core,
        protocol_core=mock_protocol_core,
        broker=mock_broker,
        api_version=api_version,
        trash=mock_trash,
        tip_racks=[],
    )


@pytest.mark.parametrize("api_version", [APIVersion(2, 0), APIVersion(2, 10)])
def test_api_version(api_version: APIVersion, subject: InstrumentContext) -> None:
    """It should have an API version."""
    assert subject.api_version == api_version


def test_move_to_well(
    decoy: Decoy,
    mock_instrument_core: InstrumentCore,
    mock_protocol_core: ProtocolCore,
    subject: InstrumentContext,
) -> None:
    """It should move to a well."""
    mock_well = decoy.mock(cls=Well)
    location = Location(point=Point(1, 2, 3), labware=mock_well)

    decoy.when(mock_instrument_core.get_mount()).then_return(Mount.RIGHT)

    result = subject.move_to(
        location=location,
        force_direct=True,
        minimum_z_height=4,
        speed=5,
    )

    assert result is subject

    decoy.verify(
        mock_instrument_core.move_to(
            point=Point(1, 2, 3),
            well_core=mock_well._core,
            labware_core=mock_well.parent._core,
            force_direct=True,
            minimum_z_height=4,
            speed=5,
        ),
        mock_protocol_core.set_last_location(location=location, mount=Mount.RIGHT),
    )


def test_move_to_coordinates(
    decoy: Decoy,
    mock_instrument_core: InstrumentCore,
    mock_protocol_core: ProtocolCore,
    subject: InstrumentContext,
) -> None:
    """It should move to a well."""
    mock_labware = decoy.mock(cls=Labware)
    location = Location(point=Point(1, 2, 3), labware=mock_labware)

    decoy.when(mock_instrument_core.get_mount()).then_return(Mount.LEFT)

    result = subject.move_to(
        location=location,
        force_direct=True,
        minimum_z_height=4,
        speed=5,
    )

    assert result is subject

    decoy.verify(
        mock_instrument_core.move_to(
            point=Point(1, 2, 3),
            well_core=None,
            labware_core=mock_labware._core,
            force_direct=True,
            minimum_z_height=4,
            speed=5,
        ),
        mock_protocol_core.set_last_location(location=location, mount=Mount.LEFT),
    )


# def test_move_to_coordinates() -> None:
#     """It should move to a well."""
