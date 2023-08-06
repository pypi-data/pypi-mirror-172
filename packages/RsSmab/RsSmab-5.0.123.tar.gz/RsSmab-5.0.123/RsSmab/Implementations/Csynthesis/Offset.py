from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CSYNthesis:OFFSet:STATe \n
		Snippet: value: bool = driver.csynthesis.offset.get_state() \n
		Activates a DC offset. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('CSYNthesis:OFFSet:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: CSYNthesis:OFFSet:STATe \n
		Snippet: driver.csynthesis.offset.set_state(state = False) \n
		Activates a DC offset. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CSYNthesis:OFFSet:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: CSYNthesis:OFFSet \n
		Snippet: value: float = driver.csynthesis.offset.get_value() \n
		Sets the value of the DC offset. \n
			:return: offset: float Range: -5 to 5
		"""
		response = self._core.io.query_str('CSYNthesis:OFFSet?')
		return Conversions.str_to_float(response)

	def set_value(self, offset: float) -> None:
		"""SCPI: CSYNthesis:OFFSet \n
		Snippet: driver.csynthesis.offset.set_value(offset = 1.0) \n
		Sets the value of the DC offset. \n
			:param offset: float Range: -5 to 5
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'CSYNthesis:OFFSet {param}')
