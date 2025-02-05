from typing import List

from modules import ToneBanks
from file_io.file import FileOutputWriter
from modules.Patch import PatchSet


class CubasePatchScriptOutput(FileOutputWriter):

    @staticmethod
    def _get_header() -> str:
        return "".join([
            "[cubase parse file]\n",
            "[parser version 0001]\n\n",
            "[creators first name] Geir\n",
            "[creators last name] Rastad\n",
            "[device manufacturer] ROLAND\n",
            "[device name] Integra-7\n",
            "[script name] Roland Integra-7\n",
            "[script version] version 1.00\n",
            "[bank: do swap value bytes]\n"
        ])

    @staticmethod
    def _format_patchset(patch_sets, level) -> str:
        retval = ""
        for ps in patch_sets:
            patches = ps.get_patches()
            if not patches or len(patches) == 0:
                continue
            retval += f"[g{level}]\t\t" + ps.get_name() + "\n"
            for p in patches:
                retval += f'[p{level+1}, {int(p.get_cc_pc(), 16)}, {int(p.get_cc_msb(), 16)}, {int(p.get_cc_lsb(), 16)}]\t{p.get_patch_name()}\n'
            retval += "\n"
        return retval

    @staticmethod
    def _write_patch_set(f, tone_banks: List[ToneBanks.ToneBank], mode: PatchSet.PatchMode, level):
        f.write(f'[mode{10 if mode == PatchSet.PatchMode.Drums else ""}] {mode.name}\n')
        for tb in tone_banks:
            data = CubasePatchScriptOutput._format_patchset(
                tb.get_patch_sets(mode, None, loaded=True), level)
            if not data or len(data.strip()) == 0:
                continue
            f.write("[g1]\t" + tb.get_name() + "\n")
            f.write(data)
            f.write("\n")

    @staticmethod
    def write(file_name, tone_banks: List[ToneBanks.ToneBank]):
        with open(file_name, "w") as f:
            f.write(CubasePatchScriptOutput._get_header())
            f.write("\n[define patchnames]\n\n")

            CubasePatchScriptOutput._write_patch_set(f, tone_banks, PatchSet.PatchMode.Tones, 2)
            CubasePatchScriptOutput._write_patch_set(f, tone_banks, PatchSet.PatchMode.Drums, 2)
            CubasePatchScriptOutput._write_patch_set(f, tone_banks, PatchSet.PatchMode.Scenes, 2)


            f.write("[end]\n")
            f.flush()
        pass
