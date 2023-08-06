from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AutoCls:
	"""Auto commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("auto", core, parent)

	def set(self, auto: enums.MeasRespTrigAutoSet, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:AUTO \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.auto.set(auto = enums.MeasRespTrigAutoSet.ONCE, channel = repcap.Channel.Default) \n
		Sets the trigger level, the hysteresis and the dropout time to default values. \n
			:param auto: ONCE
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.enum_scalar_to_str(auto, enums.MeasRespTrigAutoSet)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:AUTO {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTrigAutoSet:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:AUTO \n
		Snippet: value: enums.MeasRespTrigAutoSet = driver.sense.power.sweep.time.sensor.trigger.auto.get(channel = repcap.Channel.Default) \n
		Sets the trigger level, the hysteresis and the dropout time to default values. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: auto: ONCE"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:AUTO?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTrigAutoSet)
