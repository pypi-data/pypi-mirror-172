from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:LEVel \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.level.set(level = 1.0, channel = repcap.Channel.Default) \n
		Sets the trigger threshold. \n
			:param level: float Range: -200 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(level)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:LEVel {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:LEVel \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.trigger.level.get(channel = repcap.Channel.Default) \n
		Sets the trigger threshold. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: level: float Range: -200 to 100"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:LEVel?')
		return Conversions.str_to_float(response)
