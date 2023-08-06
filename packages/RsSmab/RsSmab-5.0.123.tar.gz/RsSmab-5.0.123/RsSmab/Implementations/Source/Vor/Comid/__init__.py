from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComidCls:
	"""Comid commands group definition. 12 total commands, 1 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comid", core, parent)

	@property
	def code(self):
		"""code commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_code'):
			from .Code import CodeCls
			self._code = CodeCls(self._core, self._cmd_group)
		return self._code

	def get_dash(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DASH \n
		Snippet: value: float = driver.source.vor.comid.get_dash() \n
		Sets the length of a Morse code dash. \n
			:return: dash: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:DASH?')
		return Conversions.str_to_float(response)

	def set_dash(self, dash: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DASH \n
		Snippet: driver.source.vor.comid.set_dash(dash = 1.0) \n
		Sets the length of a Morse code dash. \n
			:param dash: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dash)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:DASH {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DEPTh \n
		Snippet: value: float = driver.source.vor.comid.get_depth() \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DEPTh \n
		Snippet: driver.source.vor.comid.set_depth(depth = 1.0) \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:DEPTh {param}')

	def get_dot(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DOT \n
		Snippet: value: float = driver.source.vor.comid.get_dot() \n
		Sets the length of a Morse code dot. If the time schema is set to standard, the dash length (= 3 times dot length) ,
		symbol space (= dot length) and letter space (= 3 times dot length) is also determined by this entry. \n
			:return: dot: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dot: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:DOT \n
		Snippet: driver.source.vor.comid.set_dot(dot = 1.0) \n
		Sets the length of a Morse code dot. If the time schema is set to standard, the dash length (= 3 times dot length) ,
		symbol space (= dot length) and letter space (= 3 times dot length) is also determined by this entry. \n
			:param dot: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dot)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:DOT {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:FREQuency \n
		Snippet: value: float = driver.source.vor.comid.get_frequency() \n
		Sets the frequency of the COM/ID signal. \n
			:return: frequency: float Range: 0.1 to 20E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:FREQuency \n
		Snippet: driver.source.vor.comid.set_frequency(frequency = 1.0) \n
		Sets the frequency of the COM/ID signal. \n
			:param frequency: float Range: 0.1 to 20E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:FREQuency {param}')

	def get_letter(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:LETTer \n
		Snippet: value: float = driver.source.vor.comid.get_letter() \n
		Sets the length of a Morse code letter space. \n
			:return: letter: float Range: 0.05 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:LETTer?')
		return Conversions.str_to_float(response)

	def set_letter(self, letter: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:LETTer \n
		Snippet: driver.source.vor.comid.set_letter(letter = 1.0) \n
		Sets the length of a Morse code letter space. \n
			:param letter: float Range: 0.05 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(letter)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:LETTer {param}')

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:PERiod \n
		Snippet: value: float = driver.source.vor.comid.get_period() \n
		Sets the period of the COM/ID signal. \n
			:return: period: float Range: 0 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:PERiod \n
		Snippet: driver.source.vor.comid.set_period(period = 1.0) \n
		Sets the period of the COM/ID signal. \n
			:param period: float Range: 0 to 120
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:PERiod {param}')

	def get_repeat(self) -> int:
		"""SCPI: [SOURce<HW>]:VOR:COMid:REPeat \n
		Snippet: value: int = driver.source.vor.comid.get_repeat() \n
		No command help available \n
			:return: repeat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:REPeat?')
		return Conversions.str_to_int(response)

	def set_repeat(self, repeat: int) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:REPeat \n
		Snippet: driver.source.vor.comid.set_repeat(repeat = 1) \n
		No command help available \n
			:param repeat: No help available
		"""
		param = Conversions.decimal_value_to_str(repeat)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:REPeat {param}')

	def get_symbol(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:COMid:SYMBol \n
		Snippet: value: float = driver.source.vor.comid.get_symbol() \n
		Sets the length of the Morse code symbol space. \n
			:return: symbol: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:SYMBol?')
		return Conversions.str_to_float(response)

	def set_symbol(self, symbol: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:SYMBol \n
		Snippet: driver.source.vor.comid.set_symbol(symbol = 1.0) \n
		Sets the length of the Morse code symbol space. \n
			:param symbol: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(symbol)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:SYMBol {param}')

	# noinspection PyTypeChecker
	def get_tschema(self) -> enums.AvionicComIdTimeSchem:
		"""SCPI: [SOURce<HW>]:VOR:COMid:TSCHema \n
		Snippet: value: enums.AvionicComIdTimeSchem = driver.source.vor.comid.get_tschema() \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:return: tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:TSCHema?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicComIdTimeSchem)

	def set_tschema(self, tschema: enums.AvionicComIdTimeSchem) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:TSCHema \n
		Snippet: driver.source.vor.comid.set_tschema(tschema = enums.AvionicComIdTimeSchem.STD) \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:param tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		param = Conversions.enum_scalar_to_str(tschema, enums.AvionicComIdTimeSchem)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:TSCHema {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:VOR:COMid:[STATe] \n
		Snippet: value: bool = driver.source.vor.comid.get_state() \n
		Enables/disables the COM/ID signal. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:COMid:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:VOR:COMid:[STATe] \n
		Snippet: driver.source.vor.comid.set_state(state = False) \n
		Enables/disables the COM/ID signal. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:VOR:COMid:STATe {param}')

	def clone(self) -> 'ComidCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ComidCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
