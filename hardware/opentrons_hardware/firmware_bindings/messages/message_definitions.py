"""Definition of CAN messages."""
from dataclasses import dataclass
from typing import Type

from typing_extensions import Literal

from ..constants import MessageId
from . import payloads
from .. import utils


class SingletonMessageIndexGenerator(object):
    """ Singlton class that generates uinque index values """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonMessageIndexGenerator, cls).__new__(cls)
        return cls.instance

    def get_next_index(self):
        # increment before returning so we never return 0 as a value
        self.__current_index += 1
        return self.__current_index

    __current_index = 0

@dataclass(eq=False)
class BaseMessage(object):
    """Base class of a message that has an empty payload."""

    def __post_init__(self):
        index_generator = SingletonMessageIndexGenerator()
        self.message_index = index_generator.get_next_index()

    def __eq__(self, other):
        other_dict = vars(other)
        self_dict = vars(self)
        for key in self_dict:
            if key != "message_index":
                if not (key in other_dict and self_dict[key] == other_dict[key]):
                    return False
        return True

    payload: payloads.EmptyPayload = payloads.EmptyPayload()
    payload_type: Type[payloads.EmptyPayload] = payloads.EmptyPayload
    message_index: Literal[utils.UInt32Field] = 0


@dataclass(eq=False)
class Acknowledgement(BaseMessage): # noqa: D101
    message_id: Literal[MessageId.acknowledgement] = MessageId.acknowledgement


@dataclass(eq=False)
class HeartbeatRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.heartbeat_request] = MessageId.heartbeat_request


@dataclass(eq=False)
class HeartbeatResponse(Acknowledgement):  # noqa: D101
    message_id: Literal[MessageId.heartbeat_response] = MessageId.heartbeat_response


@dataclass(eq=False)
class DeviceInfoRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.device_info_request] = MessageId.device_info_request


@dataclass(eq=False)
class DeviceInfoResponse(Acknowledgement):  # noqa: D101
    payload: payloads.DeviceInfoResponsePayload
    payload_type: Type[
        payloads.DeviceInfoResponsePayload
    ] = payloads.DeviceInfoResponsePayload
    message_id: Literal[MessageId.device_info_response] = MessageId.device_info_response


@dataclass(eq=False)
class TaskInfoRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.task_info_request] = MessageId.task_info_request


@dataclass(eq=False)
class TaskInfoResponse(Acknowledgement):  # noqa: D101
    payload: payloads.TaskInfoResponsePayload
    payload_type: Type[
        payloads.TaskInfoResponsePayload
    ] = payloads.TaskInfoResponsePayload
    message_id: Literal[MessageId.task_info_response] = MessageId.task_info_response


@dataclass(eq=False)
class StopRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.stop_request] = MessageId.stop_request


@dataclass(eq=False)
class GetStatusRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.get_status_request] = MessageId.get_status_request


@dataclass(eq=False)
class EnableMotorRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.enable_motor_request] = MessageId.enable_motor_request


@dataclass(eq=False)
class DisableMotorRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.disable_motor_request
    ] = MessageId.disable_motor_request


@dataclass(eq=False)
class GetStatusResponse(Acknowledgement):  # noqa: D101
    payload: payloads.GetStatusResponsePayload
    payload_type: Type[
        payloads.GetStatusResponsePayload
    ] = payloads.GetStatusResponsePayload
    message_id: Literal[MessageId.get_status_response] = MessageId.get_status_response


@dataclass(eq=False)
class MoveRequest(BaseMessage):  # noqa: D101
    payload: payloads.MoveRequestPayload
    payload_type: Type[payloads.MoveRequestPayload] = payloads.MoveRequestPayload
    message_id: Literal[MessageId.move_request] = MessageId.move_request


@dataclass(eq=False)
class WriteToEEPromRequest(BaseMessage):  # noqa: D101
    payload: payloads.EEPromDataPayload
    payload_type: Type[payloads.EEPromDataPayload] = payloads.EEPromDataPayload
    message_id: Literal[MessageId.write_eeprom] = MessageId.write_eeprom


