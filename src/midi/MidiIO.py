import time
from time import sleep
from typing import List, Optional

from rtmidi import MidiIn, MidiOut, API_UNSPECIFIED
import binascii

from modules import ToneBanks
from modules.Patch import PatchSet
from modules.device import SynthDevice
from util.progress import text_bar


class SysEx:
    _SYSEX_START: bytes = b'F0'
    _SYSEX_END: bytes = b'F7'
    _MANUFACTURER_ID: bytes = b'41'

    def __init__(self, device_info: bytes):
        if not device_info:
            raise ValueError("device_info is empty")

        self._device_id = binascii.unhexlify(device_info)[2]
        pass

    @staticmethod
    def _calculate_checksum(data) -> bytes:
        return b'7F'

    @staticmethod
    def get_device_info_request() -> [int]:
        return [0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]

    def get_test_data(self) -> [int]:
        return [0xF0,

                0xF7]

    def _sysex_header(self) -> bytes:
        return b''.join([self._SYSEX_START,
                         self._MANUFACTURER_ID,  # Hardcoded for Roland
                         b'10',  # Request Data command
                         b'000064',  # 000064 - Hardcoded model for Integra 7
                         b'11'  # SysEx Send
                         ])

    def _sysex_footer(self, checksum_data: bytes):
        return b''.join([self._calculate_checksum(checksum_data),
                         b'F7'  # SysEx end
                         ])

    def get_data_request(self, address: bytes, request: bytes, items_returned: int) -> [int]:
        request_data: List[bytes] = [self._sysex_header()]

        if len(address) != 8:
            raise ValueError("base_address must be 4 bytes long")
        request_data.append(address)

        if len(request) != 6:
            raise ValueError("offset_address must be 3 bytes long")
        request_data.append(request)

        if items_returned > 0xFF:
            raise ValueError("Maximum 256 items are allowed per request")

        request_data.append(f'{items_returned:02X}'.encode())

        request_data.append(self._sysex_footer(address + request))

        return [b for b in binascii.unhexlify(b''.join(request_data))]

    def extract_patch_data(self, data: bytes) -> bytes:
        if not isinstance(data, bytes) or len(data) < 68 or data[0:2] != self._SYSEX_START:
            raise TypeError("Received data is not in correct format")

        return data[22:64]


class Midi:
    _in_device: MidiIn = None
    _out_device: MidiOut = None
    _sysex: SysEx = None

    def __init__(self, in_port: int, out_port: int):
        self._in_device = MidiIn(rtapi=API_UNSPECIFIED, name="Synth Patch Extractor", queue_size_limit=1024)
        self._in_device.open_port(in_port)
        # self._in_device.set_callback(self._midi_in_received, None)
        self._in_device.ignore_types(sysex=False)

        self._out_device = MidiOut(rtapi=API_UNSPECIFIED, name="Synth Patch Extractor")
        self._out_device.open_port(out_port)

        self._out_device.send_message(SysEx.get_device_info_request())
        data = self._recv_data(timeout=5.0)
        self._sysex = SysEx(data[0])
        pass

    def __del__(self):
        if self._in_device:
            self._in_device.close_port()
        if self._out_device:
            self._out_device.close_port()

    @staticmethod
    def _bytes_to_int_array(data: bytes) -> [int]:
        retval = []
        if len(bytes) % 2 != 0:
            raise ValueError("Input data must be even!")

        return [b for b in data]

    def _recv_data(self, timeout: float = 1.0) -> Optional[List[bytes]]:
        data: List[bytes] = []
        event = None

        start = time.time()
        # Wait for data
        while not event and (time.time() - start < timeout):
            event = self._in_device.get_message()
            sleep(0.02)

        # Dump data
        while event:
            msg, delta = event
            data.append(bytearray(msg).hex().encode().upper())
            sleep(0.01)
            event = self._in_device.get_message()

        return data if len(data) > 0 else None

    def ping(self):
        note_on = [0x90, 60, 112]  # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        self._out_device.send_message(note_on)
        sleep(0.5)
        self._out_device.send_message(note_off)
        sleep(0.1)

    def _fill_patch_set(self, synth_device: SynthDevice, value: PatchSet):
        base_address, base_request = value.get_request()
        _values_per_request = min(value.get_num_patches_requested(), 0x40)
        _running = True
        patch = None
        while _running:
            self._out_device.send_message(
                self._sysex.get_data_request(address=base_address, request=base_request,
                                             items_returned=_values_per_request)
            )

            response = self._recv_data()
            if not response or (len(response) == 1 and response[-1][22:24] == b'00') or (
                    len(response) == 2 and patch and response[-1][22:24] == b'00'):
                _running = False
            else:
                for r in response:
                    try:
                        if r[22:24] != b'00':
                            patch_data = self._sysex.extract_patch_data(r)
                            patch_id = value.get_next_id(patch_data)
                            patch = synth_device.create_patch(patch_data, patch_id)
                            if value.add_patch(patch):
                                text_bar.update_progress()
                                base_request = patch.get_patch_address()
                    except:
                        pass

        pass

    def get_tone_banks(self, synth_device: SynthDevice, get_user_banks: bool, get_preset_banks: bool) -> List[
        ToneBanks]:
        num_patches = 0

        banks = synth_device.get_tone_banks(get_user_banks=get_user_banks, get_preset_banks=get_preset_banks)
        # Calculate num patches to fetch...
        for tb in banks:
            num_patches += tb.get_num_patches_requested()

        text_bar.set_items(num_patches)

        print(f'Fetching: {num_patches} patches ...')
        for tb in banks:
            for ps in tb.get_all_patch_sets():
                self._fill_patch_set(synth_device, ps)

        return synth_device.get_all_banks()

    @staticmethod
    def list_interfaces() -> (int, str, str):
        results = []
        m_in = MidiIn(rtapi=API_UNSPECIFIED, name="Patch Extractor", queue_size_limit=1024)
        for in_ix in range(0, m_in.get_port_count()):
            results.append((in_ix, m_in.get_port_name(in_ix), "IN"))

        m_out = MidiOut(rtapi=API_UNSPECIFIED)
        for ix in range(0, m_out.get_port_count()):
            results.append((ix, m_out.get_port_name(ix), "OUT"))

        return results

    @staticmethod
    def get_interfaces(synth_device: SynthDevice) -> (int, int):
        # Lists the INTEGRA interface names.
        # NOTE: The interfaces must have "INTEGRA" in their name
        # Returns: in_device, out_device
        m_in = MidiIn(rtapi=API_UNSPECIFIED, name="Patch Extractor", queue_size_limit=1024)
        m_in_id = -1
        for in_ix in range(0, m_in.get_port_count()):
            if m_in.get_port_name(in_ix).find(synth_device.get_midi_driver_str()) >= 0:
                m_in_id = in_ix
                break

        m_out = MidiOut(rtapi=API_UNSPECIFIED)
        m_out_id = -1
        for ix in range(0, m_out.get_port_count()):
            if m_out.get_port_name(ix).find(synth_device.get_midi_driver_str()) >= 0:
                m_out_id = ix
                break

        return m_in_id, m_out_id

    @staticmethod
    def open_ports(in_port: int, out_port: int) -> "Midi":
        return Midi(in_port, out_port)
