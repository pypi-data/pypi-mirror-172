from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiplierCls:
	"""Multiplier commands group definition. 31 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiplier", core, parent)

	@property
	def external(self):
		"""external commands group. 3 Sub-classes, 15 commands."""
		if not hasattr(self, '_external'):
			from .External import ExternalCls
			self._external = ExternalCls(self._core, self._cmd_group)
		return self._external

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier \n
		Snippet: value: float = driver.source.frequency.multiplier.get_value() \n
		Sets the multiplication factor NFREQ:MULT of a subsequent downstream instrument. The parameters offset fFREQ:OFFSer and
		multiplier NFREQ:MULT affect the frequency value set with the command [:SOURce<hw>]:FREQuency[:CW|FIXed].
		The query [:SOURce<hw>]:FREQuency[:CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout * NFREQ:MULT
		+ fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. \n
			:return: multiplier: float Range: -10000 to 10000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier?')
		return Conversions.str_to_float(response)

	def set_value(self, multiplier: float) -> None:
		"""SCPI: [SOURce<HW>]:FREQuency:MULTiplier \n
		Snippet: driver.source.frequency.multiplier.set_value(multiplier = 1.0) \n
		Sets the multiplication factor NFREQ:MULT of a subsequent downstream instrument. The parameters offset fFREQ:OFFSer and
		multiplier NFREQ:MULT affect the frequency value set with the command [:SOURce<hw>]:FREQuency[:CW|FIXed].
		The query [:SOURce<hw>]:FREQuency[:CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout * NFREQ:MULT
		+ fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. \n
			:param multiplier: float Range: -10000 to 10000
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier {param}')

	def clone(self) -> 'MultiplierCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiplierCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
