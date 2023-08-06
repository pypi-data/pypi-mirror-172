from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LreferenceCls:
	"""Lreference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lreference", core, parent)

	def set(self, lreference: float, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:LREFerence \n
		Snippet: driver.sense.power.sweep.time.sensor.pulse.threshold.power.lreference.set(lreference = 1.0, channel = repcap.Channel.Default) \n
		Sets the lower reference level in terms of percentage of the overall pulse level. The proximal power defines the start of
		the rising edge and the end of the falling edge of the pulse. Note: This parameter is only available in time measurement
		mode and R&S NRP-Z81 power sensors. \n
			:param lreference: float Range: 0.0 to 100.0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.decimal_value_to_str(lreference)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:LREFerence {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:POWer:LREFerence \n
		Snippet: value: float = driver.sense.power.sweep.time.sensor.pulse.threshold.power.lreference.get(channel = repcap.Channel.Default) \n
		Sets the lower reference level in terms of percentage of the overall pulse level. The proximal power defines the start of
		the rising edge and the end of the falling edge of the pulse. Note: This parameter is only available in time measurement
		mode and R&S NRP-Z81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: lreference: float Range: 0.0 to 100.0"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:POWer:LREFerence?')
		return Conversions.str_to_float(response)
