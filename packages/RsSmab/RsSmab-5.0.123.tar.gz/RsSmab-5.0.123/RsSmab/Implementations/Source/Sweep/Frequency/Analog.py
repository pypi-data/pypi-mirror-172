from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnalogCls:
	"""Analog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("analog", core, parent)

	def get_sw_points(self) -> List[float]:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:ANALog:SWPoints \n
		Snippet: value: List[float] = driver.source.sweep.frequency.analog.get_sw_points() \n
		Queries blank points during the RF frequency sweep in ramp sweep mode. At certain switchover frequency points, the R&S
		SMA100B shortly blanks the RF signal to adjust the settings accordingly. This query returns all blanked frequency points
		within the entire frequency range, regardless of the set frequency sweep range. \n
			:return: sweep_ramp_blank_points: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:SWEep:FREQuency:ANALog:SWPoints?')
		return response
