from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlopeCls:
	"""Slope commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slope", core, parent)

	def set(self, trigger_slope: enums.SlopeType, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:SLOPe \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.slope.set(trigger_slope = enums.SlopeType.NEGative, channel = repcap.Channel.Default) \n
		Sets the polarity of the active slope for the trigger signals. \n
			:param trigger_slope: POSitive| NEGative
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.enum_scalar_to_str(trigger_slope, enums.SlopeType)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:SLOPe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.SlopeType:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:SLOPe \n
		Snippet: value: enums.SlopeType = driver.sense.power.sweep.time.sensor.trigger.slope.get(channel = repcap.Channel.Default) \n
		Sets the polarity of the active slope for the trigger signals. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: trigger_slope: POSitive| NEGative"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)
