import semver from 'semver'
import { createSelector } from 'reselect'

import {
  HEALTH_STATUS_OK,
  getViewableRobots,
  getRobotApiVersion,
  getRobotByName,
} from '../discovery'
import * as Constants from './constants'

import type { State } from '../types'
import type { ViewableRobot } from '../discovery/types'
import type {
  BuildrootUpdateInfo,
  BuildrootUpdateSession,
  BuildrootUpdateType,
  RobotSystemType,
} from './types'

// TODO(mc, 2020-08-02): i18n
const UPDATE_SERVER_UNAVAILABLE =
  "Unable to update because your robot's update server is not responding."
const OTHER_ROBOT_UPDATING =
  'Unable to update because the app is currently updating a different robot.'
const NO_UPDATE_FILES =
  'Unable to retrieve update for this robot. Ensure your computer is connected to the internet and try again later.'
const UNAVAILABLE = 'Update unavailable'

export function getBuildrootUpdateVersion(state: State): string | null {
  return state.buildroot.version || null
}

export function getBuildrootUpdateInfo(
  state: State
): BuildrootUpdateInfo | null {
  return state.buildroot.info || null
}

export function getBuildrootTargetVersion(state: State): string | null {
  return (
    state.buildroot.session?.userFileInfo?.version ||
    state.buildroot.version ||
    null
  )
}

export function getBuildrootUpdateSeen(state: State): boolean {
  return state.buildroot.seen || false
}

export function getBuildrootUpdateInProgress(
  state: State,
  robot: ViewableRobot
): boolean {
  const session = getBuildrootSession(state)
  const brRobot = getBuildrootRobot(state)

  return (
    robot === brRobot &&
    session?.step !== Constants.FINISHED &&
    session?.error === null
  )
}

export function getBuildrootDownloadProgress(state: State): number | null {
  return state.buildroot.downloadProgress
}

export function getBuildrootDownloadError(state: State): string | null {
  return state.buildroot.downloadError
}

export function getBuildrootSession(
  state: State
): BuildrootUpdateSession | null {
  return state.buildroot.session
}

export function getBuildrootRobotName(state: State): string | null {
  return state.buildroot.session?.robotName || null
}

export const getBuildrootRobot: (
  state: State
) => ViewableRobot | null = createSelector(
  getViewableRobots,
  getBuildrootRobotName,
  (robots, robotName) => {
    if (robotName === null) {
      console.log('returning null!')
      return null
    }

    return (
      robots.find(robot => {
        const searchName =
          robot.serverHealth?.capabilities?.buildrootUpdate != null ||
          robot.serverHealth?.capabilities.systemUpdate != null
            ? robotName.replace(/^opentrons-/, '')
            : robotName
        console.log(robot.name)

        return robot.name === searchName
      }) || null
    )
  }
)

const getBuildrootUpdateType = (
  currentVersion: string | null,
  updateVersion: string | null
): BuildrootUpdateType | null => {
  const validCurrent: string | null = semver.valid(currentVersion)
  const validUpdate: string | null = semver.valid(updateVersion)
  let type = null

  if (validUpdate && validCurrent) {
    if (semver.gt(validUpdate, validCurrent)) {
      type = Constants.UPGRADE
    } else if (semver.lt(validUpdate, validCurrent)) {
      type = Constants.DOWNGRADE
    } else if (semver.eq(validUpdate, validCurrent)) {
      type = Constants.REINSTALL
    }
  }

  return type
}

export function getBuildrootUpdateAvailable(
  state: State,
  robot: ViewableRobot
): BuildrootUpdateType | null {
  const currentVersion = getRobotApiVersion(robot)
  const updateVersion = getBuildrootUpdateVersion(state)

  return getBuildrootUpdateType(currentVersion, updateVersion)
}

export const getBuildrootUpdateDisplayInfo: (
  state: State,
  robotName: string
) => {
  autoUpdateAction: string
  autoUpdateDisabledReason: string | null
  updateFromFileDisabledReason: string | null
} = createSelector(
  getRobotByName,
  state => getBuildrootRobot(state),
  state => getBuildrootUpdateVersion(state),
  (robot, currentUpdatingRobot, updateVersion) => {
    const robotVersion = robot ? getRobotApiVersion(robot) : null
    const autoUpdateType = getBuildrootUpdateType(robotVersion, updateVersion)
    const autoUpdateAction = autoUpdateType ?? UNAVAILABLE
    let autoUpdateDisabledReason = null
    let updateFromFileDisabledReason = null

    if (robot?.serverHealthStatus !== HEALTH_STATUS_OK) {
      autoUpdateDisabledReason = UPDATE_SERVER_UNAVAILABLE
      updateFromFileDisabledReason = UPDATE_SERVER_UNAVAILABLE
    } else if (
      currentUpdatingRobot !== null &&
      currentUpdatingRobot.name !== robot?.name
    ) {
      autoUpdateDisabledReason = OTHER_ROBOT_UPDATING
      updateFromFileDisabledReason = OTHER_ROBOT_UPDATING
    } else if (autoUpdateType === null) {
      autoUpdateDisabledReason = NO_UPDATE_FILES
    }

    return {
      autoUpdateAction,
      autoUpdateDisabledReason,
      updateFromFileDisabledReason,
    }
  }
)

export function getRobotSystemType(
  robot: ViewableRobot
): RobotSystemType | null {
  const { serverHealth } = robot

  if (serverHealth) {
    const { capabilities } = serverHealth

    if (!capabilities || capabilities.balenaUpdate) {
      return Constants.BALENA
    }

    return Constants.BUILDROOT
  }

  return null
}
