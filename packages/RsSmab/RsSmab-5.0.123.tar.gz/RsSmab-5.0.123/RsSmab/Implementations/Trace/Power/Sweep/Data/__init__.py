from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def points(self):
		"""points commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_points'):
			from .Points import PointsCls
			self._points = PointsCls(self._core, self._cmd_group)
		return self._points

	@property
	def xvalues(self):
		"""xvalues commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xvalues'):
			from .Xvalues import XvaluesCls
			self._xvalues = XvaluesCls(self._core, self._cmd_group)
		return self._xvalues

	@property
	def ysValue(self):
		"""ysValue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ysValue'):
			from .YsValue import YsValueCls
			self._ysValue = YsValueCls(self._core, self._cmd_group)
		return self._ysValue

	@property
	def yvalues(self):
		"""yvalues commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_yvalues'):
			from .Yvalues import YvaluesCls
			self._yvalues = YvaluesCls(self._core, self._cmd_group)
		return self._yvalues

	def clone(self) -> 'DataCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DataCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
