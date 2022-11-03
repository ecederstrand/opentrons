import type {
  PipettingRunTimeCommand,
  PipettingCreateCommand,
} from './pipetting'
import type { GantryRunTimeCommand, GantryCreateCommand } from './gantry'
import type { ModuleRunTimeCommand, ModuleCreateCommand } from './module'
import type { SetupRunTimeCommand, SetupCreateCommand } from './setup'
import type { TimingRunTimeCommand, TimingCreateCommand } from './timing'
import type {
  CalibrationRunTimeCommand,
  CalibrationCreateCommand,
} from './calibration'

// NOTE: these key/value pairs will only be present on commands at analysis/run time
// they pertain only to the actual execution status of a command on hardware, as opposed to
// the command's identity and parameters which can be known prior to runtime

export type CommandStatus = 'queued' | 'running' | 'succeeded' | 'failed'
export interface CommonCommandRunTimeInfo {
  key?: string
  id: string
  status: CommandStatus
  error: string | null
  createdAt: string
  startedAt: string | null
  completedAt: string | null
}
export interface CommonCommandCreateInfo {
  key?: string
  meta?: { [key: string]: any }
}

export type CreateCommand =
  | PipettingCreateCommand // involves the pipettes plunger motor
  | GantryCreateCommand // movement that only effects the x,y,z position of the gantry/pipette
  | ModuleCreateCommand // directed at a hardware module
  | SetupCreateCommand // only effecting robot's equipment setup (pipettes, labware, modules, liquid), no hardware side-effects
  | TimingCreateCommand // effecting the timing of command execution
  // TODO (sb 10/26/22): Separate out calibration commands from protocol schema in RAUT-272
  | CalibrationCreateCommand // for automatic pipette calibration
  | ({
      commandType: 'custom'
      params: { [key: string]: any }
    } & CommonCommandCreateInfo) // allows for experimentation between schema versions with no expectation of system support

// commands will be required to have a key, but will not be created with one
export type RunTimeCommand =
  | PipettingRunTimeCommand // involves the pipettes plunger motor
  | GantryRunTimeCommand // movement that only effects the x,y,z position of the gantry/pipette
  | ModuleRunTimeCommand // directed at a hardware module
  | SetupRunTimeCommand // only effecting robot's equipment setup (pipettes, labware, modules, liquid), no hardware side-effects
  | TimingRunTimeCommand // effecting the timing of command execution
  // TODO (sb 10/26/22): Separate out calibration commands from protocol schema in RAUT-272
  | CalibrationRunTimeCommand // for automatic pipette calibration
  | ({
      commandType: 'custom'
      params: { [key: string]: any }
      result: any
    } & CommonCommandRunTimeInfo) // allows for experimentation between schema versions with no expectation of system support
