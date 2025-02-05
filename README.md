# Patch Extractor

This tool extracts patches from, currently, only the Roland Integra-7.
It can extract Preset and/or USER data, but default it only extracts Preset (configurable).

The Integra-7 cannot have more than 4 extensions active at a time, this means that you need to re-run the extract
tool for each new set of 4 extensions loaded. The patch info cannot be fetched unless an extension is loaded.

The tool creates a json file that always add missing patches to it, and the ourput file can be generated
based on this json instead of the actual sysex data from the hardware module.

## Run extractor

You need to have the python-rtmidi package installed

```
pip install python-rtmidi
```

The go to the project root and run:

    python src/main.py -h

This command will list the allowed options and parameters.

To extract presets from Integra-7 (included any loaded extensions):

    python src/main.py

This will automatically connect to Midi IN and OUT ports with the name "INTEGRA", then run the extraction tool.

Two files will be saved: "integra-7.txt" and "integra-7.json".

The "integra-7.txt" is the Cubase Patchname Script, and it should be copied to:

    %LocalApp%\Steinberg\CubaseXX\Scripts\Patchname

XX is you Cubase version.


The json file is just an internal cache file for the extractor. New patches are automatically added, so you can use it as a
patch source after loading all extensions.


