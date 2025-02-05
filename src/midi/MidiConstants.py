from enum import Enum

CC_SEL = "80"
CC_BS_MSB = "00"
CC_BS_LSB = "20"
CC_PC = "C0"


class Category(Enum):
    Unassigned = 0
    Acoustic_Piano = 1
    Electric_Piano = 2
    Organ = 3
    Other_Keys = 4
    Accordion_Harmonica = 5
    Bell_Mallet = 6
    Acoustic_Guitar = 7
    Electric_Guitar = 8
    Distortion_Guitar = 9
    Acoustic_Bass = 10
    Electric_Bass = 11
    Synth_Bass = 12
    Plucked_Stroke = 13
    Strings = 14
    Brass = 15
    Wind = 16
    Flute = 17
    Sax = 18
    Recorder = 19
    Vox_Choir = 20
    Synth_Lead = 21
    Synth_Brass = 22
    Synth_Pad_Strings = 23
    Synth_Bell_Pad = 24
    Synth_Poly_Key = 25
    FX = 26
    Synth_Seq_Pop = 27
    Phrase = 28
    Pulsating = 29
    Beat_Groove = 30
    Hit = 31
    Sound_FX = 32
    Drums = 33
    Percussion = 34
    Combination = 35
