from typing import List, Optional

from modules.Patch import PatchSet


def calc_by_index(data: bytes, index) -> int:
    return index + 1


class ToneBank:
    _name = "Undefined"
    _patch_sets: List[PatchSet] = []

    def __init__(self, name: str, patch_set: List[PatchSet], root_category: str = None):
        self._name: str = name
        self._patch_sets: List[PatchSet] = patch_set
        self._root_category: str = root_category

    def get_patch_sets(self, mode: PatchSet.PatchMode, set_type: PatchSet.SetType = None, loaded: bool = False):
        required_patches = -1 if not loaded else 0
        if set_type:
            return [ps for ps in self._patch_sets if ps.get_patch_mode() == mode and ps.get_set_type() == set_type and len(ps.get_patches()) > required_patches]
        else:
            return [ps for ps in self._patch_sets if ps.get_patch_mode() == mode and len(ps.get_patches()) > required_patches]

    def get_all_patch_sets(self):
        return self._patch_sets

    def get_name(self) -> str:
        return self._name

    def get_root_category(self) -> Optional[str]:
        return self._root_category

    def get_num_patches_requested(self):
        num = 0
        for p in self._patch_sets:
            num += p.get_num_patches_requested()

        return num

    def to_dict(self) -> Optional[dict]:
        if not self._patch_sets or len(self._patch_sets) == 0:
            return None

        ps = []
        for p in self._patch_sets:
            val = p.to_dict()
            if val:
                ps.append(val)

        return {
            "name": self._name,
            "patch_sets": ps
        }

    @staticmethod
    def from_dict(tone_bank: dict) -> "ToneBank":
        ps = []

        for p in tone_bank.get("patch_sets"):
            ps.append(PatchSet.from_dict(p))

        return ToneBank(tone_bank["name"], patch_set=ps)


