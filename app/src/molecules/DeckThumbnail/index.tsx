import * as React from 'react'
import map from 'lodash/map'

import { RobotWorkSpace, Module, LabwareRender } from '@opentrons/components'
import { useFeatureFlag } from '../../redux/config'

import {
  inferModuleOrientationFromXCoordinate,
  getModuleDef2,
  getDeckDefFromLoadedLabware,
  getRobotTypeFromLoadedLabware,
  THERMOCYCLER_MODULE_V1,
} from '@opentrons/shared-data'
import {
  parseInitialLoadedLabwareBySlot,
  parseInitialLoadedLabwareByModuleId,
  parseInitialLoadedModulesBySlot,
  parseLiquidsInLoadOrder,
  parseLabwareInfoByLiquidId,
} from '@opentrons/api-client'
import type {
  DeckSlot,
  LoadedLabware,
  RunTimeCommand,
} from '@opentrons/shared-data'

interface DeckThumbnailProps {
  commands: RunTimeCommand[]
  labware: LoadedLabware[]
  showLiquids?: boolean
}
const deckSetupLayerBlocklist = [
  'calibrationMarkings',
  'fixedBase',
  'doorStops',
  'metalFrame',
  'removalHandle',
  'removableDeckOutline',
  'screwHoles',
]

export function DeckThumbnail(props: DeckThumbnailProps): JSX.Element {
  const { commands, labware, showLiquids } = props
  const robotType = getRobotTypeFromLoadedLabware(labware)
  const deckDef = getDeckDefFromLoadedLabware(robotType)
  const liquidSetupEnabled = useFeatureFlag('enableLiquidSetup')

  const initialLoadedLabwareBySlot = parseInitialLoadedLabwareBySlot(commands)
  const initialLoadedModulesBySlot = parseInitialLoadedModulesBySlot(commands)
  const initialLoadedLabwareByModuleId = parseInitialLoadedLabwareByModuleId(
    commands
  )
  const liquidsInLoadOrder = parseLiquidsInLoadOrder()
  const labwareByLiquidId = parseLabwareInfoByLiquidId()

  return (
    // PR #10488 changed size
    // revert the height
    // Note add offset 18px to right and left
    <RobotWorkSpace
      deckLayerBlocklist={deckSetupLayerBlocklist}
      deckDef={deckDef}
      viewBox="-75 -20 586 480"
    >
      {({ deckSlotsById }) =>
        map<DeckSlot>(deckSlotsById, (slot: DeckSlot, slotId: string) => {
          if (!slot.matingSurfaceUnitVector) return null // if slot has no mating surface, don't render anything in it

          const moduleInSlot =
            slotId in initialLoadedModulesBySlot
              ? initialLoadedModulesBySlot[slotId]
              : null
          const labwareInSlot =
            slotId in initialLoadedLabwareBySlot
              ? initialLoadedLabwareBySlot[slotId]
              : null
          const labwareInModule =
            moduleInSlot &&
            moduleInSlot.result.moduleId in initialLoadedLabwareByModuleId
              ? initialLoadedLabwareByModuleId[moduleInSlot.result.moduleId]
              : null
          let labwareId = labwareInSlot ? labwareInSlot.result.labwareId : null
          labwareId = labwareInModule
            ? labwareInModule.result.labwareId
            : labwareId
          const wellFill =
            labwareId && showLiquids && liquidSetupEnabled
              ? getWellFillFromLabwareId(
                  labwareId,
                  liquidsInLoadOrder,
                  labwareByLiquidId
                )
              : null
          return (
            <React.Fragment key={slotId}>
              {moduleInSlot != null ? (
                <Module
                  x={slot.position[0]}
                  y={slot.position[1]}
                  orientation={inferModuleOrientationFromXCoordinate(
                    slot.position[0]
                  )}
                  def={getModuleDef2(moduleInSlot.params.model)}
                  innerProps={
                    moduleInSlot.params.model === THERMOCYCLER_MODULE_V1
                      ? { lidMotorState: 'open' }
                      : {}
                  }
                >
                  {labwareInModule != null ? (
                    <LabwareRender
                      definition={labwareInModule.result.definition}
                      wellFill={wellFill ?? undefined}
                    />
                  ) : null}
                </Module>
              ) : null}
              {labwareInSlot != null ? (
                <g
                  transform={`translate(${slot.position[0]},${slot.position[1]})`}
                >
                  <LabwareRender
                    definition={labwareInSlot.result.definition}
                    wellFill={wellFill ?? undefined}
                  />
                </g>
              ) : null}
            </React.Fragment>
          )
        })
      }
    </RobotWorkSpace>
  )
}
