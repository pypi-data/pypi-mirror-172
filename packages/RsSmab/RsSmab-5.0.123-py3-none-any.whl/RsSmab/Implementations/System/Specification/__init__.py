from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpecificationCls:
	"""Specification commands group definition. 5 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("specification", core, parent)

	@property
	def identification(self):
		"""identification commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identification'):
			from .Identification import IdentificationCls
			self._identification = IdentificationCls(self._core, self._cmd_group)
		return self._identification

	@property
	def version(self):
		"""version commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_version'):
			from .Version import VersionCls
			self._version = VersionCls(self._core, self._cmd_group)
		return self._version

	def clone(self) -> 'SpecificationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpecificationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
