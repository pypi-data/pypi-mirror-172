from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormalInverted:
		"""SCPI: [SOURce<HW>]:SWEep:MARKer:OUTPut:POLarity \n
		Snippet: value: enums.NormalInverted = driver.source.sweep.marker.output.get_polarity() \n
		Selects the polarity of the marker signal. \n
			:return: polarity: NORMal| INVerted NORMal Marker level is high when after reaching the mark. INVerted Marker level is low after reaching the mark.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:MARKer:OUTPut:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormalInverted)

	def set_polarity(self, polarity: enums.NormalInverted) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:MARKer:OUTPut:POLarity \n
		Snippet: driver.source.sweep.marker.output.set_polarity(polarity = enums.NormalInverted.INVerted) \n
		Selects the polarity of the marker signal. \n
			:param polarity: NORMal| INVerted NORMal Marker level is high when after reaching the mark. INVerted Marker level is low after reaching the mark.
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormalInverted)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:MARKer:OUTPut:POLarity {param}')
