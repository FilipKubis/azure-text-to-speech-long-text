import functools
import os

import azure.cognitiveservices.speech as speechsdk
import wave

from typing import List

# INPUTS
subscriptionKey = ""  # SPEECH SERVICES SUBSCRIPTION KEY
region = "westeurope"  # CHANGE TO THE REGION OF YOUR SERVICE
synthesis_voice = 'cs-CZ-AntoninNeural'  # SYNTHESYS VOICE

# CHANGE OPTIONALLY
output_type = speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm  # OUTPUT FORMAT


def save_text_into_audio_file(text: str, file_name: str):
    speech_config = speechsdk.SpeechConfig(subscription=subscriptionKey, region=region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    speech_config.speech_synthesis_voice_name = synthesis_voice

    speech_config.set_speech_synthesis_output_format(output_type)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def join_wav_files(input_file_names: List[str], output_file_name: str):
    data = []
    for input_file in input_file_names:
        w = wave.open(input_file, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(output_file_name, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


def accumulate_paragraphs(current_parts: List[str], new_paragraph: str) -> List[str]:
    if len(current_parts) == 0:
        return [new_paragraph]

    if (len(current_parts[-1]) + len(new_paragraph)) > 5000:
        return current_parts + [new_paragraph]

    current_parts[-1] += "\n" + new_paragraph
    return current_parts


def split_into_consumable_parts(text: str) -> List[str]:
    return functools.reduce(accumulate_paragraphs, text.split("\n"), [])


def read_text_file(file_name: str) -> str:
    with open(file_name, 'r') as f:
        text_from_file = f.read()

    return text_from_file


def save_texts_into_audio_files(text_parts) -> List[str]:
    file_names = []

    for index, part in enumerate(text_parts):
        file_name = f'part_{index + 1}.wav'
        file_names.append(file_name)
        save_text_into_audio_file(part, file_name)

    return file_names


def delete_parts(file_names: List[str]):
    for file_name in file_names:
        os.remove(file_name)


def main():
    text = read_text_file('./files/input.txt')

    text_parts = split_into_consumable_parts(text)

    audio_files = save_texts_into_audio_files(text_parts)

    os.makedirs("./output", exist_ok=True)  # creates output directory if it not exists

    join_wav_files(audio_files, "./output/audio.wav")

    delete_parts(audio_files)


if __name__ == '__main__':
    main()
