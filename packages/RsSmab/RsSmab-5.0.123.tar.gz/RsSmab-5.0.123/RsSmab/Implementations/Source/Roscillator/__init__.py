from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoscillatorCls:
	"""Roscillator commands group definition. 14 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("roscillator", core, parent)

	@property
	def external(self):
		"""external commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	@property
	def internal(self):
		"""internal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_internal'):
			from .Internal import InternalCls
			self._internal = InternalCls(self._core, self._cmd_group)
		return self._internal

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	def preset(self) -> None:
		"""SCPI: [SOURce]:ROSCillator:PRESet \n
		Snippet: driver.source.roscillator.preset() \n
		Resets the reference oscillator settings. \n
		"""
		self._core.io.write(f'SOURce:ROSCillator:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce]:ROSCillator:PRESet \n
		Snippet: driver.source.roscillator.preset_with_opc() \n
		Resets the reference oscillator settings. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce:ROSCillator:PRESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""SCPI: [SOURce]:ROSCillator:SOURce \n
		Snippet: value: enums.SourceInt = driver.source.roscillator.get_source() \n
		Selects between internal or external reference frequency. \n
			:return: source: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""SCPI: [SOURce]:ROSCillator:SOURce \n
		Snippet: driver.source.roscillator.set_source(source = enums.SourceInt.EXTernal) \n
		Selects between internal or external reference frequency. \n
			:param source: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce:ROSCillator:SOURce {param}')

	def clone(self) -> 'RoscillatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RoscillatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
