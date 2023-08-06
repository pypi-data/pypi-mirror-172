from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComidCls:
	"""Comid commands group definition. 10 total commands, 0 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comid", core, parent)

	def get_code(self) -> str:
		"""SCPI: [SOURce<HW>]:ADF:COMid:CODE \n
		Snippet: value: str = driver.source.adf.comid.get_code() \n
		Sets the coding of the COM/ID signal by the international short name of the airport (e.g. MUC for the Munich airport) .
		The COM/ID tone is sent according to the selected code, see 'Morse code settings'. If no coding is set, the COM/ID tone
		is sent uncoded (key down) . \n
			:return: code: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:CODE?')
		return trim_str_response(response)

	def set_code(self, code: str) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:CODE \n
		Snippet: driver.source.adf.comid.set_code(code = '1') \n
		Sets the coding of the COM/ID signal by the international short name of the airport (e.g. MUC for the Munich airport) .
		The COM/ID tone is sent according to the selected code, see 'Morse code settings'. If no coding is set, the COM/ID tone
		is sent uncoded (key down) . \n
			:param code: string
		"""
		param = Conversions.value_to_quoted_str(code)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:CODE {param}')

	def get_dash(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DASH \n
		Snippet: value: float = driver.source.adf.comid.get_dash() \n
		Sets the length of a Morse code dash. \n
			:return: dash: float Range: 50E-3 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:DASH?')
		return Conversions.str_to_float(response)

	def set_dash(self, dash: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DASH \n
		Snippet: driver.source.adf.comid.set_dash(dash = 1.0) \n
		Sets the length of a Morse code dash. \n
			:param dash: float Range: 50E-3 to 1
		"""
		param = Conversions.decimal_value_to_str(dash)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:DASH {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DEPTh \n
		Snippet: value: float = driver.source.adf.comid.get_depth() \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DEPTh \n
		Snippet: driver.source.adf.comid.set_depth(depth = 1.0) \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:DEPTh {param}')

	def get_dot(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DOT \n
		Snippet: value: float = driver.source.adf.comid.get_dot() \n
		Sets the length of a Morse code dot. \n
			:return: dot: float Range: 50E-3 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dot: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:DOT \n
		Snippet: driver.source.adf.comid.set_dot(dot = 1.0) \n
		Sets the length of a Morse code dot. \n
			:param dot: float Range: 50E-3 to 1
		"""
		param = Conversions.decimal_value_to_str(dot)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:DOT {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:FREQuency \n
		Snippet: value: float = driver.source.adf.comid.get_frequency() \n
		Sets the frequency of the COM/ID signal. \n
			:return: frequency: float Range: 0.1 to 20E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:FREQuency \n
		Snippet: driver.source.adf.comid.set_frequency(frequency = 1.0) \n
		Sets the frequency of the COM/ID signal. \n
			:param frequency: float Range: 0.1 to 20E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:FREQuency {param}')

	def get_letter(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:LETTer \n
		Snippet: value: float = driver.source.adf.comid.get_letter() \n
		Sets the length of a Morse code letter space. \n
			:return: letter: float Range: 50E-3 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:LETTer?')
		return Conversions.str_to_float(response)

	def set_letter(self, letter: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:LETTer \n
		Snippet: driver.source.adf.comid.set_letter(letter = 1.0) \n
		Sets the length of a Morse code letter space. \n
			:param letter: float Range: 50E-3 to 1
		"""
		param = Conversions.decimal_value_to_str(letter)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:LETTer {param}')

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:PERiod \n
		Snippet: value: float = driver.source.adf.comid.get_period() \n
		Sets the period of the COM/ID signal. \n
			:return: period: float Range: 0 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:PERiod \n
		Snippet: driver.source.adf.comid.set_period(period = 1.0) \n
		Sets the period of the COM/ID signal. \n
			:param period: float Range: 0 to 120
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:PERiod {param}')

	def get_symbol(self) -> float:
		"""SCPI: [SOURce<HW>]:ADF:COMid:SYMBol \n
		Snippet: value: float = driver.source.adf.comid.get_symbol() \n
		Sets the length of the Morse code symbol space. \n
			:return: symbol: float Range: 50E-3 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:SYMBol?')
		return Conversions.str_to_float(response)

	def set_symbol(self, symbol: float) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:SYMBol \n
		Snippet: driver.source.adf.comid.set_symbol(symbol = 1.0) \n
		Sets the length of the Morse code symbol space. \n
			:param symbol: float Range: 50E-3 to 1
		"""
		param = Conversions.decimal_value_to_str(symbol)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:SYMBol {param}')

	# noinspection PyTypeChecker
	def get_tschema(self) -> enums.AvionicComIdTimeSchem:
		"""SCPI: [SOURce<HW>]:ADF:COMid:TSCHema \n
		Snippet: value: enums.AvionicComIdTimeSchem = driver.source.adf.comid.get_tschema() \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:return: tschema: STD| USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:TSCHema?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicComIdTimeSchem)

	def set_tschema(self, tschema: enums.AvionicComIdTimeSchem) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:TSCHema \n
		Snippet: driver.source.adf.comid.set_tschema(tschema = enums.AvionicComIdTimeSchem.STD) \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:param tschema: STD| USER
		"""
		param = Conversions.enum_scalar_to_str(tschema, enums.AvionicComIdTimeSchem)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:TSCHema {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:ADF:COMid:[STATe] \n
		Snippet: value: bool = driver.source.adf.comid.get_state() \n
		Enables/disables the COM/ID signal. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:COMid:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:ADF:COMid:[STATe] \n
		Snippet: driver.source.adf.comid.set_state(state = False) \n
		Enables/disables the COM/ID signal. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ADF:COMid:STATe {param}')
