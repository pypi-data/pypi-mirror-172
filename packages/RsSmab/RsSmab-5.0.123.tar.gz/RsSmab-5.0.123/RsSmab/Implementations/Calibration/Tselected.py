from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TselectedCls:
	"""Tselected commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tselected", core, parent)

	def get_catalog(self) -> str:
		"""SCPI: CALibration:TSELected:CATalog \n
		Snippet: value: str = driver.calibration.tselected.get_catalog() \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('CALibration:TSELected:CATalog?')
		return trim_str_response(response)

	def get_step(self) -> str:
		"""SCPI: CALibration:TSELected:STEP \n
		Snippet: value: str = driver.calibration.tselected.get_step() \n
		No command help available \n
			:return: sel_string: No help available
		"""
		response = self._core.io.query_str('CALibration:TSELected:STEP?')
		return trim_str_response(response)

	def set_step(self, sel_string: str) -> None:
		"""SCPI: CALibration:TSELected:STEP \n
		Snippet: driver.calibration.tselected.set_step(sel_string = '1') \n
		No command help available \n
			:param sel_string: No help available
		"""
		param = Conversions.value_to_quoted_str(sel_string)
		self._core.io.write(f'CALibration:TSELected:STEP {param}')

	def get_measure(self) -> bool:
		"""SCPI: CALibration:TSELected:[MEASure] \n
		Snippet: value: bool = driver.calibration.tselected.get_measure() \n
		No command help available \n
			:return: meas: No help available
		"""
		response = self._core.io.query_str('CALibration:TSELected:MEASure?')
		return Conversions.str_to_bool(response)
