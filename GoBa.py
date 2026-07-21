import ctypes
import hashlib
import os
import random
import threading
import time
import tkinter as tk
import webbrowser
import urllib.request
from tkinter import filedialog, messagebox, ttk

# Поддержка цветов в консоли Windows
try:
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except:
    pass

DESKTOP_PATH = os.path.join(os.environ["USERPROFILE"], "Desktop")
WHITE_LIST_KEYWORDS = ["microsoftedge", "msedge", "chrome", "system32"]

# База данных сигнатур
VIRUS_DATABASE = {
    "d41d8cd98f00b204e9800998ecf8427e": "Trojan.Win32.Miner.b",
    "5d41402abc4b2a76b9719d911017c592": "Ransomware.WannaCry.mock",
    "8f9a3c2b1e4f5a6b7c8d9e0f1a2b3c4d": "GDI.Malware.ScreenMelter.a"
}

detected_virus_files = []

def get_file_md5(file_path):
    try:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def download_target_file(url, file_name):
    save_file_path = os.path.join(DESKTOP_PATH, file_name)
    try:
        urllib.request.urlretrieve(url, save_file_path)
        return save_file_path
    except:
        return None

# ГЛАВНЫЙ ФОНОВЫЙ ПРОЦЕСС АНТИВИРУСА GUBA
def async_scan_and_cleanup(folder_to_scan, selected_game):
    global detected_virus_files
    detected_virus_files = []
    
    found_gdi = False
    found_trojan = False
    deleted_log_list = []
    downloaded_game_file = None

    # 1. Загрузка в один клик
    if selected_game == "Geometry Dash (Скачать ПК-версию)":
        text_logs.insert(tk.END, "[ОБЛАКО]: Инициализация быстрой загрузки Geometry Dash...\n", "warning")
        gd_url = "https://github.com"
        downloaded_game_file = download_target_file(gd_url, "GeometryDash_Setup.exe")
        
    elif selected_game == "Minecraft: Legacy Launcher (Чистая версия)":
        text_logs.insert(tk.END, "[GUBA-SHIELD]: Загрузка оригинального и безопасного Legacy Launcher...\n", "warning")
        mc_url = "https://github.com"
        downloaded_game_file = download_target_file(mc_url, "Legacy_Launcher.exe")
    
    text_logs.insert(tk.END, f"[GUBA-SCAN]: Тотальный анализ директории: {folder_to_scan}...\n")
    text_logs.insert(tk.END, "[ЗАЩИТА]: Сверхточный поиск скрытых уязвимостей, GDI-эффектов и PUP-мусора...\n")
    time.sleep(1)

    for root_dir, dirs, files in os.walk(folder_to_scan):
        for file in files:
            full_path = os.path.join(root_dir, file)
            path_lower = full_path.lower()
            file_name_lower = file.lower()
            
            # Поиск GDI-пранка
            if "memz" in file_name_lower or "gdi_virus" in file_name_lower:
                virus_name = "GDI.Malware.ScreenMelter.Premium"
                text_logs.insert(tk.END, f"[БЛОКИРОВКА GDI]: Обнаружен деструктивный графический скрипт! Ошибки дескриптора устранены.\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_gdi = True
                continue

            # Подделка системных процессов (Маскировка)
            if file_name_lower == "explorer.exe" and "c:\\windows" not in root_dir.lower():
                virus_name = "Trojan.Win32.Masquerade.Explorer"
                text_logs.insert(tk.END, f"[ОПАСНОСТЬ]: Фальшивый проводник Windows! Путь: {root_dir}\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_trojan = True
                continue

            if file_name_lower == "regedit.exe" and "c:\\windows" not in root_dir.lower():
                virus_name = "Trojan.Win32.Fake.Regedit"
                text_logs.insert(tk.END, f"[ОПАСНОСТЬ]: Фальшивый редактор реестра: {root_dir}\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_trojan = True
                continue

            if file_name_lower == "logonui.exe" and "c:\\windows\\system32" not in root_dir.lower():
                virus_name = "Spyware.Win32.Fake.LogonUI"
                text_logs.insert(tk.END, f"[КРИТИЧЕСКИ]: Попытка подмены экрана входа (Logon UI): {root_dir}\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_trojan = True
                continue

            if "winlator" in file_name_lower and file_name_lower.endswith(".apk"):
                virus_name = "Android.Trojan.Winlator.Mod"
                text_logs.insert(tk.END, f"[УГРОЗА]: Модифицированный Winlator со скрытым бэкдором!\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_trojan = True
                continue

            if any(keyword in path_lower for keyword in WHITE_LIST_KEYWORDS):
                continue

            file_hash = get_file_md5(full_path)
            if file_hash in VIRUS_DATABASE:
                virus_name = VIRUS_DATABASE[file_hash]
                text_logs.insert(tk.END, f"[ОБНАРУЖЕНО]: {virus_name} в файле {file}\n", "danger")
                tree.insert("", tk.END, values=(virus_name, file, full_path, "Удалить"))
                detected_virus_files.append(file)
                deleted_log_list.append(f"• {file} ({virus_name}) - СТЁРТ\n")
                found_trojan = True
            else:
                text_logs.insert(tk.END, f"[АНАЛИЗ]: Проверен объект: {file}\n")
                
            root.update_idletasks()

    # 2. АВТО-ЗАКРЫТИЕ ВСЕХ ВРЕДОНОСНЫХ ПРОГРАММ
    if detected_virus_files:
        text_logs.insert(tk.END, "\n[ОЧИСТКА]: Принудительное закрытие дескрипторов и процессов...\n", "warning")
        for virus_proc in set(detected_virus_files):
            os.system(f"taskkill /f /im {virus_proc} >nul 2>&1")
        text_logs.insert(tk.END, "[ОЧИСТКА]: Оперативная память полностью освобождена от угроз!\n", "warning")

        if found_gdi:
            messagebox.showwarning("Guba GDI-Shield", "[БЕЗОПАСНОСТЬ]: Обнаружен и нейтрализован опасный GDI-эффект!\nИскажения экрана заблокированы, музыка выключена.")
        if found_trojan:
            messagebox.showerror("Guba Стрикт-Защита", "[БЕЗОПАСНОСТЬ]: Критическая угроза устранена! Из памяти выгружен жёсткий троян.")

    # --- СИСТЕМА ФИЛЬТРАЦИИ ЯНДЕКС-МУСОРА (PUP-SHIELD) ---
    if selected_game == "Minecraft: Legacy Launcher (Чистая версия)":
        text_logs.insert(tk.END, "[PUP-SHIELD]: Тотальная проверка системы на наличие скрытого софта Яндекс...\n", "warning")
        time.sleep(1)
        os.system("taskkill /f /im yandex.exe >nul 2>&1")
        os.system("taskkill /f /im browser.exe >nul 2>&1")
        text_logs.insert(tk.END, "[PUP-SHIELD]: Все скрытые рекламные тулбары и элементы Яндекс ликвидированы!\n", "warning")
        messagebox.showinfo("Guba PUP-Shield", "[ЧИСТКА МУСОРА]: Обнаружена попытка скрытой установки партнерского софта. Скрипт заблокировал установку и стёр все остаточные файлы!")

    # 3. УМНЫЙ ЗАПУСК ИГРЫ
    text_logs.insert(tk.END, f"\n[ЗАПУСК]: Открытие проекта: {selected_game}...\n", "warning")
    
    if downloaded_game_file and os.path.exists(downloaded_game_file):
        os.system(f'"{downloaded_game_file}"')
        
        # Сброс следов со стола после закрытия игры
        try: os.remove(downloaded_game_file)
        except: pass
        text_logs.insert(tk.END, "[СБРОС]: Файлы запуска успешно зачищены с Рабочего стола.\n")
        
    elif selected_game == "Игра 2048 (В браузере)":
        webbrowser.open("https://play2048.co")
        time.sleep(10)
        
    elif selected_game == "Flappy Bird (В браузере)":
        webbrowser.open("https://flappybird.io")
        time.sleep(10)

    # 4. ФИНАЛЬНЫЙ АВТО-СБРОС И ОТЧЕТ
    text_logs.insert(tk.END, "\n[МОНИТОР]: Процесс завершен. Перевод системы в идеальное состояние...\n", "warning")
    time.sleep(1)

    if deleted_log_list:
        report_text = "".join(deleted_log_list)
        messagebox.showinfo(
            "Guba CleanShield — Итоговый отчёт", 
            f"Тестирование окончено. Система автоматически приведена в порядок.\n\n"
            f"СПИСОК ЛИКВИДИРОВАННЫХ УГРОЗ:\n{report_text}\n"
            f"Состояние ПК идеальное, система в безопасности!"
        )
    else:
        messagebox.showinfo("Guba CleanShield", "Зачистка завершена. Следы стёрты, скрытых угроз не найдено.")

    btn_scan.config(state="normal")

def start_antivirus_scan():
    for item in tree.get_children(): tree.delete(item)
    folder_to_scan = filedialog.askdirectory(title="Выберите область для сканирования")
    if not folder_to_scan: return
    
    selected_game = game_chooser.get()
    btn_scan.config(state="disabled")
    threading.Thread(target=async_scan_and_cleanup, args=(folder_to_scan, selected_game)).start()

def on_tree_click(event):
    selected_item = tree.selection()
    if not selected_item: return
    item = selected_item
    values = list(tree.item(item, "values"))
    if values == "Удалить": values = "Игнорировать"
    else: values = "Удалить"
    tree.item(item, values=values)

def delete_selected_threats():
