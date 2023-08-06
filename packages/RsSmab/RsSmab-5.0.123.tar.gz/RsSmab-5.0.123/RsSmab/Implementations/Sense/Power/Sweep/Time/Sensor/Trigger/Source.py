from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.MeasRespTrigMode, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:SOURce \n
		Snippet: driver.sense.power.sweep.time.sensor.trigger.source.set(source = enums.MeasRespTrigMode.AUTO, channel = repcap.Channel.Default) \n
		Selects if the measurement is free running (FREE) or starts only after a trigger event. The trigger can be applied
		internally or externally. \n
			:param source: FREE| AUTO| INTernal| EXTernal
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.MeasRespTrigMode)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespTrigMode:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:TRIGger:SOURce \n
		Snippet: value: enums.MeasRespTrigMode = driver.sense.power.sweep.time.sensor.trigger.source.get(channel = repcap.Channel.Default) \n
		Selects if the measurement is free running (FREE) or starts only after a trigger event. The trigger can be applied
		internally or externally. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: source: FREE| AUTO| INTernal| EXTernal"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:TRIGger:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespTrigMode)