@dataclass(eq=False)
class ReadFromEEPromRequest(BaseMessage):  # noqa: D101
    payload: payloads.EEPromReadPayload
    payload_type: Type[payloads.EEPromReadPayload] = payloads.EEPromReadPayload
    message_id: Literal[MessageId.read_eeprom_request] = MessageId.read_eeprom_request


@dataclass(eq=False)
class ReadFromEEPromResponse(Acknowledgement):  # noqa: D101
    payload: payloads.EEPromDataPayload
    payload_type: Type[payloads.EEPromDataPayload] = payloads.EEPromDataPayload
    message_id: Literal[MessageId.read_eeprom_response] = MessageId.read_eeprom_response


@dataclass(eq=False)
class AddLinearMoveRequest(BaseMessage):  # noqa: D101
    payload: payloads.AddLinearMoveRequestPayload
    payload_type: Type[
        payloads.AddLinearMoveRequestPayload
    ] = payloads.AddLinearMoveRequestPayload
    message_id: Literal[MessageId.add_move_request] = MessageId.add_move_request


@dataclass(eq=False)
class GetMoveGroupRequest(BaseMessage):  # noqa: D101
    payload: payloads.MoveGroupRequestPayload
    payload_type: Type[
        payloads.MoveGroupRequestPayload
    ] = payloads.MoveGroupRequestPayload
    message_id: Literal[
        MessageId.get_move_group_request
    ] = MessageId.get_move_group_request


@dataclass(eq=False)
class GetMoveGroupResponse(Acknowledgement):  # noqa: D101
    payload: payloads.GetMoveGroupResponsePayload
    payload_type: Type[
        payloads.GetMoveGroupResponsePayload
    ] = payloads.GetMoveGroupResponsePayload
    message_id: Literal[
        MessageId.get_move_group_response
    ] = MessageId.get_move_group_response


@dataclass(eq=False)
class ExecuteMoveGroupRequest(BaseMessage):  # noqa: D101
    payload: payloads.ExecuteMoveGroupRequestPayload
    payload_type: Type[
        payloads.ExecuteMoveGroupRequestPayload
    ] = payloads.ExecuteMoveGroupRequestPayload
    message_id: Literal[
        MessageId.execute_move_group_request
    ] = MessageId.execute_move_group_request


@dataclass(eq=False)
class ClearAllMoveGroupsRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.clear_all_move_groups_request
    ] = MessageId.clear_all_move_groups_request


@dataclass(eq=False)
class MoveCompleted(Acknowledgement):  # noqa: D101
    payload: payloads.MoveCompletedPayload
    payload_type: Type[payloads.MoveCompletedPayload] = payloads.MoveCompletedPayload
    message_id: Literal[MessageId.move_completed] = MessageId.move_completed


@dataclass(eq=False)
class EncoderPositionRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.encoder_position_request
    ] = MessageId.encoder_position_request


@dataclass(eq=False)
class EncoderPositionResponse(Acknowledgement):  # noqa: D101
    payload: payloads.EncoderPositionResponse
    payload_type: Type[
        payloads.EncoderPositionResponse
    ] = payloads.EncoderPositionResponse
    message_id: Literal[
        MessageId.encoder_position_response
    ] = MessageId.encoder_position_response


@dataclass(eq=False)
class SetMotionConstraints(BaseMessage):  # noqa: D101
    payload: payloads.MotionConstraintsPayload
    payload_type: Type[
        payloads.MotionConstraintsPayload
    ] = payloads.MotionConstraintsPayload
    message_id: Literal[
        MessageId.set_motion_constraints
    ] = MessageId.set_motion_constraints


@dataclass(eq=False)
class GetMotionConstraintsRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.get_motion_constraints_request
    ] = MessageId.get_motion_constraints_request


