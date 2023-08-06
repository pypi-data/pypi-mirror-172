from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartCls:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def set(self, start: int, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:STARt \n
		Snippet: driver.sense.power.sweep.frequency.sensor.srange.start.set(start = 1, channel = repcap.Channel.Default) \n
		Sets the start frequency for the frequency power analysis with separate frequencies. \n
			:param start: integer Range: 0 to 1E12
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(start)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STARt {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:STARt \n
		Snippet: value: int = driver.sense.power.sweep.frequency.sensor.srange.start.get(channel = repcap.Channel.Default) \n
		Sets the start frequency for the frequency power analysis with separate frequencies. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: start: integer Range: 0 to 1E12"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STARt?')
		return Conversions.str_to_int(response)
