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
		"""SCPI: CSYNthesis:POWer:STEP:MODE \n
		Snippet: value: enums.FreqStepMode = driver.csynthesis.power.step.get_mode() \n
		Defines the type of step size to vary the frequency and level at discrete steps. \n
			:return: mode: DECimal| USER DECimal Increases or decreases the level in steps of 10. USER Increases or decreases the value in increments, set with the command: method RsSmab.Csynthesis.Frequency.Step.value method RsSmab.Csynthesis.Power.Step.increment
		"""
		response = self._core.io.query_str('CSYNthesis:POWer:STEP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqStepMode)

	def set_mode(self, mode: enums.FreqStepMode) -> None:
		"""SCPI: CSYNthesis:POWer:STEP:MODE \n
		Snippet: driver.csynthesis.power.step.set_mode(mode = enums.FreqStepMode.DECimal) \n
		Defines the type of step size to vary the frequency and level at discrete steps. \n
			:param mode: DECimal| USER DECimal Increases or decreases the level in steps of 10. USER Increases or decreases the value in increments, set with the command: method RsSmab.Csynthesis.Frequency.Step.value method RsSmab.Csynthesis.Power.Step.increment
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqStepMode)
		self._core.io.write(f'CSYNthesis:POWer:STEP:MODE {param}')

	def get_increment(self) -> float:
		"""SCPI: CSYNthesis:POWer:STEP:[INCRement] \n
		Snippet: value: float = driver.csynthesis.power.step.get_increment() \n
		Sets the step width of the rotary knob and, in user-defined step mode, increases or decreases the level. \n
			:return: increment: float Range: 0 to 35
		"""
		response = self._core.io.query_str('CSYNthesis:POWer:STEP:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""SCPI: CSYNthesis:POWer:STEP:[INCRement] \n
		Snippet: driver.csynthesis.power.step.set_increment(increment = 1.0) \n
		Sets the step width of the rotary knob and, in user-defined step mode, increases or decreases the level. \n
			:param increment: float Range: 0 to 35
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'CSYNthesis:POWer:STEP:INCRement {param}')
