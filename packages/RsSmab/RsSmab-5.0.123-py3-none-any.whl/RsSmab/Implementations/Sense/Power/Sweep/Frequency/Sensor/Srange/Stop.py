from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StopCls:
	"""Stop commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stop", core, parent)

	def set(self, stop: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:STOP \n
		Snippet: driver.sense.power.sweep.frequency.sensor.srange.stop.set(stop = 1, channel = repcap.Channel.Default) \n
		Sets the stop frequency for the frequency power analysis with separate frequencies. \n
			:param stop: integer Range: 0 to 1E12
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(stop)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STOP {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:STOP \n
		Snippet: value: int = driver.sense.power.sweep.frequency.sensor.srange.stop.get(channel = repcap.Channel.Default) \n
		Sets the stop frequency for the frequency power analysis with separate frequencies. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: stop: integer Range: 0 to 1E12"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STOP?')
		return Conversions.str_to_int(response)
