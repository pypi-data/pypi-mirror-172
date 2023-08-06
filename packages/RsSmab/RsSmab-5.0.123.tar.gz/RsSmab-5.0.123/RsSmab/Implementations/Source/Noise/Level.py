from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def get_relative(self) -> float:
		"""SCPI: [SOURce<HW>]:NOISe:LEVel:RELative \n
		Snippet: value: float = driver.source.noise.level.get_relative() \n
		Queries the level of the noise signal per Hz in the total bandwidth. \n
			:return: relative: float Range: -149.18 to -52.67
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:NOISe:LEVel:RELative?')
		return Conversions.str_to_float(response)

	def get_absolute(self) -> float:
		"""SCPI: [SOURce<HW>]:NOISe:LEVel:[ABSolute] \n
		Snippet: value: float = driver.source.noise.level.get_absolute() \n
		Queries the level of the noise signal in the system bandwidth within the enabled bandwidth limitation. \n
			:return: absolute: float Noise level within the bandwidth limitation
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:NOISe:LEVel:ABSolute?')
		return Conversions.str_to_float(response)
