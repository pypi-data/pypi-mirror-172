from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MarkerCls:
	"""Marker commands group definition. 3 total commands, 2 Subgroups, 1 group commands
	Repeated Capability: Marker, default value after init: Marker.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("marker", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_marker_get', 'repcap_marker_set', repcap.Marker.Nr0)

	def repcap_marker_set(self, marker: repcap.Marker) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Marker.Default
		Default value after init: Marker.Nr0"""
		self._cmd_group.set_repcap_enum_value(marker)

	def repcap_marker_get(self) -> repcap.Marker:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def fstate(self):
		"""fstate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fstate'):
			from .Fstate import FstateCls
			self._fstate = FstateCls(self._core, self._cmd_group)
		return self._fstate

	# noinspection PyTypeChecker
	def get_active(self) -> enums.SweMarkActive:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer:ACTive \n
		Snippet: value: enums.SweMarkActive = driver.source.sweep.frequency.marker.get_active() \n
		Defines the marker signal to be output with a higher voltage than all other markers. \n
			:return: active: NONE| M01| M02| M03| M04| M05| M06| M07| M08| M09| M10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:FREQuency:MARKer:ACTive?')
		return Conversions.str_to_scalar_enum(response, enums.SweMarkActive)

	def set_active(self, active: enums.SweMarkActive) -> None:
		"""SCPI: [SOURce<HW>]:SWEep:[FREQuency]:MARKer:ACTive \n
		Snippet: driver.source.sweep.frequency.marker.set_active(active = enums.SweMarkActive.M01) \n
		Defines the marker signal to be output with a higher voltage than all other markers. \n
			:param active: NONE| M01| M02| M03| M04| M05| M06| M07| M08| M09| M10
		"""
		param = Conversions.enum_scalar_to_str(active, enums.SweMarkActive)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:FREQuency:MARKer:ACTive {param}')

	def clone(self) -> 'MarkerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MarkerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
