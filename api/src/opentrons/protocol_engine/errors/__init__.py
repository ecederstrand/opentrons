"""Protocol engine errors module."""

from .exceptions import (
    ProtocolEngineError,
    UnexpectedProtocolError,
    FailedToLoadPipetteError,
    PipetteNotAttachedError,
    CommandDoesNotExistError,
    LabwareNotLoadedError,
    LabwareNotOnDeckError,
    LiquidDoesNotExistError,
    LabwareDefinitionDoesNotExistError,
    LabwareOffsetDoesNotExistError,
    LabwareIsNotTipRackError,
    LabwareIsTipRackError,
    TouchTipDisabledError,
    WellDoesNotExistError,
    PipetteNotLoadedError,
    PipetteTipInfoNotFoundError,
    ModuleNotLoadedError,
    ModuleNotOnDeckError,
    SlotDoesNotExistError,
    FailedToPlanMoveError,
    MustHomeError,
    RunStoppedError,
    SetupCommandNotAllowedError,
    WellOriginNotAllowedError,
    ModuleNotAttachedError,
    ModuleAlreadyPresentError,
    WrongModuleTypeError,
    ThermocyclerNotOpenError,
    RobotDoorOpenError,
    PipetteMovementRestrictedByHeaterShakerError,
    HeaterShakerLabwareLatchNotOpenError,
    EngageHeightOutOfRangeError,
    NoTargetTemperatureSetError,
    InvalidTargetSpeedError,
    InvalidTargetTemperatureError,
    InvalidBlockVolumeError,
    CannotPerformModuleAction,
    PauseNotAllowedError,
    ProtocolCommandFailedError,
    GripperNotAttachedError,
    HardwareNotSupportedError,
    LabwareMovementNotAllowedError,
    LocationIsOccupiedError,
)

from .error_occurrence import ErrorOccurrence

__all__ = [
    # exceptions
    "ProtocolEngineError",
    "UnexpectedProtocolError",
    "FailedToLoadPipetteError",
    "PipetteNotAttachedError",
    "CommandDoesNotExistError",
    "LabwareNotLoadedError",
    "LabwareNotOnDeckError",
    "LiquidDoesNotExistError",
    "LabwareDefinitionDoesNotExistError",
    "LabwareOffsetDoesNotExistError",
    "LabwareIsNotTipRackError",
    "LabwareIsTipRackError",
    "TouchTipDisabledError",
    "WellDoesNotExistError",
    "PipetteNotLoadedError",
    "PipetteTipInfoNotFoundError",
    "ModuleNotLoadedError",
    "ModuleNotOnDeckError",
    "SlotDoesNotExistError",
    "FailedToPlanMoveError",
    "MustHomeError",
    "RunStoppedError",
    "SetupCommandNotAllowedError",
    "WellOriginNotAllowedError",
    "ModuleNotAttachedError",
    "ModuleAlreadyPresentError",
    "WrongModuleTypeError",
    "ThermocyclerNotOpenError",
    "RobotDoorOpenError",
    "PipetteMovementRestrictedByHeaterShakerError",
    "HeaterShakerLabwareLatchNotOpenError",
    "EngageHeightOutOfRangeError",
    "NoTargetTemperatureSetError",
    "InvalidTargetTemperatureError",
    "InvalidTargetSpeedError",
    "InvalidBlockVolumeError",
    "CannotPerformModuleAction",
    "PauseNotAllowedError",
    "ProtocolCommandFailedError",
    "GripperNotAttachedError",
    "HardwareNotSupportedError",
    "LabwareMovementNotAllowedError",
    "LocationIsOccupiedError",
    # error occurrence models
    "ErrorOccurrence",
]
