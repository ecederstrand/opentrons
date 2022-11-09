import * as React from 'react'

import { Flex, BORDERS, COLORS, SPACING } from '@opentrons/components'

import { StyledText } from '../text'

interface InstrumentContainerProps {
  displayName: string
  id?: string
}

export const InstrumentContainer = (
  props: InstrumentContainerProps
): JSX.Element => {
  const { displayName, id } = props

  return (
    <Flex
      backgroundColor={COLORS.fundamentalsBackgroundShade}
      borderRadius={BORDERS.radiusSoftCorners}
      paddingX={SPACING.spacing3}
      paddingY={SPACING.spacing1}
      width="max-content"
    >
      <StyledText as="p" id={id}>
        {displayName}
      </StyledText>
    </Flex>
  )
}