@dataclass(eq=False)
class GetMotionConstraintsResponse(Acknowledgement):  # noqa: D101
    payload: payloads.MotionConstraintsPayload
    payload_type: Type[
        payloads.MotionConstraintsPayload
    ] = payloads.MotionConstraintsPayload
    message_id: Literal[
        MessageId.get_motion_constraints_response
    ] = MessageId.get_motion_constraints_response


@dataclass(eq=False)
class WriteMotorDriverRegister(BaseMessage):  # noqa: D101
    payload: payloads.MotorDriverRegisterDataPayload
    payload_type: Type[
        payloads.MotorDriverRegisterPayload
    ] = payloads.MotorDriverRegisterDataPayload
    message_id: Literal[
        MessageId.write_motor_driver_register_request
    ] = MessageId.write_motor_driver_register_request


@dataclass(eq=False)
class ReadMotorDriverRequest(BaseMessage):  # noqa: D101
    payload: payloads.MotorDriverRegisterPayload
    payload_type: Type[
        payloads.MotorDriverRegisterPayload
    ] = payloads.MotorDriverRegisterPayload
    message_id: Literal[
        MessageId.read_motor_driver_register_request
    ] = MessageId.read_motor_driver_register_request


@dataclass(eq=False)
class ReadMotorDriverResponse(Acknowledgement):  # noqa: D101
    payload: payloads.ReadMotorDriverRegisterResponsePayload
    payload_type: Type[
        payloads.ReadMotorDriverRegisterResponsePayload
    ] = payloads.ReadMotorDriverRegisterResponsePayload
    message_id: Literal[
        MessageId.read_motor_driver_register_response
    ] = MessageId.read_motor_driver_register_response


@dataclass(eq=False)
class WriteMotorCurrentRequest(BaseMessage):  # noqa: D101
    payload: payloads.MotorCurrentPayload
    payload_type: Type[payloads.MotorCurrentPayload] = payloads.MotorCurrentPayload
    message_id: Literal[
        MessageId.write_motor_current_request
    ] = MessageId.write_motor_current_request


@dataclass(eq=False)
class ReadPresenceSensingVoltageRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.read_presence_sensing_voltage_request
    ] = MessageId.read_presence_sensing_voltage_request


@dataclass(eq=False)
class ReadPresenceSensingVoltageResponse(Acknowledgement):  # noqa: D101
    payload: payloads.ReadPresenceSensingVoltageResponsePayload
    payload_type: Type[
        payloads.ReadPresenceSensingVoltageResponsePayload
    ] = payloads.ReadPresenceSensingVoltageResponsePayload
    message_id: Literal[
        MessageId.read_presence_sensing_voltage_response
    ] = MessageId.read_presence_sensing_voltage_response


@dataclass(eq=False)
class PushToolsDetectedNotification(BaseMessage):  # noqa: D101
    payload: payloads.ToolsDetectedNotificationPayload
    payload_type: Type[
        payloads.ToolsDetectedNotificationPayload
    ] = payloads.ToolsDetectedNotificationPayload
    message_id: Literal[
        MessageId.tools_detected_notification
    ] = MessageId.tools_detected_notification


@dataclass(eq=False)
class AttachedToolsRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.attached_tools_request
    ] = MessageId.attached_tools_request


@dataclass(eq=False)
class FirmwareUpdateInitiate(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.fw_update_initiate] = MessageId.fw_update_initiate


@dataclass(eq=False)
class FirmwareUpdateData(BaseMessage):  # noqa: D101
    payload: payloads.FirmwareUpdateData
    payload_type: Type[payloads.FirmwareUpdateData] = payloads.FirmwareUpdateData
    message_id: Literal[MessageId.fw_update_data] = MessageId.fw_update_data


@dataclass(eq=False)
class FirmwareUpdateDataAcknowledge(Acknowledgement):  # noqa: D101
    payload: payloads.FirmwareUpdateDataAcknowledge
    payload_type: Type[
        payloads.FirmwareUpdateDataAcknowledge
    ] = payloads.FirmwareUpdateDataAcknowledge
    message_id: Literal[MessageId.fw_update_data_ack] = MessageId.fw_update_data_ack


