from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	def get_deviation(self) -> int:
		"""SCPI: [SOURce<HW>]:VOR:REFerence:[DEViation] \n
		Snippet: value: int = driver.source.vor.reference.get_deviation() \n
		Sets the frequency deviation of the reference signal on the FM carrier. \n
			:return: deviation: integer Range: 0 to 960
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:VOR:REFerence:DEViation?')
		return Conversions.str_to_int(response)

	def set_deviation(self, deviation: int) -> None:
		"""SCPI: [SOURce<HW>]:VOR:REFerence:[DEViation] \n
		Snippet: driver.source.vor.reference.set_deviation(deviation = 1) \n
		Sets the frequency deviation of the reference signal on the FM carrier. \n
			:param deviation: integer Range: 0 to 960
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:VOR:REFerence:DEViation {param}')
