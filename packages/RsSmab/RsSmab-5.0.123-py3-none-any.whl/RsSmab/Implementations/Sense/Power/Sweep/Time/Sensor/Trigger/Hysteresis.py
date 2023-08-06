from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HysteresisCls:
	"""Hysteresis commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hysteresis", core, parent)

	def set(self, hysteresis: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:HYSTeresis \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.hysteresis.set(hysteresis = 1.0, channel = repcap.Channel.Default) \n
		Sets the hysteresis of the internal trigger threshold. Hysteresis is the magnitude (in dB) the trigger signal level must
		drop below the trigger threshold (positive trigger slope) before triggering can occur again. \n
			:param hysteresis: float Range: 0 to 10
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(hysteresis)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:HYSTeresis {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:HYSTeresis \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.trigger.hysteresis.get(channel = repcap.Channel.Default) \n
		Sets the hysteresis of the internal trigger threshold. Hysteresis is the magnitude (in dB) the trigger signal level must
		drop below the trigger threshold (positive trigger slope) before triggering can occur again. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: hysteresis: float Range: 0 to 10"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:HYSTeresis?')
		return Conversions.str_to_float(response)
