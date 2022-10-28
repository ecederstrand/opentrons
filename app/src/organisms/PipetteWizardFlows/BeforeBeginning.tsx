import * as React from 'react'
import { UseMutateFunction } from 'react-query'
import { Trans, useTranslation } from 'react-i18next'
import { StyledText } from '../../atoms/text'
import { GenericWizardTile } from '../../molecules/GenericWizardTile'
import { InProgressModal } from '../../molecules/InProgressModal/InProgressModal'
import { WizardRequiredEquipmentList } from '../../molecules/WizardRequiredEquipmentList'
import { CALIBRATION_PROBE, FLOWS } from './constants'
import type { Run, CreateRunData } from '@opentrons/api-client'
import type { PipetteWizardStepProps } from './types'
import type { AxiosError } from 'axios'

const BEFORE_YOU_BEGIN_URL = '' //  TODO(jr, 10/26/22): link real URL!

interface BeforeBeginningProps extends PipetteWizardStepProps {
  createRun: UseMutateFunction<Run, AxiosError<any>, CreateRunData, unknown>
}

export const BeforeBeginning = (props: BeforeBeginningProps): JSX.Element => {
  const {
    proceed,
    flowType,
    createRun,
    attachedPipette,
    chainRunCommands,
    mount,
    isRobotMoving,
  } = props
  const { t } = useTranslation('pipette_wizard_flows')
  //  TODO(jr, 10/26/22): when we wire up other flows, const will turn into let
  //  for proceedButtonText and rightHandBody
  React.useEffect(() => {
    createRun({})
  }, [])

  const pipetteId = attachedPipette[mount].id

  const handleOnClick = (): void => {
    chainRunCommands([
      {
        commandType: 'calibration/moveToLocation' as const,
        params: {
          pipetteId: pipetteId,
          location: 'attachOrDetach',
        },
      },
    ]).then(() => {
      proceed()
    })
  }

  const proceedButtonText: string = t('get_started')
  const rightHandBody = (
    <WizardRequiredEquipmentList
      width="100%"
      equipmentList={[CALIBRATION_PROBE]}
    />
  )
  switch (flowType) {
    case FLOWS.CALIBRATE: {
      break
    }
    //  TODO(jr, 10/26/22): wire up the other flows
  }
  if (isRobotMoving) return <InProgressModal description={t('stand_back')} />
  return (
    <GenericWizardTile
      header={t('before_you_begin')}
      getHelp={BEFORE_YOU_BEGIN_URL}
      rightHandBody={rightHandBody}
      bodyText={
        <Trans
          t={t}
          i18nKey="remove_labware_to_get_started"
          components={{ block: <StyledText as="p" /> }}
        />
      }
      proceedButtonText={proceedButtonText}
      proceed={handleOnClick}
    />
  )
}
