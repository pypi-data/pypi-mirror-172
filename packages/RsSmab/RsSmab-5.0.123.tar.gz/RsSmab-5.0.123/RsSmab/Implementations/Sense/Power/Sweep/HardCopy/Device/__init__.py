from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceCls:
	"""Device commands group definition. 7 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("device", core, parent)

	@property
	def language(self):
		"""language commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_language'):
			from .Language import LanguageCls
			self._language = LanguageCls(self._core, self._cmd_group)
		return self._language

	def get_size(self) -> List[int]:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:SIZE \n
		Snippet: value: List[int] = driver.sense.power.sweep.hardCopy.device.get_size() \n
		Sets the size of the hardcopy in number of pixels. The first value of the size setting defines the width, the second
		value the height of the image. \n
			:return: size: 320,240 | 640,480 | 800,600 | 1024,768
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SENSe:POWer:SWEep:HCOPy:DEVice:SIZE?')
		return response

	def set_size(self, size: List[int]) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice:SIZE \n
		Snippet: driver.sense.power.sweep.hardCopy.device.set_size(size = [1, 2, 3]) \n
		Sets the size of the hardcopy in number of pixels. The first value of the size setting defines the width, the second
		value the height of the image. \n
			:param size: 320,240 | 640,480 | 800,600 | 1024,768
		"""
		param = Conversions.list_to_csv_str(size)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice:SIZE {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.HcopyDestination:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice \n
		Snippet: value: enums.HcopyDestination = driver.sense.power.sweep.hardCopy.device.get_value() \n
		Defines the output device. The setting is fixed to FILE, i.e. the hardcopy is stored in a file. \n
			:return: device: FILE| PRINter
		"""
		response = self._core.io.query_str('SENSe:POWer:SWEep:HCOPy:DEVice?')
		return Conversions.str_to_scalar_enum(response, enums.HcopyDestination)

	def set_value(self, device: enums.HcopyDestination) -> None:
		"""SCPI: SENSe:[POWer]:SWEep:HCOPy:DEVice \n
		Snippet: driver.sense.power.sweep.hardCopy.device.set_value(device = enums.HcopyDestination.FILE) \n
		Defines the output device. The setting is fixed to FILE, i.e. the hardcopy is stored in a file. \n
			:param device: FILE| PRINter
		"""
		param = Conversions.enum_scalar_to_str(device, enums.HcopyDestination)
		self._core.io.write(f'SENSe:POWer:SWEep:HCOPy:DEVice {param}')

	def clone(self) -> 'DeviceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DeviceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
