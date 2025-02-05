import binascii
from enum import Enum
from typing import List, Optional

from midi import MidiConstants


class Patch:

    def __init__(self, data: bytes, id: int):
        if len(data) != 42:
            raise ValueError("Patch data not formated correctly. must be 21 bytes")
        self._raw_data = data
        self._id = id
        self._program = data[0:6] if data else b''
        self._category = MidiConstants.Category(int(data[6:8], 16))
        self._patch_name = binascii.unhexlify(data[10:42]).decode()
        pass

    def get_patch_address(self):
        return self._program

    def get_cc_msb(self):
        return self._program[0:2]

    def get_cc_lsb(self):
        return self._program[2:4]

    def get_cc_pc(self):
        return self._program[4:6]

    def get_program_change(self) -> str:
        return f'{MidiConstants.CC_SEL}{self._program[0:2]}{MidiConstants.CC_PC}{self._program[:-2]}'

    def get_patch_name(self):
        return self._patch_name

    def get_category_name(self):
        return self._category.name

    def get_category_id(self):
        return self._category.value

    def __str__(self):
        return f'[{self._id:04d}] {self._patch_name} ({self.get_category_name().replace("_", " ")}) [{self._program}]'

    def to_dict(self) -> dict:
        return {"id": self._id, "program": self._program.decode(), "patch_name": self._patch_name, "category": self._category.name}

    @staticmethod
    def from_dict(patch: dict) -> "Patch":
        p = Patch(b'0'*42, patch.get("id", 0))
        p._program = patch.get("program", "").encode()
        p._patch_name = patch.get("patch_name", "")
        p._category = MidiConstants.Category[patch.get("category", MidiConstants.Category.Unassigned.name)]
        return p


def _default_id_calc_function(data, index) -> int:
    return int(data[4:6], 16) + 1


class PatchSet:
    class PatchMode(Enum):
        Drums = 0
        Tones = 1
        Scenes = 2

    class SetType(Enum):
        Preset = 0
        User = 1

    def __init__(self, name: str, set_type: SetType, patch_mode: PatchMode, address: bytes, offset_address: bytes, num_patches: int, id_calc_func=_default_id_calc_function):
        self._address = address
        self._offset_address = offset_address
        self._id_calc_function = id_calc_func
        self._patches: List[Patch] = []
        self._name = name
        self._num_patches_in_set = num_patches
        self._index = 0
        self._patch_mode = patch_mode
        self._set_type = set_type

    def get_next_id(self, data) -> int:
        id = self._id_calc_function(data, self._index)
        self._index += 1
        return id

    def get_request(self) -> (bytes, bytes):
        return self._address, self._offset_address

    def add_patch(self, patch: Patch) -> Optional[Patch]:
        if patch and len([p for p in self._patches if p.get_patch_address() == patch.get_patch_address()]) == 0:
            self._patches.append(patch)
            self._index += 1
            return patch
        return None

    def get_name(self):
        return self._name

    def get_patch_mode(self) -> PatchMode:
        return self._patch_mode

    def get_set_type(self) -> SetType:
        return self._set_type

    def get_patches(self):
        return self._patches

    def get_num_patches_requested(self):
        return self._num_patches_in_set

    def to_dict(self) -> Optional[dict]:
        if not self._patches or len(self._patches) == 0:
            return None

        p_dict = []
        for p in self._patches:
            val = p.to_dict()
            if val:
                p_dict.append(val)

        return {
            "patches": p_dict,
            "name": self._name,
            "num_patches": len(p_dict),
            "patch_mode": self._patch_mode.name,
            "set_type": self._set_type.name
        }

    @staticmethod
    def from_dict(patch_set: dict) -> "PatchSet":
        patch_list = []
        for p in patch_set.get("patches", []):
            patch_list.append(Patch.from_dict(p))

        ps = PatchSet(
            name=patch_set.get("name", ""),
            address=b'',
            set_type=PatchSet.SetType[patch_set.get("set_type", "Preset")],
            num_patches=patch_set.get("num_patches", 0),
            patch_mode=PatchSet.PatchMode[patch_set.get("patch_mode", "Tones")],
            offset_address=b'',
            id_calc_func=_default_id_calc_function
        )

        ps._patches = patch_list
        return ps
