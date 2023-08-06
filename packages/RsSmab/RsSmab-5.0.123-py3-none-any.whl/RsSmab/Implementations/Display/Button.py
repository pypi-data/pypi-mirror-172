from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ButtonCls:
	"""Button commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("button", core, parent)

	def get_brightness(self) -> int:
		"""SCPI: DISPlay:BUTTon:BRIGhtness \n
		Snippet: value: int = driver.display.button.get_brightness() \n
		Sets the brightness of the [RF on/off] key. \n
			:return: button_brightnes: integer Range: 1 to 20
		"""
		response = self._core.io.query_str('DISPlay:BUTTon:BRIGhtness?')
		return Conversions.str_to_int(response)

	def set_brightness(self, button_brightnes: int) -> None:
		"""SCPI: DISPlay:BUTTon:BRIGhtness \n
		Snippet: driver.display.button.set_brightness(button_brightnes = 1) \n
		Sets the brightness of the [RF on/off] key. \n
			:param button_brightnes: integer Range: 1 to 20
		"""
		param = Conversions.decimal_value_to_str(button_brightnes)
		self._core.io.write(f'DISPlay:BUTTon:BRIGhtness {param}')
