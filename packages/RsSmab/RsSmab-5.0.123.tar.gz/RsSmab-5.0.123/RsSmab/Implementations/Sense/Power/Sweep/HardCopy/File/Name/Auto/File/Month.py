from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MonthCls:
	"""Month commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("month", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:MONTh:STATe \n
		Snippet: value: bool = driver.sense.power.sweep.hardCopy.file.name.auto.file.month.get_state() \n
		Activates the usage of the month in the automatic file name. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:MONTh:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:MONTh:STATe \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.file.month.set_state(state = False) \n
		Activates the usage of the month in the automatic file name. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:MONTh:STATe {param}')

	def get_value(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:MONTh \n
		Snippet: value: int = driver.sense.power.sweep.hardCopy.file.name.auto.file.month.get_value() \n
		Queries the day of the date part in the automatic file name. \n
			:return: month: integer Range: 1 to 12
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:MONTh?')
		return Conversions.str_to_int(response)
