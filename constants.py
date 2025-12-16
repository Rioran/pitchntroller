NOTES = (
    "C", "C#",
    "D", "D#",
    "E", "F", "F#",
    "G", "G#",
    "A", "A#", "B"
)

NOTE_TO_KEY = {
    "G": "e",
    "A": "s",
    "B": "a",
    "C": "d",
    'C#': ' ',
    "D": "w",
}

SAMPLE_RATE = 44100
SAMPLES_SIZE = 1024
SHIFT_SIZE = SAMPLES_SIZE // 2
NOTES_DEQUE_LIMIT = 4
