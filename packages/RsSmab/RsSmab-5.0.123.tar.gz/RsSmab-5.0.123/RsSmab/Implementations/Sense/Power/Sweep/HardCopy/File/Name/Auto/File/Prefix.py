from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrefixCls:
	"""Prefix commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prefix", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix:STATe \n
		Snippet: value: bool = driver.sense.power.sweep.hardCopy.file.name.auto.file.prefix.get_state() \n
		Activates the usage of the prefix in the automatic file name. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:PREFix:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix:STATe \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.file.prefix.set_state(state = False) \n
		Activates the usage of the prefix in the automatic file name. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:PREFix:STATe {param}')

	def get_value(self) -> str:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix \n
		Snippet: value: str = driver.sense.power.sweep.hardCopy.file.name.auto.file.prefix.get_value() \n
		Sets the prefix part in the automatic file name. \n
			:return: prefix: string
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:PREFix?')
		return trim_str_response(response)

	def set_value(self, prefix: str) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.auto.file.prefix.set_value(prefix = '1') \n
		Sets the prefix part in the automatic file name. \n
			:param prefix: string
		"""
		param = Conversions.value_to_quoted_str(prefix)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:PREFix {param}')
