import json
import os
from typing import List

from modules import ToneBanks
from file_io.file import FileOutputWriter


class JsonWriter(FileOutputWriter):

    @staticmethod
    def _find(item: dict, tone_banks_name, patch_set_name=None, patch_name=None):
        v = [val for val in item["tone_banks"] if val["name"] ==tone_banks_name]
        if not patch_set_name:
            return v if v and len(v) > 0 else None

        v = [val for val in v[0]["patch_sets"] if val["name"] == patch_set_name]
        if not patch_name:
            return v if v and len(v) > 0 else None

        v = [val for val in v[0]["patches"] if val["patch_name"] == patch_name]

        return v if v and len(v) > 0 else None

    @staticmethod
    def write(file_name, tone_banks: List[ToneBanks.ToneBank]):
        existing_file = None
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                existing_file = json.load(f)

        new_file = {"tone_banks": []}

        for tb in tone_banks:
            new_file["tone_banks"].append(tb.to_dict())

        if existing_file:
            # Adding missing entries. Does NOT update existing as of now ...
            for n_tb in new_file["tone_banks"]:
                if not JsonWriter._find(existing_file, n_tb["name"]):
                    existing_file["tone_banks"].append(n_tb.copy())
                else:
                    for n_tb_ps in n_tb["patch_sets"]:
                        if not JsonWriter._find(existing_file, n_tb["name"], n_tb_ps["name"]):
                            JsonWriter._find(existing_file, n_tb["name"])[0]["patch_sets"].append(n_tb_ps)
                        else:
                            for p in n_tb_ps["patches"]:
                                if not JsonWriter._find(existing_file, n_tb["name"], n_tb_ps["name"], p["patch_name"]):
                                    JsonWriter._find(existing_file, n_tb["name"], n_tb_ps["name"])[0]["patches"].append(p)
            result = existing_file
        else:
            result = new_file
        with open(file_name, "w") as f:
            f.write(json.dumps(result, indent=2))
            f.flush()

        pass
