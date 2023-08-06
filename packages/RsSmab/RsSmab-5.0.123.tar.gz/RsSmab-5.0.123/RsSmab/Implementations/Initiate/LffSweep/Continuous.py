from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ContinuousCls:
	"""Continuous commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("continuous", core, parent)

	def set(self, sw_lf_init_state: bool, channel=repcap.Channel.Default) -> None:
		"""SCPI: INITiate<HW>:LFFSweep:CONTinuous \n
		Snippet: driver.initiate.lffSweep.continuous.set(sw_lf_init_state = False, channel = repcap.Channel.Default) \n
		No command help available \n
			:param sw_lf_init_state: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Initiate')
		"""
		param = Conversions.bool_to_str(sw_lf_init_state)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'INITiate{channel_cmd_val}:LFFSweep:CONTinuous {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SCPI: INITiate<HW>:LFFSweep:CONTinuous \n
		Snippet: value: bool = driver.initiate.lffSweep.continuous.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Initiate')
			:return: sw_lf_init_state: No help available"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'INITiate{channel_cmd_val}:LFFSweep:CONTinuous?')
		return Conversions.str_to_bool(response)