@dataclass(eq=False)
class FirmwareUpdateComplete(Acknowledgement):  # noqa: D101
    payload: payloads.FirmwareUpdateComplete
    payload_type: Type[
        payloads.FirmwareUpdateComplete
    ] = payloads.FirmwareUpdateComplete
    message_id: Literal[MessageId.fw_update_complete] = MessageId.fw_update_complete


@dataclass(eq=False)
class FirmwareUpdateCompleteAcknowledge(Acknowledgement):  # noqa: D101
    payload: payloads.FirmwareUpdateAcknowledge
    payload_type: Type[
        payloads.FirmwareUpdateAcknowledge
    ] = payloads.FirmwareUpdateAcknowledge
    message_id: Literal[
        MessageId.fw_update_complete_ack
    ] = MessageId.fw_update_complete_ack


@dataclass(eq=False)
class FirmwareUpdateStatusRequest(BaseMessage):  # noqa: D101
    message_id: Literal[
        MessageId.fw_update_status_request
    ] = MessageId.fw_update_status_request


@dataclass(eq=False)
class FirmwareUpdateStatusResponse(Acknowledgement):  # noqa: D101
    payload: payloads.FirmwareUpdateStatus
    payload_type: Type[payloads.FirmwareUpdateStatus] = payloads.FirmwareUpdateStatus
    message_id: Literal[
        MessageId.fw_update_status_response
    ] = MessageId.fw_update_status_response


@dataclass(eq=False)
class FirmwareUpdateEraseAppRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.fw_update_erase_app] = MessageId.fw_update_erase_app


@dataclass(eq=False)
class FirmwareUpdateEraseAppResponse(Acknowledgement):  # noqa: D101
    payload: payloads.FirmwareUpdateAcknowledge
    payload_type: Type[
        payloads.FirmwareUpdateAcknowledge
    ] = payloads.FirmwareUpdateAcknowledge
    message_id: Literal[
        MessageId.fw_update_erase_app_ack
    ] = MessageId.fw_update_erase_app_ack


@dataclass(eq=False)
class HomeRequest(BaseMessage):  # noqa: D101
    payload: payloads.HomeRequestPayload
    payload_type: Type[payloads.HomeRequestPayload] = payloads.HomeRequestPayload
    message_id: Literal[MessageId.home_request] = MessageId.home_request


@dataclass(eq=False)
class FirmwareUpdateStartApp(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.fw_update_start_app] = MessageId.fw_update_start_app


@dataclass(eq=False)
class ReadLimitSwitchRequest(BaseMessage):  # noqa: D101
    message_id: Literal[MessageId.limit_sw_request] = MessageId.limit_sw_request


@dataclass(eq=False)
class ReadLimitSwitchResponse(Acknowledgement):  # noqa: D101
    payload: payloads.GetLimitSwitchResponse
    payload_type: Type[
        payloads.GetLimitSwitchResponse
    ] = payloads.GetLimitSwitchResponse
    message_id: Literal[MessageId.limit_sw_response] = MessageId.limit_sw_response


@dataclass(eq=False)
class ReadFromSensorRequest(BaseMessage):  # noqa: D101
    payload: payloads.ReadFromSensorRequestPayload
    payload_type: Type[
        payloads.ReadFromSensorRequestPayload
    ] = payloads.ReadFromSensorRequestPayload
    message_id: Literal[MessageId.read_sensor_request] = MessageId.read_sensor_request


@dataclass(eq=False)
class WriteToSensorRequest(BaseMessage):  # noqa: D101
    payload: payloads.WriteToSensorRequestPayload
    payload_type: Type[
        payloads.WriteToSensorRequestPayload
    ] = payloads.WriteToSensorRequestPayload
    message_id: Literal[MessageId.write_sensor_request] = MessageId.write_sensor_request


@dataclass(eq=False)
class BaselineSensorRequest(BaseMessage):  # noqa: D101
    payload: payloads.BaselineSensorRequestPayload
    payload_type: Type[
        payloads.BaselineSensorRequestPayload
    ] = payloads.BaselineSensorRequestPayload
    message_id: Literal[
        MessageId.baseline_sensor_request
    ] = MessageId.baseline_sensor_request


