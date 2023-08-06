from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CodeCls:
	"""Code commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("code", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:VOR:COMid:CODE:STATe \n
		Snippet: value: bool = driver.source.vor.comid.code.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:CODE:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:CODE:STATe \n
		Snippet: driver.source.vor.comid.code.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:CODE:STATe {param}')

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:VOR:COMid:CODE \n
		Snippet: value: str = driver.source.vor.comid.code.get_value() \n
		Sets the coding of the COM/ID signal by the international short name of the airport (e.g. MUC for the Munich airport) .
		The COM/ID tone is sent according to the selected code, see 'Morse code settings'. If no coding is set, the COM/ID tone
		is sent uncoded (key down) . \n
			:return: code: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:CODE?')
		return trim_str_response(response)

	def set_value(self, code: str) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:CODE \n
		Snippet: driver.source.vor.comid.code.set_value(code = '1') \n
		Sets the coding of the COM/ID signal by the international short name of the airport (e.g. MUC for the Munich airport) .
		The COM/ID tone is sent according to the selected code, see 'Morse code settings'. If no coding is set, the COM/ID tone
		is sent uncoded (key down) . \n
			:param code: string
		"""
		param = Conversions.value_to_quoted_str(code)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:CODE {param}')
