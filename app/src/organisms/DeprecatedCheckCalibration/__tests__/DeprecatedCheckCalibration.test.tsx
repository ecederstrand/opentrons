import * as React from 'react'
import { Provider } from 'react-redux'
import { mount } from 'enzyme'
import { act } from 'react-dom/test-utils'
import { when, resetAllWhenMocks } from 'jest-when'

import * as Sessions from '../../../redux/sessions'
import { getDeckDefinitions } from '@opentrons/components/src/hardware-sim/Deck/getDeckDefinitions'
import { mockCalibrationCheckSessionAttributes } from '../../../redux/sessions/__fixtures__'

import { DeprecatedCheckCalibration } from '../index'
import { ResultsSummary } from '../ResultsSummary'
import { ReturnTip } from '../ReturnTip'
import {
  Introduction,
  DeckSetup,
  TipPickUp,
  TipConfirmation,
  SaveXYPoint,
  SaveZPoint,
} from '../../DeprecatedCalibrationPanels'

import type { ReactWrapper } from 'enzyme'
import type { Dispatch } from '../../../redux/types'
import type { RobotCalibrationCheckStep } from '../../../redux/sessions/types'

jest.mock('@opentrons/components/src/hardware-sim/Deck/getDeckDefinitions')
jest.mock('../../../redux/calibration/selectors')
jest.mock('../../../redux/config')

interface DeprecatedCheckCalibrationSpec {
  component: React.ComponentType<any>
  currentStep: RobotCalibrationCheckStep
}

const mockGetDeckDefinitions = getDeckDefinitions as jest.MockedFunction<
  typeof getDeckDefinitions
>

describe('DeprecatedCheckCalibration', () => {
  let mockStore: any
  let render: (
    props?: Partial<React.ComponentProps<typeof DeprecatedCheckCalibration>>
  ) => ReactWrapper<React.ComponentProps<typeof DeprecatedCheckCalibration>>
  let dispatch: jest.MockedFunction<Dispatch>
  let dispatchRequests: jest.MockedFunction<any>
  let mockCalibrationCheckSession: Sessions.CalibrationCheckSession = {
    id: 'fake_check_session_id',
    ...mockCalibrationCheckSessionAttributes,
  }
  const getExitButton = (
    wrapper: ReactWrapper<
      React.ComponentProps<typeof DeprecatedCheckCalibration>
    >
  ) => wrapper.find('button[title="exit"]')

  const POSSIBLE_CHILDREN = [
    Introduction,
    DeckSetup,
    TipPickUp,
    TipConfirmation,
    SaveZPoint,
    SaveXYPoint,
    ResultsSummary,
  ]

  const SPECS: DeprecatedCheckCalibrationSpec[] = [
    { component: Introduction, currentStep: 'sessionStarted' },
    { component: DeckSetup, currentStep: 'labwareLoaded' },
    { component: TipPickUp, currentStep: 'preparingPipette' },
    { component: TipConfirmation, currentStep: 'inspectingTip' },
    { component: SaveZPoint, currentStep: 'comparingHeight' },
    { component: SaveXYPoint, currentStep: 'comparingPointOne' },
    { component: SaveXYPoint, currentStep: 'comparingPointTwo' },
    { component: SaveXYPoint, currentStep: 'comparingPointThree' },
    { component: ReturnTip, currentStep: 'returningTip' },
    { component: ResultsSummary, currentStep: 'resultsSummary' },
  ]

  beforeEach(() => {
    dispatch = jest.fn()
    mockStore = {
      subscribe: () => {},
      getState: () => ({
        robotApi: {},
      }),
      dispatch,
    }
    when(mockGetDeckDefinitions).calledWith().mockReturnValue({})

    mockCalibrationCheckSession = {
      id: 'fake_check_session_id',
      ...mockCalibrationCheckSessionAttributes,
    }
    dispatchRequests = jest.fn()

    render = (
      props: Partial<
        React.ComponentProps<typeof DeprecatedCheckCalibration>
      > = {}
    ) => {
      const { showSpinner = false, isJogging = false } = props
      return mount(
        <DeprecatedCheckCalibration
          robotName="robot-name"
          session={mockCalibrationCheckSession}
          dispatchRequests={dispatchRequests}
          showSpinner={showSpinner}
          hasBlock={false}
          isJogging={isJogging}
        />,
        {
          wrappingComponent: Provider,
          wrappingComponentProps: { store: mockStore },
        }
      )
    }
  })

  afterEach(() => {
    resetAllWhenMocks()
  })

  SPECS.forEach(spec => {
    it(`renders correct contents when currentStep is ${spec.currentStep}`, () => {
      mockCalibrationCheckSession = {
        ...mockCalibrationCheckSession,
        details: {
          ...mockCalibrationCheckSession.details,
          currentStep: spec.currentStep,
        },
      } as any
      const wrapper = render()
      POSSIBLE_CHILDREN.forEach(child => {
        if (child === spec.component) {
          expect(wrapper.exists(child)).toBe(true)
        } else {
          expect(wrapper.exists(child)).toBe(false)
        }
      })
    })
  })

  it('renders confirm exit modal on exit click', () => {
    const wrapper = render()

    expect(wrapper.find('ConfirmExitModal').exists()).toBe(false)
    act(() =>
      getExitButton(wrapper).invoke('onClick')?.({} as React.MouseEvent)
    )
    wrapper.update()
    expect(wrapper.find('ConfirmExitModal').exists()).toBe(true)
  })

  it('does not render spinner when showSpinner is false', () => {
    const wrapper = render({ showSpinner: false })
    expect(wrapper.find('SpinnerModalPage').exists()).toBe(false)
  })

  it('renders spinner when showSpinner is true', () => {
    const wrapper = render({ showSpinner: true })
    expect(wrapper.find('SpinnerModalPage').exists()).toBe(true)
  })

  it('does dispatch jog requests when not isJogging', () => {
    mockCalibrationCheckSession = {
      ...mockCalibrationCheckSession,
      details: {
        ...mockCalibrationCheckSession.details,
        currentStep: 'preparingPipette',
      },
    }
    const wrapper = render({ isJogging: false })
    wrapper.find('button[title="forward"]').invoke('onClick')?.(
      {} as React.MouseEvent
    )
    expect(dispatchRequests).toHaveBeenCalledWith(
      Sessions.createSessionCommand(
        'robot-name',
        mockCalibrationCheckSession.id,
        {
          command: Sessions.sharedCalCommands.JOG,
          data: { vector: [0, -0.1, 0] },
        }
      )
    )
  })
  it('does not dispatch jog requests when isJogging', () => {
    mockCalibrationCheckSession = {
      ...mockCalibrationCheckSession,
      details: {
        ...mockCalibrationCheckSession.details,
        currentStep: 'preparingPipette',
      },
    }
    const wrapper = render({ isJogging: true })
    dispatch.mockClear()
    wrapper.find('button[title="forward"]').invoke('onClick')?.(
      {} as React.MouseEvent
    )
    expect(dispatchRequests).not.toHaveBeenCalled()
  })
})
