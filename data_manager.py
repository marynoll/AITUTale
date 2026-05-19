# data_manager.py
import json
import os

SAVE_FILE = "save.json"

def load_game_data():
    """Загружает данные из JSON. Если файла нет, создает базовые."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            pass # Если файл сломан, создадим новый
            
    # Базовые данные, если сохранений еще нет
    return {
        "launch_count": 0,
        "player_lv": 1,
        "player_hp": 20
    }

def save_game_data(data):
    """Сохраняет данные в JSON файл."""
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)