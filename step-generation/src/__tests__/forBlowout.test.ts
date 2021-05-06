import { forBlowout as _forBlowout } from '../getNextRobotStateAndWarnings/forBlowout'
import { makeImmutableStateUpdater } from '../__utils__'
import {
  makeContext,
  getRobotStateWithTipStandard,
  DEFAULT_PIPETTE,
  SOURCE_LABWARE,
} from '../__fixtures__'
import type { BlowoutParams } from '@opentrons/shared-data/protocol/types/schemaV3'
import type { InvariantContext, RobotState } from '../types'

const forBlowout = makeImmutableStateUpdater(_forBlowout)
let invariantContext: InvariantContext
let robotStateWithTip: RobotState
let params: BlowoutParams
beforeEach(() => {
  invariantContext = makeContext()
  robotStateWithTip = getRobotStateWithTipStandard(invariantContext)
  params = {
    pipette: DEFAULT_PIPETTE,
    labware: SOURCE_LABWARE,
    well: 'A1',
    flowRate: 21.1,
    offsetFromBottomMm: 1.3,
  }
})
describe('Blowout command', () => {
  describe('liquid tracking', () => {
    it('blowout updates with max volume of pipette', () => {
      robotStateWithTip.liquidState.pipettes.p300SingleId['0'] = {
        ingred1: {
          volume: 150,
        },
      }
      const result = forBlowout(params, invariantContext, robotStateWithTip)
      expect(result).toMatchObject({
        robotState: {
          liquidState: {
            pipettes: {
              p300SingleId: {
                '0': {
                  ingred1: {
                    volume: 0,
                  },
                },
              },
            },
            labware: {
              sourcePlateId: {
                A1: {
                  ingred1: {
                    volume: 150,
                  },
                },
              },
            },
          },
        },
      })
    })
  })
})
