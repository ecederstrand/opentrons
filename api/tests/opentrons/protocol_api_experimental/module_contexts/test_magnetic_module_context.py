"""Tests for `magnetic_module_context`."""

from decoy import Decoy
import pytest

from opentrons.protocols.models import LabwareDefinition

from opentrons.protocol_engine import (
    ModuleLocation,
    commands as pe_commands,
)
from opentrons.protocol_engine.clients import SyncClient

from opentrons.protocol_api_experimental import (
    Labware,
    MagneticModuleContext,
)


@pytest.fixture
def engine_client(decoy: Decoy) -> SyncClient:
    """Return a mock in the shape of a Protocol Engine client."""
    return decoy.mock(cls=SyncClient)


@pytest.fixture
def subject_module_id() -> str:
    """Return the Protocol Engine module ID of the subject."""
    return "subject-module-id"


@pytest.fixture
def subject(engine_client: SyncClient, subject_module_id: str) -> MagneticModuleContext:
    """Return a MagneticModuleContext with mocked dependencies."""
    return MagneticModuleContext(
        engine_client=engine_client, module_id=subject_module_id
    )


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_api_version(subject: MagneticModuleContext) -> None:  # noqa: D103
    _ = subject.api_version


def test_load_labware_default_namespace_and_version(
    decoy: Decoy,
    minimal_labware_def: LabwareDefinition,
    engine_client: SyncClient,
    subject_module_id: str,
    subject: MagneticModuleContext,
) -> None:
    """It should default namespace to "opentrons" and version to 1."""
    decoy.when(
        engine_client.load_labware(
            location=ModuleLocation(moduleId=subject_module_id),
            load_name="some_labware",
            namespace="opentrons",
            version=1,
        )
    ).then_return(
        pe_commands.LoadLabwareResult(
            labwareId="abc123",
            definition=minimal_labware_def,
            offsetId=None,
        )
    )

    result = subject.load_labware(name="some_labware")
    assert result == Labware(labware_id="abc123", engine_client=engine_client)


def test_load_labware_explicit_namespace_and_version(
    decoy: Decoy,
    minimal_labware_def: LabwareDefinition,
    engine_client: SyncClient,
    subject_module_id: str,
    subject: MagneticModuleContext,
) -> None:
    """It should pass along the namespace, version, and load name."""
    decoy.when(
        engine_client.load_labware(
            location=ModuleLocation(moduleId=subject_module_id),
            load_name="some_labware",
            namespace="some_explicit_namespace",
            version=9001,
        )
    ).then_return(
        pe_commands.LoadLabwareResult(
            labwareId="abc123",
            definition=minimal_labware_def,
            offsetId=None,
        )
    )
    result = subject.load_labware(
        name="some_labware",
        namespace="some_explicit_namespace",
        version=9001,
    )
    assert result == Labware(labware_id="abc123", engine_client=engine_client)


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_load_labware_with_label(  # noqa: D103
    subject: MagneticModuleContext,
) -> None:
    subject.load_labware(name="some_load_name", label="some_label")


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_load_labware_from_definition(  # noqa: D103
    subject: MagneticModuleContext,
) -> None:
    subject.load_labware_from_definition(definition={})  # type: ignore[typeddict-item]


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_labware_property(subject: MagneticModuleContext) -> None:  # noqa: D103
    _ = subject.labware


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_engage(subject: MagneticModuleContext) -> None:  # noqa: D103
    _ = subject.engage(offset=3.0)


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_disengage(subject: MagneticModuleContext) -> None:  # noqa: D103
    subject.disengage()


@pytest.mark.xfail(strict=True, raises=NotImplementedError)
def test_status(subject: MagneticModuleContext) -> None:  # noqa: D103
    _ = subject.status
