from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GridCls:
	"""Grid commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("grid", core, parent)

	def get_state(self) -> bool:
		"""SCPI: DISPlay:[WINDow]:[POWer]:SWEep:GRID:STATe \n
		Snippet: value: bool = driver.display.window.power.sweep.grid.get_state() \n
		Indicates a grid in the diagram. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('DISPlay:WINDow:POWer:SWEep:GRID:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: DISPlay:[WINDow]:[POWer]:SWEep:GRID:STATe \n
		Snippet: driver.display.window.power.sweep.grid.set_state(state = False) \n
		Indicates a grid in the diagram. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'DISPlay:WINDow:POWer:SWEep:GRID:STATe {param}')
