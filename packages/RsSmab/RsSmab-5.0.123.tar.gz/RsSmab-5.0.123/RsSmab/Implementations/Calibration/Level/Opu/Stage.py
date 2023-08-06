from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StageCls:
	"""Stage commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stage", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.StagMode:
		"""SCPI: CALibration:LEVel:OPU:STAGe:MODE \n
		Snippet: value: enums.StagMode = driver.calibration.level.opu.stage.get_mode() \n
		No command help available \n
			:return: stage_mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:OPU:STAGe:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.StagMode)

	def set_mode(self, stage_mode: enums.StagMode) -> None:
		"""SCPI: CALibration:LEVel:OPU:STAGe:MODE \n
		Snippet: driver.calibration.level.opu.stage.set_mode(stage_mode = enums.StagMode.AUTO) \n
		No command help available \n
			:param stage_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(stage_mode, enums.StagMode)
		self._core.io.write(f'CALibration:LEVel:OPU:STAGe:MODE {param}')

	def get_sub(self) -> int:
		"""SCPI: CALibration:LEVel:OPU:STAGe:SUB \n
		Snippet: value: int = driver.calibration.level.opu.stage.get_sub() \n
		No command help available \n
			:return: stage_sub: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:OPU:STAGe:SUB?')
		return Conversions.str_to_int(response)

	def set_sub(self, stage_sub: int) -> None:
		"""SCPI: CALibration:LEVel:OPU:STAGe:SUB \n
		Snippet: driver.calibration.level.opu.stage.set_sub(stage_sub = 1) \n
		No command help available \n
			:param stage_sub: No help available
		"""
		param = Conversions.decimal_value_to_str(stage_sub)
		self._core.io.write(f'CALibration:LEVel:OPU:STAGe:SUB {param}')

	def get_value(self) -> int:
		"""SCPI: CALibration:LEVel:OPU:STAGe \n
		Snippet: value: int = driver.calibration.level.opu.stage.get_value() \n
		No command help available \n
			:return: stage: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:OPU:STAGe?')
		return Conversions.str_to_int(response)

	def set_value(self, stage: int) -> None:
		"""SCPI: CALibration:LEVel:OPU:STAGe \n
		Snippet: driver.calibration.level.opu.stage.set_value(stage = 1) \n
		No command help available \n
			:param stage: No help available
		"""
		param = Conversions.decimal_value_to_str(stage)
		self._core.io.write(f'CALibration:LEVel:OPU:STAGe {param}')