@dataclass(eq=False)
class ReadFromSensorResponse(Acknowledgement):  # noqa: D101
    payload: payloads.ReadFromSensorResponsePayload
    payload_type: Type[
        payloads.ReadFromSensorResponsePayload
    ] = payloads.ReadFromSensorResponsePayload
    message_id: Literal[MessageId.read_sensor_response] = MessageId.read_sensor_response


@dataclass(eq=False)
class SetSensorThresholdRequest(BaseMessage):  # noqa: D101
    payload: payloads.SetSensorThresholdRequestPayload
    payload_type: Type[
        payloads.SetSensorThresholdRequestPayload
    ] = payloads.SetSensorThresholdRequestPayload
    message_id: Literal[
        MessageId.set_sensor_threshold_request
    ] = MessageId.set_sensor_threshold_request


@dataclass(eq=False)
class SensorThresholdResponse(Acknowledgement):  # noqa: D101
    payload: payloads.SensorThresholdResponsePayload
    payload_type: Type[
        payloads.SensorThresholdResponsePayload
    ] = payloads.SensorThresholdResponsePayload
    message_id: Literal[
        MessageId.set_sensor_threshold_response
    ] = MessageId.set_sensor_threshold_response


@dataclass(eq=False)
class SensorDiagnosticRequest(BaseMessage):  # noqa: D101
    payload: payloads.SensorDiagnosticRequestPayload
    payload_type: Type[
        payloads.SensorDiagnosticRequestPayload
    ] = payloads.SensorDiagnosticRequestPayload
    message_id: Literal[
        MessageId.sensor_diagnostic_request
    ] = MessageId.sensor_diagnostic_request


@dataclass(eq=False)
class SensorDiagnosticResponse(Acknowledgement):  # noqa: D101
    payload: payloads.SensorDiagnosticResponsePayload
    payload_type: Type[
        payloads.SensorDiagnosticResponsePayload
    ] = payloads.SensorDiagnosticResponsePayload
    message_id: Literal[
        MessageId.sensor_diagnostic_response
    ] = MessageId.sensor_diagnostic_response


@dataclass(eq=False)
class PipetteInfoResponse(Acknowledgement):  # noqa: D101
    payload: payloads.PipetteInfoResponsePayload
    payload_type: Type[
        payloads.PipetteInfoResponsePayload
    ] = payloads.PipetteInfoResponsePayload
    message_id: Literal[
        MessageId.pipette_info_response
    ] = MessageId.pipette_info_response


@dataclass(eq=False)
class SetBrushedMotorVrefRequest(BaseMessage):  # noqa: D101
    payload: payloads.BrushedMotorVrefPayload
    payload_type: Type[
        payloads.BrushedMotorVrefPayload
    ] = payloads.BrushedMotorVrefPayload
    message_id: Literal[
        MessageId.set_brushed_motor_vref_request
    ] = MessageId.set_brushed_motor_vref_request


@dataclass(eq=False)
class SetBrushedMotorPwmRequest(BaseMessage):  # noqa: D101
    payload: payloads.BrushedMotorPwmPayload
    payload_type: Type[
        payloads.BrushedMotorPwmPayload
    ] = payloads.BrushedMotorPwmPayload
    message_id: Literal[
        MessageId.set_brushed_motor_pwm_request
    ] = MessageId.set_brushed_motor_pwm_request


@dataclass(eq=False)
class GripperGripRequest(BaseMessage):  # noqa: D101
    payload: payloads.GripperMoveRequestPayload
    payload_type: Type[
        payloads.GripperMoveRequestPayload
    ] = payloads.GripperMoveRequestPayload
    message_id: Literal[MessageId.gripper_grip_request] = MessageId.gripper_grip_request


