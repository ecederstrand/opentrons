from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from opentrons import types
from opentrons.hardware_control import (
    CriticalPoint,
    NoTipAttachedError,
    TipAttachedError,
)
from opentrons.hardware_control.dev_types import PipetteDict
from opentrons.hardware_control.types import HardwareAction
from opentrons.protocols.api_support.types import APIVersion
from opentrons.protocols.api_support.definitions import MAX_SUPPORTED_VERSION
from opentrons.protocols.api_support.util import FlowRates, PlungerSpeeds, Clearances
from opentrons.protocols.geometry import planning

from ..instrument import AbstractInstrument
from ..protocol_api.labware import LabwareImplementation
from ..protocol_api.well import WellImplementation

if TYPE_CHECKING:
    from .protocol_context import ProtocolContextSimulation


class InstrumentContextSimulation(
    AbstractInstrument[LabwareImplementation, WellImplementation]
):
    """A simulation of an instrument context."""

    def __init__(
        self,
        protocol_interface: ProtocolContextSimulation,
        pipette_dict: PipetteDict,
        mount: types.Mount,
        instrument_name: str,
        default_speed: float = 400.0,
        api_version: Optional[APIVersion] = None,
    ):
        """Constructor."""
        self._protocol_interface = protocol_interface
        self._mount = mount
        self._pipette_dict = pipette_dict
        self._instrument_name = instrument_name
        self._default_speed = default_speed
        self._api_version = api_version or MAX_SUPPORTED_VERSION
        self._flow_rate = FlowRates(self)
        self._flow_rate.set_defaults(api_level=self._api_version)
        self._plunger_speeds = PlungerSpeeds(self)
        # Cache the maximum instrument height
        self._instrument_max_height = (
            protocol_interface.get_hardware().get_instrument_max_height(self._mount)
        )

    def get_default_speed(self) -> float:
        return self._default_speed

    def set_default_speed(self, speed: float) -> None:
        self._default_speed = speed

    def aspirate(self, volume: float, rate: float) -> None:
        self._raise_if_no_tip(HardwareAction.ASPIRATE.name)
        new_volume = self.get_current_volume() + volume
        assert (
            new_volume <= self._pipette_dict["working_volume"]
        ), "Cannot aspirate more than pipette max volume"
        self._pipette_dict["ready_to_aspirate"] = True
        self._update_volume(new_volume)

    def dispense(self, volume: float, rate: float) -> None:
        self._raise_if_no_tip(HardwareAction.DISPENSE.name)
        self._update_volume(self.get_current_volume() - volume)

    def blow_out(self) -> None:
        self._raise_if_no_tip(HardwareAction.BLOWOUT.name)
        self._update_volume(0)
        self._pipette_dict["ready_to_aspirate"] = False

    def _update_volume(self, vol: float) -> None:
        self._pipette_dict["current_volume"] = vol
        self._pipette_dict["available_volume"] = (
            self._pipette_dict["working_volume"] - vol
        )

    def touch_tip(
        self, location: WellImplementation, radius: float, v_offset: float, speed: float
    ) -> None:
        pass

    def pick_up_tip(
        self,
        well: WellImplementation,
        tip_length: float,
        presses: Optional[int],
        increment: Optional[float],
        prep_after: bool,
    ) -> None:
        geometry = well.get_geometry()
        self._raise_if_tip("pick up tip")
        self._pipette_dict["has_tip"] = True
        self._pipette_dict["tip_length"] = tip_length
        self._pipette_dict["current_volume"] = 0
        self._pipette_dict["working_volume"] = min(
            geometry.max_volume, self.get_max_volume()
        )
        self._pipette_dict["available_volume"] = self._pipette_dict["working_volume"]
        if prep_after:
            self._pipette_dict["ready_to_aspirate"] = True

    def drop_tip(self, home_after: bool) -> None:
        self._raise_if_no_tip(HardwareAction.DROPTIP.name)
        self._pipette_dict["has_tip"] = False
        self._pipette_dict["tip_length"] = 0.0
        self._update_volume(0)

    def home(self) -> None:
        self._protocol_interface.set_last_location(None)

    def home_plunger(self) -> None:
        pass

    def move_to(
        self,
        point: types.Point,
        well_core: WellImplementation,
        labware_core: LabwareImplementation,
        force_direct: bool,
        minimum_z_height: Optional[float],
        speed: Optional[float],
    ) -> None:
        """Simulation of only the motion planning portion of move_to."""
        location_cache_mount = (
            self._mount if self._api_version >= APIVersion(2, 10) else None
        )

        last_location = self._protocol_interface.get_last_location(
            mount=location_cache_mount
        )

        from_point = types.Point(0, 0, 0)
        from_slot = None
        from_well_highest_z = None
        from_labware_highest_z = None
        from_critical_point = None
        to_slot = None
        to_well_highest_z = None
        to_labware_highest_z = None
        to_critical_point = None
        same_labware = False
        same_well = False

        if labware_core:
            to_slot = labware_core.get_slot()
            to_labware_highest_z = labware_core.highest_z
            if labware_core.get_center_multichannel_on_wells():
                to_critical_point = CriticalPoint.XY_CENTER

        if well_core:
            to_well_highest_z = well_core.get_geometry().top().z

        if last_location:
            from_point = last_location.point
            from_lw, from_well = last_location.labware.get_parent_labware_and_well()
            from_slot = last_location.labware.first_parent

            if last_location.labware.center_multichannel_on_wells():
                from_critical_point = CriticalPoint.XY_CENTER

            if from_well:
                same_well = from_well._core is well_core
                from_well_highest_z = from_well.top().point.z

            if from_lw:
                same_labware = from_lw._core is labware_core
                from_labware_highest_z = from_lw.highest_z

        # We just want to catch planning errors.
        planning.plan_moves(
            from_point=from_point,
            from_slot=from_slot,
            from_well_highest_z=from_well_highest_z,
            from_labware_highest_z=from_labware_highest_z,
            from_critical_point=from_critical_point,
            to_point=point,
            to_slot=to_slot,
            to_labware_highest_z=to_labware_highest_z,
            to_well_hightest_z=to_well_highest_z,
            to_critical_point=to_critical_point,
            same_labware=same_labware,
            same_well=same_well,
            deck=self._protocol_interface.get_deck(),
            instr_max_height=self._instrument_max_height,
            force_direct=force_direct,
            minimum_z_height=minimum_z_height,
        )

    def get_mount(self) -> types.Mount:
        return self._mount

    def get_instrument_name(self) -> str:
        return self._instrument_name

    def get_pipette_name(self) -> str:
        return self._pipette_dict["name"]

    def get_model(self) -> str:
        return self._pipette_dict["model"]

    def get_min_volume(self) -> float:
        return self._pipette_dict["min_volume"]

    def get_max_volume(self) -> float:
        return self._pipette_dict["max_volume"]

    def get_current_volume(self) -> float:
        return self._pipette_dict["current_volume"]

    def get_available_volume(self) -> float:
        return self._pipette_dict["available_volume"]

    def get_pipette(self) -> PipetteDict:
        return self._pipette_dict

    def get_channels(self) -> int:
        return self._pipette_dict["channels"]

    def has_tip(self) -> bool:
        return self._pipette_dict["has_tip"]

    def is_ready_to_aspirate(self) -> bool:
        return self._pipette_dict["ready_to_aspirate"]

    def prepare_for_aspirate(self) -> None:
        self._raise_if_no_tip(HardwareAction.PREPARE_ASPIRATE.name)

    def get_return_height(self) -> float:
        return self._pipette_dict["return_tip_height"]

    def get_well_bottom_clearance(self) -> Clearances:
        return Clearances(default_aspirate=1, default_dispense=1)

    def get_speed(self) -> PlungerSpeeds:
        return self._plunger_speeds

    def get_flow_rate(self) -> FlowRates:
        return self._flow_rate

    def set_flow_rate(
        self,
        aspirate: Optional[float] = None,
        dispense: Optional[float] = None,
        blow_out: Optional[float] = None,
    ) -> None:
        self._protocol_interface.get_hardware().set_flow_rate(
            mount=self._mount,
            aspirate=aspirate,
            dispense=dispense,
            blow_out=blow_out,
        )
        self._update_flow_rate()

    def set_pipette_speed(
        self,
        aspirate: Optional[float] = None,
        dispense: Optional[float] = None,
        blow_out: Optional[float] = None,
    ) -> None:
        self._protocol_interface.get_hardware().set_pipette_speed(
            mount=self._mount,
            aspirate=aspirate,
            dispense=dispense,
            blow_out=blow_out,
        )
        self._update_flow_rate()

    def _update_flow_rate(self) -> None:
        """Update cached speed and flow rates from hardware controller pipette."""
        p = self._protocol_interface.get_hardware().get_attached_instrument(
            self.get_mount()
        )
        self._pipette_dict["aspirate_flow_rate"] = p["aspirate_flow_rate"]
        self._pipette_dict["dispense_flow_rate"] = p["dispense_flow_rate"]
        self._pipette_dict["blow_out_flow_rate"] = p["blow_out_flow_rate"]
        self._pipette_dict["aspirate_speed"] = p["aspirate_speed"]
        self._pipette_dict["dispense_speed"] = p["dispense_speed"]
        self._pipette_dict["blow_out_speed"] = p["blow_out_speed"]

    def _raise_if_no_tip(self, action: str) -> None:
        """Raise NoTipAttachedError if no tip."""
        if not self.has_tip():
            raise NoTipAttachedError(f"Cannot perform {action} without a tip attached")

    def _raise_if_tip(self, action: str) -> None:
        """Raise TipAttachedError if tip."""
        if self.has_tip():
            raise TipAttachedError(f"Cannot {action} with a tip attached")
