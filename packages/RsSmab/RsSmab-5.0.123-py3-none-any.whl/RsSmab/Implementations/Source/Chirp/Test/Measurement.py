from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MeasurementCls:
	"""Measurement commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	def get_delay(self) -> bool:
		"""SCPI: [SOURce<HW>]:CHIRp:TEST:MEASurement:DELay \n
		Snippet: value: bool = driver.source.chirp.test.measurement.get_delay() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CHIRp:TEST:MEASurement:DELay?')
		return Conversions.str_to_bool(response)

	def set_delay(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CHIRp:TEST:MEASurement:DELay \n
		Snippet: driver.source.chirp.test.measurement.set_delay(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CHIRp:TEST:MEASurement:DELay {param}')
