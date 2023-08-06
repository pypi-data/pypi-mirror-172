from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfLevelCls:
	"""RfLevel commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfLevel", core, parent)

	def get_expected(self) -> float:
		"""SCPI: CALibration:DETector:RFLevel:EXPected \n
		Snippet: value: float = driver.calibration.detector.rfLevel.get_expected() \n
		No command help available \n
			:return: level_value_exp: No help available
		"""
		response = self._core.io.query_str('CALibration:DETector:RFLevel:EXPected?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""SCPI: CALibration:DETector:RFLevel \n
		Snippet: value: float = driver.calibration.detector.rfLevel.get_value() \n
		No command help available \n
			:return: level_value: No help available
		"""
		response = self._core.io.query_str('CALibration:DETector:RFLevel?')
		return Conversions.str_to_float(response)
