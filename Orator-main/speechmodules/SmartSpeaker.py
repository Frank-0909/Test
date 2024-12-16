import socket
import threading
from time import sleep

from speech2text import BaiduASR
from text2speech import BaiduTTS
from pydub import AudioSegment
from BaiduChat import BaiduLLM

AudioOutputIP = '192.168.1.30'#'192.168.92.1'
AudioOutputPort = 8088

AudioInputPort = 8089

APP_ID = '54570578'
API_KEY = 'RSh0wcMlzfWR1VnyHfcD1Qwk'
SECRET_KEY = 'NdxrD750KS2YttSWYn1OO9zhmzKfOOZv'

file_audioraw = "./audioraw.wav"    #原始语音
file_audiosyn = "./audio.wav"   #合成的语音

def getllmreply(text):
    llmmodel = BaiduLLM()
    reply = llmmodel.chat_with_baidu_llm(input_text = text)
    return reply

def text2audio(text):
    baidutts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    wav = baidutts.text_to_wav(text)
    return wav


def audio2text(path):
    # 加载双声道WAV音频文件
    sound = AudioSegment.from_wav(path)
    # 转换为单声道，这里我们选择第一个声道（左声道）
    mono_sound = sound.set_channels(1)
    # 保存为新的单声道WAV文件
    mono_sound.export("output_mono.wav", format="wav")

    baiduasr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)
    result = baiduasr.speech_to_text(audio_path = 'output_mono.wav', if_microphone=False)
    print(result)
    return result

def audio_output(client_socket, audiofile):
    # 接收数据
    print('audio_output is running !!!')
    f = open(audiofile, 'rb')
    while True:
        data = f.read(1024)
        if len(data) > 0:
            client_socket.send(data)
        else:
            break
    while True:
        sleep(0.1)
        print('sleep....')
        break
    client_socket.close()
    print('audio_output exit !!!')

def audio_input(client_socket, audiofile):
    """线程函数，处理单个客户端的连接"""
    # 接收客户端发送的信息
    print('audio_input is running !!!')
    f = open(audiofile, "wb")
    while True:
        received_data = client_socket.recv(1024)
        if  len(received_data) == 0:
            break
        else:
            f.write(received_data)
    # 关闭客户端连接
    client_socket.close()
    print('audio_input exit !!!')



def main():
    ###################创建server socket####################
    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket = socket.socket()
    # 允许重用端口
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 绑定到本地端口
    # server_socket.bind(('0.0.0.0', AudioInputPort))
    server_socket.bind(("192.168.1.10", AudioInputPort))
    # 监听连接请求
    server_socket.listen(5)
    print("Server is running on port 8089...")
    ###################创建server socket####################


    while True:
        # 服务器线程，接受客户端连接
        client_socket, addr = server_socket.accept()
        # 创建新线程来处理客户端连接
        client_thread = threading.Thread(target=audio_input, args=(client_socket,file_audioraw,))
        client_thread.start()
        # 主线程可以继续执行其他任务，或者等待
        client_thread.join()

        text = audio2text(file_audioraw)
        text = getllmreply(text)
        file_audiosyn = text2audio(text)

        ###################创建client socket####################
        # 创建TCP/IP socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        server_address = (AudioOutputIP, AudioOutputPort)
        ###################创建client socket####################

        # 客户端线程，将合成语音发送出去
        client_sock.connect(server_address)
        # 创建并启动一个线程来处理客户端连接
        client_thread = threading.Thread(target=audio_output, args=(client_sock,file_audiosyn,))
        client_thread.start()
        # 主线程可以继续执行其他任务，或者等待
        client_thread.join()

        # break

    # 关闭服务器套接字
    server_socket.close()
    print('关闭服务器套接字')

    client_sock.close()
    print('关闭客户端套接字')



if __name__ == "__main__":
    main()