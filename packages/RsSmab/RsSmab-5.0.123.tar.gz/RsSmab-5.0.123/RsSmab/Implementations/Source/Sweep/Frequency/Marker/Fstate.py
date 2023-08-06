from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FstateCls:
	"""Fstate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fstate", core, parent)

	def set(self, fstate: bool, marker=repcap.Marker.Default) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FSTate \n
		Snippet: driver.source.sweep.frequency.marker.fstate.set(fstate = False, marker = repcap.Marker.Default) \n
		Activates the selected marker. \n
			:param fstate: 1| ON| 0| OFF
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
		"""
		param = Conversions.bool_to_str(fstate)
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{marker_cmd_val}:FSTate {param}')

	def get(self, marker=repcap.Marker.Default) -> bool:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer<CH>:FSTate \n
		Snippet: value: bool = driver.source.sweep.frequency.marker.fstate.get(marker = repcap.Marker.Default) \n
		Activates the selected marker. \n
			:param marker: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Marker')
			:return: fstate: 1| ON| 0| OFF"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		response = self._core.io.query_str(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer{marker_cmd_val}:FSTate?')
		return Conversions.str_to_bool(response)
