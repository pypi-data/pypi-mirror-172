from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MarkerCls:
	"""Marker commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("marker", core, parent)

	def get_frequency(self) -> int:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:MARKer:FREQuency \n
		Snippet: value: int = driver.source.ils.mbeacon.marker.get_frequency() \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:return: frequency: 400| 1300| 3000 Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:MARKer:FREQuency?')
		return Conversions.str_to_int(response)

	def set_frequency(self, frequency: int) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:MARKer:FREQuency \n
		Snippet: driver.source.ils.mbeacon.marker.set_frequency(frequency = 1) \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:param frequency: 400| 1300| 3000 Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:MARKer:FREQuency {param}')

	def get_depth(self) -> float:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:[MARKer]:DEPTh \n
		Snippet: value: float = driver.source.ils.mbeacon.marker.get_depth() \n
		Sets the modulation depth of the marker signal for the ILS marker beacon signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:MARKer:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:[MARKer]:DEPTh \n
		Snippet: driver.source.ils.mbeacon.marker.set_depth(depth = 1.0) \n
		Sets the modulation depth of the marker signal for the ILS marker beacon signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:MARKer:DEPTh {param}')

	def get_pulsed(self) -> bool:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:[MARKer]:PULSed \n
		Snippet: value: bool = driver.source.ils.mbeacon.marker.get_pulsed() \n
		Activates the modulation of a pulsed marker signal (morse coding) . \n
			:return: pulsed: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:MARKer:PULSed?')
		return Conversions.str_to_bool(response)

	def set_pulsed(self, pulsed: bool) -> None:
		"""SCPI: [SOURce<HW>]:[ILS]:MBEacon:[MARKer]:PULSed \n
		Snippet: driver.source.ils.mbeacon.marker.set_pulsed(pulsed = False) \n
		Activates the modulation of a pulsed marker signal (morse coding) . \n
			:param pulsed: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(pulsed)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:MARKer:PULSed {param}')
