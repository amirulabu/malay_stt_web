import malaya_speech
import os
import logging

import torchaudio

os.environ["CUDA_VISIBLE_DEVICES"] = ""
logging.basicConfig(level=logging.INFO)


medium_whisper = malaya_speech.stt.transducer.pt_transformer(
    model="mesolitica/conformer-medium-malay-whisper"
)


def speech_to_text(audio_path):
    audio, sr = torchaudio.load(audio_path)
    y = malaya_speech.load(audio)
    print(y.count)
    result_arr = medium_whisper.beam_decoder([y])
    return result_arr[0]
