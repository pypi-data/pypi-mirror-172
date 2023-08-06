from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TestCls:
	"""Test commands group definition. 14 total commands, 7 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("test", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def device(self):
		"""device commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_device'):
			from .Device import DeviceCls
			self._device = DeviceCls(self._core, self._cmd_group)
		return self._device

	@property
	def remote(self):
		"""remote commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_remote'):
			from .Remote import RemoteCls
			self._remote = RemoteCls(self._core, self._cmd_group)
		return self._remote

	@property
	def res(self):
		"""res commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_res'):
			from .Res import ResCls
			self._res = ResCls(self._core, self._cmd_group)
		return self._res

	@property
	def serror(self):
		"""serror commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_serror'):
			from .Serror import SerrorCls
			self._serror = SerrorCls(self._core, self._cmd_group)
		return self._serror

	@property
	def sw(self):
		"""sw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sw'):
			from .Sw import SwCls
			self._sw = SwCls(self._core, self._cmd_group)
		return self._sw

	@property
	def write(self):
		"""write commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_write'):
			from .Write import WriteCls
			self._write = WriteCls(self._core, self._cmd_group)
		return self._write

	# noinspection PyTypeChecker
	def get_level(self) -> enums.SelftLev:
		"""SCPI: TEST:LEVel \n
		Snippet: value: enums.SelftLev = driver.test.get_level() \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('TEST:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.SelftLev)

	def set_level(self, level: enums.SelftLev) -> None:
		"""SCPI: TEST:LEVel \n
		Snippet: driver.test.set_level(level = enums.SelftLev.CUSTomer) \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.enum_scalar_to_str(level, enums.SelftLev)
		self._core.io.write(f'TEST:LEVel {param}')

	def set_nrp_trigger(self, nrp_trigger: bool) -> None:
		"""SCPI: TEST:NRPTrigger \n
		Snippet: driver.test.set_nrp_trigger(nrp_trigger = False) \n
		No command help available \n
			:param nrp_trigger: No help available
		"""
		param = Conversions.bool_to_str(nrp_trigger)
		self._core.io.write(f'TEST:NRPTrigger {param}')

	def preset(self) -> None:
		"""SCPI: TEST:PRESet \n
		Snippet: driver.test.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'TEST:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: TEST:PRESet \n
		Snippet: driver.test.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'TEST:PRESet', opc_timeout_ms)

	def clone(self) -> 'TestCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TestCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