@dataclass(eq=False)
class GripperHomeRequest(BaseMessage):  # noqa: D101
    payload: payloads.GripperMoveRequestPayload
    payload_type: Type[
        payloads.GripperMoveRequestPayload
    ] = payloads.GripperMoveRequestPayload
    message_id: Literal[MessageId.gripper_home_request] = MessageId.gripper_home_request


@dataclass(eq=False)
class AddBrushedLinearMoveRequest(BaseMessage):  # noqa: D101
    payload: payloads.GripperMoveRequestPayload
    payload_type: Type[
        payloads.GripperMoveRequestPayload
    ] = payloads.GripperMoveRequestPayload
    message_id: Literal[
        MessageId.add_brushed_linear_move_request
    ] = MessageId.add_brushed_linear_move_request


@dataclass(eq=False)
class BindSensorOutputRequest(BaseMessage):  # noqa: D101
    payload: payloads.BindSensorOutputRequestPayload
    payload_type: Type[
        payloads.BindSensorOutputRequestPayload
    ] = payloads.BindSensorOutputRequestPayload
    message_id: Literal[
        MessageId.bind_sensor_output_request
    ] = MessageId.bind_sensor_output_request


@dataclass(eq=False)
class BindSensorOutputResponse(Acknowledgement):  # noqa: D101
    payload: payloads.BindSensorOutputResponsePayload
    payload_type: Type[
        payloads.BindSensorOutputResponsePayload
    ] = payloads.BindSensorOutputResponsePayload
    message_id: Literal[
        MessageId.bind_sensor_output_response
    ] = MessageId.bind_sensor_output_response


@dataclass(eq=False)
class GripperInfoResponse(Acknowledgement):  # noqa: D101
    payload: payloads.GripperInfoResponsePayload
    payload_type: Type[
        payloads.GripperInfoResponsePayload
    ] = payloads.GripperInfoResponsePayload
    message_id: Literal[
        MessageId.gripper_info_response
    ] = MessageId.gripper_info_response


@dataclass(eq=False)
class TipActionRequest(BaseMessage):  # noqa: D101
    payload: payloads.TipActionRequestPayload
    payload_type: Type[
        payloads.TipActionRequestPayload
    ] = payloads.TipActionRequestPayload
    message_id: Literal[
        MessageId.do_self_contained_tip_action_request
    ] = MessageId.do_self_contained_tip_action_request


@dataclass(eq=False)
class TipActionResponse(Acknowledgement):  # noqa: D101
    payload: payloads.TipActionResponsePayload
    payload_type: Type[
        payloads.TipActionResponsePayload
    ] = payloads.TipActionResponsePayload
    message_id: Literal[
        MessageId.do_self_contained_tip_action_response
    ] = MessageId.do_self_contained_tip_action_response


@dataclass(eq=False)
class PeripheralStatusRequest(BaseMessage):  # noqa: D101
    payload: payloads.SensorPayload
    payload_type: Type[payloads.SensorPayload] = payloads.SensorPayload
    message_id: Literal[
        MessageId.peripheral_status_request
    ] = MessageId.peripheral_status_request


@dataclass(eq=False)
class PeripheralStatusResponse(Acknowledgement):  # noqa: D101
    payload: payloads.PeripheralStatusResponsePayload
    payload_type: Type[
        payloads.PeripheralStatusResponsePayload
    ] = payloads.PeripheralStatusResponsePayload
    message_id: Literal[
        MessageId.peripheral_status_response
    ] = MessageId.peripheral_status_response


@dataclass(eq=False)
class SetSerialNumber(BaseMessage):  # noqa: D101
    payload: payloads.SerialNumberPayload
    payload_type: Type[payloads.SerialNumberPayload] = payloads.SerialNumberPayload
    message_id: Literal[MessageId.set_serial_number] = MessageId.set_serial_number


@dataclass(eq=False)
class InstrumentInfoRequest(BaseMessage):
    """Prompt pipettes and grippers to respond.

    Pipette should respond with PipetteInfoResponse.
    Gripper should respond with GripperInfoResponse.
    """

    message_id: Literal[
        MessageId.instrument_info_request
    ] = MessageId.instrument_info_request
