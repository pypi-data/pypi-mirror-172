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
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:PULSe:DISPlay:ANNotation:[STATe] \n
		Snippet: value: bool = driver.trace.power.sweep.measurement.pulse.display.annotation.get_state() \n
		Activates the indication of the pulse data below the measurement diagram and storing the data in the hardcopy file. The
		parameters to be indicated can be selected with the following TRAC:SWE:MEAS:…. commands. Only six parameters are
		indicated at one time. Note: This command is only avalaible in time measurement mode and with R&S NRPZ81 power sensors. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('TRACe:POWer:SWEep:MEASurement:PULSe:DISPlay:ANNotation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: TRACe:[POWer]:SWEep:MEASurement:PULSe:DISPlay:ANNotation:[STATe] \n
		Snippet: driver.trace.power.sweep.measurement.pulse.display.annotation.set_state(state = False) \n
		Activates the indication of the pulse data below the measurement diagram and storing the data in the hardcopy file. The
		parameters to be indicated can be selected with the following TRAC:SWE:MEAS:…. commands. Only six parameters are
		indicated at one time. Note: This command is only avalaible in time measurement mode and with R&S NRPZ81 power sensors. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TRACe:POWer:SWEep:MEASurement:PULSe:DISPlay:ANNotation:STATe {param}')
