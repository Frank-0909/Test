# 感谢Linky小伙伴对于Windows版本运行说明以及代码的贡献!
from aip import AipSpeech
from playsound import playsound # windows环境下playsound运行可能不稳定
# pip install pygame
import pygame # 导入pygame，playsound报错或运行不稳定时直接使用
import asyncio
# pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import pyttsx3
from edge_tts import Communicate
from speech2text import BaiduASR
import wave
#
# def add_wav_header(raw_audio_data):
#     # 假设你已经有了裸音频数据raw_audio_data，以及以下参数
#     sample_rate = 16000  # 采样率
#     channels = 1  # 通道数（单声道为1，双声道为2）
#     bits_per_sample = 16#16  # 位深度
#
#     # 计算音频帧的数量和总字节数
#     nframes = len(raw_audio_data) // (channels * (bits_per_sample // 8))
#     nbytes = len(raw_audio_data)
#
#     # 创建WAV文件对象
#     with wave.open('output_with_header.wav', 'wb') as wav_file:
#         # 设置WAV文件参数
#         wav_file.setnchannels(channels)
#         wav_file.setsampwidth(bits_per_sample // 8)
#         wav_file.setframerate(sample_rate)
#         wav_file.setnframes(nframes)
#         wav_file.setcomptype("NONE","not compressed")
#         # wav_file.setcompname("not compressed")
#
#         # 写入WAV文件头
#         wav_file.writeframes(b"")
#
#         # 写入音频数据
#         wav_file.writeframes(raw_audio_data[:])
def mono_to_stereo(input_filename, output_filename):
    # 打开输入文件
    with wave.open(input_filename, 'rb') as input_file:
        # 获取WAV文件的参数
        nchannels, sampwidth, framerate, nframes, comptype, compname = input_file.getparams()

        # 读取数据
        frames = input_file.readframes(nframes)

        # 创建输出文件，将单声道转换为双声道
    with wave.open(output_filename, 'wb') as output_file:
        # 设置新的参数，将声道数改为2（双声道）
        output_file.setparams((2, sampwidth, framerate, nframes, comptype, compname))

        # 将单声道数据复制到左右两个声道
        stereo_frames = b''.join([frames[i:i + sampwidth] * 2 for i in range(0, len(frames), sampwidth)])

        # 写入数据到输出文件
        output_file.writeframes(stereo_frames)

class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per': 3#4  # 发声人 百度丫丫
        })  # 得到音频的二进制文件

        if not isinstance(result, dict):
            with open("./audio.mp3", "wb") as f:
                f.write(result)
        else:
            print("语音合成失败", result)
        # playsound('./audio.mp3')  # playsound无法运行时删去此行改用pygame，若正常运行择一即可
        self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式

    def text_to_wav(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,  # 语速
            'vol': 5,  # 音量大小
            'per': 4,  # 发声人 百度丫丫
            'aue': 6 # 3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）; 注意aue=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
        })  # 得到音频的二进制文件
        # add_wav_header(result)
        if not isinstance(result, dict):
            with open("./audio.wav", "wb") as f:
                f.write(result)

            mono_to_stereo("./audio.wav","./audio.wav")
            return "./audio.wav"
        else:
            print("语音合成失败", result)
            return None



    def play_audio_with_pygame(self, audio_file_path):
        # 代码来自Linky的贡献
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()


class Pyttsx3TTS:
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text=""):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


class AzureTTS:
    def __init__(self, AZURE_API_KEY, AZURE_REGION):
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        # The language of the voice that speaks.
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoyiNeural"
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config,
                                                              audio_config=self.audio_config)

    def text_to_speech_and_play(self, text):
        # Get text from the console and synthesize to the default speaker.
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled:{}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details :{}".format(cancellation_details.error_details))
                    print("Didy you set the speech resource key and region values?")


class EdgeTTS:
    def __init__(self, voice: str = "zh-CN-XiaoyiNeural", rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def text_to_speech_and_play(self, text):
        # voices = await VoicesManager.create()
        # voice = voices.find(Gender="Female", Language="zh")
        # communicate = edge_tts.Communicate(text, random.choice(voice)["Name"])
        communicate = Communicate(text, self.voice)
        await communicate.save('./audio.mp3')
        # playsound('./audio.wav') # playsound无法运行时删去此行改用pygame，若正常运行择一即可
        self.play_audio_with_pygame('audio.mp3')  # 注意pygame只能识别mp3格式


    def play_audio_with_pygame(self, audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()




if __name__ == '__main__':
    APP_ID = '54570578'
    API_KEY = 'RSh0wcMlzfWR1VnyHfcD1Qwk'
    SECRET_KEY = 'NdxrD750KS2YttSWYn1OO9zhmzKfOOZv'
    # baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    # baidutts.text_to_speech_and_play('Hey Yuki, 春天来了，每天的天气都很好！')

    # baiduasr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)
    # result = baiduasr.speech_to_text()
    # baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    # baidutts.text_to_speech_and_play(result)

    result = '今天星期二!'
    baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    baidutts.text_to_wav(result)

    # mono_to_stereo('audio.wav','audio.wav')
    #
    # pyttsx3tts = Pyttsx3TTS()
    # pyttsx3tts.text_to_speech_and_play('春天来了，每天的天气都很好！')
    #
    # AZURE_API_KEY = ""
    # AZURE_REGION = ""
    # azuretts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    # azuretts.text_to_speech_and_play("嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！")

    # edgetts = EdgeTTS()
    # asyncio.run(edgetts.text_to_speech_and_play(
    #     "嗯，你好，我是你的智能小伙伴，我的名字叫Murphy，你可以和我畅所欲言，我是很会聊天的哦！"))
