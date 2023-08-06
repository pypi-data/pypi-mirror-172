from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MeasureCls:
	"""Measure commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measure", core, parent)

	# noinspection PyTypeChecker
	def get(self, to_test_args: str) -> enums.TestCalSelected:
		"""SCPI: CALibration:SELected:[MEASure] \n
		Snippet: value: enums.TestCalSelected = driver.calibration.selected.measure.get(to_test_args = '1') \n
		No command help available \n
			:param to_test_args: No help available
			:return: test_result: No help available"""
		param = Conversions.value_to_quoted_str(to_test_args)
		response = self._core.io.query_str(f'CALibration:SELected:MEASure? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TestCalSelected)
