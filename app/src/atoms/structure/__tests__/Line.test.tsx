import * as React from 'react'
import { renderWithProviders, SPACING, COLORS } from '@opentrons/components'
import { Line } from '../index'

const render = (props: React.ComponentProps<typeof Line>) => {
  return renderWithProviders(<Line {...props} />)[0]
}

describe('Line', () => {
  let props: React.ComponentProps<typeof Line>

  beforeEach(() => {
    props = {
      width: '100%',
    }
  })

  it('renders line', () => {
    const { getByTestId } = render(props)
    const line = getByTestId('line')
    expect(line).toHaveStyle('width: 100%')
    expect(line).toHaveStyle(`borderBottom: 1px solid ${COLORS.medGreyEnabled}`)
  })

  it('renders line with additional props', () => {
    props = {
      ...props,
      width: '80%',
      color: COLORS.blueEnabled,
      marginY: 0,
      paddingX: SPACING.spacing2,
    }
    const { getByTestId } = render(props)
    const line = getByTestId('line')
    expect(line).toHaveStyle(`color: ${COLORS.blueEnabled}`)
    expect(line).toHaveStyle('width: 80%')
    expect(line).toHaveStyle('margin-top: 0')
    expect(line).toHaveStyle('margin-bottom: 0')
    expect(line).toHaveStyle('padding-left: 0.25rem')
    expect(line).toHaveStyle('padding-right: 0.25rem')
  })
})
