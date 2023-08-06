from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BangleCls:
	"""Bangle commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bangle", core, parent)

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.AvionicVorDir:
		"""SCPI: [SOURce<HW>]:VOR:[BANGle]:DIRection \n
		Snippet: value: enums.AvionicVorDir = driver.source.vor.bangle.get_direction() \n
		Sets the reference position of the phase information. \n
			:return: direction: FROM| TO FROM The bearing angle is measured between the geographic north and the connection line from beacon to airplane. TO The bearing angle is measured between the geographic north and the connection line from airplane to beacon.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:BANGle:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicVorDir)

	def set_direction(self, direction: enums.AvionicVorDir) -> None:
		"""SCPI: [SOURce<HW>]:VOR:[BANGle]:DIRection \n
		Snippet: driver.source.vor.bangle.set_direction(direction = enums.AvionicVorDir.FROM) \n
		Sets the reference position of the phase information. \n
			:param direction: FROM| TO FROM The bearing angle is measured between the geographic north and the connection line from beacon to airplane. TO The bearing angle is measured between the geographic north and the connection line from airplane to beacon.
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.AvionicVorDir)
		self._core.io.write(f'SOURce<HwInstance>:VOR:BANGle:DIRection {param}')

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:VOR:[BANGle] \n
		Snippet: value: float = driver.source.vor.bangle.get_value() \n
		Sets the bearing angle between the VAR signal and the reference signal. The orientation of the angle can be set with
		[:SOURce<hw>]:VOR[:BANGle]:DIRection. \n
			:return: bangle: float Range: 0 to 360
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:BANGle?')
		return Conversions.str_to_float(response)

	def set_value(self, bangle: float) -> None:
		"""SCPI: [SOURce<HW>]:VOR:[BANGle] \n
		Snippet: driver.source.vor.bangle.set_value(bangle = 1.0) \n
		Sets the bearing angle between the VAR signal and the reference signal. The orientation of the angle can be set with
		[:SOURce<hw>]:VOR[:BANGle]:DIRection. \n
			:param bangle: float Range: 0 to 360
		"""
		param = Conversions.decimal_value_to_str(bangle)
		self._core.io.write(f'SOURce<HwInstance>:VOR:BANGle {param}')
