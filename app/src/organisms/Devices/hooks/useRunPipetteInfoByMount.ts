import last from 'lodash/last'
import { getPipetteNameSpecs, getLabwareDefURI } from '@opentrons/shared-data'
import { MATCH, INEXACT_MATCH, INCOMPATIBLE } from '../../../redux/pipettes'
import {
  useAttachedPipetteCalibrations,
  useAttachedPipettes,
  useTipLengthCalibrations,
  useProtocolDetailsForRun,
  useStoredProtocolAnalysis,
} from '.'

import type { LoadPipetteRunTimeCommand } from '@opentrons/shared-data/protocol/types/schemaV6/command/setup'
import type { PickUpTipRunTimeCommand } from '@opentrons/shared-data/protocol/types/schemaV6/command/pipetting'
import type {
  Mount,
  AttachedPipette,
  TipRackCalibrationData,
} from '../../../redux/pipettes/types'
import type {
  LabwareDefinition2,
  PipetteNameSpecs,
} from '@opentrons/shared-data'

const EMPTY_MOUNTS = { left: null, right: null }

export interface PipetteInfo {
  pipetteSpecs: PipetteNameSpecs
  tipRacksForPipette: TipRackCalibrationData[]
  requestedPipetteMatch:
    | typeof MATCH
    | typeof INEXACT_MATCH
    | typeof INCOMPATIBLE
  pipetteCalDate: string | null
}

export function useRunPipetteInfoByMount(
  robotName: string,
  runId: string
): {
  [mount in Mount]: PipetteInfo | null
} {
  const { protocolData: robotProtocolAnalysis } = useProtocolDetailsForRun(
    runId
  )
  const storedProtocolAnalysis = useStoredProtocolAnalysis(runId)
  const protocolData = robotProtocolAnalysis ?? storedProtocolAnalysis
  const attachedPipettes = useAttachedPipettes()
  const attachedPipetteCalibrations =
    useAttachedPipetteCalibrations(robotName) ?? EMPTY_MOUNTS
  const tipLengthCalibrations = useTipLengthCalibrations(robotName) ?? []

  if (protocolData == null) {
    return EMPTY_MOUNTS
  }
  const { pipettes, labware, labwareDefinitions, commands } = protocolData
  const loadPipetteCommands = commands.filter(
    (command): command is LoadPipetteRunTimeCommand =>
      command.commandType === 'loadPipette'
  )
  const pickUpTipCommands = commands.filter(
    (command): command is PickUpTipRunTimeCommand =>
      command.commandType === 'pickUpTip'
  )

  return pipettes.reduce((acc, pipette) => {
    const loadCommand = loadPipetteCommands.find(
      command => command.result?.pipetteId === pipette.id
    )
    if (loadCommand != null) {
      const { mount } = loadCommand.params
      const { pipetteId } = loadCommand.result
      const pipetteName = pipette.pipetteName
      const requestedPipetteName = pipetteName
      const pipetteSpecs = getPipetteNameSpecs(requestedPipetteName)
      if (pipetteSpecs != null) {
        const tipRackDefs: LabwareDefinition2[] = pickUpTipCommands.reduce<
          LabwareDefinition2[]
        >((acc, command) => {
          if (pipetteId === command.params?.pipetteId) {
            const tipRack = labware.find(
              item => item.id === command.params?.labwareId
            )
            const tipRackDefinition =
              tipRack?.definitionUri != null
                ? labwareDefinitions[tipRack.definitionUri]
                : null

            if (tipRackDefinition != null && !acc.includes(tipRackDefinition)) {
              return [...acc, tipRackDefinition]
            }
          }
          return acc
        }, [])

        const attachedPipette = attachedPipettes[mount as Mount]
        const requestedPipetteMatch = getRequestedPipetteMatch(
          pipetteName,
          attachedPipette
        )
        const tipRacksForPipette = tipRackDefs.map(tipRackDef => {
          const tlcDataMatch = last(
            tipLengthCalibrations.filter(
              tlcData =>
                tlcData.uri === getLabwareDefURI(tipRackDef) &&
                attachedPipette != null &&
                tlcData.pipette === attachedPipette.id
            )
          )
          const lastModifiedDate =
            tlcDataMatch != null && requestedPipetteMatch !== INCOMPATIBLE
              ? tlcDataMatch.lastModified
              : null
          return {
            displayName: tipRackDef.metadata.displayName,
            lastModifiedDate,
            tipRackDef,
          }
        })
        const pipetteCalDate =
          requestedPipetteMatch !== INCOMPATIBLE
            ? attachedPipetteCalibrations[mount]?.offset?.lastModified
            : null

        return {
          ...acc,
          [mount]: {
            pipetteName: requestedPipetteName,
            id: pipetteId,
            pipetteSpecs,
            tipRacksForPipette,
            requestedPipetteMatch,
            pipetteCalDate,
          },
        }
      } else {
        return acc
      }
    } else {
      return acc
    }
  }, EMPTY_MOUNTS)
}

function getRequestedPipetteMatch(
  requestedPipetteName: string,
  attachedPipette: AttachedPipette | null
): string {
  if (
    attachedPipette?.modelSpecs?.backCompatNames != null &&
    attachedPipette?.modelSpecs?.backCompatNames.includes(requestedPipetteName)
  ) {
    return INEXACT_MATCH
  } else if (requestedPipetteName === attachedPipette?.modelSpecs?.name) {
    return MATCH
  } else {
    return INCOMPATIBLE
  }
}
