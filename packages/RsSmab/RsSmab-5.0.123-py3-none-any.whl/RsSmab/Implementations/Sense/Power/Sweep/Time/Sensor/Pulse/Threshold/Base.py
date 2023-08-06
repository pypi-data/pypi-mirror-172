from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BaseCls:
	"""Base commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("base", core, parent)

	def set(self, base: enums.MeasRespPulsThrBase, channel=repcap.Channel.Default) -> None:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:BASE \n
		Snippet: driver.sense.power.sweep.time.sensor.pulse.threshold.base.set(base = enums.MeasRespPulsThrBase.POWer, channel = repcap.Channel.Default) \n
		Selects how the threshold parameters for pulse analysis are calculated. Note: The command is only available in time
		measurement mode and with R&S NRPZ81 power sensors. \n
			:param base: VOLTage| POWer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
		"""
		param = Conversions.enum_scalar_to_str(base, enums.MeasRespPulsThrBase)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:BASE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.MeasRespPulsThrBase:
		"""SCPI: SENSe<CH>:[POWer]:SWEep:TIME:[SENSor]:PULSe:THReshold:BASE \n
		Snippet: value: enums.MeasRespPulsThrBase = driver.sense.power.sweep.time.sensor.pulse.threshold.base.get(channel = repcap.Channel.Default) \n
		Selects how the threshold parameters for pulse analysis are calculated. Note: The command is only available in time
		measurement mode and with R&S NRPZ81 power sensors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: base: VOLTage| POWer"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:SWEep:TIME:SENSor:PULSe:THReshold:BASE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespPulsThrBase)
