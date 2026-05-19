# settings.py

# --- Внутреннее разрешение (пиксель-арт) ---
WIDTH, HEIGHT = 320, 240
SCALE = 3  # окно будет 960x720

# --- ЦВЕТА ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AUTUMN_YELLOW = (204, 153, 51)

# --- СОСТОЯНИЯ ИГРЫ ---
STATE_TITLE      = "TITLE"
STATE_STORY      = "STORY"
STATE_GAME       = "GAME"
STATE_DOOR       = "DOOR"
STATE_TRANSITION = "TRANSITION"
STATE_ATRIUM     = "ATRIUM"
STATE_GUARD_CHOICE = "GUARD_CHOICE"
STATE_GUARD_DIALOG = "GUARD_DIALOG"
STATE_GUARD_FIRST = "GUARD_FIRST"
STATE_BAHA_EVENT   = "BAHA_EVENT"


# --- ТАЙМИНГИ ПЕРЕХОДОВ ---
BLACK_DURATION = 400   
FADEIN_DURATION = 1000