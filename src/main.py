import argparse
import sys

from file_io.FileIO import JsonFileReader
from midi import MidiIO
from modules.U110 import U110
from modules.integra7 import Integra7
from file_io.cubase_text import CubasePatchScriptOutput
from file_io.json_file import JsonWriter

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Cubase Patch Script Creator v 1.0")
    parser.add_argument("--user", default=False, action='store_true', help="Fetches USER banks as well")
    parser.add_argument("--no-preset", dest='preset', default=True, action='store_false', help="Turns off PRESET bank fetching.")
    parser.add_argument("--in-file", help="Load data from json file, not MIDI device")
    parser.add_argument("--module", choices=["integra7", "u110"], help="Specifies module to extract patch data from", default="integra7")
    parser.add_argument("--list-midi-drivers", "-l", action="store_true", help="List midi drivers on system")
    parser.add_argument("--midi-in", help="Index of MIDI-IN driver. For valid indexes run --list-midi-devices")
    parser.add_argument("--midi-out", help="Index of MIDI-OUT driver. For valid indexes run --list-midi-devices")
    parser.add_argument("--midi-dev-str", help="A part of the midi driver name for the driver to use")
    args = parser.parse_args()

    if args.list_midi_drivers:
        interfaces = MidiIO.Midi.list_interfaces()
        print("Valid interfaces: \n")
        for i in interfaces:
            dev_id, dev_name, dev_type = i
            print(f'\tID={dev_id}, Name={dev_name}, Type={dev_type}')
        print()
        sys.exit(0)

    match args.module:
        case "u110":
            synth_device = U110(args.midi_dev_str)
            file_name = "U-110"
        case _:
            synth_device = Integra7()
            file_name = "Integra-7"

    if args.in_file:
        f = JsonFileReader(args.in_file)
        tones = f.get_tone_banks(get_user_banks=args.user, get_preset_banks=args.preset)
    else:
        (i_port, o_port) = MidiIO.Midi.get_interfaces(synth_device=synth_device)
        m = MidiIO.Midi.open_ports(i_port, o_port)
        # m.ping()
        tones = m.get_tone_banks(synth_device=synth_device, get_user_banks=args.user, get_preset_banks=args.preset)
        JsonWriter.write(f"{file_name}", tones)

    CubasePatchScriptOutput.write(f"{file_name}.txt", tones)

    print("File written")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
