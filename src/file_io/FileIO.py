import json
from typing import List

from modules.Patch import PatchSet
from modules.ToneBanks import ToneBank


class JsonFileReader:

    def __init__(self, file):
        self._file = file

    def get_tone_banks(self, get_user_banks: bool, get_preset_banks: bool) -> List[ToneBank]:
        with open(self._file, "r") as f:
            data = json.load(f)

        if not data:
            return []

        parsed_banks: List[ToneBank] = []

        for tb in data["tone_banks"]:
            parsed_banks.append(ToneBank.from_dict(tb))

        result = []
        for tb in parsed_banks:
            patch_sets = []
            if get_user_banks:
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Drums, PatchSet.SetType.User))
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Tones, PatchSet.SetType.User))
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Scenes, PatchSet.SetType.User))
            if get_preset_banks:
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Drums, PatchSet.SetType.Preset))
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Tones, PatchSet.SetType.Preset))
                patch_sets.extend(tb.get_patch_sets(PatchSet.PatchMode.Scenes, PatchSet.SetType.Preset))
            result.append(ToneBank(tb.get_name(), patch_set=patch_sets))

        return result
