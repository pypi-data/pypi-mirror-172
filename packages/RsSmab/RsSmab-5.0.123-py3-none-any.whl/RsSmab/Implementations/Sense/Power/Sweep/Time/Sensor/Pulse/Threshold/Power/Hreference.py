from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HreferenceCls:
	"""Hreference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hreference", core, parent)

	def set(self, hreference: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:HREFerence \n
		Snippet: driver.sense.power.sweep.time.sensor.pulse.threshold.power.hreference.set(hreference = 1.0, channel = repcap.Channel.Default) \n
		Sets the upper reference level in terms of percentage of the overall pulse level (power or voltage) . The distal power
		defines the end of the rising edge and the start of the falling edge of the pulse. Note: The command is only available in
		time measurement mode and with R&S NRPZ81 power sensors. \n
			:param hreference: float Range: 0 to 100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(hreference)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:HREFerence {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:HREFerence \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.pulse.threshold.power.hreference.get(channel = repcap.Channel.Default) \n
		Sets the upper reference level in terms of percentage of the overall pulse level (power or voltage) . The distal power
		defines the end of the rising edge and the start of the falling edge of the pulse. Note: The command is only available in
		time measurement mode and with R&S NRPZ81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: hreference: float Range: 0 to 100"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:HREFerence?')
		return Conversions.str_to_float(response)
