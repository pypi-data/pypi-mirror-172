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
		"""SCPI: SENSe:[POWer]:SWEep:POWer:SPACing:[MODE] \n
		Snippet: value: enums.MeasRespSpacingMode = driver.sense.power.sweep.power.spacing.get_mode() \n
		Selects the spacing for the frequency power analysis. \n
			:return: mode: LINear
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:POWer:SPACing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasRespSpacingMode)

	def set_mode(self, mode: enums.MeasRespSpacingMode) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:POWer:SPACing:[MODE] \n
		Snippet: driver.sense.power.sweep.power.spacing.set_mode(mode = enums.MeasRespSpacingMode.LINear) \n
		Selects the spacing for the frequency power analysis. \n
			:param mode: LINear
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MeasRespSpacingMode)
		self._core.io.write(f'SENSe:POWer:SWEep:POWer:SPACing:MODE {param}')
