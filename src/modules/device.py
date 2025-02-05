from typing import List, Optional

from modules import ToneBanks
from modules.Patch import Patch, PatchSet


class SynthDevice:

    def __init__(self, midi_string: str, tone_banks: List[ToneBanks.ToneBank]):
        self._midi_string = midi_string
        self._tone_banks: List[ToneBanks.ToneBank] = tone_banks.copy()

    def get_midi_driver_str(self):
        return self._midi_string

    def get_all_banks(self) -> List[ToneBanks.ToneBank]:
        return self._tone_banks

    def get_total_num_patches(self) -> int:
        num = 0
        for t in self._tone_banks:
            num += t.get_num_patches_requested()

        return num

    def get_tone_banks(self, get_user_banks: bool, get_preset_banks: bool) -> List[ToneBanks.ToneBank]:
        result = []
        for tb in self.get_all_banks():
            ps = []
            if get_user_banks:
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Drums, PatchSet.SetType.User))
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Tones, PatchSet.SetType.User))
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Scenes, PatchSet.SetType.USer))
            if get_preset_banks:
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Drums, PatchSet.SetType.Preset))
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Tones, PatchSet.SetType.Preset))
                ps.extend(tb.get_patch_sets(PatchSet.PatchMode.Scenes, PatchSet.SetType.Preset))
            result.append(ToneBanks.ToneBank(tb.get_name(), patch_set=ps.copy()))
        return result

    def create_patch(self, patch_data: bytes, patch_id: int) -> Optional[Patch]:
        return None

