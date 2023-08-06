from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComidCls:
	"""Comid commands group definition. 11 total commands, 1 Subgroups, 9 group commands"""

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
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DASH \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_dash() \n
		Sets the length of a Morse code dash. \n
			:return: dash: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:DASH?')
		return Conversions.str_to_float(response)

	def set_dash(self, dash: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DASH \n
		Snippet: driver.source.ils.mbeacon.comid.set_dash(dash = 1.0) \n
		Sets the length of a Morse code dash. \n
			:param dash: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dash)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:DASH {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DEPTh \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_depth() \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DEPTh \n
		Snippet: driver.source.ils.mbeacon.comid.set_depth(depth = 1.0) \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:DEPTh {param}')

	def get_dot(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DOT \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_dot() \n
		Sets the length of a Morse code dot. \n
			:return: dot: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dot: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:DOT \n
		Snippet: driver.source.ils.mbeacon.comid.set_dot(dot = 1.0) \n
		Sets the length of a Morse code dot. \n
			:param dot: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(dot)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:DOT {param}')

	def get_frequency(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:FREQuency \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_frequency() \n
		Sets the frequency of the COM/ID signal. \n
			:return: frequency: float Range: 0.1 to 20E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:FREQuency \n
		Snippet: driver.source.ils.mbeacon.comid.set_frequency(frequency = 1.0) \n
		Sets the frequency of the COM/ID signal. \n
			:param frequency: float Range: 0.1 to 20E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:FREQuency {param}')

	def get_letter(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:LETTer \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_letter() \n
		Sets the length of a Morse code letter space. \n
			:return: letter: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:LETTer?')
		return Conversions.str_to_float(response)

	def set_letter(self, letter: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:LETTer \n
		Snippet: driver.source.ils.mbeacon.comid.set_letter(letter = 1.0) \n
		Sets the length of a Morse code letter space. \n
			:param letter: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(letter)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:LETTer {param}')

	def get_period(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:PERiod \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_period() \n
		Sets the period of the COM/ID signal. \n
			:return: period: float Range: 0 to 120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:PERiod \n
		Snippet: driver.source.ils.mbeacon.comid.set_period(period = 1.0) \n
		Sets the period of the COM/ID signal. \n
			:param period: float Range: 0 to 120
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:PERiod {param}')

	def get_symbol(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:SYMBol \n
		Snippet: value: float = driver.source.ils.mbeacon.comid.get_symbol() \n
		Sets the length of the Morse code symbol space. \n
			:return: symbol: float Range: 0.05 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:SYMBol?')
		return Conversions.str_to_float(response)

	def set_symbol(self, symbol: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:SYMBol \n
		Snippet: driver.source.ils.mbeacon.comid.set_symbol(symbol = 1.0) \n
		Sets the length of the Morse code symbol space. \n
			:param symbol: float Range: 0.05 to 1
		"""
		param = Conversions.decimal_value_to_str(symbol)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:SYMBol {param}')

	# noinspection PyTypeChecker
	def get_tschema(self) -> enums.AvionicComIdTimeSchem:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:TSCHema \n
		Snippet: value: enums.AvionicComIdTimeSchem = driver.source.ils.mbeacon.comid.get_tschema() \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:return: tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:TSCHema?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicComIdTimeSchem)

	def set_tschema(self, tschema: enums.AvionicComIdTimeSchem) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:TSCHema \n
		Snippet: driver.source.ils.mbeacon.comid.set_tschema(tschema = enums.AvionicComIdTimeSchem.STD) \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:param tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		param = Conversions.enum_scalar_to_str(tschema, enums.AvionicComIdTimeSchem)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:TSCHema {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:[STATe] \n
		Snippet: value: bool = driver.source.ils.mbeacon.comid.get_state() \n
		Enables/disables the COM/ID signal. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:COMid:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:COMid:[STATe] \n
		Snippet: driver.source.ils.mbeacon.comid.set_state(state = False) \n
		Enables/disables the COM/ID signal. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:COMid:STATe {param}')

	def clone(self) -> 'ComidCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ComidCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
