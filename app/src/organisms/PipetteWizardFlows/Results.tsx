import * as React from 'react'
import { useTranslation } from 'react-i18next'
import {
  NINETY_SIX_CHANNEL,
  SINGLE_MOUNT_PIPETTES,
} from '@opentrons/shared-data'
import { COLORS, TEXT_TRANSFORM_CAPITALIZE } from '@opentrons/components'
import { PrimaryButton } from '../../atoms/buttons'
import { SimpleWizardBody } from '../../molecules/SimpleWizardBody'
import { FLOWS } from './constants'
import { getIsGantryEmpty } from './utils'
import type { PipetteWizardStepProps } from './types'

interface ResultsProps extends PipetteWizardStepProps {
  handleCleanUpAndClose: () => void
  currentStepIndex: number
}

export const Results = (props: ResultsProps): JSX.Element => {
  const {
    proceed,
    flowType,
    attachedPipette,
    mount,
    handleCleanUpAndClose,
    selectedPipette,
    currentStepIndex,
  } = props
  const { t } = useTranslation(['pipette_wizard_flows', 'shared'])
  const isGantryEmpty = getIsGantryEmpty(attachedPipette)
  const is96ChannelAttachFailedToDetachOthers =
    flowType === FLOWS.ATTACH &&
    selectedPipette === NINETY_SIX_CHANNEL &&
    currentStepIndex === 2 &&
    !isGantryEmpty
  const is96ChannelAttachFlowPostCal =
    selectedPipette === NINETY_SIX_CHANNEL &&
    (currentStepIndex === 7 || currentStepIndex === 9)
  const isSinlgeMountAttachFlowPostCal =
    selectedPipette === SINGLE_MOUNT_PIPETTES && currentStepIndex === 5

  let header: string = 'unknown results screen'
  let iconColor: string = COLORS.successEnabled
  let isSuccess: boolean = true
  let buttonText: string = t('shared:exit')
  switch (flowType) {
    case FLOWS.CALIBRATE: {
      header = t('pip_cal_success')
      break
    }
    case FLOWS.ATTACH: {
      //  96-channel attachment with pipette attached before hand failed to detach
      if (
        !isGantryEmpty &&
        selectedPipette === NINETY_SIX_CHANNEL &&
        currentStepIndex === 2
      ) {
        header = t('pipette_failed_to_detach')
        iconColor = COLORS.errorEnabled
        isSuccess = false
        //  96-channel attachment with pipette attached before hand succeeded to detach
      } else if (
        isGantryEmpty &&
        selectedPipette === NINETY_SIX_CHANNEL &&
        currentStepIndex === 2
      ) {
        header = t('pipette_detached')
        buttonText = t('continue')
      } else if (attachedPipette[mount] != null) {
        const pipetteName = attachedPipette[mount]?.modelSpecs.displayName
        //  attach flow followed by calibrate success
        if (is96ChannelAttachFlowPostCal || isSinlgeMountAttachFlowPostCal) {
          header = t('pip_cal_success')
          // normal attachment flow success
        } else {
          header = t('pipette_attached', { pipetteName: pipetteName })
          buttonText = t('cal_pipette')
        }
        // normal detachment flow fail
      } else {
        header = t('pipette_failed_to_attach')
        iconColor = COLORS.errorEnabled
        isSuccess = false
      }
      break
    }
    case FLOWS.DETACH: {
      if (attachedPipette[mount] != null) {
        header = t('pipette_failed_to_detach')
        iconColor = COLORS.errorEnabled
        isSuccess = false
      } else {
        header = t('pipette_detached')
      }
      break
    }
  }

  const handleProceed = (): void => {
    if (flowType === FLOWS.DETACH || is96ChannelAttachFailedToDetachOthers) {
      handleCleanUpAndClose()
    } else {
      proceed()
    }
  }

  return (
    <SimpleWizardBody
      iconColor={iconColor}
      header={header}
      isSuccess={isSuccess}
    >
      <PrimaryButton
        textTransform={TEXT_TRANSFORM_CAPITALIZE}
        onClick={handleProceed}
        aria-label="Results_exit"
      >
        {buttonText}
      </PrimaryButton>
    </SimpleWizardBody>
  )
}
