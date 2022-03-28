import * as React from 'react'
import { Trans, useTranslation } from 'react-i18next'
import {
  Flex,
  ALIGN_CENTER,
  SPACING,
  TEXT_TRANSFORM_UPPERCASE,
} from '@opentrons/components'
import { getLabwareDisplayName } from '@opentrons/shared-data'

import { getLabwareLocation } from '../../../organisms/ProtocolSetup/utils/getLabwareLocation'
import {
  useLabwareRenderInfoForRunById,
  useProtocolDetailsForRun,
} from '../hooks'
import { RunLogProtocolSetupInfo } from './RunLogProtocolSetupInfo'

import type { RunTimeCommand } from '@opentrons/shared-data'
import type { RunCommandSummary } from '@opentrons/api-client'

const TRASH_ID = 'fixedTrash'

interface Props {
  analysisCommand: RunTimeCommand | null
  robotName: string
  runCommand: RunCommandSummary | null
  runId: string
}
export function StepText(props: Props): JSX.Element | null {
  const { analysisCommand, robotName, runCommand, runId } = props
  const { t } = useTranslation('run_details')
  const { protocolData } = useProtocolDetailsForRun(runId)
  const labwareRenderInfoById = useLabwareRenderInfoForRunById(runId)

  let messageNode = null

  const displayCommand = runCommand !== null ? runCommand : analysisCommand

  if (displayCommand === null) {
    console.warn(
      'display command should never be null, command text could find no source'
    )
    return null
  }
  // protocolData should never be null as we don't render the `RunDetails` unless we have an analysis
  // but we're experiencing a zombie children issue, see https://github.com/Opentrons/opentrons/pull/9091
  if (protocolData == null) {
    console.warn(
      'protocolData never be null, command text could find no protocolData'
    )
    return null
  }
  // params will not exist on command summaries
  switch (displayCommand.commandType) {
    case 'delay': {
      messageNode = (
        <>
          <Flex
            textTransform={TEXT_TRANSFORM_UPPERCASE}
            padding={SPACING.spacing2}
            id={`RunDetails_CommandList`}
          >
            {t('comment')}
          </Flex>
          {displayCommand != null ? displayCommand.result : null}
        </>
      )
      break
    }
    case 'dropTip': {
      const { wellName, labwareId } = displayCommand.params
      const labwareLocation = getLabwareLocation(
        labwareId,
        protocolData.commands
      )
      if (!('slotName' in labwareLocation)) {
        throw new Error('expected tip rack to be in a slot')
      }
      messageNode = (
        <Trans
          t={t}
          i18nKey={'drop_tip'}
          values={{
            well_name: wellName,
            labware:
              labwareId === TRASH_ID
                ? 'Opentrons Fixed Trash'
                : getLabwareDisplayName(
                    protocolData.labwareDefinitions[
                      protocolData.labware[labwareId].definitionId
                    ]
                  ),
            labware_location: labwareLocation.slotName,
          }}
        />
      )
      break
    }
    case 'pickUpTip': {
      const { wellName, labwareId } = displayCommand.params
      const labwareLocation = getLabwareLocation(
        labwareId,
        protocolData.commands
      )
      if (!('slotName' in labwareLocation)) {
        throw new Error('expected tip rack to be in a slot')
      }
      messageNode = (
        <Trans
          t={t}
          i18nKey={'pickup_tip'}
          values={{
            well_name: wellName,
            labware: getLabwareDisplayName(
              labwareRenderInfoById[labwareId].labwareDef
            ),
            labware_location: labwareLocation.slotName,
          }}
        />
      )
      break
    }
    case 'pause': {
      messageNode = displayCommand.params?.message ?? displayCommand.commandType
      break
    }
    case 'loadLabware':
    case 'loadPipette':
    case 'loadModule': {
      messageNode = (
        <RunLogProtocolSetupInfo
          robotName={robotName}
          runId={runId}
          setupCommand={displayCommand}
        />
      )
      break
    }
    case 'custom': {
      messageNode =
        displayCommand.params?.legacyCommandText ?? displayCommand.commandType
      break
    }
    default: {
      messageNode = displayCommand.commandType
      break
    }
  }

  return <Flex alignItems={ALIGN_CENTER}>{messageNode}</Flex>
}