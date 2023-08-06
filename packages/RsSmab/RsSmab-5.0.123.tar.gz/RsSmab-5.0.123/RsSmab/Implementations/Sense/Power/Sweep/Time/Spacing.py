from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpacingCls:
	"""Spacing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spacing", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MeasRespSpacingMode:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:SPACing:[MODE] \n
		Snippet: value: enums.MeasRespSpacingMode = driver.sense.power.sweep.time.spacing.get_mode() \n
		Queries the sweep spacing for the power versus time measurement. The spacing is fixed to linear. \n
			:return: mode: LINear
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:TIME:SPACing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespSpacingMode)

	def set_mode(self, mode: enums.MeasRespSpacingMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:TIME:SPACing:[MODE] \n
		Snippet: driver.sense.power.sweep.time.spacing.set_mode(mode = enums.MeasRespSpacingMode.LINear) \n
		Queries the sweep spacing for the power versus time measurement. The spacing is fixed to linear. \n
			:param mode: LINear
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MeasRespSpacingMode)
		self._core.io.write(f'SENSe:POWer:SWEep:TIME:SPACing:MODE {param}')
