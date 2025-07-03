import subprocess
import time
import random

# 你的设备 ID（使用 adb devices 查看）
DEVICE_ID = "127.0.0.1:5555"

# 输入框和发送按钮坐标
INPUT_COORDS = (133, 1805)
SEND_COORDS = (1000, 1770)

# 消息文件路径
MESSAGE_FILE = "messages.txt"

def adb_shell(cmd):
    return subprocess.run(["adb", "-s", DEVICE_ID, "shell"] + cmd, capture_output=True, text=True)

def adb_tap(x, y):
    adb_shell(["input", "tap", str(x), str(y)])

def set_clipboard(text):
    subprocess.run(["adb", "-s", DEVICE_ID, "shell", "am", "broadcast",
                    "-a", "clipper.set", "-e", "text", text],
                   capture_output=True, text=True)

def send_message(msg):
    print(f"📋 准备发送: {msg}")
    set_clipboard(msg)
    time.sleep(1)
    adb_tap(*INPUT_COORDS)
    time.sleep(0.5)
    adb_shell(["input", "keyevent", "KEYCODE_PASTE"])
    time.sleep(0.5)
    adb_tap(*SEND_COORDS)
    print("✅ 已发送")

def read_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    messages = read_messages(MESSAGE_FILE)
    while True:
        print("🚀 开始新一轮发送...")
        for msg in messages:
            send_message(msg)
            sleep_time = random.randint(260, 360)  # 每条消息间隔10~12分钟
            print(f"⏳ 等待 {sleep_time} 秒后继续...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()
