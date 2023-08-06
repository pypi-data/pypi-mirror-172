from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BackgroundCls:
	"""Background commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("background", core, parent)

	# noinspection PyTypeChecker
	def get_color(self) -> enums.DiagBgColor:
		"""SCPI: DISPlay:[WINDow]:[POWer]:SWEep:BACKground:COLor \n
		Snippet: value: enums.DiagBgColor = driver.display.window.power.sweep.background.get_color() \n
		Defines the background color of the measurement diagram. The selected color applies also to the hardcopy of the diagram. \n
			:return: color: BLACk| WHITe
		"""
		response = self._core.io.query_str('DISPlay:WINDow:POWer:SWEep:BACKground:COLor?')
		return Conversions.str_to_scalar_enum(response, enums.DiagBgColor)

	def set_color(self, color: enums.DiagBgColor) -> None:
		"""SCPI: DISPlay:[WINDow]:[POWer]:SWEep:BACKground:COLor \n
		Snippet: driver.display.window.power.sweep.background.set_color(color = enums.DiagBgColor.BLACk) \n
		Defines the background color of the measurement diagram. The selected color applies also to the hardcopy of the diagram. \n
			:param color: BLACk| WHITe
		"""
		param = Conversions.enum_scalar_to_str(color, enums.DiagBgColor)
		self._core.io.write(f'DISPlay:WINDow:POWer:SWEep:BACKground:COLor {param}')
