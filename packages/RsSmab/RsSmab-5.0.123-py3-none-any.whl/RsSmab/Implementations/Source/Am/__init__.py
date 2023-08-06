from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AmCls:
	"""Am commands group definition. 11 total commands, 4 Subgroups, 3 group commands
	Repeated Capability: GeneratorIx, default value after init: GeneratorIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("am", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_generatorIx_get', 'repcap_generatorIx_set', repcap.GeneratorIx.Nr1)

	def repcap_generatorIx_set(self, generatorIx: repcap.GeneratorIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to GeneratorIx.Default
		Default value after init: GeneratorIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(generatorIx)

	def repcap_generatorIx_get(self) -> repcap.GeneratorIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def depth(self):
		"""depth commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_depth'):
			from .Depth import DepthCls
			self._depth = DepthCls(self._core, self._cmd_group)
		return self._depth

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviation'):
			from .Deviation import DeviationCls
			self._deviation = DeviationCls(self._core, self._cmd_group)
		return self._deviation

	@property
	def sensitivity(self):
		"""sensitivity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensitivity'):
			from .Sensitivity import SensitivityCls
			self._sensitivity = SensitivityCls(self._core, self._cmd_group)
		return self._sensitivity

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AmMode:
		"""SCPI: [SOURce<HW>]:AM:MODE \n
		Snippet: value: enums.AmMode = driver.source.am.get_mode() \n
		Selects the mode of the amplitude modulation. [:SOURce<hw>]:AM:MODE > SCAN sets [:SOURce<hw>]:AM:TYPE > EXPonential. For
		active external exponential AM, automatically sets [:SOURce<hw>]:INPut:MODext:COUPling<ch> > DC. \n
			:return: am_mode: SCAN| NORMal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AmMode)

	def set_mode(self, am_mode: enums.AmMode) -> None:
		"""SCPI: [SOURce<HW>]:AM:MODE \n
		Snippet: driver.source.am.set_mode(am_mode = enums.AmMode.NORMal) \n
		Selects the mode of the amplitude modulation. [:SOURce<hw>]:AM:MODE > SCAN sets [:SOURce<hw>]:AM:TYPE > EXPonential. For
		active external exponential AM, automatically sets [:SOURce<hw>]:INPut:MODext:COUPling<ch> > DC. \n
			:param am_mode: SCAN| NORMal
		"""
		param = Conversions.enum_scalar_to_str(am_mode, enums.AmMode)
		self._core.io.write(f'SOURce<HwInstance>:AM:MODE {param}')

	def get_ratio(self) -> float:
		"""SCPI: [SOURce<HW>]:AM:RATio \n
		Snippet: value: float = driver.source.am.get_ratio() \n
		Sets the deviation ratio (path#2 to path#1) in percent. \n
			:return: ratio: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""SCPI: [SOURce<HW>]:AM:RATio \n
		Snippet: driver.source.am.set_ratio(ratio = 1.0) \n
		Sets the deviation ratio (path#2 to path#1) in percent. \n
			:param ratio: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'SOURce<HwInstance>:AM:RATio {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.AmType:
		"""SCPI: [SOURce<HW>]:AM:TYPE \n
		Snippet: value: enums.AmType = driver.source.am.get_type_py() \n
		Selects the type of amplitude modulation. For [:SOURce<hw>]:AM:MODE SCAN, only EXPonential is available.
		For active external exponential AM, automatically sets [:SOURce<hw>]:INPut:MODext:COUPling<ch>DC. \n
			:return: am_type: LINear| EXPonential
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.AmType)

	def set_type_py(self, am_type: enums.AmType) -> None:
		"""SCPI: [SOURce<HW>]:AM:TYPE \n
		Snippet: driver.source.am.set_type_py(am_type = enums.AmType.EXPonential) \n
		Selects the type of amplitude modulation. For [:SOURce<hw>]:AM:MODE SCAN, only EXPonential is available.
		For active external exponential AM, automatically sets [:SOURce<hw>]:INPut:MODext:COUPling<ch>DC. \n
			:param am_type: LINear| EXPonential
		"""
		param = Conversions.enum_scalar_to_str(am_type, enums.AmType)
		self._core.io.write(f'SOURce<HwInstance>:AM:TYPE {param}')

	def clone(self) -> 'AmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
