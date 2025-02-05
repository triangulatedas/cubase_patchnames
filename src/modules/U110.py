from modules.device import SynthDevice


class U110(SynthDevice):

    def __init__(self, midi_driver: str = None):
        super().__init__(midi_driver, [])


