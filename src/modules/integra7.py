from enum import StrEnum
from typing import Optional

from modules.Patch import PatchSet, Patch
from modules.ToneBanks import ToneBank, calc_by_index
from modules.device import SynthDevice


class ValidToneBanks(StrEnum):
    PCMToneBank = "PCM Tone Bank"
    StudioSet = "Studio Sets"
    GM2ToneBank = "GM2 Tone Bank"
    SuperNaturalToneBank = "SuperNatural Tone Bank"
    SuperNaturalExpansionBank = "SuperNatural Expansion Bank"
    SRXExpansionBank = "SRX Expansion Bank"
    PCMExpansionBank = "PCM Expansion Bank"


_integra_base_address = b'0F000402'


class PCMToneBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.PCMToneBank,
                         [
                             PatchSet("User Tones", PatchSet.SetType.User, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'570000', 256, Integra7.calc_id_shl7),
                             PatchSet("User Drum Kits", PatchSet.SetType.User, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'560000', 32),
                             PatchSet("Preset Tones", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'574000', 896, Integra7.calc_user_tone_id),
                             PatchSet("Preset Drum Kits", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'564000', 14)
                         ])


class StudioSet(ToneBank):
    def __init__(self):
        super().__init__(ValidToneBanks.StudioSet,
                         [
                             PatchSet("Studio Set", PatchSet.SetType.Preset, PatchSet.PatchMode.Scenes, b'0F000302',
                                      b'550000', 64, calc_by_index),
                         ])


class GM2ToneBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.GM2ToneBank,
                         [
                             PatchSet("Drum Kits", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'780000', 9, calc_by_index),
                             PatchSet("Preset Tones", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'790000', 256, calc_by_index),
                         ])


class SuperNaturalToneBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.SuperNaturalToneBank,
                         [
                             PatchSet("Acoustic User Tones", PatchSet.SetType.User, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'590000', 254, Integra7.calc_id_shl7),
                             PatchSet("User Drum Kits", PatchSet.SetType.User, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'580000', 64),
                             PatchSet("Acoustic Preset Tones", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'594000', 256, Integra7.calc_sn_preset_tones),
                             PatchSet("Preset Drum Kits", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'584000', 26),
                             PatchSet("Synth Preset Tones", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5F4000', 1109, Integra7.calc_user_tone_id),
                             PatchSet("Synth User Tones", PatchSet.SetType.User, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5F0000', 512, Integra7.calc_id_shl7),
                         ])


class SuperNaturalExpansionBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.SuperNaturalExpansionBank,
                         [
                             PatchSet("Ethnic", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'596000', 0x11),
                             PatchSet("WoodWinds", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'596100', 0x11),
                             PatchSet("Session", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'596200', 0x32),
                             PatchSet("Acoustic Guitar", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'596300', 0x0C),
                             PatchSet("Brass", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'596400', 0x0C),
                             PatchSet("SFX", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums, _integra_base_address,
                                      b'586500', 0x07),
                         ])


class SRXExpansionBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.SRXExpansionBank,
                         [
                             PatchSet("SRX-01 Dynamic Drum Kits", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0000', 79, calc_by_index),
                             PatchSet("SRX-03 Studio SRX Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0200', 12, calc_by_index),
                             PatchSet("SRX-05 Supreme Dance Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0400', 34, calc_by_index),
                             PatchSet("SRX-06 Orchestra Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0700', 5, calc_by_index),
                             PatchSet("SRX-07 Ultimate Keys Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0B00', 11, calc_by_index),
                             PatchSet("SRX-08 Platinum Trax Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C0F00', 21, calc_by_index),
                             PatchSet("SRX-09 Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'5C1300', 12, calc_by_index),

                             PatchSet("SRX-01: Drums", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0000', 41, calc_by_index),
                             PatchSet("SRX-02: Concert Piano", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0100', 50, calc_by_index),
                             PatchSet("SRX-03: Studio SRX", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0200', 128, calc_by_index),
                             PatchSet("SRX-04: Symphonique Strings", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0300', 128, calc_by_index),
                             PatchSet("SRX-05: Supreme Dance", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0400', 312, calc_by_index),
                             PatchSet("SRX-06: Complete Orchestra", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0700', 449, calc_by_index),
                             PatchSet("SRX-07: Ultimate Keys", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0B00', 475, calc_by_index),
                             PatchSet("SRX-08: Platinum Trax", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D0F00', 448, calc_by_index),
                             PatchSet("SRX-09: World Collection", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D1300', 414, calc_by_index),
                             PatchSet("SRX-10: Big Brass Ensamble", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D1700', 100, calc_by_index),
                             PatchSet("SRX-11: Complete Piano", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D1800', 42, calc_by_index),
                             PatchSet("SRX-12: Classic EPs", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'5D1A00', 50, calc_by_index),
                         ])


class PCMExpansionBank(ToneBank):

    def __init__(self):
        super().__init__(ValidToneBanks.PCMExpansionBank,
                         [
                             PatchSet("PCM Kit", PatchSet.SetType.Preset, PatchSet.PatchMode.Drums,
                                      _integra_base_address, b'600000', 19),
                             PatchSet("PCM Tone", PatchSet.SetType.Preset, PatchSet.PatchMode.Tones,
                                      _integra_base_address, b'610000', 512, calc_by_index),
                         ])


class Integra7(SynthDevice):

    @staticmethod
    def calc_id_shl7(data: bytes, index) -> int:
        return (int(data[2:4], 16) << 7) + int(data[4:6], 16) + 1

    @staticmethod
    def calc_sn_preset_tones(data: bytes, index) -> int:
        return ((int(data[2:4], 16) - 64) << 7) + int(data[4:6], 16) + 1

    @staticmethod
    def calc_user_tone_id(data: bytes, index) -> int:
        return ((int(data[2:4], 16) - 64) * 128) + int(data[4:6], 16) + 1

    def __init__(self, midi_driver: str = "INTEGRA"):
        super().__init__(midi_driver, [
            SuperNaturalToneBank(),
            PCMToneBank(),
            GM2ToneBank(),
            SuperNaturalExpansionBank(),
            SRXExpansionBank(),
            PCMExpansionBank(),
            StudioSet(),
        ])

    def create_patch(self, patch_data: bytes, patch_id: int) -> Optional[Patch]:
        if patch_data[0:2] != b'00':
            return Patch(patch_data, patch_id)
        return None

