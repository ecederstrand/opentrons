import {
  getModuleType,
  getLabwareDefURI,
  RunTimeCommand,
  getPipetteNameSpecs,
} from '@opentrons/shared-data'
import { PickUpTipRunTimeCommand } from '@opentrons/shared-data/protocol/types/schemaV6/command/pipetting'
import { LoadLabwareRunTimeCommand } from '@opentrons/shared-data/protocol/types/schemaV6/command/setup'
import { InvariantContext } from '../types'

export function constructInvariantContextFromRunCommands(
  commands: RunTimeCommand[]
): InvariantContext {
  return commands.reduce(
    (acc, command) => {
      if (command.commandType === 'loadLabware') {
        return {
          ...acc,
          labwareEntities: {
            ...acc.labwareEntities,
            [command.result.labwareId]: {
              id: command.result.labwareId,
              labwareDefURI: getLabwareDefURI(command.result.definition),
              def: command.result.definition,
            },
          },
        }
      } else if (command.commandType === 'loadModule') {
        return {
          ...acc,
          moduleEntities: {
            ...acc.moduleEntities,
            [command.result.moduleId]: {
              id: command.result.moduleId,
              type: getModuleType(command.result.model),
              model: command.result.model,
            },
          },
        }
      } else if (command.commandType === 'loadPipette') {
        const labwareId =
          commands.find(
            (c): c is PickUpTipRunTimeCommand =>
              c.commandType === 'pickUpTip' &&
              c.params.pipetteId === command.result.pipetteId
          )?.params.labwareId ?? null
        const tiprackLabwareDef =
          labwareId != null
            ? commands.find(
                (c): c is LoadLabwareRunTimeCommand =>
                  c.commandType === 'loadLabware' &&
                  c.result.labwareId === labwareId
              )?.result.definition ?? null
            : null

        return {
          ...acc,
          pipetteEntities: {
            ...acc.pipetteEntities,
            [command.result.pipetteId]: {
              tiprackLabwareDef,
              spec: getPipetteNameSpecs(command.params.pipetteName),
            },
          },
        }
      }
      return acc
    },
    {
      labwareEntities: {},
      moduleEntities: {},
      pipetteEntities: {},
      config: { OT_PD_DISABLE_MODULE_RESTRICTIONS: true },
    }
  )
}