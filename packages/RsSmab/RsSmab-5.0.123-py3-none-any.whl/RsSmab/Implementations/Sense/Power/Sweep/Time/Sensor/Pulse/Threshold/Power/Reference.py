from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def set(self, reference: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:REFerence \n
		Snippet: driver.sense.power.sweep.time.sensor.pulse.threshold.power.reference.set(reference = 1.0, channel = repcap.Channel.Default) \n
		Sets the medial reference level in terms of percentage of the overall pulse level (power or voltage related) . This level
		is used to define pulse width and pulse period. Note: The command is only available in time measurement mode and with R&S
		NRPZ81 power sensors. \n
			:param reference: float Range: 0.0 to 100.0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(reference)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:REFerence {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:REFerence \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.pulse.threshold.power.reference.get(channel = repcap.Channel.Default) \n
		Sets the medial reference level in terms of percentage of the overall pulse level (power or voltage related) . This level
		is used to define pulse width and pulse period. Note: The command is only available in time measurement mode and with R&S
		NRPZ81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: reference: float Range: 0.0 to 100.0"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:REFerence?')
		return Conversions.str_to_float(response)
