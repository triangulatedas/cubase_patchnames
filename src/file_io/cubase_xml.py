from typing import List

from modules import ToneBanks
from file_io.file import FileOutputWriter


class CubaseXMLWriter(FileOutputWriter):

    @staticmethod
    def write(file_name, tone_banks: List[ToneBanks.ToneBank]):
        pass
