import * as React from 'react'
import { MemoryRouter } from 'react-router-dom'
import { fireEvent } from '@testing-library/react'

import { renderWithProviders } from '@opentrons/components'

import { i18n } from '../../../../../i18n'
import { getRobotSettings } from '../../../../../redux/robot-settings'
import { useIsRobotBusy } from '../../../hooks'

import { LegacySettings } from '../LegacySettings'

jest.mock('../../../../../redux/robot-settings/selectors')
jest.mock('../../../hooks')

const mockUpdateRobotStatus = jest.fn()
const mockGetRobotSettings = getRobotSettings as jest.MockedFunction<
  typeof getRobotSettings
>
const mockUseIsRobotBusy = useIsRobotBusy as jest.MockedFunction<
  typeof useIsRobotBusy
>

const mockSettings = {
  id: 'deckCalibrationDots',
  title: 'Deck calibration to dots',
  description:
    'Perform deck calibration to dots rather than crosses, for robots that do not have crosses etched on the deck',
  value: true,
  restart_required: false,
}

const render = () => {
  return renderWithProviders(
    <MemoryRouter>
      <LegacySettings
        settings={mockSettings}
        robotName="otie"
        updateIsRobotBusy={mockUpdateRobotStatus}
      />
    </MemoryRouter>,
    { i18nInstance: i18n }
  )
}

describe('RobotSettings LegacySettings', () => {
  beforeEach(() => {
    mockGetRobotSettings.mockReturnValue([mockSettings])
    mockUseIsRobotBusy.mockReturnValue(false)
  })

  afterEach(() => {
    jest.resetAllMocks()
  })

  it('should render title, description, and toggle button', () => {
    const [{ getByText, getByRole }] = render()
    getByText('Legacy Settings')
    getByText('Calibrate deck to dots')
    getByText(
      'For pre-2019 robots that do not have crosses etched on the deck.'
    )
    const toggleButton = getByRole('switch', { name: 'legacy_settings' })
    expect(toggleButton.getAttribute('aria-checked')).toBe('true')
  })

  it('should change the value when a user clicks a toggle button', () => {
    const tempMockSettings = {
      ...mockSettings,
      value: false,
    }
    mockGetRobotSettings.mockReturnValue([tempMockSettings])
    const [{ getByRole }] = render()
    const toggleButton = getByRole('switch', {
      name: 'legacy_settings',
    })
    fireEvent.click(toggleButton)
    expect(toggleButton.getAttribute('aria-checked')).toBe('true')
  })

  it('should call update robot status if a robot is busy', () => {
    mockUseIsRobotBusy.mockReturnValue(true)
    const [{ getByRole }] = render()
    const toggleButton = getByRole('switch', {
      name: 'legacy_settings',
    })
    fireEvent.click(toggleButton)
    expect(mockUpdateRobotStatus).toHaveBeenCalled()
  })
})
