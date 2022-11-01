import * as React from 'react'
import { useTranslation } from 'react-i18next'
import { Flex } from '@opentrons/components'
import { StyledText } from '../../atoms/text'
import { GenericWizardTile } from '../../molecules/GenericWizardTile'
import { InProgressModal } from '../../molecules/InProgressModal/InProgressModal'
import attachProbe from '../../assets/images/change-pip/attach-stem.png'
import pipetteCalibrating from '../../assets/images/change-pip/pipette-is-calibrating.png'
import type { PipetteWizardStepProps } from './types'

export const AttachStem = (props: PipetteWizardStepProps): JSX.Element => {
  const {
    proceed,
    attachedPipette,
    chainRunCommands,
    mount,
    isRobotMoving,
    goBack,
  } = props
  const motorAxis = mount === 'left' ? 'leftZ' : 'rightZ'
  const pipetteId = attachedPipette[mount].id
  const handleOnClick = (): void => {
    chainRunCommands([
      {
        commandType: 'calibration/moveToLocation' as const,
        params: {
          pipetteId: pipetteId,
          location: 'probePosition',
        },
      },
      {
        commandType: 'calibration/calibratePipette' as const,
        params: {
          mount: mount,
        },
      },
      {
        commandType: 'home' as const,
        params: {
          axes: [motorAxis],
        },
      },
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

  const { t } = useTranslation('pipette_wizard_flows')
  const pipetteCalibratingImage = (
    <Flex marginTop="-5.2rem" height="10.2rem">
      <img src={pipetteCalibrating} alt="Pipette is calibrating" />
    </Flex>
  )

  if (isRobotMoving)
    return (
      <InProgressModal
        alternativeSpinner={pipetteCalibratingImage}
        description={t('pipette_calibrating')}
      />
    )
  return (
    <GenericWizardTile
      header={t('attach_stem')}
      //  TODO(Jr, 10/26/22): replace image with correct one!
      rightHandBody={<img src={attachProbe} width="100%" alt="Attach stem" />}
      bodyText={<StyledText as="p">{t('install_probe')}</StyledText>}
      proceedButtonText={t('initiate_calibration')}
      proceed={handleOnClick}
      back={goBack}
    />
  )
}
