from math import log2
from collections import Counter, deque

from constants import (
    NOTES,
    NOTES_DEQUE_LIMIT,
    NOTE_TO_KEY,
    SAMPLE_RATE,
    SHIFT_SIZE,
)

import numpy as np
import parselmouth
from pynput.keyboard import Controller
from sounddevice import InputStream, sleep as device_sleep


keyboard = Controller()


class NotesCash:
    count = Counter()
    deque = deque(maxlen=NOTES_DEQUE_LIMIT)
    is_pressed = False
    last_key = ''


def frequency_to_note(frequency: float) -> str:
    if frequency <= 0:
        return ''

    midi_index = round(69 + 12 * log2(frequency / 440.0))

    return NOTES[midi_index % 12]


def audio_callback(indata, frames, time, status):
    samples = np.frombuffer(indata, dtype=np.float32)
    sound = parselmouth.Sound(samples)
    pitch = sound.to_pitch(time_step=0.01, pitch_floor=300, pitch_ceiling=1200)
    frequency = pitch.selected_array['frequency']
    note = frequency_to_note(frequency)

    if len(NotesCash.deque) == NOTES_DEQUE_LIMIT:
        old_note = NotesCash.deque.pop()
        NotesCash.count[old_note] -= 1

    NotesCash.deque.appendleft(note)
    NotesCash.count[note] += 1

    if NotesCash.count[note] != NOTES_DEQUE_LIMIT:
        if NotesCash.is_pressed:
            print('...release')
            keyboard.release(NotesCash.last_key)

        NotesCash.is_pressed = False
        return

    if NotesCash.is_pressed or note not in NOTE_TO_KEY:
        return

    NotesCash.is_pressed = True
    key = NOTE_TO_KEY[note]
    print(f"{note = } → pressing '{key}'")
    keyboard.press(key)
    NotesCash.last_key = key


def main():
    with InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=SAMPLE_RATE,
            blocksize=SHIFT_SIZE,
    ):
        device_sleep(-1)


if __name__ == '__main__':
    main()
