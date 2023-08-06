from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DayCls:
	"""Day commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("day", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:DAY:STATe \n
		Snippet: value: bool = driver.sense.power.sweep.hardCopy.file.name.auto.file.day.get_state() \n
		Activates the usage of the day in the automatic file name. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:DAY:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:DAY:STATe \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.file.day.set_state(state = False) \n
		Activates the usage of the day in the automatic file name. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:DAY:STATe {param}')

	def get_value(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:DAY \n
		Snippet: value: int = driver.sense.power.sweep.hardCopy.file.name.auto.file.day.get_value() \n
		Queries the day of the date part in the automatic file name. \n
			:return: day: integer Range: 1 to 31
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:DAY?')
		return Conversions.str_to_int(response)
