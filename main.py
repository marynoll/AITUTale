import pygame
import sys
import os
import math 
from settings import *
from data_manager import load_game_data, save_game_data

pygame.init()

screen_surface = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("AITUTALE")
clock = pygame.time.Clock()

# --- ДОПОЛНИТЕЛЬНЫЕ СОСТОЯНИЯ ---
STATE_BAHA_EVENT = "BAHA_EVENT"
STATE_GUARD_POST_BAHA = "GUARD_POST_BAHA"
STATE_CORIDOR = "CORIDOR"
STATE_CORIDOR_DOOR = "CORIDOR_DOOR"
STATE_LADDER = "LADDER"
STATE_LADDER_DOOR = "LADDER_DOOR"
STATE_CORIDOR_BAHA_DIALOG = "CORIDOR_BAHA_DIALOG"
STATE_CORIDOR_BAHA_RUN = "CORIDOR_BAHA_RUN"

STATE_CORIDOR2FLOOR = "CORIDOR2FLOOR"
STATE_CORIDOR2FLOOR_DOOR = "CORIDOR2FLOOR_DOOR" 
STATE_LOCKERS_DIALOG = "LOCKERS_DIALOG"         
STATE_SPECIAL_LOCKER_DIALOG = "SPECIAL_LOCKER_DIALOG"

STATE_CABINET = "CABINET"
STATE_CABINET_DOOR = "CABINET_DOOR"
STATE_CORIDORFINAL = "CORIDORFINAL" 

STATE_TITLE_2 = "TITLE_2"       
STATE_MAIN_MENU = "MAIN_MENU"   
main_menu_choice = 0            
title_2_start_time = 0          

# --- МЕНЮ СОХРАНЕНИЯ ---
STATE_SAVE_MENU = "SAVE_MENU"
save_menu_choice = 0

# --- СОСТОЯНИЯ ОФИСА ---
STATE_OFFICE = "OFFICE"
STATE_MORADION_DIALOG = "MORADION_DIALOG"
STATE_PIMURDOM_DIALOG = "PIMURDOM_DIALOG"
STATE_PAKETT_DIALOG = "PAKETT_DIALOG"
STATE_SPECIFICCOMP_DIALOG = "SPECIFICCOMP_DIALOG"

# --- РАБОТА С JSON СЧЕТЧИКОМ И ИНВЕНТАРЕМ ---
game_data = load_game_data()
game_data["launch_count"] = game_data.get("launch_count", 0) + 1 

# Создаем базовые ключи, если их нет
if "inventory" not in game_data: game_data["inventory"] = []
if "has_saved" not in game_data: game_data["has_saved"] = False

inventory = game_data["inventory"]
save_game_data(game_data)
print(f"Игра запущена {game_data['launch_count']} раз(а)!")

# --- ЗАГРУЗКА ШРИФТА ---
try:
    font = pygame.font.Font(os.path.join("textures", "determination.ttf"), 8)
except:
    font = pygame.font.SysFont("arial", 12)

# --- ДАННЫЕ ПЕРСОНАЖА ---
player_name = "Frisk"
player_lv = game_data.get("player_lv", 1)
player_hp = game_data.get("player_hp", 20)
player_max_hp = 20
show_menu = False

# --- ФУНКЦИИ ЗАГРУЗКИ ---
def load_texture(filename):
    path = os.path.join("textures", filename)
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        return pygame.Surface((100, 100))

def load_texture_no_alpha(filename):
    path = os.path.join("textures", filename)
    try:
        return pygame.image.load(path).convert()
    except:
        return pygame.Surface((100, 100))

# === КЛАССЫ ===
class SpriteSheet:
    def __init__(self, filename):
        path = os.path.join("textures", filename)
        try:
            self.sheet = pygame.image.load(path).convert_alpha()
            bg_color = self.sheet.get_at((0, 0))
            self.sheet.set_colorkey(bg_color)
        except:
            self.sheet = pygame.Surface((160, 10)) 

    def get_image(self, x, y, width, height, scale_w, scale_h):
        image = self.sheet.subsurface(pygame.Rect(x, y, width, height))
        return pygame.transform.scale(image, (scale_w, scale_h))

# --- ЗАГРУЗКА ЛОГОТИПА ---
try:
    title_image = load_texture_no_alpha('title.png')
    title_image = pygame.transform.scale(title_image, (200, 40))
except:
    title_image = pygame.Surface((200, 40))
title_x = (WIDTH - 200) // 2
title_y = (HEIGHT - 40) // 2

# ==========================================
# --- ИДЕАЛЬНЫЙ ФИКС МАСОК КОЛЛИЗИЙ ---
# ==========================================
def load_black_mask(filename, fallback_size):
    path = os.path.join("textures", filename)
    try:
        img = pygame.image.load(path).convert_alpha()
        white_bg = pygame.Surface(img.get_size())
        white_bg.fill((255, 255, 255))
        white_bg.blit(img, (0, 0))
        mask = pygame.mask.from_threshold(white_bg, (0, 0, 0, 255), (80, 80, 80, 255))
        return mask
    except:
        return pygame.Mask(fallback_size)

# ==========================================
# --- ЗАГРУЗКА ВСЕХ КАРТ И КОЛЛИЗИЙ ---
# ==========================================

# 1. УЛИЦА
layer_outside = load_texture('outside.png')  
layer_kurilka = load_texture('kurilka.png')
layer_tapok = load_texture('kurilkatapok.png') 
map_rect = layer_outside.get_rect()
layer_outside_col = load_texture('outside granitsa.png')
mask_outside = pygame.mask.from_surface(layer_outside_col)
collision_masks = [mask_outside]

# 2. АТРИУМ
layer_atrium = load_texture('HallDemoNoTur.png') 
atrium_rect = layer_atrium.get_rect()
mask_colisia_atrium = load_black_mask('colisiaatrium.png', layer_atrium.get_size())
mask_colisia_turniket = load_black_mask('colisiaturniket.png', layer_atrium.get_size())

# 3. КОРИДОР (1 ЭТАЖ)
layer_coridor = load_texture('coridor.png')
coridor_rect = layer_coridor.get_rect()
mask_colisia_coridor = load_black_mask('colisiacoridor.png', layer_coridor.get_size())

# 4. ЛЕСТНИЦА
layer_ladder = load_texture('ladder.png')
ladder_rect = layer_ladder.get_rect()
mask_colisia_ladder = load_black_mask('colisialadder.png', layer_ladder.get_size())

# 5. КОРИДОР (2 ЭТАЖ)
layer_coridor2floor = load_texture('coridor2floor.png')
coridor2floor_rect = layer_coridor2floor.get_rect()
mask_colisia_coridor2fl = load_black_mask('colisiacoridor2fl.png', layer_coridor2floor.get_size())

# Шкафчики для коридора 2 этажа
lockers2floor_img = load_texture('lockers.png')
lockers2floor_mask = pygame.mask.from_surface(lockers2floor_img)
lockers2floor_real_rect = lockers2floor_img.get_bounding_rect()

# 6. НОВАЯ КОМНАТА СО ШКАФЧИКАМИ (coridorfinal)
layer_coridorfinal = load_texture('coridorfinal.png')
coridorfinal_rect = layer_coridorfinal.get_rect()
mask_colisia_coridorfinal = load_black_mask('colisiacoridorfinal.png', layer_coridorfinal.get_size())

# Объекты внутри coridorfinal
lockersfinal_img = load_texture('lockersfinalt.png')
lockersfinal_mask = pygame.mask.from_surface(lockersfinal_img)
lockersfinal_real_rect = lockersfinal_img.get_bounding_rect() 

speciallocker_img = load_texture('speciallocker.png')
speciallocker_mask = pygame.mask.from_surface(speciallocker_img)
speciallocker_real_rect = speciallocker_img.get_bounding_rect() 

specialdoor_img = load_texture('specialdoort.png')
specialdoor_mask = pygame.mask.from_surface(specialdoor_img)
specialdoor_real_rect = specialdoor_img.get_bounding_rect()

# --- ТОЧКА СОХРАНЕНИЯ ---
try:
    sp_sheet = load_texture('savepoint.png')
    sp_w = sp_sheet.get_width() // 2
    sp_h = sp_sheet.get_height()
    savepoint_frames = [sp_sheet.subsurface((i * sp_w, 0, sp_w, sp_h)) for i in range(2)]
except:
    dummy_sp = pygame.Surface((20, 20))
    dummy_sp.fill((255, 255, 0))
    savepoint_frames = [dummy_sp, dummy_sp]

savepoint_pos = (215, 548)
savepoint_rect = pygame.Rect(savepoint_pos[0], savepoint_pos[1], savepoint_frames[0].get_width(), savepoint_frames[0].get_height())
savepoint_frame_idx = 0
savepoint_anim_tick = 0

