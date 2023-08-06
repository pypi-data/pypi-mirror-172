from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPyCls:
	"""FilterPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PowHarmMode:
		"""SCPI: OUTPut<HW>:FILTer:MODE \n
		Snippet: value: enums.PowHarmMode = driver.output.filterPy.get_mode() \n
		Activates low harmonic filter or enables its automatic switching. \n
			:return: mode: ON| AUTO| 1 ON|1 Ensures best low harmonics performance but decreases the level range AUTO Applies an automatically selected harmonic filter that fits to the current level setting.
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:FILTer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PowHarmMode)

	def set_mode(self, mode: enums.PowHarmMode) -> None:
		"""SCPI: OUTPut<HW>:FILTer:MODE \n
		Snippet: driver.output.filterPy.set_mode(mode = enums.PowHarmMode._1) \n
		Activates low harmonic filter or enables its automatic switching. \n
			:param mode: ON| AUTO| 1 ON|1 Ensures best low harmonics performance but decreases the level range AUTO Applies an automatically selected harmonic filter that fits to the current level setting.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PowHarmMode)
		self._core.io.write(f'OUTPut<HwInstance>:FILTer:MODE {param}')
