from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:[STATe] \n
		Snippet: driver.sense.power.sweep.frequency.sensor.srange.state.set(state = False, channel = repcap.Channel.Default) \n
		Activates the use of a frequency range for the power measurement that is different to the set signal generator frequency
		range. The separate frequency range is entered with commands method RsSmab.Sense.Power.Sweep.Frequency.Sensor.Srange.
		Start.set and method RsSmab.Sense.Power.Sweep.Frequency.Sensor.Srange.Stop.set. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STATe {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:FREQuency:[SENSor]:SRANge:[STATe] \n
		Snippet: value: bool = driver.sense.power.sweep.frequency.sensor.srange.state.get(channel = repcap.Channel.Default) \n
		Activates the use of a frequency range for the power measurement that is different to the set signal generator frequency
		range. The separate frequency range is entered with commands method RsSmab.Sense.Power.Sweep.Frequency.Sensor.Srange.
		Start.set and method RsSmab.Sense.Power.Sweep.Frequency.Sensor.Srange.Stop.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:FREQuency:SENSor:SRANge:STATe?')
		return Conversions.str_to_bool(response)
