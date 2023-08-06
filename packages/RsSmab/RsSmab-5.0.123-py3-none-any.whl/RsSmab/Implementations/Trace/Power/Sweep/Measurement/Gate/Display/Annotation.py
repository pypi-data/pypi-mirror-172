from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnnotationCls:
	"""Annotation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("annotation", core, parent)

	def get_state(self) -> bool:
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:GATE:DISPlay:ANNotation:[STATe] \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.gate.display.annotation.get_state() \n
		Activates th eindication of the time gate borders and values in the measurement diagram and in the hardcopy file.
		The gate settings are performed with the CALC:POW:SWE:TIME:GATE:… commands. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('TRACe:POWer:SWEep:MEASurement:GATE:DISPlay:ANNotation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:GATE:DISPlay:ANNotation:[STATe] \n
		Snippet: driver.trace.power.sweep.measurement.gate.display.annotation.set_state(state = False) \n
		Activates th eindication of the time gate borders and values in the measurement diagram and in the hardcopy file.
		The gate settings are performed with the CALC:POW:SWE:TIME:GATE:… commands. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TRACe:POWer:SWEep:MEASurement:GATE:DISPlay:ANNotation:STATe {param}')
