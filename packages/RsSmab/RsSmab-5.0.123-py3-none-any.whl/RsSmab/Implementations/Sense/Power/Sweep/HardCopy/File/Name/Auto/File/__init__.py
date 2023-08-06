from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 10 total commands, 4 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	@property
	def day(self):
		"""day commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_day'):
			from .Day import DayCls
			self._day = DayCls(self._core, self._cmd_group)
		return self._day

	@property
	def month(self):
		"""month commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_month'):
			from .Month import MonthCls
			self._month = MonthCls(self._core, self._cmd_group)
		return self._month

	@property
	def prefix(self):
		"""prefix commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prefix'):
			from .Prefix import PrefixCls
			self._prefix = PrefixCls(self._core, self._cmd_group)
		return self._prefix

	@property
	def year(self):
		"""year commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_year'):
			from .Year import YearCls
			self._year = YearCls(self._core, self._cmd_group)
		return self._year

	def get_number(self) -> int:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:[FILE]:NUMBer \n
		Snippet: value: int = driver.sense.power.sweep.hardCopy.file.name.auto.file.get_number() \n
		Queries the generated number in the automatic file name. \n
			:return: number: integer Range: 0 to 999999
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE:NUMBer?')
		return Conversions.str_to_int(response)

	def get_value(self) -> str:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME]:AUTO:FILE \n
		Snippet: value: str = driver.sense.power.sweep.hardCopy.file.name.auto.file.get_value() \n
		Queries the file name generated with the automatic naming settings. Note: As default the automatically generated file
		name is composed of: >PAth>/<Prefix><YYYY><MM><DD><Number>.<Format>. Each component can be deactivated/ activated
		separately to individually design the file name. \n
			:return: file: string
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME:AUTO:FILE?')
		return trim_str_response(response)

	def clone(self) -> 'FileCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FileCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
