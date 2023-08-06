from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 15 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	@property
	def auto(self):
		"""auto commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import AutoCls
			self._auto = AutoCls(self._core, self._cmd_group)
		return self._auto

	def get_value(self) -> str:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME] \n
		Snippet: value: str = driver.sense.power.sweep.hardCopy.file.name.get_value() \n
		Creates of selects a file for storing the hardcopy after the method RsSmab.Sense.Power.Sweep.HardCopy.Execute.set command
		is sent. The directory is either defined with the command method RsSmab.MassMemory.currentDirectory or the path is
		specified together with the file name. Access to the file via remote control is possible using the commands of the
		MMEM-Subsystem. In contrast, command method RsSmab.Sense.Power.Sweep.HardCopy.data transfers the hardcopy contents
		directly to the remote client where they can be further processed. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:FILE:NAME?')
		return trim_str_response(response)

	def set_value(self, name: str) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:FILE:[NAME] \n
		Snippet: driver.sense.power.sweep.hardCopy.file.name.set_value(name = '1') \n
		Creates of selects a file for storing the hardcopy after the method RsSmab.Sense.Power.Sweep.HardCopy.Execute.set command
		is sent. The directory is either defined with the command method RsSmab.MassMemory.currentDirectory or the path is
		specified together with the file name. Access to the file via remote control is possible using the commands of the
		MMEM-Subsystem. In contrast, command method RsSmab.Sense.Power.Sweep.HardCopy.data transfers the hardcopy contents
		directly to the remote client where they can be further processed. \n
			:param name: string
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:FILE:NAME {param}')

	def clone(self) -> 'NameCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NameCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
