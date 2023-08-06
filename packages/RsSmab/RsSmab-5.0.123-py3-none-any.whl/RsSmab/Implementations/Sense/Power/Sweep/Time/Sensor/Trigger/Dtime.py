from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtimeCls:
	"""Dtime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtime", core, parent)

	def set(self, dtime: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:DTIMe \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.dtime.set(dtime = 1.0, channel = repcap.Channel.Default) \n
		Determines the minimum time for which the signal must be below (above) the power level defined by level and hysteresis
		before triggering can occur again. \n
			:param dtime: float Range: 0 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(dtime)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:DTIMe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:DTIMe \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.trigger.dtime.get(channel = repcap.Channel.Default) \n
		Determines the minimum time for which the signal must be below (above) the power level defined by level and hysteresis
		before triggering can occur again. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: dtime: float Range: 0 to 10"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:DTIMe?')
		return Conversions.str_to_float(response)
