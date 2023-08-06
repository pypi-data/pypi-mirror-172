from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, frequency: float, marker=repcap.Marker.Default) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FREQuency \n
		Snippet: driver.source.sweep.frequency.marker.frequency.set(frequency = 1.0, marker = repcap.Marker.Default) \n
		Sets the frequency of the selected marker. \n
			:param frequency: float
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
		"""
		param = Conversions.decimal_value_to_str(frequency)
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{marker_cmd_val}:FREQuency {param}')

	def get(self, marker=repcap.Marker.Default) -> float:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FREQuency \n
		Snippet: value: float = driver.source.sweep.frequency.marker.frequency.get(marker = repcap.Marker.Default) \n
		Sets the frequency of the selected marker. \n
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
			:return: frequency: float"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		response = self._core.io.query_str(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{marker_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
