from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsynthesisCls:
	"""Csynthesis commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csynthesis", core, parent)

	def get_measure(self) -> bool:
		"""SCPI: CALibration:CSYNthesis:[MEASure] \n
		Snippet: value: bool = driver.calibration.csynthesis.get_measure() \n
		No command help available \n
			:return: measure: No help available
		"""
		response = self._core.io.query_str('CALibration:CSYNthesis:MEASure?')
		return Conversions.str_to_bool(response)
