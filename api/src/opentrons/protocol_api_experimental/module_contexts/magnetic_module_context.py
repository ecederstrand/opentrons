"""Protocol API interfaces for Magnetic Modules."""

from enum import Enum
from typing import Optional, overload

from opentrons_shared_data.labware.dev_types import LabwareDefinition

from opentrons.protocol_engine.clients import SyncClient as ProtocolEngineClient
from opentrons.protocols.api_support.types import APIVersion

from ..constants import DEFAULT_LABWARE_NAMESPACE
from ..labware import Labware
from ..types import ModuleLocation


class MagneticModuleStatus(str, Enum):
    """The status of a Temperature Module's magnets.

    Returned by `MagneticModuleContext.status`.

    .. versionadded:: 3.0
        This enum is now returned instead of a simple string.
    """

    ENGAGED = "engaged"
    DISENGAGED = "disengaged"


class MagneticModuleContext:  # noqa: D101
    # TODO(mc, 2022-02-09): copy or rewrite docstrings from
    # src/opentrons/protocol_api/module_contexts.py

    def __init__(self, engine_client: ProtocolEngineClient, module_id: str) -> None:
        self._engine_client = engine_client
        self._module_id = module_id

    # todo(mm, 2022-02-15): This public method returns an internal, undocumented type.
    @property
    def api_version(self) -> APIVersion:  # noqa: D102
        raise NotImplementedError()

    def load_labware(  # noqa: D102
        self,
        name: str,
        label: Optional[str] = None,
        namespace: Optional[str] = None,
        version: int = 1,
    ) -> Labware:
        if label is not None:  # github.com/Opentrons/opentrons/issues/9454
            raise NotImplementedError("Labware labels not yet supported.")

        namespace = DEFAULT_LABWARE_NAMESPACE if namespace is None else namespace

        engine_result = self._engine_client.load_labware(
            location=ModuleLocation(moduleId=self._module_id),
            load_name=name,
            namespace=namespace,
            version=version,
        )
        return Labware(
            engine_client=self._engine_client, labware_id=engine_result.labwareId
        )

    def load_labware_from_definition(  # noqa: D102
        self, definition: LabwareDefinition, label: Optional[str] = None
    ) -> Labware:
        raise NotImplementedError()

    @property
    def labware(self) -> Optional[Labware]:  # noqa: D102
        raise NotImplementedError()

    @overload
    def engage(self) -> None:
        ...

    @overload
    def engage(self, height: float) -> None:
        ...

    @overload
    def engage(self, *, height_from_base: float) -> None:
        ...

    @overload
    def engage(self, *, offset: float) -> None:
        ...

    def engage(
        self,
        height: Optional[float] = None,
        *,
        height_from_base: Optional[float] = None,
        offset: Optional[float] = None,
    ) -> None:
        """
        .. versionchanged:: 3.0
            An error is now raised if you provide more than one of
            ``height``, ``height_from_base``, and ``offset``.
            Formerly, the behavior was unspecified.

        .. versionchanged:: 3.0
            You must now specify ``height_from_base`` and ``offset`` as keyword
            arguments.
        """  # noqa: D205,D212,D415
        raise NotImplementedError()

    def disengage(self) -> None:  # noqa: D102
        raise NotImplementedError()

    @property
    def status(self) -> MagneticModuleStatus:  # noqa: D102
        raise NotImplementedError()

    def __hash__(self) -> int:
        """Return a hash.

        Uses the module instance's unique identifier in protocol state.
        """
        return hash(self._module_id)

    def __eq__(self, other: object) -> bool:
        """Compare for object equality using identifier string."""
        return (
            isinstance(other, MagneticModuleContext)
            and self._module_id == other._module_id
        )
