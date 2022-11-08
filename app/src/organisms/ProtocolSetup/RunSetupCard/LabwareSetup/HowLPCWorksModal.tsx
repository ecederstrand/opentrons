import * as React from 'react'
import { Trans, useTranslation } from 'react-i18next'
import {
  Btn,
  Box,
  Flex,
  Icon,
  Link,
  Modal,
  NewPrimaryBtn,
  Text,
  C_BLUE,
  C_MED_DARK_GRAY,
  FONT_SIZE_BODY_1,
  FONT_WEIGHT_REGULAR,
  FONT_WEIGHT_SEMIBOLD,
  JUSTIFY_CENTER,
  JUSTIFY_SPACE_BETWEEN,
  SIZE_2,
  SIZE_4,
  SPACING_2,
  SPACING_3,
  SPACING_1,
} from '@opentrons/components'
import { Portal } from '../../../../App/portal'
import styles from '../../styles.css'

const ROBOT_CAL_HELP_ARTICLE =
  'https://support.opentrons.com/s/article/How-positional-calibration-works-on-the-OT-2'
const OFFSET_DATA_HELP_ARTICLE =
  'https://support.opentrons.com/s/article/How-Labware-Offsets-work-on-the-OT-2'
interface HowLPCWorksModalProps {
  onCloseClick: () => unknown
}

export const HowLPCWorksModal = (props: HowLPCWorksModalProps): JSX.Element => {
  const { t } = useTranslation(['protocol_setup', 'shared'])
  return (
    <Portal level="top">
      <Modal className={styles.modal} contentsClassName={styles.modal_contents}>
        <Box marginX={SPACING_3}>
          <Flex justifyContent={JUSTIFY_SPACE_BETWEEN}>
            <Text as="h3" marginBottom={SPACING_3}>
              {t('how_offset_data_works_title')}
            </Text>
            <Btn size={SIZE_2} onClick={props.onCloseClick}>
              <Icon name="close" color={C_MED_DARK_GRAY}></Icon>
            </Btn>
          </Flex>
          <Trans
            t={t}
            i18nKey="position_offset_overview_and_description"
            components={{
              h4: (
                <Text
                  as="h4"
                  fontWeight={FONT_WEIGHT_SEMIBOLD}
                  marginBottom={SPACING_2}
                />
              ),
              block: <Text fontSize={FONT_SIZE_BODY_1} />,
            }}
          />
          <Link
            fontSize={FONT_SIZE_BODY_1}
            color={C_BLUE}
            href={ROBOT_CAL_HELP_ARTICLE}
            id="HowLPCWorksModal_helpArticleLink1"
            external
          >
            {t('learn_more_about_robot_cal_offset_modal_link')}
            <Icon name="open-in-new" marginLeft={SPACING_1} size="10px" />
          </Link>
          <Text
            marginTop={SPACING_2}
            fontSize={FONT_SIZE_BODY_1}
            fontWeight={FONT_WEIGHT_REGULAR}
          >
            {t('labware_offset_data_info')}
          </Text>
          <Link
            fontSize={FONT_SIZE_BODY_1}
            color={C_BLUE}
            href={OFFSET_DATA_HELP_ARTICLE}
            id="HowLPCWorksModal_helpArticleLink2"
            external
          >
            {t('learn_more_about_offset_data_link')}
            <Icon name="open-in-new" marginLeft={SPACING_1} size="10px" />
          </Link>
          <Trans
            t={t}
            i18nKey="creating_labware_offset_data"
            components={{
              h4: (
                <Text
                  as="h4"
                  marginTop={SPACING_3}
                  fontWeight={FONT_WEIGHT_SEMIBOLD}
                  marginBottom={SPACING_2}
                />
              ),
              block: (
                <Text fontSize={FONT_SIZE_BODY_1} marginBottom={SPACING_3} />
              ),
            }}
          />
          <Trans
            t={t}
            i18nKey="rerunning_a_protocol"
            components={{
              h4: (
                <Text
                  as="h4"
                  marginTop={SPACING_3}
                  fontWeight={FONT_WEIGHT_SEMIBOLD}
                  marginBottom={SPACING_2}
                />
              ),
              block: (
                <Text fontSize={FONT_SIZE_BODY_1} marginBottom={SPACING_3} />
              ),
            }}
          />
          <Flex justifyContent={JUSTIFY_CENTER} marginBottom={SPACING_3}>
            <NewPrimaryBtn
              onClick={props.onCloseClick}
              width={SIZE_4}
              id="LabwareSetupModal_closeButton"
            >
              {t('shared:close')}
            </NewPrimaryBtn>
          </Flex>
        </Box>
      </Modal>
    </Portal>
  )
}
