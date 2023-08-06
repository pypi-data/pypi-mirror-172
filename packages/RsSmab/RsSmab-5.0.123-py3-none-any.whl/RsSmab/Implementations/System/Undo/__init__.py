from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UndoCls:
	"""Undo commands group definition. 5 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("undo", core, parent)

	@property
	def hclear(self):
		"""hclear commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hclear'):
			from .Hclear import HclearCls
			self._hclear = HclearCls(self._core, self._cmd_group)
		return self._hclear

	@property
	def hid(self):
		"""hid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hid'):
			from .Hid import HidCls
			self._hid = HidCls(self._core, self._cmd_group)
		return self._hid

	@property
	def hlable(self):
		"""hlable commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hlable'):
			from .Hlable import HlableCls
			self._hlable = HlableCls(self._core, self._cmd_group)
		return self._hlable

	def get_state(self) -> bool:
		"""SCPI: SYSTem:UNDO:STATe \n
		Snippet: value: bool = driver.system.undo.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:UNDO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: SYSTem:UNDO:STATe \n
		Snippet: driver.system.undo.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:UNDO:STATe {param}')

	def clone(self) -> 'UndoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UndoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
