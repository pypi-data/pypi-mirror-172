from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StepCls:
	"""Step commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("step", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqStepMode:
		"""SCPI: CSYNthesis:FREQuency:STEP:MODE \n
		Snippet: value: enums.FreqStepMode = driver.csynthesis.frequency.step.get_mode() \n
		Defines the type of step size to vary the frequency and level at discrete steps. \n
			:return: mode: DECimal| USER DECimal Increases or decreases the level in steps of 10. USER Increases or decreases the value in increments, set with the command: method RsSmab.Csynthesis.Frequency.Step.value method RsSmab.Csynthesis.Power.Step.increment
		"""
		response = self._core.io.query_str('CSYNthesis:FREQuency:STEP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqStepMode)

	def set_mode(self, mode: enums.FreqStepMode) -> None:
		"""SCPI: CSYNthesis:FREQuency:STEP:MODE \n
		Snippet: driver.csynthesis.frequency.step.set_mode(mode = enums.FreqStepMode.DECimal) \n
		Defines the type of step size to vary the frequency and level at discrete steps. \n
			:param mode: DECimal| USER DECimal Increases or decreases the level in steps of 10. USER Increases or decreases the value in increments, set with the command: method RsSmab.Csynthesis.Frequency.Step.value method RsSmab.Csynthesis.Power.Step.increment
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqStepMode)
		self._core.io.write(f'CSYNthesis:FREQuency:STEP:MODE {param}')

	def get_value(self) -> float:
		"""SCPI: CSYNthesis:FREQuency:STEP \n
		Snippet: value: float = driver.csynthesis.frequency.step.get_value() \n
		Sets the step width of the rotary knob and, in user-defined step mode, increases or decreases the frequency. \n
			:return: step: float Range: 0 to 14999E5
		"""
		response = self._core.io.query_str('CSYNthesis:FREQuency:STEP?')
		return Conversions.str_to_float(response)

	def set_value(self, step: float) -> None:
		"""SCPI: CSYNthesis:FREQuency:STEP \n
		Snippet: driver.csynthesis.frequency.step.set_value(step = 1.0) \n
		Sets the step width of the rotary knob and, in user-defined step mode, increases or decreases the frequency. \n
			:param step: float Range: 0 to 14999E5
		"""
		param = Conversions.decimal_value_to_str(step)
		self._core.io.write(f'CSYNthesis:FREQuency:STEP {param}')
