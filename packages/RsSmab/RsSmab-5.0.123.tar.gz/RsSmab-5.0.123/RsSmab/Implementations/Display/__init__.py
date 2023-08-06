from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DisplayCls:
	"""Display commands group definition. 20 total commands, 7 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	@property
	def annotation(self):
		"""annotation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_annotation'):
			from .Annotation import AnnotationCls
			self._annotation = AnnotationCls(self._core, self._cmd_group)
		return self._annotation

	@property
	def button(self):
		"""button commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_button'):
			from .Button import ButtonCls
			self._button = ButtonCls(self._core, self._cmd_group)
		return self._button

	@property
	def dialog(self):
		"""dialog commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_dialog'):
			from .Dialog import DialogCls
			self._dialog = DialogCls(self._core, self._cmd_group)
		return self._dialog

	@property
	def psave(self):
		"""psave commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_psave'):
			from .Psave import PsaveCls
			self._psave = PsaveCls(self._core, self._cmd_group)
		return self._psave

	@property
	def ukey(self):
		"""ukey commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ukey'):
			from .Ukey import UkeyCls
			self._ukey = UkeyCls(self._core, self._cmd_group)
		return self._ukey

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_update'):
			from .Update import UpdateCls
			self._update = UpdateCls(self._core, self._cmd_group)
		return self._update

	@property
	def window(self):
		"""window commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Window import WindowCls
			self._window = WindowCls(self._core, self._cmd_group)
		return self._window

	def get_brightness(self) -> float:
		"""SCPI: DISPlay:BRIGhtness \n
		Snippet: value: float = driver.display.get_brightness() \n
		Sets the brightness of the dispaly. \n
			:return: brightness: float Range: 1.0 to 20.0
		"""
		response = self._core.io.query_str('DISPlay:BRIGhtness?')
		return Conversions.str_to_float(response)

	def set_brightness(self, brightness: float) -> None:
		"""SCPI: DISPlay:BRIGhtness \n
		Snippet: driver.display.set_brightness(brightness = 1.0) \n
		Sets the brightness of the dispaly. \n
			:param brightness: float Range: 1.0 to 20.0
		"""
		param = Conversions.decimal_value_to_str(brightness)
		self._core.io.write(f'DISPlay:BRIGhtness {param}')

	def set_focus_object(self, obj_name: str) -> None:
		"""SCPI: DISPlay:FOCusobject \n
		Snippet: driver.display.set_focus_object(obj_name = '1') \n
		No command help available \n
			:param obj_name: No help available
		"""
		param = Conversions.value_to_quoted_str(obj_name)
		self._core.io.write(f'DISPlay:FOCusobject {param}')

	def set_message(self, message: str) -> None:
		"""SCPI: DISPlay:MESSage \n
		Snippet: driver.display.set_message(message = '1') \n
		No command help available \n
			:param message: No help available
		"""
		param = Conversions.value_to_quoted_str(message)
		self._core.io.write(f'DISPlay:MESSage {param}')

	def clone(self) -> 'DisplayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DisplayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
