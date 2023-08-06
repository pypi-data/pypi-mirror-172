from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class YearCls:
	"""Year commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("year", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:YEAR:STATe \n
		Snippet: value: bool = driver.sense.power.sweep.hardCopy.file.name.auto.file.year.get_state() \n
		Activates the usage of the year in the automatic file name. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:YEAR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:YEAR:STATe \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.file.year.set_state(state = False) \n
		Activates the usage of the year in the automatic file name. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:YEAR:STATe {param}')

	def get_value(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:YEAR \n
		Snippet: value: int = driver.sense.power.sweep.hardCopy.file.name.auto.file.year.get_value() \n
		Queries the year of the date part in the automatic file name. \n
			:return: year: integer Range: 1784 to 8000
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:YEAR?')
		return Conversions.str_to_int(response)
