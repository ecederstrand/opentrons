import { PipetteName } from '@opentrons/shared-data'
import { when, resetAllWhenMocks } from 'jest-when'
import { getPipetteWorkflow } from '../getPipetteWorkflow'
import { doesPipetteVisitAllTipracks } from '../../utils/doesPipetteVisitAllTipracks'
import type { RunTimeCommand } from '@opentrons/shared-data/protocol/types/schemaV6'
import type { LoadedLabware } from '@opentrons/shared-data'

jest.mock('../../utils/doesPipetteVisitAllTipracks')

const mockDoesPipetteVisitAllTipracks = doesPipetteVisitAllTipracks as jest.MockedFunction<
  typeof doesPipetteVisitAllTipracks
>

describe('getPipetteWorkflow', () => {
  afterEach(() => {
    resetAllWhenMocks()
  })
  it('should return 1 if there is only one pipette', () => {
    const pipetteNames: PipetteName[] = ['p1000_single']
    expect(
      getPipetteWorkflow({
        pipetteNames,
        primaryPipetteId: 'someId',
        labware: [] as LoadedLabware[],
        labwareDefinitions: {},
        commands: [],
      })
    ).toBe(1)
  })
  it('should return 1 if the two pipettes are the same', () => {
    const pipetteNames: PipetteName[] = ['p1000_single', 'p1000_single']
    expect(
      getPipetteWorkflow({
        pipetteNames,
        primaryPipetteId: 'someId',
        labware: [] as LoadedLabware[],
        labwareDefinitions: {},
        commands: [],
      })
    ).toBe(1)
  })
  it('should return 1 if the primary pipette visits all tipracks', () => {
    const pipetteNames: PipetteName[] = ['p1000_single', 'p1000_single_gen2']
    const primaryPipetteId = 'someId'
    const labware: LoadedLabware[] = []
    const labwareDefinitions = {}
    const moveToWellCommand: RunTimeCommand = {
      id: '1',
      commandType: 'moveToWell',
      params: {
        pipetteId: '',
        labwareId: '',
        wellName: '',
        wellLocation: {
          origin: 'top',
          offset: {
            x: 0,
            y: 0,
            z: 0,
          },
        },
      },
    } as any
    const commands: RunTimeCommand[] = [moveToWellCommand]

    when(mockDoesPipetteVisitAllTipracks)
      .calledWith(primaryPipetteId, labware, labwareDefinitions, commands)
      .mockReturnValue(true)

    expect(
      getPipetteWorkflow({
        pipetteNames,
        primaryPipetteId,
        labware,
        labwareDefinitions,
        commands,
      })
    ).toBe(1)
  })
  it('should return 2 if the primary pipette does NOT visit all tipracks', () => {
    const pipetteNames: PipetteName[] = ['p1000_single', 'p1000_single_gen2']
    const primaryPipetteId = 'someId'
    const labware: LoadedLabware[] = []
    const labwareDefinitions = {}
    const moveToWellCommand: RunTimeCommand = {
      id: '1',
      commandType: 'moveToWell',
      params: {
        pipetteId: '',
        labwareId: '',
        wellName: '',
        wellLocation: {
          origin: 'top',
          offset: {
            x: 0,
            y: 0,
            z: 0,
          },
        },
      },
    } as any
    const commands: RunTimeCommand[] = [moveToWellCommand]

    when(mockDoesPipetteVisitAllTipracks)
      .calledWith(primaryPipetteId, labware, labwareDefinitions, commands)
      .mockReturnValue(false)

    expect(
      getPipetteWorkflow({
        pipetteNames,
        primaryPipetteId,
        labware,
        labwareDefinitions,
        commands,
      })
    ).toBe(2)
  })
})
