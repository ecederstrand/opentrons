"""Common APIs for protocol core interfaces."""

# TODO(mc, 2022-08-22): move to __init__ when dependency cycles are resolved
from .instrument import AbstractInstrument
from .labware import AbstractLabware
from .module import (
    AbstractModuleCore,
    AbstractTemperatureModuleCore,
    AbstractMagneticModuleCore,
    AbstractThermocyclerCore,
    AbstractHeaterShakerCore,
)
from .protocol import AbstractProtocol
from .well import AbstractWellCore


WellCore = AbstractWellCore
LabwareCore = AbstractLabware[WellCore]
InstrumentCore = AbstractInstrument[WellCore]
ModuleCore = AbstractModuleCore[LabwareCore]
TemperatureModuleCore = AbstractTemperatureModuleCore[LabwareCore]
MagneticModuleCore = AbstractMagneticModuleCore[LabwareCore]
ThermocyclerCore = AbstractThermocyclerCore[LabwareCore]
HeaterShakerCore = AbstractHeaterShakerCore[LabwareCore]
ProtocolCore = AbstractProtocol[InstrumentCore, LabwareCore, ModuleCore]