# ==========================================
# 7. ОФИС (Слои как на твоем скрине)
# ==========================================
layer_office = load_texture('office.png')
office_rect = layer_office.get_rect()
mask_office = load_black_mask('colisiaoffice.png', layer_office.get_size())

layer_comp = load_texture('comps1.png')
layer_comp2 = load_texture('comps2.png')
layer_specificcomp = load_texture('specificcomp.png')

img_moradion = load_texture('moradion.png')
img_pimurdom = load_texture('pimurdom.png') 
img_pakett = load_texture('paketoffice.png')

rect_moradion = img_moradion.get_bounding_rect()
rect_pimurdom = img_pimurdom.get_bounding_rect()
rect_pakett = img_pakett.get_bounding_rect()
rect_specificcomp = layer_specificcomp.get_bounding_rect()

office_exit_zone = pygame.Rect(750, 480, 80, 80)

# =================================================================
# === НАСТРОЙКА КООРДИНАТ ПОЯВЛЕНИЯ (СПАВНЫ) ===
# =================================================================
SPAWN_CORIDOR_X = coridor_rect.width // 2 - 20
SPAWN_CORIDOR_Y = 550 

SPAWN_LADDER_X = 753
SPAWN_LADDER_Y = 560

SPAWN_CORIDOR2FLOOR_X = 52
SPAWN_CORIDOR2FLOOR_Y = 590

SPAWN_CORIDORFINAL_X = 764
SPAWN_CORIDORFINAL_Y = 528

SPAWN_OFFICE_X = 790
SPAWN_OFFICE_Y = 494

SPAWN_SAVE_CONTINUE_X = 210
SPAWN_SAVE_CONTINUE_Y = 602
# =================================================================

# --- ЗАГРУЗКА И НАРЕЗКА ТУРНИКЕТОВ НА КАДРЫ ---
try:
    turniket_sheet = load_texture('turniket (1).png')
    t_width = turniket_sheet.get_width() // 3
    t_height = turniket_sheet.get_height()
    turniket_frames = [turniket_sheet.subsurface((i * t_width, 0, t_width, t_height)) for i in range(3)]
except:
    dummy = pygame.Surface((20, 30))
    dummy.fill((100, 100, 100))
    turniket_frames = [dummy, dummy, dummy]

turniket_positions = [
    (64, 486), (124, 486), (183, 486), (242, 486), (302, 486), (361, 486),
    (631, 486), (691, 486), (750, 486), (809, 486), (869, 486), (928, 486)
]
TARGET_TURNIKET_IDX = 10
target_turniket_state = 0 
turniket_anim_last_tick = 0

try:
    guard_img = load_texture('Guard-sheet.png')
except:
    guard_img = pygame.Surface((30, 50))
    guard_img.fill((50, 50, 50))

try:
    baha_img = load_texture('baha-Sheet.png')
except:
    baha_img = pygame.Surface((30, 50))
    baha_img.fill((0, 255, 0)) 

baha_sheet = SpriteSheet('baha-Sheet.png')
baha_w = baha_sheet.sheet.get_width() // 16 if baha_sheet.sheet.get_width() > 16 else 30
baha_h = baha_sheet.sheet.get_height() if baha_sheet.sheet.get_height() > 10 else 50

try:
    baha_walk_left  = [baha_sheet.get_image(i * baha_w, 0, baha_w, baha_h, baha_w, baha_h) for i in range(0, 4)]
    baha_walk_down  = [baha_sheet.get_image(i * baha_w, 0, baha_w, baha_h, baha_w, baha_h) for i in range(4, 8)]
    baha_walk_right = [baha_sheet.get_image(i * baha_w, 0, baha_w, baha_h, baha_w, baha_h) for i in range(8, 12)]
    baha_walk_up    = [baha_sheet.get_image(i * baha_w, 0, baha_w, baha_h, baha_w, baha_h) for i in range(12, 16)]
except:
    surf = pygame.Surface((baha_w, baha_h))
    surf.fill((0, 255, 0))
    baha_walk_down = baha_walk_up = baha_walk_right = baha_walk_left = [surf, surf, surf, surf]

baha_x = 867 
baha_y = 163 
baha_stage = 0 
baha_frame = 0
baha_current_anim = baha_walk_down
baha_last_anim_tick = pygame.time.get_ticks()
baha_event_finished = False 

baha_texts = [
    "Агай , ассалаумагалейкум! Так это\n наш новичок",
    "Что ? Реально? ",
    "Ладно проходи!"
]

guard_pos = (938, 516)
guard_rect = guard_img.get_rect(topleft=guard_pos)
guard_talk_rect = guard_rect.inflate(30, 30)

try:
    stoika_img = load_texture('StoikaSWoman.png')
except:
    stoika_img = pygame.Surface((80, 90))
    stoika_img.fill((150, 150, 150))
    
stoika_pos = (atrium_rect.width // 2 - stoika_img.get_width() // 2, 0)
stoika_rect = stoika_img.get_bounding_rect()
stoika_rect.x += stoika_pos[0]
stoika_rect.y += stoika_pos[1]

stoika_hitbox = pygame.Rect(stoika_rect.x, stoika_rect.bottom - 40, stoika_rect.width, 40)

# --- БАХА В КОРИДОРЕ ---
coridor_baha_x = 399
coridor_baha_y = 522
baha_in_coridor = True
coridor_baha_anim = baha_walk_down 
coridor_baha_frame = 0

coridor_baha_dialogs = [
    {
        "text": "Ну салам , новенький. Как дела?",
        "choices": [("нормально", 1), ("уйти", -1)]
    },
    {
        "text": "Добро пожаловать в нашу группу!\nНе бойся тебе понравится.",
        "choices": [("Не знаешь где кабинет?", 2), ("уйти", -1)]
    },
    {
        "text": "Тебя в нашу группу не добавили?\nНадо сказать Алиби... Корпус второй , \nи кабинет 241К.",
        "choices": [] 
    },
    {
        "text": "Блин мне нужно идти! ДАвай!",
        "choices": [] 
    }
]

# --- ТЕКСТЫ ДИАЛОГОВ ---
lockers_text = "У вас нет ключа."
lockers_dialog_char_index = 0

special_locker_text = ""  # Текст назначается динамически
special_locker_char_index = 0

office_dialog_text = ""
office_dialog_char_index = 0
office_dialog_choices = []
office_dialog_choice_idx = 0
office_dialog_speaker = ""

# --- ДАННЫЕ ИСТОРИИ ---
slides = [
    "Фриск упала в гору НО она попала\nне в подземелье а в шарагу\nАстаны Айту.",
    "Не понимая чо происходит она\nпытается уйти куда нибудь но\nтам везде сикс севен.",
    "Ей остается только зайти туда\nв АЙту."
]
current_slide = 0
char_index = 0
text_speed = 50

# --- СОСТОЯНИЯ ---
current_state = STATE_TITLE
turniket_closed = True 
is_behind_turniket = False 

start_time = pygame.time.get_ticks()
last_tick = start_time

door_choice = 0
coridor_door_choice = 0 
ladder_door_choice = 0 
coridor2floor_door_choice = 0 
cabinet_door_choice = 0

dialog_char_index = 0
dialog_text_speed = 50
dialog_last_tick = 0

first_char_index = 0
first_text_speed = 30
first_last_tick = 0
first_text = "Где твоя айдишка? Убирайся."

post_baha_text = "Проходи! Чего стоишь?"
post_baha_char_index = 0

guard_choice = 0
dialog_choice = 0
dialog_step = 0
guard_talk_count = 0
guard_dialogs = [
    {
        "text": "...",
        "choices": [("Ассалаумагалейкум!", 1), ("Здравствуйте!", -1)]
    },
    {
        "text": "Уалейкумассалам! Ты ваще из какой группы?",
        "choices": [("2567", -1), ("2519", 2), ("2619", -1)]
    },
    {
        "text": "Ааа, так ты перваш. Ладно, балмуздак, \nно ответь на еще один вопрос...",
        "choices": [("Какой?", -1)]
    }
]

# Зоны дверей
door_zone = pygame.Rect(800, 73, 66, 116) 
coridor_door_zone = pygame.Rect(463, 38, 103, 94) 
ladder_door_zone = pygame.Rect(28, 566, 5, 147) 
to_2floor_zone = pygame.Rect(524, 305, 121, 93) 

cabinet_door_zone = pygame.Rect(184, 719 , 109, 9)

transition_start = 0
transition_phase = "black"
next_state_after_transition = STATE_ATRIUM

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill(BLACK)

# === АНИМАЦИЯ ИГРОКА И МАСКИ ===
sheet = SpriteSheet('walking_sheet.png')
sheet_width  = sheet.sheet.get_width()

FRAME_WIDTH  = sheet_width // 16 if sheet_width > 16.815 else 10
FRAME_HEIGHT = sheet.sheet.get_height() if sheet.sheet.get_height() > 10 else 10
SCALE_W, SCALE_H = FRAME_WIDTH, FRAME_HEIGHT

# 1. ПОЛНАЯ МАСКА
player_surf_mask_full = pygame.Surface((SCALE_W, SCALE_H), pygame.SRCALPHA)
player_surf_mask_full.fill((255, 255, 255, 255))
player_mask_full = pygame.mask.from_surface(player_surf_mask_full)

# 2. МАСКА ГОЛОВЫ
player_surf_mask_head = pygame.Surface((SCALE_W, 20), pygame.SRCALPHA)
player_surf_mask_head.fill((255, 255, 255, 255))
player_mask_head = pygame.mask.from_surface(player_surf_mask_head)

try:
    walk_left  = [sheet.get_image(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT, SCALE_W, SCALE_H) for i in range(0, 4)]
    walk_down  = [sheet.get_image(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT, SCALE_W, SCALE_H) for i in range(4, 8)]
    walk_right = [sheet.get_image(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT, SCALE_W, SCALE_H) for i in range(8, 12)]
    walk_up    = [sheet.get_image(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT, SCALE_W, SCALE_H) for i in range(12, 16)]
except:
    surf = pygame.Surface((SCALE_W, SCALE_H))
    surf.fill((255,0,0))
    walk_down = walk_up = walk_right = walk_left = [surf, surf, surf, surf]

player_rect    = pygame.Rect(map_rect.width//2, map_rect.height - SCALE_H - 50, SCALE_W, SCALE_H)
player_hitbox = pygame.Rect(0, 0, 40, 30)

player_speed   = 2
current_frame  = 0
is_moving      = False
animation_speed = 120 
last_anim_tick = pygame.time.get_ticks()
current_anim   = walk_down 

camera_x, camera_y = 0, 0
atrium_cam_x, atrium_cam_y = 0, 0
coridor_cam_x, coridor_cam_y = 0, 0 
ladder_cam_x, ladder_cam_y = 0, 0 
coridor2floor_cam_x, coridor2floor_cam_y = 0, 0 
coridorfinal_cam_x, coridorfinal_cam_y = 0, 0 
office_cam_x, office_cam_y = 0, 0

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def draw_world():
    cx, cy = -camera_x, -camera_y
    screen_surface.blit(layer_outside, (cx, cy))
    screen_surface.blit(current_anim[current_frame], (player_rect.x - camera_x, player_rect.y - camera_y))
    screen_surface.blit(layer_kurilka, (cx, cy))
    screen_surface.blit(layer_tapok, (cx, cy))

def draw_atrium():
    cx, cy = -atrium_cam_x, -atrium_cam_y
    screen_surface.blit(layer_atrium, (cx, cy))
    
    drawables = []
    drawables.append((stoika_img, stoika_pos[0] + cx, stoika_pos[1] + cy, stoika_rect.bottom))
    drawables.append((guard_img, guard_pos[0] + cx, guard_pos[1] + cy, guard_rect.bottom))
    
    for i, pos in enumerate(turniket_positions):
        frame = turniket_frames[target_turniket_state] if i == TARGET_TURNIKET_IDX else turniket_frames[0]
        drawables.append((frame, pos[0] + cx, pos[1] + cy, pos[1] + frame.get_height()))
        
    sort_y = player_rect.y + 20 if is_behind_turniket else player_hitbox.bottom
    drawables.append((current_anim[current_frame], player_rect.x - atrium_cam_x, player_rect.y - atrium_cam_y, sort_y))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_coridor():
    cx, cy = -coridor_cam_x, -coridor_cam_y
    screen_surface.blit(layer_coridor, (cx, cy))
    
    drawables = []
    if baha_in_coridor:
        drawables.append((coridor_baha_anim[coridor_baha_frame], coridor_baha_x + cx, coridor_baha_y + cy, coridor_baha_y + baha_h))
        
    drawables.append((current_anim[current_frame], player_rect.x - coridor_cam_x, player_rect.y - coridor_cam_y, player_hitbox.bottom))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_ladder():
    cx, cy = -ladder_cam_x, -ladder_cam_y
    screen_surface.blit(layer_ladder, (cx, cy))
    screen_surface.blit(current_anim[current_frame], (player_rect.x - ladder_cam_x, player_rect.y - ladder_cam_y))

def draw_coridor2floor():
    cx, cy = -coridor2floor_cam_x, -coridor2floor_cam_y
    screen_surface.blit(layer_coridor2floor, (cx, cy))
    
    drawables = []
    if lockers2floor_real_rect.height > 0:
        drawables.append((lockers2floor_img, cx, cy, lockers2floor_real_rect.bottom))
        
    drawables.append((current_anim[current_frame], player_rect.x - coridor2floor_cam_x, player_rect.y - coridor2floor_cam_y, player_hitbox.bottom))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_coridorfinal():
    cx, cy = -coridorfinal_cam_x, -coridorfinal_cam_y
    screen_surface.blit(layer_coridorfinal, (cx, cy))
    
    drawables = []
    
    if lockersfinal_real_rect.height > 0:
        drawables.append((lockersfinal_img, cx, cy, lockersfinal_real_rect.bottom))
    if speciallocker_real_rect.height > 0:
        drawables.append((speciallocker_img, cx, cy, speciallocker_real_rect.bottom))
    if specialdoor_real_rect.height > 0:
        drawables.append((specialdoor_img, cx, cy, specialdoor_real_rect.bottom))

    # Рисуем точку сохранения
    drawables.append((savepoint_frames[savepoint_frame_idx], savepoint_pos[0] + cx, savepoint_pos[1] + cy, savepoint_pos[1] + savepoint_frames[0].get_height()))

    drawables.append((current_anim[current_frame], player_rect.x - coridorfinal_cam_x, player_rect.y - coridorfinal_cam_y, player_hitbox.bottom))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_office():
    cx, cy = -office_cam_x, -office_cam_y
    
    bob_offset = int(math.sin(pygame.time.get_ticks() / 200.0) * 3)
    
    screen_surface.blit(layer_office, (cx, cy))
    screen_surface.blit(layer_specificcomp, (cx, cy))
    screen_surface.blit(layer_comp2, (cx, cy))
    screen_surface.blit(img_pimurdom, (cx, cy + bob_offset))
    screen_surface.blit(current_anim[current_frame], (player_rect.x - office_cam_x, player_rect.y - office_cam_y))
    screen_surface.blit(img_pakett, (cx, cy))
    screen_surface.blit(layer_comp, (cx, cy))
    screen_surface.blit(img_moradion, (cx, cy + bob_offset))

def start_transition(next_state):
    global transition_start, transition_phase, next_state_after_transition, current_state
    transition_start = pygame.time.get_ticks()
    transition_phase = "black"
    next_state_after_transition = next_state
    current_state = STATE_TRANSITION

def draw_lockers_dialog():
    global lockers_dialog_char_index
    dialog_rect = pygame.Rect(10, 160, 300, 70)
    pygame.draw.rect(screen_surface, BLACK, dialog_rect)
    pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
    
    if current_time - dialog_last_tick > dialog_text_speed:
        if lockers_dialog_char_index < len(lockers_text):
            lockers_dialog_char_index += 1
        
    visible_text = lockers_text[:lockers_dialog_char_index]
    screen_surface.blit(font.render("* " + visible_text, True, WHITE), (20, 168))

def draw_special_locker_dialog():
    global special_locker_char_index
    dialog_rect = pygame.Rect(10, 160, 300, 70)
    pygame.draw.rect(screen_surface, BLACK, dialog_rect)
    pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
    
    if current_time - dialog_last_tick > dialog_text_speed:
        if special_locker_char_index < len(special_locker_text):
            special_locker_char_index += 1
        
    visible_text = special_locker_text[:special_locker_char_index]
    screen_surface.blit(font.render("* " + visible_text, True, WHITE), (20, 168))

# --- ГЛАВНЫЙ ЦИКЛ ---
while True:
    screen_surface.fill(BLACK)
    current_time = pygame.time.get_ticks()

    # Анимация точки сохранения
    if current_time - savepoint_anim_tick > 200:
        savepoint_frame_idx = (savepoint_frame_idx + 1) % len(savepoint_frames)
        savepoint_anim_tick = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(game_data)
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and current_state == STATE_DOOR:
            if event.key == pygame.K_LEFT: door_choice = 0
            elif event.key == pygame.K_RIGHT: door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if door_choice == 0:
                    player_rect.x = atrium_rect.width // 2
                    player_rect.y = atrium_rect.height - SCALE_H - 120 
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    is_behind_turniket = False
                    start_transition(STATE_ATRIUM)
                else:
                    current_state = STATE_GAME
                door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_GAME
                door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR_DOOR:
            if event.key == pygame.K_LEFT: coridor_door_choice = 0
            elif event.key == pygame.K_RIGHT: coridor_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if coridor_door_choice == 0:
                    player_rect.x = SPAWN_CORIDOR_X
                    player_rect.y = SPAWN_CORIDOR_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_CORIDOR)
                else:
                    current_state = STATE_ATRIUM
                coridor_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_ATRIUM
                coridor_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_LADDER_DOOR:
            if event.key == pygame.K_LEFT: ladder_door_choice = 0
            elif event.key == pygame.K_RIGHT: ladder_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if ladder_door_choice == 0:
                    player_rect.x = SPAWN_LADDER_X
                    player_rect.y = SPAWN_LADDER_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_LADDER)
                else:
                    current_state = STATE_CORIDOR
                ladder_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDOR
                ladder_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR2FLOOR_DOOR:
            if event.key == pygame.K_LEFT: coridor2floor_door_choice = 0
            elif event.key == pygame.K_RIGHT: coridor2floor_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if coridor2floor_door_choice == 0:
                    player_rect.x = SPAWN_CORIDOR2FLOOR_X
                    player_rect.y = SPAWN_CORIDOR2FLOOR_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_CORIDOR2FLOOR)
                else:
                    current_state = STATE_LADDER
                coridor2floor_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_LADDER
                coridor2floor_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CABINET_DOOR:
            if event.key == pygame.K_LEFT: cabinet_door_choice = 0
            elif event.key == pygame.K_RIGHT: cabinet_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if cabinet_door_choice == 0:
                    player_rect.x = SPAWN_CORIDORFINAL_X
                    player_rect.y = SPAWN_CORIDORFINAL_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_CORIDORFINAL)
                else:
                    current_state = STATE_CORIDOR2FLOOR
                cabinet_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDOR2FLOOR
                cabinet_door_choice = 0
        
        elif event.type == pygame.KEYDOWN and current_state == STATE_LOCKERS_DIALOG:
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if lockers_dialog_char_index >= len(lockers_text):
                    if "FINAL" in next_state_after_transition:
                        current_state = STATE_CORIDORFINAL
                    else:
                        current_state = STATE_CORIDOR2FLOOR
                    lockers_dialog_char_index = 0
                else:
                    lockers_dialog_char_index = len(lockers_text)

        elif event.type == pygame.KEYDOWN and current_state == STATE_SPECIAL_LOCKER_DIALOG:
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if special_locker_char_index >= len(special_locker_text):
                    current_state = STATE_CORIDORFINAL
                    special_locker_char_index = 0
                else:
                    special_locker_char_index = len(special_locker_text)

        elif event.type == pygame.KEYDOWN and current_state in (STATE_MORADION_DIALOG, STATE_PIMURDOM_DIALOG, STATE_PAKETT_DIALOG, STATE_SPECIFICCOMP_DIALOG):
            if office_dialog_choices:
                if event.key == pygame.K_LEFT: office_dialog_choice_idx = max(0, office_dialog_choice_idx - 1)
                elif event.key == pygame.K_RIGHT: office_dialog_choice_idx = min(len(office_dialog_choices) - 1, office_dialog_choice_idx + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    if office_dialog_char_index >= len(office_dialog_text):
                        current_state = STATE_OFFICE
                        office_dialog_char_index = 0
                    else:
                        office_dialog_char_index = len(office_dialog_text)
            else:
                if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                    if office_dialog_char_index >= len(office_dialog_text):
                        current_state = STATE_OFFICE
                        office_dialog_char_index = 0
                    else:
                        office_dialog_char_index = len(office_dialog_text)

        elif event.type == pygame.KEYDOWN and current_state == STATE_GUARD_FIRST:
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if first_char_index < len(first_text):
                    first_char_index = len(first_text)
                else:
                    current_state = STATE_ATRIUM

        elif event.type == pygame.KEYDOWN and current_state == STATE_GUARD_CHOICE:
            if event.key == pygame.K_LEFT: guard_choice = 0
            elif event.key == pygame.K_RIGHT: guard_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if guard_choice == 0:
                    if baha_event_finished:
                        current_state = STATE_GUARD_POST_BAHA
                        post_baha_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
                    else:
                        if guard_talk_count == 0:
                            guard_talk_count += 1
                            current_state = STATE_GUARD_FIRST
                            first_char_index = 0
                            first_last_tick = pygame.time.get_ticks()
                        else:
                            current_state = STATE_GUARD_DIALOG
                            dialog_step = 0
                            dialog_choice = 0
                            dialog_char_index = 0
                            dialog_last_tick = pygame.time.get_ticks()
                else:
                    current_state = STATE_ATRIUM
                guard_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_ATRIUM
                guard_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_GUARD_POST_BAHA:
            if event.key in (pygame.K_RETURN, pygame.K_z):
                if post_baha_char_index < len(post_baha_text):
                    post_baha_char_index = len(post_baha_text)
                else:
                    current_state = STATE_ATRIUM
                    turniket_closed = False
                    target_turniket_state = 1 

        elif event.type == pygame.KEYDOWN and current_state == STATE_GUARD_DIALOG:
            choices = guard_dialogs[dialog_step]["choices"]
            if event.key == pygame.K_LEFT and choices:
                dialog_choice = max(0, dialog_choice - 1)
            elif event.key == pygame.K_RIGHT and choices:
                dialog_choice = min(len(choices) - 1, dialog_choice + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if dialog_char_index < len(guard_dialogs[dialog_step]["text"]):
                    dialog_char_index = len(guard_dialogs[dialog_step]["text"])
                    continue
                
                if dialog_step == 2:
                    current_state = STATE_BAHA_EVENT
                    baha_stage = 0
                    baha_x = 867  
                    baha_y = 163  
                    baha_frame = 0
                    baha_current_anim = baha_walk_down
                    dialog_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                    continue

                if choices:
                    next_step = choices[dialog_choice][1]
                    if next_step == -1:
                        current_state = STATE_ATRIUM
                        dialog_step = 0
                        dialog_choice = 0
                    else:
                        dialog_step = next_step
                        dialog_choice = 0
                        dialog_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_ATRIUM
                dialog_step = 0
                dialog_choice = 0
        
        elif event.type == pygame.KEYDOWN and current_state == STATE_BAHA_EVENT:
            if baha_stage in (1, 2, 3):
                if event.key in (pygame.K_RETURN, pygame.K_z):
                    current_text_target = baha_texts[baha_stage - 1]
                    if dialog_char_index < len(current_text_target):
                        dialog_char_index = len(current_text_target) 
                    else:
                        baha_stage += 1
                        dialog_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
                        if baha_stage == 4:
                            baha_current_anim = baha_walk_up
                            baha_frame = 0
                            baha_last_anim_tick = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR_BAHA_DIALOG:
            data = coridor_baha_dialogs[dialog_step]
            if event.key == pygame.K_LEFT and data["choices"]:
                dialog_choice = max(0, dialog_choice - 1)
            elif event.key == pygame.K_RIGHT and data["choices"]:
                dialog_choice = min(len(data["choices"]) - 1, dialog_choice + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if dialog_char_index < len(data["text"]):
                    dialog_char_index = len(data["text"])
                    continue
                
                if not data["choices"]:
                    next_step = dialog_step + 1
                else:
                    next_step = data["choices"][dialog_choice][1]

                if next_step == -1:
                    current_state = STATE_CORIDOR
                    dialog_step = 0
                    dialog_choice = 0
                elif next_step >= len(coridor_baha_dialogs):
                    current_state = STATE_CORIDOR_BAHA_RUN
                    coridor_baha_anim = baha_walk_right
                    coridor_baha_frame = 0
                    baha_last_anim_tick = pygame.time.get_ticks()
                else:
                    dialog_step = next_step
                    dialog_choice = 0
                    dialog_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == STATE_GAME:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if door_zone.colliderect(player_hitbox):
                    current_state = STATE_DOOR
                    door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_ATRIUM:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if player_hitbox.colliderect(guard_talk_rect):
                    current_state = STATE_GUARD_CHOICE
                    guard_choice = 0
                elif coridor_door_zone.colliderect(player_hitbox):
                    current_state = STATE_CORIDOR_DOOR
                    coridor_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if baha_in_coridor:
                    coridor_baha_talk_rect = pygame.Rect(coridor_baha_x - 15, coridor_baha_y - 15, baha_w + 30, baha_h + 30)
                    if player_hitbox.colliderect(coridor_baha_talk_rect):
                        current_state = STATE_CORIDOR_BAHA_DIALOG
                        dialog_step = 0
                        dialog_choice = 0
                        dialog_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
                
                elif ladder_door_zone.colliderect(player_hitbox):
                    if not baha_in_coridor:
                        current_state = STATE_LADDER_DOOR
                        ladder_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_LADDER:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if to_2floor_zone.colliderect(player_hitbox):
                    current_state = STATE_CORIDOR2FLOOR_DOOR
                    coridor2floor_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR2FLOOR:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if cabinet_door_zone.colliderect(player_hitbox):
                    current_state = STATE_CABINET_DOOR
                    cabinet_door_choice = 0
                elif lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                     lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    current_state = STATE_LOCKERS_DIALOG
                    lockers_dialog_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                    
        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDORFINAL:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_ESCAPE:
                player_rect.x = 315 - SCALE_W // 2
                player_rect.y = 528 + 20 
                player_hitbox.centerx = player_rect.centerx
                player_hitbox.bottom = player_rect.bottom
                start_transition(STATE_CORIDOR2FLOOR)
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                # Вход в меню сохранения
                if savepoint_rect.inflate(20, 20).colliderect(player_hitbox):
                    current_state = STATE_SAVE_MENU
                    save_menu_choice = 0
                elif specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                   specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    player_rect.x = SPAWN_OFFICE_X
                    player_rect.y = SPAWN_OFFICE_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_OFFICE)
                elif speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                   speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    current_state = STATE_SPECIAL_LOCKER_DIALOG
                    if "Секретные файлы" not in inventory:
                        inventory.append("Секретные файлы")
                        game_data["inventory"] = inventory
                        save_game_data(game_data)
                        special_locker_text = "Вы нашли 'Секретные файлы'!"
                    else:
                        special_locker_text = "Пусто."
                    special_locker_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                     lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    current_state = STATE_LOCKERS_DIALOG
                    lockers_dialog_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()

        # --- ОБРАБОТКА МЕНЮ СОХРАНЕНИЯ ---
        elif event.type == pygame.KEYDOWN and current_state == STATE_SAVE_MENU:
            if event.key == pygame.K_LEFT:
                save_menu_choice = 0
            elif event.key == pygame.K_RIGHT:
                save_menu_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                if save_menu_choice == 0:
                    # СОХРАНЕНИЕ
                    game_data["inventory"] = inventory
                    game_data["has_saved"] = True
                    game_data["player_lv"] = player_lv
                    game_data["player_hp"] = player_hp
                    save_game_data(game_data)
                    current_state = STATE_CORIDORFINAL
                else:
                    # УЙТИ
                    current_state = STATE_CORIDORFINAL
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDORFINAL

        elif event.type == pygame.KEYDOWN and current_state == STATE_OFFICE:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                interact_rect_moradion = rect_moradion.inflate(40, 40) if rect_moradion.width > 0 else pygame.Rect(0,0,0,0)
                interact_rect_pimurdom = rect_pimurdom.inflate(40, 40) if rect_pimurdom.width > 0 else pygame.Rect(0,0,0,0)
                interact_rect_pakett = rect_pakett.inflate(40, 40) if rect_pakett.width > 0 else pygame.Rect(0,0,0,0)
                interact_rect_spec = rect_specificcomp.inflate(40, 40) if rect_specificcomp.width > 0 else pygame.Rect(0,0,0,0)
                
                if interact_rect_moradion.colliderect(player_hitbox):
                    current_state = STATE_MORADION_DIALOG
                    office_dialog_text = "u are in trap"
                    office_dialog_choices = ["уйти"]
                    office_dialog_char_index = 0
                    office_dialog_choice_idx = 0
                    office_dialog_speaker = "Moradion"
                    dialog_last_tick = pygame.time.get_ticks()
                elif interact_rect_pimurdom.colliderect(player_hitbox):
                    current_state = STATE_PIMURDOM_DIALOG
                    office_dialog_text = "stay."
                    office_dialog_choices = ["уйти"]
                    office_dialog_char_index = 0
                    office_dialog_choice_idx = 0
                    office_dialog_speaker = "Pimurdom"
                    dialog_last_tick = pygame.time.get_ticks()
                elif interact_rect_pakett.colliderect(player_hitbox):
                    current_state = STATE_PAKETT_DIALOG
                    office_dialog_text = "Кто то оставил пакет с весом будто в тонну"
                    office_dialog_choices = []
                    office_dialog_char_index = 0
                    office_dialog_speaker = ""
                    dialog_last_tick = pygame.time.get_ticks()
                elif interact_rect_spec.colliderect(player_hitbox):
                    current_state = STATE_SPECIFICCOMP_DIALOG
                    office_dialog_text = "Техническая работа!"
                    office_dialog_choices = []
                    office_dialog_char_index = 0
                    office_dialog_speaker = ""
                    dialog_last_tick = pygame.time.get_ticks()
                elif office_exit_zone.colliderect(player_hitbox):
                    player_rect.x = SPAWN_CORIDORFINAL_X
                    player_rect.y = SPAWN_CORIDORFINAL_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_CORIDORFINAL)

        elif event.type == pygame.KEYDOWN and current_state == STATE_STORY:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if char_index < len(slides[current_slide]):
                    char_index = len(slides[current_slide])
                else:
                    current_slide += 1
                    char_index = 0
                    if current_slide >= len(slides):
                        current_state = STATE_TITLE_2
                        title_2_start_time = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == STATE_MAIN_MENU:
            if event.key == pygame.K_LEFT:
                main_menu_choice = 0
            elif event.key == pygame.K_RIGHT:
                main_menu_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_z):
                if main_menu_choice == 0: 
                    if game_data.get("has_saved", False):
                        player_rect.x = SPAWN_SAVE_CONTINUE_X
                        player_rect.y = SPAWN_SAVE_CONTINUE_Y
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        start_transition(STATE_CORIDORFINAL)
                    else:
                        player_rect.x = map_rect.width // 2
                        player_rect.y = map_rect.height - SCALE_H - 50
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        start_transition(STATE_GAME)
                        
                elif main_menu_choice == 1: 
                    # Полный сброс (RESET)
                    game_data["launch_count"] = 1
                    game_data["player_lv"] = 1
                    game_data["player_hp"] = 20
                    game_data["inventory"] = []
                    game_data["has_saved"] = False
                    inventory.clear()
                    player_lv = 1
                    player_hp = 20
                    save_game_data(game_data)
                    
                    player_rect.x = map_rect.width // 2
                    player_rect.y = map_rect.height - SCALE_H - 50
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    start_transition(STATE_GAME) 

    # =========================================================
    # --- ДВИЖЕНИЕ НА УЛИЦЕ ---
    # =========================================================
    if current_state == STATE_GAME:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < map_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < map_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_out_collision(px, py):
            for col_mask in collision_masks:
                if col_mask.overlap(player_mask_full, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_out_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_out_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        camera_x = player_rect.centerx - WIDTH // 2
        camera_y = player_rect.centery - HEIGHT // 2
        camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
        camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT)))

    # =========================================================
    # --- ДВИЖЕНИЕ В АТРИУМЕ ---
    # =========================================================
    elif current_state == STATE_ATRIUM:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < atrium_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < atrium_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        current_mask = player_mask_head if is_behind_turniket else player_mask_full

        def check_atrium_collision(px, py):
            temp_hitbox = pygame.Rect(0, 0, 40, 30)
            temp_hitbox.centerx = px + SCALE_W // 2
            temp_hitbox.bottom = py + SCALE_H
            if temp_hitbox.colliderect(stoika_hitbox) or temp_hitbox.colliderect(guard_rect): return True
            if mask_colisia_atrium.overlap(current_mask, (px, py)): return True
            if turniket_closed and mask_colisia_turniket.overlap(current_mask, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_atrium_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_atrium_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        if not turniket_closed and target_turniket_state == 1:
            pass_rect = pygame.Rect(850, 440, 60, 40) 
            if pass_rect.colliderect(player_hitbox) and player_hitbox.bottom < 475:
                target_turniket_state = 2 
                turniket_anim_last_tick = current_time
                turniket_closed = True
                is_behind_turniket = True 
        
        if target_turniket_state == 2:
            if current_time - turniket_anim_last_tick > 150: 
                target_turniket_state = 0

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        atrium_cam_x = player_rect.centerx - WIDTH // 2
        atrium_cam_y = player_rect.centery - HEIGHT // 2
        atrium_cam_x = max(0, min(atrium_cam_x, max(0, atrium_rect.width - WIDTH)))
        atrium_cam_y = max(0, min(atrium_cam_y, max(0, atrium_rect.height - HEIGHT)))

    # =========================================================
    # --- ДВИЖЕНИЕ В КОРИДОРЕ (1 ЭТАЖ) ---
    # =========================================================
    elif current_state == STATE_CORIDOR:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < coridor_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < coridor_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_coridor_collision(px, py):
            if mask_colisia_coridor.overlap(player_mask_full, (px, py)): return True
            
            if baha_in_coridor:
                temp_hitbox = pygame.Rect(0, 0, 40, 30)
                temp_hitbox.centerx = px + SCALE_W // 2
                temp_hitbox.bottom = py + SCALE_H
                b_hitbox = pygame.Rect(coridor_baha_x, coridor_baha_y + baha_h - 20, baha_w, 20)
                if temp_hitbox.colliderect(b_hitbox): return True
                
            return False

        if dx != 0:
            player_rect.x += dx
            if check_coridor_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_coridor_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        coridor_cam_x = player_rect.centerx - WIDTH // 2
        coridor_cam_y = player_rect.centery - HEIGHT // 2
        coridor_cam_x = max(0, min(coridor_cam_x, max(0, coridor_rect.width - WIDTH)))
        coridor_cam_y = max(0, min(coridor_cam_y, max(0, coridor_rect.height - HEIGHT)))

    # =========================================================
    # --- ДВИЖЕНИЕ НА ЛЕСТНИЦЕ ---
    # =========================================================
    elif current_state == STATE_LADDER:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < ladder_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < ladder_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_ladder_collision(px, py):
            if mask_colisia_ladder.overlap(player_mask_full, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_ladder_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_ladder_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        ladder_cam_x = player_rect.centerx - WIDTH // 2
        ladder_cam_y = player_rect.centery - HEIGHT // 2
        ladder_cam_x = max(0, min(ladder_cam_x, max(0, ladder_rect.width - WIDTH)))
        ladder_cam_y = max(0, min(ladder_cam_y, max(0, ladder_rect.height - HEIGHT)))

    # =========================================================
    # --- ДВИЖЕНИЕ НА 2 ЭТАЖЕ ---
    # =========================================================
    elif current_state == STATE_CORIDOR2FLOOR:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < coridor2floor_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < coridor2floor_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_coridor2floor_collision(px, py):
            if mask_colisia_coridor2fl.overlap(player_mask_full, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_coridor2floor_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_coridor2floor_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        if cabinet_door_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        elif lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
             lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        coridor2floor_cam_x = player_rect.centerx - WIDTH // 2
        coridor2floor_cam_y = player_rect.centery - HEIGHT // 2
        coridor2floor_cam_x = max(0, min(coridor2floor_cam_x, max(0, coridor2floor_rect.width - WIDTH)))
        coridor2floor_cam_y = max(0, min(coridor2floor_cam_y, max(0, coridor2floor_rect.height - HEIGHT)))
        
    # =========================================================
    # --- ДВИЖЕНИЕ В НОВОЙ КОМНАТЕ С ШКАФЧИКАМИ ---
    # =========================================================
    elif current_state == STATE_CORIDORFINAL:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < coridorfinal_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < coridorfinal_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_coridorfinal_collision(px, py):
            if mask_colisia_coridorfinal.overlap(player_mask_full, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_coridorfinal_collision(player_rect.x, player_rect.y): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_coridorfinal_collision(player_rect.x, player_rect.y): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        # ХИНТЫ ДЛЯ ОБЪЕКТОВ
        if savepoint_rect.inflate(20, 20).colliderect(player_hitbox):
            hint = font.render("ENTER - сохранить", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
           specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
           speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
             lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        hint_esc = font.render("ESC - выйти в коридор", True, AUTUMN_YELLOW)
        screen_surface.blit(hint_esc, (WIDTH//2 - hint_esc.get_width()//2, HEIGHT - 20))

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        coridorfinal_cam_x = player_rect.centerx - WIDTH // 2
        coridorfinal_cam_y = player_rect.centery - HEIGHT // 2
        coridorfinal_cam_x = max(0, min(coridorfinal_cam_x, max(0, coridorfinal_rect.width - WIDTH)))
        coridorfinal_cam_y = max(0, min(coridorfinal_cam_y, max(0, coridorfinal_rect.height - HEIGHT)))
        
    # =========================================================
    # --- ДВИЖЕНИЕ В ОФИСЕ ---
    # =========================================================
    elif current_state == STATE_OFFICE:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT] and player_rect.left > 0: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT] and player_rect.right < office_rect.width: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP] and player_rect.top > 0: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN] and player_rect.bottom < office_rect.height: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        # Простая коллизия офиса (одна маска)
        if dx != 0:
            player_rect.x += dx
            if mask_office.overlap(player_mask_full, (player_rect.x, player_rect.y)): player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if mask_office.overlap(player_mask_full, (player_rect.x, player_rect.y)): player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

        # Подсказки для взаимодействия в офисе
        interact_rect_moradion = rect_moradion.inflate(40, 40) if rect_moradion.width > 0 else pygame.Rect(0,0,0,0)
        interact_rect_pimurdom = rect_pimurdom.inflate(40, 40) if rect_pimurdom.width > 0 else pygame.Rect(0,0,0,0)
        interact_rect_pakett = rect_pakett.inflate(40, 40) if rect_pakett.width > 0 else pygame.Rect(0,0,0,0)
        interact_rect_spec = rect_specificcomp.inflate(40, 40) if rect_specificcomp.width > 0 else pygame.Rect(0,0,0,0)

        if interact_rect_moradion.colliderect(player_hitbox) or interact_rect_pimurdom.colliderect(player_hitbox):
            hint = font.render("ENTER - говорить", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif interact_rect_pakett.colliderect(player_hitbox) or interact_rect_spec.colliderect(player_hitbox):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif office_exit_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - выйти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

        if old_anim != current_anim: current_frame = 0
        if is_moving:
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            current_frame = 0

        office_cam_x = player_rect.centerx - WIDTH // 2
        office_cam_y = player_rect.centery - HEIGHT // 2
        office_cam_x = max(0, min(office_cam_x, max(0, office_rect.width - WIDTH)))
        office_cam_y = max(0, min(office_cam_y, max(0, office_rect.height - HEIGHT)))

    elif current_state == STATE_CORIDOR_BAHA_RUN:
        run_speed = 4
        coridor_baha_x += run_speed
        
        if current_time - baha_last_anim_tick > animation_speed:
            coridor_baha_frame = (coridor_baha_frame + 1) % len(coridor_baha_anim)
            baha_last_anim_tick = current_time
            
        if coridor_baha_x > coridor_rect.width + 100:
            baha_in_coridor = False
            current_state = STATE_CORIDOR

        coridor_cam_x = player_rect.centerx - WIDTH // 2
        coridor_cam_y = player_rect.centery - HEIGHT // 2
        coridor_cam_x = max(0, min(coridor_cam_x, max(0, coridor_rect.width - WIDTH)))
        coridor_cam_y = max(0, min(coridor_cam_y, max(0, coridor_rect.height - HEIGHT)))

    elif current_state == STATE_BAHA_EVENT:
        if baha_stage == 0:
            target_x = 895  
            target_y = 456  
            speed = 3       

            dx = target_x - baha_x
            dy = target_y - baha_y
            distance = (dx**2 + dy**2)**0.5 

            if distance > speed:
                baha_x += (dx / distance) * speed
                baha_y += (dy / distance) * speed
                
                if abs(dx) > abs(dy):
                    baha_current_anim = baha_walk_right if dx > 0 else baha_walk_left
                else:
                    baha_current_anim = baha_walk_down if dy > 0 else baha_walk_up
                
                if current_time - baha_last_anim_tick > animation_speed:
                    baha_frame = (baha_frame + 1) % len(baha_current_anim)
                    baha_last_anim_tick = current_time
            else:
                baha_x = target_x
                baha_y = target_y
                baha_frame = 0
                baha_current_anim = baha_walk_down 
                
                baha_stage = 1 
                dialog_char_index = 0
                dialog_last_tick = pygame.time.get_ticks()
                
        elif baha_stage == 4:
            run_speed = 4
            baha_y -= run_speed
            
            if current_time - baha_last_anim_tick > animation_speed:
                baha_frame = (baha_frame + 1) % len(baha_current_anim)
                baha_last_anim_tick = current_time
                
            if baha_y < 120:
                current_state = STATE_ATRIUM
                baha_event_finished = True 

        atrium_cam_x = player_rect.centerx - WIDTH // 2
        atrium_cam_y = player_rect.centery - HEIGHT // 2
        atrium_cam_x = max(0, min(atrium_cam_x, max(0, atrium_rect.width - WIDTH)))
        atrium_cam_y = max(0, min(atrium_cam_y, max(0, atrium_rect.height - HEIGHT)))

    # =========================================================
    # --- БЛОК ОТРИСОВКИ ВСЕХ ЭЛЕМЕНТОВ ---
    # =========================================================
    if current_state == STATE_TITLE:
        screen_surface.blit(title_image, (title_x, title_y))
        if current_time - start_time > 4000:
            current_state = STATE_STORY
            last_tick = current_time

    elif current_state == STATE_STORY:
        pygame.draw.rect(screen_surface, AUTUMN_YELLOW, (10, 10, 300, 150))
        if current_time - last_tick > text_speed:
            if char_index < len(slides[current_slide]):
                char_index += 1
            last_tick = current_time
        current_text = slides[current_slide][:char_index]
        for i, line in enumerate(current_text.split('\n')):
            screen_surface.blit(font.render(line, True, WHITE), (15, 170 + i * 12))

    elif current_state == STATE_TITLE_2:
        screen_surface.blit(title_image, (title_x, title_y))
        if current_time - title_2_start_time > 2000:
            current_state = STATE_MAIN_MENU

    elif current_state == STATE_MAIN_MENU:
        screen_surface.blit(font.render(player_name, True, WHITE), (60, 80))
        screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE), (140, 80))
        screen_surface.blit(font.render(":D", True, WHITE), (220, 80))
        
        screen_surface.blit(font.render("Final Coridor", True, WHITE), (60, 100))
        
        play_color = AUTUMN_YELLOW if main_menu_choice == 0 else WHITE
        reset_color = AUTUMN_YELLOW if main_menu_choice == 1 else WHITE
        
        play_text = "Continue" if game_data.get("has_saved", False) else "Play"
        
        screen_surface.blit(font.render(play_text, True, play_color), (90, 150))
        screen_surface.blit(font.render("Reset", True, reset_color), (190, 150))

    elif current_state == STATE_GAME:
        draw_world()
        if door_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    elif current_state == STATE_DOOR:
        draw_world()
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да"  if door_choice == 0 else "  Да",  True, da_color),  (80,  205))
        screen_surface.blit(font.render("* Нет" if door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_CORIDOR_DOOR:
        draw_atrium() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти в коридор?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if coridor_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if coridor_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да"  if coridor_door_choice == 0 else "  Да",  True, da_color),  (80,  205))
        screen_surface.blit(font.render("* Нет" if coridor_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_LADDER_DOOR:
        draw_coridor() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Перейти к лестнице?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if ladder_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if ladder_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да"  if ladder_door_choice == 0 else "  Да",  True, da_color),  (80,  205))
        screen_surface.blit(font.render("* Нет" if ladder_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_ATRIUM:
        draw_atrium()
        if player_hitbox.colliderect(guard_talk_rect):
            hint = font.render("ENTER - говорить", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif coridor_door_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    elif current_state == STATE_CORIDOR:
        draw_coridor()
        if baha_in_coridor:
            coridor_baha_talk_rect = pygame.Rect(coridor_baha_x - 15, coridor_baha_y - 15, baha_w + 30, baha_h + 30)
            if player_hitbox.colliderect(coridor_baha_talk_rect):
                hint = font.render("ENTER - говорить", True, AUTUMN_YELLOW)
                screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        
        if ladder_door_zone.colliderect(player_hitbox):
            if not baha_in_coridor:
                hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            else:
                hint = font.render("Сначала поговори с Бахой!", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    elif current_state == STATE_LADDER:
        draw_ladder()
        if to_2floor_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - подняться", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    elif current_state == STATE_CORIDOR2FLOOR:
        draw_coridor2floor()
        if cabinet_door_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
             lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))
                    
    elif current_state == STATE_CORIDORFINAL:
        draw_coridorfinal()
        if savepoint_rect.inflate(20, 20).colliderect(player_hitbox):
            hint = font.render("ENTER - сохранить", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
           specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
           speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
             lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    # --- ОТРИСОВКА МЕНЮ СОХРАНЕНИЯ В КОРИДОРЕ ---
    elif current_state == STATE_SAVE_MENU:
        draw_coridorfinal()
        
        box = pygame.Rect(30, 40, 260, 100)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        
        screen_surface.blit(font.render(player_name, True, WHITE), (45, 50))
        screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE), (125, 50))
        screen_surface.blit(font.render(":D", True, WHITE), (230, 50))
        screen_surface.blit(font.render("Final Coridor", True, WHITE), (45, 75))
        
        c_save = AUTUMN_YELLOW if save_menu_choice == 0 else WHITE
        c_ret = AUTUMN_YELLOW if save_menu_choice == 1 else WHITE
        
        prefix_save = "\u2665 " if save_menu_choice == 0 else "  "
        prefix_ret = "\u2665 " if save_menu_choice == 1 else "  "
        
        screen_surface.blit(font.render(f"{prefix_save}Save", True, c_save), (50, 115))
        screen_surface.blit(font.render(f"{prefix_ret}Return", True, c_ret), (150, 115))

    # --- ОТРИСОВКА ОФИСА И ЕГО ДИАЛОГОВ ---
    elif current_state == STATE_OFFICE:
        draw_office()
        if show_menu:
            box1 = pygame.Rect(4, 4, 80, 46)
            pygame.draw.rect(screen_surface, BLACK, box1)
            pygame.draw.rect(screen_surface, WHITE, box1, 2)
            screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
            screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+16))
            screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+28))
            
            box2 = pygame.Rect(4, 54, 80, 30)
            pygame.draw.rect(screen_surface, BLACK, box2)
            pygame.draw.rect(screen_surface, WHITE, box2, 2)
            screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
            screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+16))
            
            if inventory:
                inv_box = pygame.Rect(90, 4, 180, 24 + 14 * len(inventory))
                pygame.draw.rect(screen_surface, BLACK, inv_box)
                pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
                screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
                for idx, item in enumerate(inventory):
                    screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+20 + idx*14))

    elif current_state in (STATE_MORADION_DIALOG, STATE_PIMURDOM_DIALOG, STATE_PAKETT_DIALOG, STATE_SPECIFICCOMP_DIALOG):
        draw_office()
        
        dialog_rect = pygame.Rect(10, 160, 300, 70)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if office_dialog_char_index < len(office_dialog_text):
                office_dialog_char_index += 1
            dialog_last_tick = current_time

        visible_text = office_dialog_text[:office_dialog_char_index]
        
        for i, line in enumerate(visible_text.split("\n")):
            prefix = f"* {office_dialog_speaker}: " if i == 0 and office_dialog_speaker else ("* " if i == 0 else "")
            screen_surface.blit(font.render(prefix + line, True, WHITE), (20 if not office_dialog_speaker else 80, 168 + i * 12))

        if office_dialog_char_index >= len(office_dialog_text):
            if not office_dialog_choices:
                screen_surface.blit(font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (20 if not office_dialog_speaker else 85, 205))
            else:
                x = 20 if not office_dialog_speaker else 85
                for i, choice in enumerate(office_dialog_choices):
                    color = AUTUMN_YELLOW if i == office_dialog_choice_idx else WHITE
                    prefix = "* " if i == office_dialog_choice_idx else "  "
                    text_surf = font.render(prefix + choice, True, color)
                    screen_surface.blit(text_surf, (x, 205))
                    x += text_surf.get_width() + 20

    elif current_state == STATE_CORIDOR_BAHA_RUN:
        draw_coridor() 

    elif current_state == STATE_CORIDOR_BAHA_DIALOG:
        draw_coridor()
        dialog_rect = pygame.Rect(10, 160, 300, 70)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        data = coridor_baha_dialogs[dialog_step]
        if current_time - dialog_last_tick > dialog_text_speed:
            if dialog_char_index < len(data["text"]):
                dialog_char_index += 1
            dialog_last_tick = current_time

        visible_text = data["text"][:dialog_char_index]
        speaker_prefix = "* Баха: "
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render(speaker_prefix + line if i == 0 else line, True, WHITE), (80, 168 + i * 12))

        if dialog_char_index >= len(data["text"]):
            if not data["choices"]:
                screen_surface.blit(font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (85, 205))
            else:
                x = 85
                for i, choice in enumerate(data["choices"]):
                    color = AUTUMN_YELLOW if i == dialog_choice else WHITE
                    prefix = "* " if i == dialog_choice else "  "
                    text = font.render(prefix + choice[0], True, color)
                    screen_surface.blit(text, (x, 205))
                    x += text.get_width() + 20

    elif current_state == STATE_LOCKERS_DIALOG:
        # Проверяем, откуда вызван диалог, чтобы правильно отрисовать фон
        if lockersfinal_real_rect.height > 0 and lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)):
            draw_coridorfinal()
        else:
            draw_coridor2floor()
        draw_lockers_dialog()
        
    elif current_state == STATE_SPECIAL_LOCKER_DIALOG:
        draw_coridorfinal()
        draw_special_locker_dialog()

    elif current_state == STATE_CORIDOR2FLOOR_DOOR:
        draw_ladder() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Перейти на 2 этаж?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if coridor2floor_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if coridor2floor_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да"  if coridor2floor_door_choice == 0 else "  Да",  True, da_color),  (80,  205))
        screen_surface.blit(font.render("* Нет" if coridor2floor_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_CABINET_DOOR:
        draw_coridor2floor()
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти в кабинет?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if cabinet_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if cabinet_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да"  if cabinet_door_choice == 0 else "  Да",  True, da_color),  (80,  205))
        screen_surface.blit(font.render("* Нет" if cabinet_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_GUARD_CHOICE:
        draw_atrium()
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Поговорить?", True, WHITE), (18, 182))
        yes_color = AUTUMN_YELLOW if guard_choice == 0 else WHITE
        no_color = AUTUMN_YELLOW if guard_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да" if guard_choice == 0 else "  Да", True, yes_color), (80, 205))
        screen_surface.blit(font.render("* Нет" if guard_choice == 1 else "  Нет", True, no_color), (180, 205))
    
    elif current_state == STATE_GUARD_POST_BAHA:
        draw_atrium()
        dialog_rect = pygame.Rect(10, 160, 300, 70)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        if current_time - dialog_last_tick > dialog_text_speed:
            if post_baha_char_index < len(post_baha_text):
                post_baha_char_index += 1
            dialog_last_tick = current_time

        visible_text = post_baha_text[:post_baha_char_index]
        screen_surface.blit(font.render("* Охранник: " + visible_text, True, WHITE), (80, 168))

        if post_baha_char_index >= len(post_baha_text):
            screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == STATE_GUARD_FIRST:
        draw_atrium()
        dialog_rect = pygame.Rect(10, 160, 300, 70)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        if current_time - first_last_tick > first_text_speed:
            if first_char_index < len(first_text):
                first_char_index += 1
            first_last_tick = current_time

        visible_text = first_text[:first_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render(line, True, WHITE), (80, 168 + i * 12))

        if first_char_index >= len(first_text):
            screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))
    
    elif current_state == STATE_GUARD_DIALOG:
        draw_atrium()
        dialog_rect = pygame.Rect(10, 160, 300, 70)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        data = guard_dialogs[dialog_step]
        if current_time - dialog_last_tick > dialog_text_speed:
            if dialog_char_index < len(data["text"]):
                dialog_char_index += 1
            dialog_last_tick = current_time

        visible_text = data["text"][:dialog_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render(line, True, WHITE), (80, 168 + i * 12))

        if dialog_step == 2:
            if dialog_char_index >= len(data["text"]):
                screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))
        else:
            x = 85
            for i, choice in enumerate(data["choices"]):
                color = AUTUMN_YELLOW if i == dialog_choice else WHITE
                prefix = "* " if i == dialog_choice else "  "
                text = font.render(prefix + choice[0], True, color)
                screen_surface.blit(text, (x, 205))
                x += text.get_width() + 20
                
    elif current_state == STATE_BAHA_EVENT:
        cx, cy = -atrium_cam_x, -atrium_cam_y
        
        screen_surface.blit(layer_atrium, (cx, cy))
        
        drawables = []
        drawables.append((stoika_img, stoika_pos[0] + cx, stoika_pos[1] + cy, stoika_rect.bottom))
        drawables.append((guard_img, guard_pos[0] + cx, guard_pos[1] + cy, guard_rect.bottom))
        for i, pos in enumerate(turniket_positions):
            drawables.append((turniket_frames[0], pos[0] + cx, pos[1] + cy, pos[1] + turniket_frames[0].get_height()))
        drawables.append((current_anim[current_frame], player_rect.x - atrium_cam_x, player_rect.y - atrium_cam_y, player_hitbox.bottom))
        drawables.append((baha_current_anim[baha_frame], baha_x + cx, baha_y + cy, baha_y + baha_h))
        
        drawables.sort(key=lambda item: item[3])
        
        for item in drawables:
            screen_surface.blit(item[0], (item[1], item[2]))

        if baha_stage in (1, 2, 3):
            dialog_rect = pygame.Rect(10, 160, 300, 70)
            pygame.draw.rect(screen_surface, BLACK, dialog_rect)
            pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

            current_text_target = baha_texts[baha_stage - 1]
            if current_time - dialog_last_tick > dialog_text_speed:
                if dialog_char_index < len(current_text_target):
                    dialog_char_index += 1
                dialog_last_tick = current_time

            visible_text = current_text_target[:dialog_char_index]
            speaker_prefix = "* Баха: " if baha_stage == 1 else "* Охранник: "
            
            for i, line in enumerate(visible_text.split("\n")):
                screen_surface.blit(font.render(speaker_prefix + line if i == 0 else line, True, WHITE), (80, 168 + i * 12))

            if dialog_char_index >= len(current_text_target):
                screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == STATE_TRANSITION:
        elapsed = current_time - transition_start
        if transition_phase == "black":
            screen_surface.fill(BLACK)
            if elapsed >= BLACK_DURATION:
                transition_phase = "fadein"
                transition_start = current_time
        elif transition_phase == "fadein":
            if next_state_after_transition == STATE_ATRIUM:
                atrium_cam_x = player_rect.centerx - WIDTH // 2
                atrium_cam_y = player_rect.centery - HEIGHT // 2
                atrium_cam_x = max(0, min(atrium_cam_x, max(0, atrium_rect.width - WIDTH)))
                atrium_cam_y = max(0, min(atrium_cam_y, max(0, atrium_rect.height - HEIGHT)))
                draw_atrium()
            elif next_state_after_transition == STATE_CORIDOR:
                coridor_cam_x = player_rect.centerx - WIDTH // 2
                coridor_cam_y = player_rect.centery - HEIGHT // 2
                coridor_cam_x = max(0, min(coridor_cam_x, max(0, coridor_rect.width - WIDTH)))
                coridor_cam_y = max(0, min(coridor_cam_y, max(0, coridor_rect.height - HEIGHT)))
                draw_coridor()
            elif next_state_after_transition == STATE_LADDER:
                ladder_cam_x = player_rect.centerx - WIDTH // 2
                ladder_cam_y = player_rect.centery - HEIGHT // 2
                ladder_cam_x = max(0, min(ladder_cam_x, max(0, ladder_rect.width - WIDTH)))
                ladder_cam_y = max(0, min(ladder_cam_y, max(0, ladder_rect.height - HEIGHT)))
                draw_ladder()
            elif next_state_after_transition == STATE_CORIDOR2FLOOR:
                coridor2floor_cam_x = player_rect.centerx - WIDTH // 2
                coridor2floor_cam_y = player_rect.centery - HEIGHT // 2
                coridor2floor_cam_x = max(0, min(coridor2floor_cam_x, max(0, coridor2floor_rect.width - WIDTH)))
                coridor2floor_cam_y = max(0, min(coridor2floor_cam_y, max(0, coridor2floor_rect.height - HEIGHT)))
                draw_coridor2floor()
            elif next_state_after_transition == STATE_CORIDORFINAL:
                coridorfinal_cam_x = player_rect.centerx - WIDTH // 2
                coridorfinal_cam_y = player_rect.centery - HEIGHT // 2
                coridorfinal_cam_x = max(0, min(coridorfinal_cam_x, max(0, coridorfinal_rect.width - WIDTH)))
                coridorfinal_cam_y = max(0, min(coridorfinal_cam_y, max(0, coridorfinal_rect.height - HEIGHT)))
                draw_coridorfinal()
            elif next_state_after_transition == STATE_OFFICE:
                office_cam_x = player_rect.centerx - WIDTH // 2
                office_cam_y = player_rect.centery - HEIGHT // 2
                office_cam_x = max(0, min(office_cam_x, max(0, office_rect.width - WIDTH)))
                office_cam_y = max(0, min(office_cam_y, max(0, office_rect.height - HEIGHT)))
                draw_office()
            else:
                camera_x = player_rect.centerx - WIDTH // 2
                camera_y = player_rect.centery - HEIGHT // 2
                camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
                camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT)))
                draw_world()

            alpha = max(0, 255 - int(255 * elapsed / FADEIN_DURATION))
            fade_surface.set_alpha(alpha)
            screen_surface.blit(fade_surface, (0, 0))
            if elapsed >= FADEIN_DURATION:
                current_state = next_state_after_transition

    scaled = pygame.transform.scale(screen_surface, (WIDTH * SCALE, HEIGHT * SCALE))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    clock.tick(60)
