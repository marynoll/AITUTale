import pygame
import sys
import os
import math 
from settings import *
from data_manager import load_game_data, save_game_data
from utils import *
from dialogs import *
from battle import Battle

pygame.init()

screen_surface = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("AITUTALE")
clock = pygame.time.Clock()

main_menu_choice = 0            
title_2_start_time = 0 
save_menu_choice = 0
show_menu = False
current_bgm = None
next_bgm_queue = None
bgm_fade_timer = 0
current_battle = None  

game_data = load_game_data()
game_data["launch_count"] = game_data.get("launch_count", 0) + 1 

if "inventory" not in game_data: 
    game_data["inventory"] = []
if "has_saved" not in game_data: 
    game_data["has_saved"] = False

inventory = game_data["inventory"]
special_locker_opened = game_data.get("special_locker_opened", False)
save_game_data(game_data)
print(f"Игра запущена {game_data['launch_count']} раз(а)!")

try:
    font = pygame.font.Font(os.path.join("textures", "determination.ttf"), 12)
    choice_font = pygame.font.Font(os.path.join("textures", "determination.ttf"), 9)
    baha_font = pygame.font.Font(os.path.join("textures", "bahafront.ttf"), 14)
except:
    font = pygame.font.SysFont("arial", 16)
    choice_font = pygame.font.SysFont("arial", 12)
    baha_font = pygame.font.SysFont("arial", 16)

try:
    snd_battleappear = pygame.mixer.Sound(os.path.join("sounds", "battleappear.ogg"))
except:
    snd_battleappear = None    

try:
    snd_baha = pygame.mixer.Sound(os.path.join("sounds", "snd_baha.ogg"))
    snd_guard = pygame.mixer.Sound(os.path.join("sounds", "snd_guard.ogg"))
except:
    snd_baha = None
    snd_guard = None


try:
    snd_dramatic = pygame.mixer.Sound(os.path.join("sounds", "dramatic_beginning.ogg"))
except:
    snd_dramatic = None

# === ДОБАВЛЕННЫЕ ЗВУКИ ДВЕРЕЙ И ШАГОВ ===
try:
    snd_dooropen = pygame.mixer.Sound(os.path.join("sounds", "mus_dooropen.ogg"))
except:
    snd_dooropen = None

try:
    snd_doorclose = pygame.mixer.Sound(os.path.join("sounds", "mus_doorclose.ogg"))
except:
    snd_doorclose = None

try:
    snd_ladder = pygame.mixer.Sound(os.path.join("sounds", "ladder.ogg"))
except:
    snd_ladder = None

try:
    snd_steps = pygame.mixer.Sound(os.path.join("sounds", "steps.ogg"))
except:
    snd_steps = None

try:
    snd_savetouch = pygame.mixer.Sound(os.path.join("sounds", "savetouch.ogg"))
    snd_save = pygame.mixer.Sound(os.path.join("sounds", "snd_save.ogg"))
    snd_txt1 = pygame.mixer.Sound(os.path.join("sounds", "SND_TXT1.ogg"))
    snd_select = pygame.mixer.Sound(os.path.join("sounds", "snd_select.ogg"))
    snd_encounter = pygame.mixer.Sound(os.path.join("sounds", "enemy_encounter.ogg"))
except:
    snd_savetouch = snd_save = snd_txt1 = snd_select = None
# ==========================================

player_name = "Salim"
player_lv = game_data.get("player_lv", 1)
player_hp = game_data.get("player_hp", 20)
player_max_hp = 20

baha_defeated = game_data.get("baha_defeated", False)

title_image = load_texture_no_alpha('title.png')
if title_image.get_width() > 100: 
    title_image = pygame.transform.scale(title_image, (200, 40))
title_x = (WIDTH - 200) // 2
title_y = (HEIGHT - 40) // 2

try:
    img_game_over = load_texture('gameover.png')
    if img_game_over.get_width() > WIDTH:
        img_game_over = pygame.transform.scale(img_game_over, (WIDTH - 40, int((WIDTH - 40) / img_game_over.get_width() * img_game_over.get_height())))
except:
    img_game_over = pygame.Surface((200, 50))
    img_game_over.fill((255, 0, 0))

try:
    snd_shatter = pygame.mixer.Sound(os.path.join("sounds", "shatter.ogg"))
except:
    snd_shatter = None

game_over_timer = 0
gameover_heart_x = 0
gameover_heart_y = 0
shatter_played = False

layer_outside = load_texture('outside.png')  
layer_kurilka = load_texture('kurilka.png')
layer_tapok = load_texture('kurilkatapok.png') 
map_rect = layer_outside.get_rect()
layer_outside_col = load_texture('outside granitsa.png')
mask_outside = pygame.mask.from_surface(layer_outside_col)
collision_masks = [mask_outside]

layer_atrium = load_texture('HallDemoNoTur.png') 
atrium_rect = layer_atrium.get_rect()
mask_colisia_atrium = load_black_mask('colisiaatrium.png', layer_atrium.get_size())
mask_colisia_turniket = load_black_mask('colisiaturniket.png', layer_atrium.get_size())

layer_coridor = load_texture('coridor.png')
coridor_rect = layer_coridor.get_rect()
mask_colisia_coridor = load_black_mask('colisiacoridor.png', layer_coridor.get_size())

layer_ladder = load_texture('ladder.png')
ladder_rect = layer_ladder.get_rect()
mask_colisia_ladder = load_black_mask('colisialadder.png', layer_ladder.get_size())

layer_tables = load_texture('tables.png')
tables_real_rect = layer_tables.get_bounding_rect()

layer_coridor2floor = load_texture('coridor2floor.png')
coridor2floor_rect = layer_coridor2floor.get_rect()
mask_colisia_coridor2fl = load_black_mask('colisiacoridor2fl.png', layer_coridor2floor.get_size())

lockers2floor_img = load_texture('lockers.png')
lockers2floor_mask = pygame.mask.from_surface(lockers2floor_img)
lockers2floor_real_rect = lockers2floor_img.get_bounding_rect()

layer_coridorfinal = load_texture('coridorfinal.png')
coridorfinal_rect = layer_coridorfinal.get_rect()
mask_colisia_coridorfinal = load_black_mask('colisiacoridorfinal.png', layer_coridorfinal.get_size())

lockersfinal_img = load_texture('lockersfinalt.png')
lockersfinal_mask = pygame.mask.from_surface(lockersfinal_img)
lockersfinal_real_rect = lockersfinal_img.get_bounding_rect() 

speciallocker_img = load_texture('speciallocker.png')
speciallocker_mask = pygame.mask.from_surface(speciallocker_img)
speciallocker_real_rect = speciallocker_img.get_bounding_rect() 

specialdoor_img = load_texture('specialdoort.png')
specialdoor_mask = pygame.mask.from_surface(specialdoor_img)
specialdoor_real_rect = specialdoor_img.get_bounding_rect()

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

layer_office = load_texture('office.png')
office_rect = layer_office.get_rect()

mask_office = load_black_mask('colisiaoffice.png', layer_office.get_size())
mask_higher = load_black_mask('colisiahigher.png', layer_office.get_size())
mask_mid = load_black_mask('colisiamid.png', layer_office.get_size())
mask_lower = load_black_mask('colisialower.png', layer_office.get_size())

layer_comp = load_texture('comps1.png')
layer_comp2 = load_texture('comps2.png')
layer_specificcomp = load_texture('specificcomp.png')
img_pakett = load_texture('paketoffice.png')

rect_pakett = img_pakett.get_bounding_rect()
rect_specificcomp = layer_specificcomp.get_bounding_rect()
office_exit_zone = pygame.Rect(750, 480, 80, 80)

baha_in_office = False
office_baha_x = 0
office_baha_y = 0
office_baha_frame = 0
office_baha_char_index = 0
office_baha_dialog_step = 0
flash_start_time = 0

battle_sound_played = False

# ПЕРЕМЕННЫЕ ПОСЛЕ БИТВЫ В ОФИСЕ
post_battle_texts = []
post_battle_step = 0

# --- ПЕРЕМЕННЫЕ ДЛЯ КОНЦОВКИ ---
ending_baha_texts = [
    "Братишка, за такую доброту \nя тебе должен оплатить",
    "Поэтому....",
    "Поехали со мной на работу!"
]
ending_baha_step = 0
ending_fade_start = 0

try:
    sheet_silent = load_texture('BakhaNotTalking.png')
    rw = sheet_silent.get_width() // 4
    rh = sheet_silent.get_height()
    riding_frames_silent = [sheet_silent.subsurface((i * rw, 0, rw, rh)) for i in range(4)]
    
    sheet_talking = load_texture('BakhaTalking.png')
    riding_frames_talking = [sheet_talking.subsurface((i * rw, 0, rw, rh)) for i in range(4)]
except:
    dummy_r = pygame.Surface((200, 100))
    dummy_r.fill((100, 100, 100))
    riding_frames_silent = [dummy_r] * 4
    riding_frames_talking = [dummy_r] * 4

riding_anim_frame = 0
riding_anim_tick = 0
riding_timer = 0
riding_dialog_step = 0
riding_char_index = 0

riding_dialogs = [
    "Салим... вот как",
    "Приятно познакомиться.",
    "Я как вышел, этих типов встретил",
    "Парня ищут, сказали.\nДолг родине пора отдавать.",
    "Думали, погиб в аварии. Сбежать пытался.\nА нет, живучий оказался,\nв эту сторону побежал.",
    "Я сразу понял, про кого они.\nКак с тебя наушники то не слетели?",
    "PAUSE",
    "Подумал, просто так нового брата не отдам.",
    "Я не позволил бы случиться этому еще раз.",
    "PAUSE",
    "Как видишь, теперь ты свободен.\nМы все свободны. Я ни о чем не жалею.",
    "Пора заняться нашим истинным делом, Салим.\nНадевай курьерскую сумку."
]

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

guard_pos = (938, 516)
guard_rect = guard_img.get_rect(topleft=guard_pos)
guard_talk_rect = guard_rect.inflate(30, 30)

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


# ==========================================
# --- ЗАГРУЗКА ЛИЦ ДЛЯ ДИАЛОГОВ ---
# ==========================================
try:
    baha_face_sheet = load_texture('BahaSpriteTalking.png')
    fw = baha_face_sheet.get_width() // 2
    fh = baha_face_sheet.get_height()
    baha_faces = [
        pygame.transform.scale(baha_face_sheet.subsurface((0, 0, fw, fh)), (50, 50)),
        pygame.transform.scale(baha_face_sheet.subsurface((fw, 0, fw, fh)), (50, 50))
    ]
except:
    dummy_f = pygame.Surface((50, 50)); dummy_f.fill((0, 255, 0))
    baha_faces = [dummy_f, dummy_f]

try:
    guard_face_sheet = load_texture('GuardTalkingSprite.png')
    fw = guard_face_sheet.get_width() // 2
    fh = guard_face_sheet.get_height()
    guard_faces = [
        pygame.transform.scale(guard_face_sheet.subsurface((0, 0, fw, fh)), (50, 50)),
        pygame.transform.scale(guard_face_sheet.subsurface((fw, 0, fw, fh)), (50, 50))
    ]
except:
    dummy_f = pygame.Surface((50, 50)); dummy_f.fill((100, 100, 100))
    guard_faces = [dummy_f, dummy_f]

dialog_face_frame = 0
dialog_face_tick = 0
# ==========================================


try:
    stoika_img = load_texture('StoikaSWoman.png')
except:
    stoika_img = pygame.Surface((80, 90))
    stoika_img.fill((150, 150, 150))

# --- ВОЕНКОМ И КОНЦОВКА ---
try:
    voenkom_img = load_texture('voenkom.png')
except:
    voenkom_img = pygame.Surface((40, 20))
    voenkom_img.fill((100, 50, 50))


ending_timer = 0
    
stoika_pos = (atrium_rect.width // 2 - stoika_img.get_width() // 2, 0)
stoika_rect = stoika_img.get_bounding_rect()
stoika_rect.x += stoika_pos[0]
stoika_rect.y += stoika_pos[1]
stoika_hitbox = pygame.Rect(stoika_rect.x, stoika_rect.bottom - 40, stoika_rect.width, 40)

coridor_baha_x = 399
coridor_baha_y = 522
baha_in_coridor = True
coridor_baha_anim = baha_walk_down 
coridor_baha_frame = 0

current_state = "STATE_NEW_INTRO"
intro_start_time = pygame.time.get_ticks()
intro_sound_played = False

turniket_closed = True 
is_behind_turniket = False

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

post_baha_char_index = 0
guard_choice = 0
dialog_choice = 0
dialog_step = 0
guard_talk_count = 0

lockers_dialog_char_index = 0
special_locker_char_index = 0
special_locker_text = ""

office_dialog_text = ""
office_dialog_char_index = 0
office_dialog_choices = []
office_dialog_choice_idx = 0
office_dialog_speaker = ""

current_slide = 0
char_index = 0
text_speed = 50

door_zone_1 = pygame.Rect(775, 74, 70, 94) 
door_zone_2 = pygame.Rect(557, 74, 70, 94) 

coridor_door_zone_1 = pygame.Rect(709, 38, 103, 94) 
coridor_door_zone_2 = pygame.Rect(220, 38, 103, 94) 
ladder_door_zone = pygame.Rect(28, 566, 5, 147) 
to_2floor_zone = pygame.Rect(524, 305, 121, 93) 
cabinet_door_zone = pygame.Rect(184, 719 , 109, 9)

# --- ЗОНЫ ДЛЯ ПРИКОЛОВ В КОРИДОРЕ ---
coridor_joke_door = pygame.Rect(458, 507, 113, 94)
coridor_joke_pic1 = pygame.Rect(49, 507, 163, 94)
coridor_joke_pic2 = pygame.Rect(814, 507, 163, 94)
coridor_inspect_text = ""
coridor_inspect_char_index = 0
# ------------------------------------


c2f_pic = pygame.Rect(814, 505, 163, 94)         # Картина
c2f_door1 = pygame.Rect(458, 505, 114, 94)       # Дверь 1
c2f_pass1 = pygame.Rect(311, 505, 76, 60)        # Проход 1
c2f_pass2 = pygame.Rect(644, 505, 76, 60)        # Проход 2
c2f_door2 = pygame.Rect(96, 505, 52, 94)         # Дверь 2
c2f_inspect_text = ""
c2f_inspect_char_index = 0

target_spawn_atrium = 1  
target_spawn_coridor = 1 

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

player_surf_mask_full = pygame.Surface((SCALE_W, SCALE_H), pygame.SRCALPHA)
player_surf_mask_full.fill((255, 255, 255, 255))
player_mask_full = pygame.mask.from_surface(player_surf_mask_full)

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

# --- ФУНКЦИИ ОТРИСОВКИ ---
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
        drawables.append((coridor_baha_anim[coridor_baha_frame], coridor_baha_x - coridor_cam_x, coridor_baha_y - coridor_cam_y, coridor_baha_y + baha_h))
        
    drawables.append((current_anim[current_frame], player_rect.x - coridor_cam_x, player_rect.y - coridor_cam_y, player_hitbox.bottom))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_ladder():
    cx, cy = -ladder_cam_x, -ladder_cam_y
    screen_surface.blit(layer_ladder, (cx, cy))
    
    drawables = []
    
    # Добавляем столы в список для отрисовки
    if tables_real_rect.height > 0:
        drawables.append((layer_tables, cx, cy, tables_real_rect.bottom))
        
    # Добавляем игрока
    drawables.append((current_anim[current_frame], player_rect.x - ladder_cam_x, player_rect.y - ladder_cam_y, player_hitbox.bottom))
    
    # Сортируем: кто находится ниже по экрану (Y), тот рисуется поверх остальных
    drawables.sort(key=lambda item: item[3])
    
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

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

    drawables.append((savepoint_frames[savepoint_frame_idx], savepoint_pos[0] + cx, savepoint_pos[1] + cy, savepoint_pos[1] + savepoint_frames[0].get_height()))
    drawables.append((current_anim[current_frame], player_rect.x - coridorfinal_cam_x, player_rect.y - coridorfinal_cam_y, player_hitbox.bottom))
    
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def draw_office():
    cx, cy = -office_cam_x, -office_cam_y
    screen_surface.blit(layer_office, (cx, cy))
    
    drawables = []
    drawables.append((layer_specificcomp, cx, cy, 429))
    drawables.append((layer_comp2, cx, cy, 430))
    drawables.append((layer_comp, cx, cy, 560))
    drawables.append((img_pakett, cx, cy, 560))
    drawables.append((current_anim[current_frame], player_rect.x - office_cam_x, player_rect.y - office_cam_y, player_hitbox.bottom))
    
    if baha_in_office:
        drawables.append((baha_current_anim[office_baha_frame], office_baha_x - office_cam_x, office_baha_y - office_cam_y, office_baha_y + baha_h))
        
    drawables.sort(key=lambda item: item[3])
    for item in drawables:
        screen_surface.blit(item[0], (item[1], item[2]))

def start_transition(next_state):
    global transition_start, transition_phase, next_state_after_transition, current_state
    transition_start = pygame.time.get_ticks()
    transition_phase = "black"
    next_state_after_transition = next_state
    current_state = STATE_TRANSITION

def draw_lockers_dialog():
    global lockers_dialog_char_index, dialog_last_tick
    dialog_rect = pygame.Rect(10, 150, 300, 80)
    pygame.draw.rect(screen_surface, BLACK, dialog_rect)
    pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
    
    if current_time - dialog_last_tick > dialog_text_speed:
        if lockers_dialog_char_index < len(lockers_text):
            # --- ДОБАВЛЕН ЗВУК ТЕКСТА ---
            if lockers_text[lockers_dialog_char_index] not in [" ", "\n"]:
                if snd_txt1:
                    snd_txt1.stop()
                    snd_txt1.play()
            lockers_dialog_char_index += 1
        dialog_last_tick = current_time # Исправлен таймер
        
    visible_text = lockers_text[:lockers_dialog_char_index]
    screen_surface.blit(font.render("* " + visible_text, True, WHITE), (20, 158))

def draw_special_locker_dialog():
    global special_locker_char_index, dialog_last_tick
    dialog_rect = pygame.Rect(10, 150, 300, 80)
    pygame.draw.rect(screen_surface, BLACK, dialog_rect)
    pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
    
    if current_time - dialog_last_tick > dialog_text_speed:
        if special_locker_char_index < len(special_locker_text):
            # --- ДОБАВЛЕН ЗВУК ТЕКСТА ---
            if special_locker_text[special_locker_char_index] not in [" ", "\n"]:
                if snd_txt1:
                    snd_txt1.stop()
                    snd_txt1.play()
            special_locker_char_index += 1
        dialog_last_tick = current_time # Исправлен таймер
        
    visible_text = special_locker_text[:special_locker_char_index]
    screen_surface.blit(font.render("* " + visible_text, True, WHITE), (20, 158))
# ==========================================
# --- ГЛАВНЫЙ ЦИКЛ ---
# ==========================================
while True:
    screen_surface.fill(BLACK)
    current_time = pygame.time.get_ticks()

    # === УМНАЯ СИСТЕМА ФОНОВОЙ МУЗЫКИ С ПЛАВНЫМИ ПЕРЕХОДАМИ ===
    # Если у нас сейчас затемнение экрана (переход), смотрим на следующую локацию,
    # чтобы музыка начала меняться ЗАРАНЕЕ, вместе с экраном.
    test_state = next_state_after_transition if current_state == STATE_TRANSITION else current_state
    target_bgm = None
    
    # 1. Улица (И менюшка входа в дверь тоже оставляет уличную музыку)
    if test_state in ["STATE_NEW_GAME_CUTSCENE", STATE_GAME, STATE_DOOR]:
        target_bgm = "confusing place.ogg"
        
    # 2. Внутри здания (Атриум, коридоры, лестница, и все их менюшки/диалоги)
    elif test_state in [
        STATE_ATRIUM, STATE_CORIDOR, STATE_LADDER, STATE_CORIDOR2FLOOR, STATE_CORIDORFINAL,
        STATE_GUARD_CHOICE, STATE_GUARD_FIRST, STATE_GUARD_DIALOG, STATE_GUARD_POST_BAHA,
        STATE_BAHA_EVENT, STATE_CORIDOR_BAHA_DIALOG, STATE_CORIDOR_BAHA_RUN,
        STATE_LOCKERS_DIALOG, STATE_SPECIAL_LOCKER_DIALOG,
        "CORIDOR_INSPECT", "CORIDOR2FLOOR_INSPECT",
        STATE_CORIDOR_DOOR, STATE_LADDER_DOOR, STATE_CORIDOR2FLOOR_DOOR, STATE_CABINET_DOOR,
        STATE_SAVE_MENU
    ]:
        target_bgm = "totally not hotel from undertale.ogg"
        
    # 3. Офис и сцена снаружи перед концовкой (Без музыки)
    # 3. Офис и сцена снаружи перед концовкой (Без музыки)
    elif test_state in [
        STATE_OFFICE, STATE_PAKETT_DIALOG, STATE_SPECIFICCOMP_DIALOG, 
        "OFFICE_BAHA_POST_BATTLE", "OFFICE_BAHA_LEAVES",
        "ENDING_OUTSIDE_WALK", "ENDING_EXCLAMATION", "ENDING_PAN_CAMERA", "ENDING_OUTSIDE_DIALOG", "ENDING_FADE_OUT"
    ]:
        target_bgm = "STOP" # ИСПРАВЛЕНО ЗДЕСЬ
        
    # 4. Наезд камеры на Баху в офисе (Страшная музыка)
    elif test_state in [STATE_OFFICE_BAHA_EVENT_START, STATE_OFFICE_BAHA_DIALOG_1, STATE_OFFICE_BAHA_WALK, STATE_OFFICE_BAHA_DIALOG_2]:
        target_bgm = "In_My_Way_Genocide.ogg"
        
    # 5. Возврат камеры обратно к Салиму (Плавное затухание страшной музыки)
    elif test_state in ["OFFICE_CAMERA_TO_PLAYER", "OFFICE_BAHA_RUN_TO_PLAYER", "OFFICE_BAHA_HEART_BLINK", "OFFICE_BAHA_HEART_MOVE"]:
        target_bgm = "fade_out"
        
    # 6. Концовка в машине
    elif test_state in ["RIDING_CUTSCENE_SILENCE", "RIDING_CUTSCENE_DIALOG", "RIDING_FADE_OUT"]:
        target_bgm = "undertale.ogg"
        
    # Исключения: Стейты, которые САМИ управляют своей музыкой (битва, смерть, меню запуска)
    elif test_state in [STATE_BATTLE, STATE_GAMEOVER_ANIM, "GAMEOVER_FADE_IN_LOGO", "GAMEOVER_TEXT", "GAMEOVER_WAIT_INPUT", "GAMEOVER_FADE_OUT", "GAMEOVER_RESTART", "STATE_NEW_INTRO", STATE_TITLE_2, STATE_MAIN_MENU, "AITUTALE_LOGO", "RESET_GAME_TO_TITLE"]:
        target_bgm = "ignore"


    # --- ЛОГИКА ПЛЕЕРА И ПЛАВНЫХ ПЕРЕХОДОВ ---
    if target_bgm != "ignore":
        # Если нужна новая песня, и мы её еще не начали грузить
        if target_bgm != current_bgm and target_bgm != next_bgm_queue:
            if current_bgm is not None and current_bgm != "fade_out":
                # Запускаем плавное затухание старого трека (1 секунда)
                pygame.mixer.music.fadeout(1000) 
                bgm_fade_timer = current_time
                next_bgm_queue = target_bgm
            else:
                # Если ничего не играло, переключаем моментально
                next_bgm_queue = target_bgm
                bgm_fade_timer = 0
                
        # Ждем 1 секунду, пока старый трек полностью затухнет, затем включаем новый
        if next_bgm_queue is not None and current_time - bgm_fade_timer > 1000:
            if next_bgm_queue == "fade_out" or next_bgm_queue == "STOP": # ИСПРАВЛЕНО ЗДЕСЬ
                pygame.mixer.music.stop()
                current_bgm = next_bgm_queue
            else:
                try:
                    path = os.path.join("sounds", next_bgm_queue)
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(1.0)
                    # fade_ms=1000 делает так, что НОВЫЙ трек плавно нарастает (Fade-in)
                    pygame.mixer.music.play(-1, fade_ms=1000) 
                    current_bgm = next_bgm_queue
                except Exception as e:
                    print(f"[Музыка] Ошибка загрузки {next_bgm_queue}: {e}")
                    current_bgm = next_bgm_queue
            
            next_bgm_queue = None
    # ==============================================================
    if current_time - savepoint_anim_tick > 200:
        savepoint_frame_idx = (savepoint_frame_idx + 1) % len(savepoint_frames)
        savepoint_anim_tick = current_time

    # --- ТАЙМЕР АНИМАЦИИ ГОВОРЯЩИХ ЛИЦ ---
    if current_time - dialog_face_tick > 150:
        dialog_face_frame = (dialog_face_frame + 1) % 2
        dialog_face_tick = current_time

    # ==========================================
    # 1. ОБРАБОТКА ИВЕНТОВ (КНОПОК)
    # ==========================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(game_data)
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and current_state == STATE_BATTLE:
            if current_battle:
                current_battle.handle_event(event)
                
        elif event.type == pygame.KEYDOWN and current_state == "OFFICE_BAHA_POST_BATTLE":
            if event.key in (pygame.K_RETURN, pygame.K_z):
                if office_baha_char_index >= len(post_battle_texts[post_battle_step]):
                    post_battle_step += 1
                    if post_battle_step >= len(post_battle_texts):
                        current_state = "OFFICE_BAHA_LEAVES"
                        baha_last_anim_tick = pygame.time.get_ticks()
                        baha_current_anim = baha_walk_right
                        office_baha_frame = 0
                    else:
                        office_baha_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == STATE_DOOR:
            if event.key == pygame.K_LEFT: 
                door_choice = 0
            elif event.key == pygame.K_RIGHT: 
                door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if door_choice == 0:
                    if target_spawn_atrium == 1:
                        player_rect.x = SPAWN_ATRIUM_1_X
                        player_rect.y = SPAWN_ATRIUM_1_Y
                    else:
                        player_rect.x = SPAWN_ATRIUM_2_X
                        player_rect.y = SPAWN_ATRIUM_2_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    is_behind_turniket = False
                    if snd_dooropen: snd_dooropen.play() # ДОБАВИТЬ ЭТУ СТРОКУ
                    start_transition(STATE_ATRIUM)
                else:
                    current_state = STATE_GAME
                door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_GAME
                door_choice = 0

        

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR_DOOR:
            if event.key == pygame.K_LEFT: 
                coridor_door_choice = 0
            elif event.key == pygame.K_RIGHT: 
                coridor_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if coridor_door_choice == 0:
                    if target_spawn_coridor == 1:
                        player_rect.x = SPAWN_CORIDOR_1_X
                        player_rect.y = SPAWN_CORIDOR_1_Y
                    else:
                        player_rect.x = SPAWN_CORIDOR_2_X
                        player_rect.y = SPAWN_CORIDOR_2_Y
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
            if event.key == pygame.K_LEFT: 
                ladder_door_choice = 0
            elif event.key == pygame.K_RIGHT: 
                ladder_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if ladder_door_choice == 0:
                    player_rect.x = SPAWN_LADDER_X
                    player_rect.y = SPAWN_LADDER_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    if snd_dooropen: snd_dooropen.play() # ДОБАВИТЬ ЭТУ СТРОКУ
                    start_transition(STATE_LADDER)
                else:
                    current_state = STATE_CORIDOR
                ladder_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDOR
                ladder_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR2FLOOR_DOOR:
            if event.key == pygame.K_LEFT: 
                coridor2floor_door_choice = 0
            elif event.key == pygame.K_RIGHT: 
                coridor2floor_door_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if coridor2floor_door_choice == 0:
                    player_rect.x = SPAWN_CORIDOR2FLOOR_X
                    player_rect.y = SPAWN_CORIDOR2FLOOR_Y
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    if snd_ladder: snd_ladder.play() # ДОБАВИТЬ ЭТУ СТРОКУ
                    start_transition(STATE_CORIDOR2FLOOR)
                else:
                    current_state = STATE_LADDER
                coridor2floor_door_choice = 0
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_LADDER
                coridor2floor_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == STATE_CABINET_DOOR:
            if event.key == pygame.K_LEFT: 
                cabinet_door_choice = 0
            elif event.key == pygame.K_RIGHT: 
                cabinet_door_choice = 1
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

        elif event.type == pygame.KEYDOWN and current_state in (STATE_PAKETT_DIALOG, STATE_SPECIFICCOMP_DIALOG):
            if office_dialog_choices:
                if event.key == pygame.K_LEFT: 
                    office_dialog_choice_idx = max(0, office_dialog_choice_idx - 1)
                elif event.key == pygame.K_RIGHT: 
                    office_dialog_choice_idx = min(len(office_dialog_choices) - 1, office_dialog_choice_idx + 1)
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
            if event.key == pygame.K_LEFT: 
                guard_choice = 0
            elif event.key == pygame.K_RIGHT: 
                guard_choice = 1
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
                if snd_select: snd_select.play()
            elif event.key == pygame.K_RIGHT and choices:
                dialog_choice = min(len(choices) - 1, dialog_choice + 1)
                if snd_select: snd_select.play()
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
                if snd_select: snd_select.play()
            elif event.key == pygame.K_RIGHT and data["choices"]:
                dialog_choice = min(len(data["choices"]) - 1, dialog_choice + 1)
                if snd_select: snd_select.play()
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

        elif event.type == pygame.KEYDOWN and current_state == STATE_OFFICE_BAHA_DIALOG_1:
            if event.key in (pygame.K_RETURN, pygame.K_z):
                if office_baha_char_index >= len(office_baha_dialog_1[office_baha_dialog_step]):
                    office_baha_dialog_step += 1
                    if office_baha_dialog_step >= len(office_baha_dialog_1):
                        current_state = STATE_OFFICE_BAHA_WALK
                        if snd_steps: snd_steps.play(loops=-1) # <--- ЗАПУСКАЕМ ШАГИ
                    else:
                        office_baha_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == STATE_OFFICE_BAHA_DIALOG_2:
            if event.key in (pygame.K_RETURN, pygame.K_z):
                if office_baha_char_index >= len(office_baha_dialog_2[office_baha_dialog_step]):
                    office_baha_dialog_step += 1
                    if office_baha_dialog_step >= len(office_baha_dialog_2):
                        current_state = "OFFICE_CAMERA_TO_PLAYER"
                    else:
                        office_baha_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == "GAMEOVER_WAIT_INPUT":
            if event.key in (pygame.K_RETURN, pygame.K_z):
                # Нажали Enter - запускаем плавное затухание
                current_state = "GAMEOVER_FADE_OUT"
                game_over_timer = pygame.time.get_ticks()

        elif event.type == pygame.KEYDOWN and current_state == "STATE_NEW_GAME_CUTSCENE":
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                # Если текст напечатался, идем к следующей фразе
                if cutscene_char_index >= len(cutscene_text):
                    if cutscene_step == 0:
                        cutscene_step = 1
                        cutscene_text = "Голова болит..."
                        cutscene_char_index = 0
                        dialog_last_tick = current_time
                        current_anim = walk_down # Смотрит вниз
                        current_frame = 0
                    elif cutscene_step == 1:
                        cutscene_step = 2
                        cutscene_text = "Нагнетающее чувство тревоги оставляет\nмне только единственный выбор."
                        cutscene_char_index = 0
                        dialog_last_tick = current_time
                    elif cutscene_step == 2:
                        cutscene_step = 3
                        cutscene_text = "Войти в это здание любой ценой."
                        cutscene_char_index = 0
                        dialog_last_tick = current_time
                        current_anim = walk_up # Смотрит вверх
                        current_frame = 0
                    elif cutscene_step == 3:
                        # Заканчиваем катсцену, отдаем управление
                        current_state = STATE_GAME
                else:
                    # Пропуск печати текста (вывести сразу всё)
                    cutscene_char_index = len(cutscene_text)
                    
        elif event.type == pygame.KEYDOWN and current_state == STATE_GAME:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if door_zone_1.colliderect(player_hitbox):
                    current_state = STATE_DOOR
                    door_choice = 0
                    target_spawn_atrium = 1
                elif door_zone_2.colliderect(player_hitbox):
                    current_state = STATE_DOOR
                    door_choice = 0
                    target_spawn_atrium = 2

        elif event.type == pygame.KEYDOWN and current_state == STATE_ATRIUM:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                if player_hitbox.colliderect(guard_talk_rect):
                    current_state = STATE_GUARD_CHOICE
                    guard_choice = 0
                elif coridor_door_zone_1.colliderect(player_hitbox):
                    current_state = STATE_CORIDOR_DOOR
                    coridor_door_choice = 0
                    target_spawn_coridor = 1
                elif coridor_door_zone_2.colliderect(player_hitbox):
                    current_state = STATE_CORIDOR_DOOR
                    coridor_door_choice = 0
                    target_spawn_coridor = 2

        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDOR:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if baha_in_coridor:
                    coridor_baha_talk_rect = pygame.Rect(coridor_baha_x - 15, coridor_baha_y - 15, baha_w + 30, baha_h + 30)
                    if player_hitbox.colliderect(coridor_baha_talk_rect):
                        current_state = STATE_CORIDOR_BAHA_DIALOG
                        dialog_step = 0
                        dialog_choice = 0
                        dialog_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
                        continue 
                
                if coridor_joke_door.colliderect(player_hitbox):
                    current_state = "CORIDOR_INSPECT"
                    coridor_inspect_text = "Мне нужно в кабинет."
                    coridor_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif coridor_joke_pic1.colliderect(player_hitbox):
                    current_state = "CORIDOR_INSPECT"
                    coridor_inspect_text = "О это ведь...!\nЗабыл. Знакомое лицо."
                    coridor_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif coridor_joke_pic2.colliderect(player_hitbox):
                    current_state = "CORIDOR_INSPECT"
                    coridor_inspect_text = "Влюбленная пара...\nочень знакомая."
                    coridor_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()

                elif ladder_door_zone.colliderect(player_hitbox):
                    if not baha_in_coridor:
                        current_state = STATE_LADDER_DOOR
                        ladder_door_choice = 0

        elif event.type == pygame.KEYDOWN and current_state == "CORIDOR_INSPECT":
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if coridor_inspect_char_index >= len(coridor_inspect_text):
                    current_state = STATE_CORIDOR
                    coridor_inspect_char_index = 0
                else:
                    coridor_inspect_char_index = len(coridor_inspect_text)

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
                # --- ПРОВЕРКА ПРИКОЛОВ 2 ЭТАЖА ---
                elif c2f_pic.colliderect(player_hitbox):
                    current_state = "CORIDOR2FLOOR_INSPECT"
                    c2f_inspect_text = "Команда мечты."
                    c2f_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif c2f_door1.colliderect(player_hitbox):
                    current_state = "CORIDOR2FLOOR_INSPECT"
                    c2f_inspect_text = "Мне нужно в кабинет."
                    c2f_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif c2f_pass1.colliderect(player_hitbox) or c2f_pass2.colliderect(player_hitbox):
                    current_state = "CORIDOR2FLOOR_INSPECT"
                    c2f_inspect_text = "Странно, проход закрыт лентами."
                    c2f_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                elif c2f_door2.colliderect(player_hitbox):
                    current_state = "CORIDOR2FLOOR_INSPECT"
                    c2f_inspect_text = "Идет урок!"
                    c2f_inspect_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()

        # === ЗАКРЫТИЕ ДИАЛОГА НА ENTER ===
        elif event.type == pygame.KEYDOWN and current_state == "CORIDOR2FLOOR_INSPECT":
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if c2f_inspect_char_index >= len(c2f_inspect_text):
                    current_state = STATE_CORIDOR2FLOOR
                    c2f_inspect_char_index = 0
                else:
                    c2f_inspect_char_index = len(c2f_inspect_text)
                    
        elif event.type == pygame.KEYDOWN and current_state == STATE_CORIDORFINAL:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key == pygame.K_ESCAPE:
                start_transition(STATE_CORIDOR2FLOOR)
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                
                # 1. Проверка сохранения
                if savepoint_rect.inflate(20, 20).colliderect(player_hitbox):
                    if snd_savetouch: snd_savetouch.play()
                    current_state = STATE_SAVE_MENU
                    save_menu_choice = 0
                    
                # 2. Проверка входа в Офис (specialdoor)
                elif specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                     specialdoor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    # Координаты спавна в офисе (возле двери)
                    player_rect.x = 750  
                    player_rect.y = 450
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    if snd_dooropen: snd_dooropen.play()
                    start_transition(STATE_OFFICE)
                    
                # 3. Проверка специального шкафчика
                elif speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                     speciallocker_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    current_state = STATE_SPECIAL_LOCKER_DIALOG
                    special_locker_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                    
                    # НОВАЯ ЛОГИКА ВЫДАЧИ:
                    if not special_locker_opened:
                        special_locker_text = "Вы нашли Секретные файлы!"
                        inventory.append("Секретные файлы")
                        special_locker_opened = True
                    else:
                        special_locker_text = "Пусто."
                    
                # 4. Проверка остальных шкафчиков
                elif lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
                     lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
                    current_state = STATE_LOCKERS_DIALOG
                    lockers_dialog_char_index = 0
                    dialog_last_tick = pygame.time.get_ticks()
                # ... остальной код входа в двери и шкафчиков ...

        elif event.type == pygame.KEYDOWN and current_state == STATE_SAVE_MENU:
            if event.key == pygame.K_LEFT:
                save_menu_choice = 0
                if snd_select: snd_select.play() # <--- ЗВУК ВЫБОРА
            elif event.key == pygame.K_RIGHT:
                save_menu_choice = 1
                if snd_select: snd_select.play() # <--- ЗВУК ВЫБОРА
            elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                if save_menu_choice == 0:
                    game_data["inventory"] = inventory
                    game_data["has_saved"] = True
                    game_data["player_lv"] = player_lv
                    game_data["player_hp"] = player_hp
                    game_data["baha_defeated"] = baha_defeated
                    
                    game_data["special_locker_opened"] = special_locker_opened # <--- ДОБАВИТЬ ЭТУ СТРОКУ
                    
                    save_game_data(game_data)
                    
                    if snd_save: snd_save.play() # <--- ЗВУК УСПЕШНОГО СОХРАНЕНИЯ
                    current_state = "STATE_SAVE_DONE" # <--- ПЕРЕХОД НА НОВЫЙ ЭКРАН
                else:
                    current_state = STATE_CORIDORFINAL
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDORFINAL

        # --- НОВЫЙ БЛОК ДЛЯ ЗАКРЫТИЯ ОКНА "File saved." ---
        elif event.type == pygame.KEYDOWN and current_state == "STATE_SAVE_DONE":
            if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE, pygame.K_ESCAPE):
                current_state = STATE_CORIDORFINAL

        elif event.type == pygame.KEYDOWN and current_state == STATE_SAVE_MENU:
            if event.key == pygame.K_LEFT:
                save_menu_choice = 0
            elif event.key == pygame.K_RIGHT:
                save_menu_choice = 1
            elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                if save_menu_choice == 0:
                    game_data["inventory"] = inventory
                    game_data["has_saved"] = True
                    game_data["player_lv"] = player_lv
                    game_data["player_hp"] = player_hp
                    game_data["baha_defeated"] = baha_defeated
                    save_game_data(game_data)
                    current_state = STATE_CORIDORFINAL
                else:
                    current_state = STATE_CORIDORFINAL
            elif event.key == pygame.K_ESCAPE:
                current_state = STATE_CORIDORFINAL

        elif event.type == pygame.KEYDOWN and current_state == STATE_OFFICE:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                show_menu = not show_menu
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                interact_rect_pakett = rect_pakett.inflate(40, 40) if rect_pakett.width > 0 else pygame.Rect(0,0,0,0)
                interact_rect_spec = rect_specificcomp.inflate(40, 40) if rect_specificcomp.width > 0 else pygame.Rect(0,0,0,0)
                
                if interact_rect_pakett.colliderect(player_hitbox):
                    current_state = STATE_PAKETT_DIALOG
                    office_dialog_text = "Кто то оставил пакет с весом будто в тонну"
                    office_dialog_choices = []
                    office_dialog_char_index = 0
                    office_dialog_speaker = ""
                    dialog_last_tick = pygame.time.get_ticks()
                
                elif interact_rect_spec.colliderect(player_hitbox):
                    if not baha_defeated:
                        # --- ИЗМЕНЕННЫЙ БЛОК ---
                        current_state = "STATE_OFFICE_DOORCLOSE" # Сначала закрывается дверь
                        office_timer = pygame.time.get_ticks()     
                        if snd_doorclose: snd_doorclose.play()   
                        
                        current_anim = walk_right
                        current_frame = 0
                        baha_in_office = True       
                        office_baha_x = 771
                        office_baha_y = 385  
                        baha_current_anim = baha_walk_left
                        office_baha_frame = 0
                    else:
                        current_state = STATE_SPECIFICCOMP_DIALOG
                        office_dialog_text = "* Компьютер выключен.\n* Кажется, здесь больше нечего делать."
                        office_dialog_choices = []
                        office_dialog_char_index = 0
                        office_dialog_speaker = ""
                        dialog_last_tick = pygame.time.get_ticks()

                elif office_exit_zone.colliderect(player_hitbox):
                    if baha_defeated:
                        # Запускаем концовку
                        player_rect.x = 570
                        player_rect.y = 75
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        current_anim = walk_down
                        current_frame = 0
                        
                        baha_x = 862
                        baha_y = 134
                        baha_current_anim = baha_walk_left  # Баха смотрит на Салима (налево)
                        baha_frame = 0
                        
                        ending_baha_step = 0
                        office_baha_char_index = 0
                        
                        start_transition("ENDING_OUTSIDE_WALK")
                    else:
                        # Обычный выход
                        player_rect.x = SPAWN_CORIDORFINAL_X
                        player_rect.y = SPAWN_CORIDORFINAL_Y
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        start_transition(STATE_CORIDORFINAL)


        elif event.type == pygame.KEYDOWN and current_state == "ENDING_OUTSIDE_DIALOG":
            if event.key in (pygame.K_RETURN, pygame.K_z):
                if office_baha_char_index >= len(ending_baha_texts[ending_baha_step]):
                    ending_baha_step += 1
                    if ending_baha_step >= len(ending_baha_texts):
                        current_state = "ENDING_FADE_OUT"
                        ending_fade_start = pygame.time.get_ticks()
                    else:
                        office_baha_char_index = 0
                        dialog_last_tick = pygame.time.get_ticks()
        # ------------------------------------------------

        
                        
        elif event.type == pygame.KEYDOWN and current_state == "AITUTALE_LOGO":
            # Позволяем пропустить титры по нажатию
            if event.key in (pygame.K_RETURN, pygame.K_z):
                current_state = "RESET_GAME_TO_TITLE"

        elif event.type == pygame.KEYDOWN and current_state == "STATE_NEW_INTRO":
            # Игрок может скипнуть заставку нажав ENTER, ПРОБЕЛ или ESC
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z, pygame.K_ESCAPE):
                if snd_dramatic:
                    snd_dramatic.stop()
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
                        baha_defeated = game_data.get("baha_defeated", False)
                        player_lv = game_data.get("player_lv", 1)
                        
                        player_rect.x = SPAWN_SAVE_CONTINUE_X
                        player_rect.y = SPAWN_SAVE_CONTINUE_Y
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        start_transition(STATE_CORIDORFINAL)
                    else:
                        # ЕСЛИ НЕТ СОХРАНЕНИЙ И МЫ НАЖАЛИ PLAY (Левая кнопка)
                        player_rect.x = map_rect.width // 2
                        player_rect.y = map_rect.height - SCALE_H - 50
                        player_hitbox.centerx = player_rect.centerx
                        player_hitbox.bottom = player_rect.bottom
                        
                        cutscene_step = 0
                        cutscene_char_index = 0
                        cutscene_text = "...Где я?"
                        cutscene_timer = pygame.time.get_ticks()
                        dialog_last_tick = pygame.time.get_ticks()
                        start_transition("STATE_NEW_GAME_CUTSCENE")
                        
                elif main_menu_choice == 1: 
                    # ЕСЛИ МЫ НАЖАЛИ RESET (Правая кнопка)
                    game_data["launch_count"] = 1
                    game_data["player_lv"] = 1
                    game_data["player_hp"] = 20
                    game_data["inventory"] = []
                    game_data["has_saved"] = False
                    game_data["baha_defeated"] = False 
                    game_data["special_locker_opened"] = False
                    
                    inventory.clear()
                    player_lv = 1
                    player_hp = 20
                    baha_defeated = False 
                    special_locker_opened = False
                    save_game_data(game_data)
                    
                    player_rect.x = map_rect.width // 2
                    player_rect.y = map_rect.height - SCALE_H - 50
                    player_hitbox.centerx = player_rect.centerx
                    player_hitbox.bottom = player_rect.bottom
                    
                    cutscene_step = 0
                    cutscene_char_index = 0
                    cutscene_text = "...Где я?"
                    cutscene_timer = pygame.time.get_ticks()
                    dialog_last_tick = pygame.time.get_ticks()
                    start_transition("STATE_NEW_GAME_CUTSCENE")


    # ==========================================
    # 2. ЛОГИКА ДВИЖЕНИЯ И АНИМАЦИИ (Вычисления, без графики)
    # ==========================================

    if current_state == "STATE_NEW_GAME_CUTSCENE":
        camera_x = player_rect.centerx - WIDTH // 2
        camera_y = player_rect.centery - HEIGHT // 2
        camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
        camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT)))
        
        # Салим крутится только на нулевом шаге (когда спрашивает "Где я?")
        if cutscene_step == 0:
            elapsed_turn = current_time - cutscene_timer
            if elapsed_turn < 600:
                current_anim = walk_down
            elif elapsed_turn < 1200:
                current_anim = walk_left
            elif elapsed_turn < 1800:
                current_anim = walk_up
            elif elapsed_turn < 2400:
                current_anim = walk_right
            else:
                current_anim = walk_down # Возвращается в исходное
            current_frame = 0


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
        
    elif current_state == STATE_OFFICE:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        old_anim = current_anim

        if keys[pygame.K_LEFT]: dx = -player_speed; current_anim = walk_left
        elif keys[pygame.K_RIGHT]: dx = player_speed; current_anim = walk_right
        if keys[pygame.K_UP]: dy = -player_speed; current_anim = walk_up
        elif keys[pygame.K_DOWN]: dy = player_speed; current_anim = walk_down

        is_moving = (dx != 0 or dy != 0)

        def check_office_collision(px, py):
            future_bottom = py + SCALE_H
            if mask_office.overlap(player_mask_full, (px, py)): return True
            if future_bottom < 430:
                if mask_higher.overlap(player_mask_full, (px, py)): return True
            elif future_bottom < 560:
                if mask_mid.overlap(player_mask_full, (px, py)): return True
            else:
                if mask_lower.overlap(player_mask_full, (px, py)): return True
            return False

        if dx != 0:
            player_rect.x += dx
            if check_office_collision(player_rect.x, player_rect.y) or player_rect.left < 0 or player_rect.right > office_rect.width: 
                player_rect.x -= dx
        if dy != 0:
            player_rect.y += dy
            if check_office_collision(player_rect.x, player_rect.y) or player_rect.top < 0 or player_rect.bottom > office_rect.height: 
                player_rect.y -= dy

        player_hitbox.centerx = player_rect.centerx
        player_hitbox.bottom = player_rect.bottom

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

    elif current_state == "STATE_OFFICE_DOORCLOSE":
        # Дверь захлопнулась. Ждем, например, 700 мс (0.7 секунды) тишины/эффекта
        if current_time - office_timer > 700:
            current_state = "STATE_OFFICE_EXCLAMATION" # Теперь Салим пугается
            office_timer = current_time # Перезапускаем таймер для знака "!"
            if snd_encounter: snd_encounter.play() # Вот теперь звучит эффект обнаружения!

    elif current_state == "STATE_OFFICE_EXCLAMATION":
        # Стоим в шоке 1 секунду, затем камера едет к Бахе
        if current_time - office_timer > 1000:
            current_state = STATE_OFFICE_BAHA_EVENT_START
    # --------------------------

    elif current_state == STATE_OFFICE_BAHA_EVENT_START:
        target_cx = 507  
        target_cy = 303  
        dx = target_cx - office_cam_x
        dy = target_cy - office_cam_y
        dist = math.hypot(dx, dy)
        
        if dist > 3:
            office_cam_x += (dx / dist) * 3
            office_cam_y += (dy / dist) * 3
        else:
            office_cam_x = target_cx
            office_cam_y = target_cy
            current_state = STATE_OFFICE_BAHA_DIALOG_1
            office_baha_char_index = 0
            office_baha_dialog_step = 0
            dialog_last_tick = current_time

    elif current_state == STATE_OFFICE_BAHA_WALK:
        office_baha_x -= 2
        if current_time - baha_last_anim_tick > animation_speed:
            office_baha_frame = (office_baha_frame + 1) % len(baha_current_anim)
            baha_last_anim_tick = current_time
            
        if office_baha_x <= 593:
            office_baha_x = 593 
            office_baha_frame = 0
            if snd_steps: snd_steps.stop() # <--- ОСТАНАВЛИВАЕМ ШАГИ
            current_state = STATE_OFFICE_BAHA_DIALOG_2
            office_baha_char_index = 0
            office_baha_dialog_step = 0
            dialog_last_tick = current_time

    elif current_state == STATE_OFFICE_BAHA_FLASH:
        if current_time - flash_start_time > 600:
            current_state = STATE_BATTLE
            current_battle = Battle(font, player_name, player_hp, player_max_hp, player_lv, inventory)

    elif current_state == STATE_CORIDOR_BAHA_RUN:
        coridor_baha_x += 4
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
            dx = target_x - baha_x
            dy = target_y - baha_y
            distance = (dx**2 + dy**2)**0.5 

            if distance > 3:
                baha_x += (dx / distance) * 3
                baha_y += (dy / distance) * 3
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
            baha_y -= 4
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


    elif current_state == "ENDING_OUTSIDE_WALK":
        # Камера зафиксирована на Салиме
        camera_x = player_rect.centerx - WIDTH // 2
        camera_y = player_rect.centery - HEIGHT // 2
        camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
        camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT)))
        
        # Салим идет вниз
        if player_rect.y < 160: 
            player_rect.y += 1
            if current_time - last_anim_tick > animation_speed:
                current_frame = (current_frame + 1) % len(current_anim)
                last_anim_tick = current_time
        else:
            player_rect.y = 160
            current_frame = 0
            current_state = "ENDING_EXCLAMATION"
            ending_timer = current_time # Засекаем время для восклицательного знака
            if snd_encounter: snd_encounter.play()

    elif current_state == "ENDING_EXCLAMATION":
        camera_x = player_rect.centerx - WIDTH // 2
        camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
        camera_y = player_rect.centery - HEIGHT // 2
        camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT))) # Добавлено ограничение по Y
        
        current_anim = walk_right # Салим резко поворачивается направо к Бахе
        
        # Ждем 1 секунду с восклицательным знаком
        if current_time - ending_timer > 1000:
            current_state = "ENDING_PAN_CAMERA"

    elif current_state == "ENDING_PAN_CAMERA":
        # Вычисляем, где должна быть камера, чтобы видеть Баху
        target_cam_x = baha_x - WIDTH // 2 + 30
        target_cam_x = max(0, min(target_cam_x, max(0, map_rect.width - WIDTH)))
        
        # Камера плавно едет к Бахе
        if camera_x < target_cam_x:
            camera_x += 3 # Скорость камеры
            if camera_x >= target_cam_x:
                camera_x = target_cam_x
                current_state = "ENDING_OUTSIDE_DIALOG"
                dialog_last_tick = current_time

    elif current_state in ("RIDING_CUTSCENE_SILENCE", "RIDING_CUTSCENE_DIALOG", "RIDING_FADE_OUT"):
        # Анимация за окном едет
        if current_time - riding_anim_tick > 150:
            riding_anim_frame = (riding_anim_frame + 1) % 4
            riding_anim_tick = current_time
            
        if current_state == "RIDING_CUTSCENE_SILENCE":
            # Ждем 5 секунд молчания
            if current_time - riding_timer > 5000:
                current_state = "RIDING_CUTSCENE_DIALOG"
                riding_dialog_step = 0
                riding_char_index = 0
                dialog_last_tick = current_time
                riding_timer = 0 # Сбрасываем таймер для диалога
                
        elif current_state == "RIDING_CUTSCENE_DIALOG":
            current_text = riding_dialogs[riding_dialog_step]
            
            if current_text == "PAUSE":
                # Автоматическая пауза 2 секунды
                if current_time - riding_timer > 2000:
                    riding_dialog_step += 1
                    riding_char_index = 0
                    dialog_last_tick = current_time
                    riding_timer = 0
            else:
                # Текст печатается
                if riding_char_index >= len(current_text):
                    # Если допечатался, запускаем таймер чтения
                    if riding_timer == 0:
                        riding_timer = current_time 
                        
                    # Ждем 3.5 секунды, чтобы игрок успел прочитать фразу
                    if current_time - riding_timer > 3500:
                        riding_dialog_step += 1
                        if riding_dialog_step >= len(riding_dialogs):
                            current_state = "RIDING_FADE_OUT"
                            ending_fade_start = current_time
                        else:
                            riding_char_index = 0
                            dialog_last_tick = current_time
                            # Если дальше пауза, запускаем таймер паузы
                            if riding_dialogs[riding_dialog_step] == "PAUSE":
                                riding_timer = current_time
                            else:
                                riding_timer = 0
                else:
                    riding_timer = 0 # Пока печатается, таймер отдыхает
                        
    elif current_state == "RESET_GAME_TO_TITLE":
        # ПОЛНЫЙ СБРОС ИГРЫ И ВОЗВРАТ НА ГЛАВНЫЙ ЭКРАН
        game_data["launch_count"] = 1
        game_data["player_lv"] = 1
        game_data["player_hp"] = 20
        game_data["inventory"] = []
        game_data["has_saved"] = False
        game_data["baha_defeated"] = False 
        game_data["special_locker_opened"] = False
        save_game_data(game_data)
        
        inventory.clear()
        player_lv = 1
        player_hp = 20
        baha_defeated = False 
        special_locker_opened = False
        turniket_closed = True 
        is_behind_turniket = False
        target_turniket_state = 0 
        guard_talk_count = 0
        dialog_step = 0
        baha_event_finished = False
        baha_in_coridor = True
        baha_in_office = False
        
        current_state = "STATE_NEW_INTRO"
        intro_start_time = current_time
        intro_sound_played = False


    # ==========================================
    # 3. ОТРИСОВКА И ГРАФИКА ЭКРАНА (Рисование картинок)
    # ==========================================
    if current_state == "STATE_NEW_INTRO":
        screen_surface.fill(BLACK)
        elapsed = current_time - intro_start_time
        
        # 1. Ждем 2 секунды (2000 мс) и запускаем аудио
        if elapsed >= 2000 and not intro_sound_played:
            if snd_dramatic:
                snd_dramatic.play()
            intro_sound_played = True

        # 2. На 6-й секунде после начала аудио (2000 + 6000 = 8000 мс)
        if 8000 <= elapsed < 15000:
            txt = font.render("* Сбила машина!", True, WHITE)
            screen_surface.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

        # 3. На 13-й секунде после начала аудио (2000 + 13000 = 15000 мс)
        elif 15000 <= elapsed < 23000:
            txt = font.render("* Бежит от ???", True, WHITE)
            screen_surface.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

        # 4. На 21-й секунде после аудио (2000 + 21000 = 23000 мс)
        elif elapsed >= 23000:
            distort_time = elapsed - 23000
            text_str = "* Упал! Потеряв сознание...."
            
            # Эффект длится 6 секунд, затем кидает на логотип игры
            if distort_time > 6000:
                current_state = STATE_TITLE_2
                title_2_start_time = current_time
            else:
                # Плавное затухание текста (уход в темноту)
                alpha = max(0, 255 - int((distort_time / 6000) * 255))
                txt_surf = font.render(text_str, True, WHITE)
                txt_surf.set_alpha(alpha)
                
                base_x = WIDTH//2 - txt_surf.get_width()//2
                base_y = HEIGHT//2
                
                # Эффект "потери сознания": текст расплывается и трясется всё сильнее
                intensity = (distort_time / 1000) * 1.5 
                
                # Рисуем текст 6 раз с хаотичным сдвигом (эффект сильного размытия)
                import random # На всякий случай
                for i in range(6):
                    ox = random.uniform(-intensity, intensity)
                    oy = random.uniform(-intensity, intensity)
                    screen_surface.blit(txt_surf, (base_x + ox, base_y + oy))

    elif current_state == STATE_TITLE_2:
        screen_surface.blit(title_image, (title_x, title_y))
        if current_time - title_2_start_time > 2000: 
            current_state = STATE_MAIN_MENU

    elif current_state == STATE_MAIN_MENU:
        screen_surface.blit(font.render(player_name, True, WHITE), (60, 80))
        screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE), (140, 80))
        screen_surface.blit(font.render(":D", True, WHITE), (220, 80))
        
        # --- ДИНАМИЧЕСКИЙ ТЕКСТ ЛОКАЦИИ ---
        if game_data.get("has_saved", False):
            location_text = "Final Corridor"
        else:
            location_text = "Outside"
        screen_surface.blit(font.render(location_text, True, WHITE), (60, 100))
        # ----------------------------------
        
        play_color = AUTUMN_YELLOW if main_menu_choice == 0 else WHITE
        reset_color = AUTUMN_YELLOW if main_menu_choice == 1 else WHITE
        play_text = "Continue" if game_data.get("has_saved", False) else "Play"
        
        screen_surface.blit(font.render(play_text, True, play_color), (90, 150))
        screen_surface.blit(font.render("Reset", True, reset_color), (190, 150))

    elif current_state == STATE_GAME:
        draw_world()
        if door_zone_1.colliderect(player_hitbox) or door_zone_2.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

    elif current_state == STATE_ATRIUM:
        draw_atrium()
        if player_hitbox.colliderect(guard_talk_rect):
            hint = font.render("ENTER - говорить", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif coridor_door_zone_1.colliderect(player_hitbox) or coridor_door_zone_2.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

    elif current_state == STATE_CORIDOR:
        draw_coridor()
        is_showing_hint = False
        if baha_in_coridor:
            coridor_baha_talk_rect = pygame.Rect(coridor_baha_x - 15, coridor_baha_y - 15, baha_w + 30, baha_h + 30)
            if player_hitbox.colliderect(coridor_baha_talk_rect):
                hint = font.render("ENTER - говорить", True, AUTUMN_YELLOW)
                screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
                is_showing_hint = True
        
        if not is_showing_hint:
            if coridor_joke_door.colliderect(player_hitbox) or coridor_joke_pic1.colliderect(player_hitbox) or coridor_joke_pic2.colliderect(player_hitbox):
                hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
                screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
            elif ladder_door_zone.colliderect(player_hitbox):
                if not baha_in_coridor:
                    hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
                else:
                    hint = font.render("Сначала поговори с Бахой!", True, AUTUMN_YELLOW)
                screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
                
    elif current_state == "CORIDOR_INSPECT":
        draw_coridor()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if coridor_inspect_char_index < len(coridor_inspect_text):
                # --- ЗВУК ---
                if coridor_inspect_text[coridor_inspect_char_index] not in [" ", "\n"]:
                    if snd_txt1: snd_txt1.stop(); snd_txt1.play()
                coridor_inspect_char_index += 1
            dialog_last_tick = current_time
            coridor_inspect_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = coridor_inspect_text[:coridor_inspect_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            prefix = "* " if i == 0 else "  "
            screen_surface.blit(font.render(prefix + line, True, WHITE), (20, 158 + i * 16))

    elif current_state == "CORIDOR2FLOOR_INSPECT":
        draw_coridor2floor()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if c2f_inspect_char_index < len(c2f_inspect_text):
                c2f_inspect_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = c2f_inspect_text[:c2f_inspect_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            prefix = "* " if i == 0 else "  "
            screen_surface.blit(font.render(prefix + line, True, WHITE), (20, 158 + i * 16))

    elif current_state == STATE_LADDER:
        draw_ladder()
        if to_2floor_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - подняться", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

    elif current_state == STATE_CORIDOR2FLOOR:
        draw_coridor2floor()
        if cabinet_door_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - войти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)) or \
             lockers2floor_mask.overlap(player_mask_full, (player_rect.x, player_rect.y)):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        # --- НОВЫЕ ЗОНЫ ЗДЕСЬ ---
        elif c2f_pic.colliderect(player_hitbox) or c2f_door1.colliderect(player_hitbox) or c2f_pass1.colliderect(player_hitbox) or c2f_pass2.colliderect(player_hitbox) or c2f_door2.colliderect(player_hitbox):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

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

    elif current_state == STATE_OFFICE:
        draw_office()
        interact_rect_pakett = rect_pakett.inflate(40, 40) if rect_pakett.width > 0 else pygame.Rect(0,0,0,0)
        interact_rect_spec = rect_specificcomp.inflate(40, 40) if rect_specificcomp.width > 0 else pygame.Rect(0,0,0,0)

        if interact_rect_pakett.colliderect(player_hitbox) or interact_rect_spec.colliderect(player_hitbox):
            hint = font.render("ENTER - осмотреть", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        elif office_exit_zone.colliderect(player_hitbox):
            hint = font.render("ENTER - выйти", True, AUTUMN_YELLOW)
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))

    elif current_state in (STATE_PAKETT_DIALOG, STATE_SPECIFICCOMP_DIALOG):
        draw_office()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if office_dialog_char_index < len(office_dialog_text): 
                # --- ЗВУК ---
                if office_dialog_text[office_dialog_char_index] not in [" ", "\n"]:
                    if snd_txt1: snd_txt1.stop(); snd_txt1.play()
                office_dialog_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = office_dialog_text[:office_dialog_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            prefix = "* " if i == 0 else ""
            screen_surface.blit(font.render(prefix + line, True, WHITE), (20 if not office_dialog_speaker else 80, 168 + i * 16))
            
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

    # --- ДОБАВИТЬ ЭТОТ КУСОЧЕК ---
    elif current_state == "STATE_OFFICE_DOORCLOSE":
        draw_office() # Просто рисуем офис, Салим ещё не заметил подвоха

    # --- ДОБАВИТЬ ЭТОТ БЛОК ---
    elif current_state == "STATE_OFFICE_EXCLAMATION":
        draw_office()
        # Рисуем красный прыгающий восклицательный знак
        exclam_text = font.render("!", True, (255, 50, 50))
        jump_offset = 0 if (current_time // 150) % 2 == 0 else -4
        screen_surface.blit(exclam_text, (player_rect.centerx - office_cam_x - exclam_text.get_width()//2, player_rect.top - office_cam_y - 20 + jump_offset))
    # --------------------------

    elif current_state in (STATE_OFFICE_BAHA_EVENT_START, STATE_OFFICE_BAHA_WALK):
        draw_office()

    elif current_state in (STATE_OFFICE_BAHA_DIALOG_1, STATE_OFFICE_BAHA_DIALOG_2):
        draw_office()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        current_array = office_baha_dialog_1 if current_state == STATE_OFFICE_BAHA_DIALOG_1 else office_baha_dialog_2
        current_text = current_array[office_baha_dialog_step]

        # --- РИСУЕМ ЛИЦО БАХИ ---
        is_talking = office_baha_char_index < len(current_text)
        current_face = baha_faces[dialog_face_frame] if is_talking else baha_faces[0]
        screen_surface.blit(current_face, (20, 160))

        if current_time - dialog_last_tick > 80: 
            if office_baha_char_index < len(current_text):
                if current_text[office_baha_char_index] not in [" ", "\n"]:
                    if snd_baha:
                        snd_baha.stop()
                        snd_baha.play()
                office_baha_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = current_text[:office_baha_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(baha_font.render("* " + line if i == 0 else line, True, WHITE), (80, 158 + i * 16))
            
        if office_baha_char_index >= len(current_text):
            screen_surface.blit(choice_font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == "OFFICE_CAMERA_TO_PLAYER":
        draw_office()
        target_cam_x = player_rect.centerx - WIDTH // 2
        target_cam_y = player_rect.centery - HEIGHT // 2
        target_cam_x = max(0, min(target_cam_x, max(0, office_rect.width - WIDTH)))
        target_cam_y = max(0, min(target_cam_y, max(0, office_rect.height - HEIGHT)))
        
        dx = target_cam_x - office_cam_x
        dy = target_cam_y - office_cam_y
        dist = math.hypot(dx, dy)
        
        if dist > 3:
            office_cam_x += (dx / dist) * 3
            office_cam_y += (dy / dist) * 3
        else:
            office_cam_x = target_cam_x
            office_cam_y = target_cam_y
            current_state = "OFFICE_BAHA_RUN_TO_PLAYER"
            baha_last_anim_tick = current_time
            if snd_steps: snd_steps.play(loops=-1) # <--- ВСТАВИТЬ ЭТО СЮДА (Начинает звук)

    elif current_state == "OFFICE_BAHA_RUN_TO_PLAYER":
        draw_office()
        office_cam_x = player_rect.centerx - WIDTH // 2
        office_cam_y = player_rect.centery - HEIGHT // 2
        office_cam_x = max(0, min(office_cam_x, max(0, office_rect.width - WIDTH)))
        office_cam_y = max(0, min(office_cam_y, max(0, office_rect.height - HEIGHT)))
        
        dx = player_rect.x - office_baha_x
        dy = 0
        baha_current_anim = baha_walk_right if dx > 0 else baha_walk_left

        if abs(dx) > 5:
            office_baha_x += (dx / abs(dx)) * 5
            if current_time - baha_last_anim_tick > animation_speed:
                office_baha_frame = (office_baha_frame + 1) % len(baha_current_anim)
                baha_last_anim_tick = current_time
        else:
            if snd_steps: snd_steps.stop() # <--- ВОТ ЭТА СТРОЧКА ОБРЕЗАЕТ ЗВУК ШАГОВ
            current_state = "OFFICE_BAHA_HEART_BLINK"
            flash_start_time = current_time
            heart_anim_x = player_rect.centerx - office_cam_x - 7
            heart_anim_y = player_rect.centery - office_cam_y - 7
            
            if snd_battleappear and not battle_sound_played:
                snd_battleappear.play()
                battle_sound_played = True

    elif current_state == "OFFICE_BAHA_HEART_BLINK":
        try:
            global_heart = pygame.image.load(os.path.join("textures", "heart.png")).convert_alpha()
            global_heart = pygame.transform.scale(global_heart, (12, 12))
        except:
            global_heart = pygame.Surface((12, 12))
            global_heart.fill((255, 0, 0))
            
        if ((current_time - flash_start_time) // 80) % 2 == 0:
            screen_surface.blit(global_heart, (heart_anim_x, heart_anim_y))
            
        if current_time - flash_start_time > 500:
            current_state = "OFFICE_BAHA_HEART_MOVE"

    elif current_state == "OFFICE_BAHA_HEART_MOVE":
        try:
            global_heart = pygame.image.load(os.path.join("textures", "heart.png")).convert_alpha()
            global_heart = pygame.transform.scale(global_heart, (12, 12))
        except:
            global_heart = pygame.Surface((12, 12))
            global_heart.fill((255, 0, 0))

        target_hx = WIDTH // 2 - 6
        target_hy = 165
        dx = target_hx - heart_anim_x
        dy = target_hy - heart_anim_y
        dist = math.hypot(dx, dy)
        
        if dist > 4:
            heart_anim_x += (dx / dist) * 4
            heart_anim_y += (dy / dist) * 4
            screen_surface.blit(global_heart, (heart_anim_x, heart_anim_y))
        else:
            current_state = STATE_BATTLE
            current_battle = Battle(font, player_name, player_hp, player_max_hp, player_lv, inventory)

    elif current_state == STATE_BATTLE:
        if current_battle:
            new_state = current_battle.update_and_draw(screen_surface, current_time)
            
            if new_state == "GAMEOVER_ANIM":
                current_state = STATE_GAMEOVER_ANIM
                game_over_timer = current_time
                gameover_heart_x = current_battle.heart_x
                gameover_heart_y = current_battle.heart_y
                shatter_played = False
                pygame.mixer.music.stop() 
                
            elif new_state == "WIN_BATTLE":
                player_lv = 19
                baha_defeated = True
                
                current_battle = None
                pygame.mixer.music.stop()
                office_baha_char_index = 0
                post_battle_texts = ["слушай я щас выйду с аиту", "пошли развеемся"]
                post_battle_step = 0
                
                baha_in_office = True
                office_baha_x = player_rect.centerx + 70      
                office_baha_y = player_rect.bottom - baha_h   
                baha_current_anim = baha_walk_left            
                office_baha_frame = 0

                # ЗАПУСК ПЛАВНОГО ПЕРЕХОДА ИЗ ЧЕРНОГО ЭКРАНА
                start_transition("OFFICE_BAHA_POST_BATTLE")
                transition_phase = "fadein" # Пропускаем фазу "black", так как битва уже затемнила экран
                transition_start = current_time 
            else:
                current_state = new_state
                
                baha_in_office = True
                office_baha_x = player_rect.centerx + 70      
                office_baha_y = player_rect.bottom - baha_h   
                baha_current_anim = baha_walk_left            
                office_baha_frame = 0

    elif current_state == "OFFICE_BAHA_POST_BATTLE":
        draw_office()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        current_text = post_battle_texts[post_battle_step]

        # --- РИСУЕМ ЛИЦО БАХИ ---
        is_talking = office_baha_char_index < len(current_text)
        current_face = baha_faces[dialog_face_frame] if is_talking else baha_faces[0]
        screen_surface.blit(current_face, (20, 160))

        if current_time - dialog_last_tick > 80:
            if office_baha_char_index < len(current_text):
                if current_text[office_baha_char_index] not in [" ", "\n"]:
                    if snd_baha:
                        snd_baha.stop()
                        snd_baha.play()
                office_baha_char_index += 1
            dialog_last_tick = current_time

        visible_text = current_text[:office_baha_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(baha_font.render("* " + line if i == 0 else line, True, WHITE), (80, 158 + i * 16))

        if office_baha_char_index >= len(current_text):
            screen_surface.blit(choice_font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == "OFFICE_BAHA_LEAVES":
        draw_office()
        office_baha_x += 4
        if current_time - baha_last_anim_tick > animation_speed:
            office_baha_frame = (office_baha_frame + 1) % len(baha_current_anim)
            baha_last_anim_tick = current_time

        if office_baha_x > office_rect.width + 50:
            baha_in_office = False
            current_state = STATE_OFFICE

    elif current_state == STATE_CORIDOR_BAHA_RUN: 
        draw_coridor() 

    elif current_state == STATE_CORIDOR_BAHA_DIALOG:
        draw_coridor()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        data = coridor_baha_dialogs[dialog_step]

        # --- РИСУЕМ ЛИЦО БАХИ ---
        is_talking = dialog_char_index < len(data["text"])
        current_face = baha_faces[dialog_face_frame] if is_talking else baha_faces[0]
        screen_surface.blit(current_face, (20, 160))

        if current_time - dialog_last_tick > dialog_text_speed:
            if dialog_char_index < len(data["text"]):
                if data["text"][dialog_char_index] not in [" ", "\n"]:
                    if snd_baha:
                        snd_baha.stop()
                        snd_baha.play()
                dialog_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = data["text"][:dialog_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(baha_font.render("* " + line if i == 0 else line, True, WHITE), (80, 158 + i * 16))
            
        if dialog_char_index >= len(data["text"]):
            if not data["choices"]: 
                screen_surface.blit(choice_font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (85, 205))
            else:
                x = 85
                for i, choice in enumerate(data["choices"]):
                    color = AUTUMN_YELLOW if i == dialog_choice else WHITE
                    prefix = "* " if i == dialog_choice else "  "
                    text = choice_font.render(prefix + choice[0], True, color)
                    screen_surface.blit(text, (x, 205))
                    x += text.get_width() + 20

    elif current_state == STATE_LOCKERS_DIALOG:
        if lockersfinal_real_rect.height > 0 and lockersfinal_mask.overlap(player_mask_full, (player_rect.x, player_rect.y - 10)): 
            draw_coridorfinal()
        else: 
            draw_coridor2floor()
        draw_lockers_dialog()
        
    elif current_state == STATE_SPECIAL_LOCKER_DIALOG:
        draw_coridorfinal()
        draw_special_locker_dialog()

    elif current_state == STATE_DOOR:
        draw_world()
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if door_choice == 1 else WHITE
        screen_surface.blit(choice_font.render("* Да" if door_choice == 0 else "  Да", True, da_color), (80, 205))
        screen_surface.blit(choice_font.render("* Нет" if door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_CORIDOR_DOOR:
        draw_atrium() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти в коридор?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if coridor_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if coridor_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да" if coridor_door_choice == 0 else "  Да", True, da_color), (80, 205))
        screen_surface.blit(font.render("* Нет" if coridor_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_LADDER_DOOR:
        draw_coridor() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Перейти к лестнице?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if ladder_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if ladder_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да" if ladder_door_choice == 0 else "  Да", True, da_color), (80, 205))
        screen_surface.blit(font.render("* Нет" if ladder_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_CORIDOR2FLOOR_DOOR:
        draw_ladder() 
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Перейти на 2 этаж?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if coridor2floor_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if coridor2floor_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да" if coridor2floor_door_choice == 0 else "  Да", True, da_color), (80, 205))
        screen_surface.blit(font.render("* Нет" if coridor2floor_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_CABINET_DOOR:
        draw_coridor2floor()
        box = pygame.Rect(10, 175, 300, 55)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render("Хотите войти в кабинет?", True, WHITE), (18, 182))
        da_color  = AUTUMN_YELLOW if cabinet_door_choice == 0 else WHITE
        net_color = AUTUMN_YELLOW if cabinet_door_choice == 1 else WHITE
        screen_surface.blit(font.render("* Да" if cabinet_door_choice == 0 else "  Да", True, da_color), (80, 205))
        screen_surface.blit(font.render("* Нет" if cabinet_door_choice == 1 else "  Нет", True, net_color), (180, 205))

    elif current_state == STATE_SAVE_MENU:
        draw_coridorfinal()
        box = pygame.Rect(30, 40, 260, 100)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render(player_name, True, WHITE), (45, 50))
        screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE), (125, 50))
        screen_surface.blit(font.render(":D", True, WHITE), (230, 50)) 
        screen_surface.blit(font.render("Last Corridor", True, WHITE), (45, 75))
        
        c_save = AUTUMN_YELLOW if save_menu_choice == 0 else WHITE
        c_ret = AUTUMN_YELLOW if save_menu_choice == 1 else WHITE
        
        # 1. Загружаем картинку сердечка (с защитой от ошибок)
        try:
            menu_heart = pygame.image.load(os.path.join("textures", "heart.png")).convert_alpha()
            menu_heart = pygame.transform.scale(menu_heart, (12, 12))
        except:
            menu_heart = pygame.Surface((12, 12))
            menu_heart.fill((255, 0, 0))

        # 2. Рисуем сердечко в зависимости от выбора
        if save_menu_choice == 0:
            screen_surface.blit(menu_heart, (45, 114)) # Рядом с Save
        else:
            screen_surface.blit(menu_heart, (145, 114)) # Рядом с Return
            
        # 3. Рисуем сам текст (немного сдвинули вправо, чтобы влезла картинка)
        screen_surface.blit(font.render("Save", True, c_save), (60, 115))
        screen_surface.blit(font.render("Return", True, c_ret), (160, 115))
    # --- НОВЫЙ ЭКРАН "FILE SAVED" ---
    elif current_state == "STATE_SAVE_DONE":
        draw_coridorfinal()
        box = pygame.Rect(30, 40, 260, 100)
        pygame.draw.rect(screen_surface, BLACK, box)
        pygame.draw.rect(screen_surface, WHITE, box, 2)
        screen_surface.blit(font.render(player_name, True, AUTUMN_YELLOW), (45, 50))
        screen_surface.blit(font.render(f"LV {player_lv}", True, AUTUMN_YELLOW), (125, 50))
        screen_surface.blit(font.render(":D", True, AUTUMN_YELLOW), (230, 50)) 
        screen_surface.blit(font.render("Last Corridor", True, AUTUMN_YELLOW), (45, 75))
        
        screen_surface.blit(font.render("File saved.", True, AUTUMN_YELLOW), (80, 115))
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
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        # --- РИСУЕМ ЛИЦО ОХРАННИКА ---
        is_talking = post_baha_char_index < len(post_baha_text)
        current_face = guard_faces[dialog_face_frame] if is_talking else guard_faces[0]
        screen_surface.blit(current_face, (20, 160))

        if current_time - dialog_last_tick > dialog_text_speed:
            if post_baha_char_index < len(post_baha_text):
                if post_baha_text[post_baha_char_index] not in [" ", "\n"]:
                    if snd_guard:
                        snd_guard.stop()
                        snd_guard.play()
                post_baha_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = post_baha_text[:post_baha_char_index]
        screen_surface.blit(font.render("* " + visible_text, True, WHITE), (80, 158))
        if post_baha_char_index >= len(post_baha_text): 
            screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == STATE_GUARD_FIRST:
        draw_atrium()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)

        # --- РИСУЕМ ЛИЦО ОХРАННИКА ---
        is_talking = first_char_index < len(first_text)
        current_face = guard_faces[dialog_face_frame] if is_talking else guard_faces[0]
        screen_surface.blit(current_face, (20, 160))

        if current_time - first_last_tick > first_text_speed:
            if first_char_index < len(first_text):
                if first_text[first_char_index] not in [" ", "\n"]:
                    if snd_guard:
                        snd_guard.stop() 
                        snd_guard.play() 
                first_char_index += 1
            first_last_tick = current_time
            
        visible_text = first_text[:first_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render(line, True, WHITE), (80, 158 + i * 16))
            
        if first_char_index >= len(first_text): 
            screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))
    
    elif current_state == STATE_GUARD_DIALOG:
        draw_atrium()
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        data = guard_dialogs[dialog_step]

        # --- РИСУЕМ ЛИЦО ОХРАННИКА ---
        is_talking = dialog_char_index < len(data["text"])
        current_face = guard_faces[dialog_face_frame] if is_talking else guard_faces[0]
        screen_surface.blit(current_face, (20, 160))
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if dialog_char_index < len(data["text"]):
                if data["text"][dialog_char_index] not in [" ", "\n"]:
                    if snd_guard:
                        snd_guard.stop()
                        snd_guard.play()
                dialog_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = data["text"][:dialog_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render(line, True, WHITE), (80, 158 + i * 16))
            
        if dialog_step == 2:
            if dialog_char_index >= len(data["text"]): 
                screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))
        else:
            x = 85
            for i, choice in enumerate(data["choices"]):
                color = AUTUMN_YELLOW if i == dialog_choice else WHITE
                prefix = "* " if i == dialog_choice else "  "
                text = choice_font.render(prefix + choice[0], True, color)
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
            dialog_rect = pygame.Rect(10, 150, 300, 80)
            pygame.draw.rect(screen_surface, BLACK, dialog_rect)
            pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
            current_text_target = baha_texts[baha_stage - 1]

            # --- РИСУЕМ ЛИЦО (ЗАВИСИТ ОТ ТОГО КТО ГОВОРИТ) ---
            is_talking = dialog_char_index < len(current_text_target)
            faces = baha_faces if baha_stage == 1 else guard_faces
            current_face = faces[dialog_face_frame] if is_talking else faces[0]
            screen_surface.blit(current_face, (20, 160))
            
            if current_time - dialog_last_tick > dialog_text_speed:
                if dialog_char_index < len(current_text_target): 
                    if current_text_target[dialog_char_index] not in [" ", "\n"]:
                        current_snd = snd_baha if baha_stage == 1 else snd_guard
                        if current_snd:
                            current_snd.stop()
                            current_snd.play()
                    dialog_char_index += 1
                dialog_last_tick = current_time
                
            speaker_prefix = "* "
            current_speak_font = baha_font if baha_stage == 1 else font
            
            visible_text = current_text_target[:dialog_char_index]
            for i, line in enumerate(visible_text.split("\n")):
                screen_surface.blit(current_speak_font.render(speaker_prefix + line if i == 0 else line, True, WHITE), (80, 158 + i * 16))
                
            if dialog_char_index >= len(current_text_target): 
                screen_surface.blit(font.render("* ...", True, AUTUMN_YELLOW), (85, 205))

    elif current_state == STATE_TRANSITION:
        elapsed = current_time - transition_start
        if transition_phase == "black":
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
            elif next_state_after_transition in (STATE_OFFICE, "OFFICE_BAHA_POST_BATTLE"):
                office_cam_x = player_rect.centerx - WIDTH // 2
                office_cam_y = player_rect.centery - HEIGHT // 2
                office_cam_x = max(0, min(office_cam_x, max(0, office_rect.width - WIDTH)))
                office_cam_y = max(0, min(office_cam_y, max(0, office_rect.height - HEIGHT)))
                draw_office()
            elif next_state_after_transition == "ENDING_OUTSIDE_WALK":
                # Камера четко нацеливается на Салима
                camera_x = player_rect.centerx - WIDTH // 2
                camera_y = player_rect.centery - HEIGHT // 2
                camera_x = max(0, min(camera_x, max(0, map_rect.width - WIDTH)))
                camera_y = max(0, min(camera_y, max(0, map_rect.height - HEIGHT)))
                draw_world()
                
                # РИСУЕМ ВОЕНКОМОВ ДАЖЕ ПОКА ЭКРАН СВЕТЛЕЕТ
                screen_surface.blit(voenkom_img, (-camera_x, -camera_y))
                
                screen_surface.blit(baha_current_anim[baha_frame], (baha_x - camera_x, baha_y - camera_y))
            
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
                # Запускаем таймер текста только ПОСЛЕ того, как экран стал светлым
                if current_state == "OFFICE_BAHA_POST_BATTLE":
                    dialog_last_tick = pygame.time.get_ticks()
                elif current_state == "STATE_NEW_GAME_CUTSCENE":
                    cutscene_timer = pygame.time.get_ticks()
                    dialog_last_tick = pygame.time.get_ticks()

    elif current_state in ("ENDING_OUTSIDE_WALK", "ENDING_EXCLAMATION", "ENDING_PAN_CAMERA", "ENDING_OUTSIDE_DIALOG", "ENDING_FADE_OUT", "ENDING_DONE"):
        # Камера берется из вычислений Секции 2
        draw_world()
        
        # --- РИСУЕМ ВОЕНКОМА (сзади Бахи) ---
        screen_surface.blit(voenkom_img, (-camera_x, -camera_y))
        
        # Рисуем Баху (он нарисуется поверх Военкома)
        screen_surface.blit(baha_current_anim[baha_frame], (baha_x - camera_x, baha_y - camera_y))
        # Если стадия удивления, рисуем знак "!" над Салимом
        if current_state == "ENDING_EXCLAMATION":
            exclam_text = font.render("!", True, (255, 50, 50))
            # Заставляем "!" прыгать
            jump_offset = 0 if (current_time // 150) % 2 == 0 else -4
            screen_surface.blit(exclam_text, (player_rect.centerx - camera_x - exclam_text.get_width()//2, player_rect.top - camera_y - 20 + jump_offset))
        
        if current_state == "ENDING_OUTSIDE_DIALOG":
            dialog_rect = pygame.Rect(10, 150, 300, 80)
            pygame.draw.rect(screen_surface, BLACK, dialog_rect)
            pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
            
            # --- ЛИЦО БАХИ ---
            current_text = ending_baha_texts[ending_baha_step]
            is_talking = office_baha_char_index < len(current_text)
            current_face = baha_faces[dialog_face_frame] if is_talking else baha_faces[0]
            screen_surface.blit(current_face, (20, 160))

            if current_time - dialog_last_tick > 80:
                if office_baha_char_index < len(current_text):
                    if current_text[office_baha_char_index] not in [" ", "\n"]:
                        if snd_baha:
                            snd_baha.stop()
                            snd_baha.play()
                    office_baha_char_index += 1
                dialog_last_tick = current_time
                
            visible_text = current_text[:office_baha_char_index]
            for i, line in enumerate(visible_text.split("\n")):
                screen_surface.blit(baha_font.render("* " + line if i == 0 else line, True, WHITE), (80, 158 + i * 16))
                
            if office_baha_char_index >= len(current_text):
                screen_surface.blit(choice_font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (85, 205))
                
        elif current_state == "ENDING_FADE_OUT":
            elapsed = current_time - ending_fade_start
            alpha = min(255, int(255 * elapsed / 3000))
            fade_surface.set_alpha(alpha)
            screen_surface.blit(fade_surface, (0, 0))
            if elapsed > 4000:
                # ВМЕСТО ENDING_DONE ЗАПУСКАЕМ КАТСЦЕНУ В МАШИНЕ
                current_state = "RIDING_CUTSCENE_SILENCE"
                riding_timer = current_time
                riding_anim_tick = current_time
                
    elif current_state in ("RIDING_CUTSCENE_SILENCE", "RIDING_CUTSCENE_DIALOG", "RIDING_FADE_OUT", "AITUTALE_LOGO"):
        screen_surface.fill(BLACK)
        
        if current_state != "AITUTALE_LOGO":
            # Проверяем, говорит ли Баха прямо сейчас (чтобы открыть рот)
            is_talking = False
            if current_state == "RIDING_CUTSCENE_DIALOG" and riding_dialogs[riding_dialog_step] != "PAUSE":
                if riding_char_index < len(riding_dialogs[riding_dialog_step]):
                    is_talking = True
                    
            current_frame_img = riding_frames_talking[riding_anim_frame] if is_talking else riding_frames_silent[riding_anim_frame]
            
            # Отрисовка картинки по центру (чуть выше, чтобы влез диалог)
            img_x = (WIDTH - current_frame_img.get_width()) // 2
            img_y = (HEIGHT - current_frame_img.get_height()) // 2 - 20
            screen_surface.blit(current_frame_img, (img_x, img_y))
            
            # Отрисовка диалога (без рамок, чисто по центру внизу)
            if current_state == "RIDING_CUTSCENE_DIALOG":
                current_text = riding_dialogs[riding_dialog_step]
                if current_text != "PAUSE":
                    
                    if current_time - dialog_last_tick > 60:
                        if riding_char_index < len(current_text):
                            if current_text[riding_char_index] not in [" ", "\n"]:
                                if snd_baha:
                                    snd_baha.stop()
                                    snd_baha.play()
                            riding_char_index += 1
                        dialog_last_tick = current_time
                        
                    visible_text = current_text[:riding_char_index]
                    
                    # Привязываем текст к самому низу экрана (чтобы картинка его не перекрывала)
                    # HEIGHT - 20 отступает от нижнего края экрана вверх
                    lines = visible_text.split("\n")
                    start_y = HEIGHT - 20 - (len(current_text.split("\n")) * 18)
                    
                    for i, line in enumerate(lines):
                        text_surf = baha_font.render(line, True, WHITE)
                        text_x = WIDTH // 2 - text_surf.get_width() // 2
                        text_y = start_y + i * 18
                        screen_surface.blit(text_surf, (text_x, text_y))
                        
            # Финальное затемнение после машины
            elif current_state == "RIDING_FADE_OUT":
                elapsed = current_time - ending_fade_start
                alpha = min(255, int(255 * elapsed / 3000))
                fade_surface.set_alpha(alpha)
                screen_surface.blit(fade_surface, (0, 0))
                if elapsed > 4000:
                    current_state = "AITUTALE_LOGO"
                    ending_fade_start = current_time
                    
        # Отрисовка ОРИГИНАЛЬНОГО логотипа игры
        elif current_state == "AITUTALE_LOGO":
            elapsed = current_time - ending_fade_start
            
            # Копируем оригинальный логотип из главного меню
            temp_title = title_image.copy()
            
            # Плавное появление логотипа
            alpha = min(255, int(255 * elapsed / 2000))
            temp_title.set_alpha(alpha)
            
            screen_surface.blit(temp_title, (title_x, title_y))
            
            # Через 6 секунд сбрасываем игру
            if elapsed > 6000:
                current_state = "RESET_GAME_TO_TITLE"
                
        elif current_state == "ENDING_DONE":
            screen_surface.fill(BLACK)
            txt = font.render("КОНЕЦ DEMO", True, WHITE)
            screen_surface.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

    elif current_state == "STATE_NEW_GAME_CUTSCENE":
        draw_world()
        
        dialog_rect = pygame.Rect(10, 150, 300, 80)
        pygame.draw.rect(screen_surface, BLACK, dialog_rect)
        pygame.draw.rect(screen_surface, WHITE, dialog_rect, 2)
        
        if current_time - dialog_last_tick > dialog_text_speed:
            if cutscene_char_index < len(cutscene_text):
                cutscene_char_index += 1
            dialog_last_tick = current_time
            
        visible_text = cutscene_text[:cutscene_char_index]
        for i, line in enumerate(visible_text.split("\n")):
            screen_surface.blit(font.render("* " + line if i == 0 else line, True, WHITE), (20, 158 + i * 16))
            
        if cutscene_char_index >= len(cutscene_text):
            screen_surface.blit(choice_font.render("* (Нажмите ENTER)", True, AUTUMN_YELLOW), (20, 205))

    elif current_state == STATE_GAMEOVER_ANIM:
        elapsed = current_time - game_over_timer

        try:
            global_heart = pygame.image.load(os.path.join("textures", "heart.png")).convert_alpha()
            global_heart = pygame.transform.scale(global_heart, (12, 12))
        except:
            global_heart = pygame.Surface((12, 12))
            global_heart.fill((255, 0, 0))

        if elapsed < 1000:
            screen_surface.blit(global_heart, (gameover_heart_x, gameover_heart_y))
        elif elapsed < 2500:
            if not shatter_played:
                if snd_shatter: snd_shatter.play()
                shatter_played = True
                
            half_w = global_heart.get_width() // 2
            h = global_heart.get_height()
            left_half = global_heart.subsurface((0, 0, half_w, h))
            right_half = global_heart.subsurface((half_w, 0, half_w, h))

            screen_surface.blit(left_half, (gameover_heart_x - 4, gameover_heart_y + 2))
            screen_surface.blit(right_half, (gameover_heart_x + half_w + 4, gameover_heart_y + 2))
        else:
            current_state = "GAMEOVER_FADE_IN_LOGO"
            game_over_timer = current_time
            gameover_text_index = 0
            gameover_text = "Не сдавайся, балмуздак!"
            try:
                # Включаем музыку геймовера
                pygame.mixer.music.load(os.path.join("sounds", "game over.ogg"))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(1.0)
            except:
                pass

    elif current_state == "GAMEOVER_FADE_IN_LOGO":
        screen_surface.fill(BLACK)
        elapsed = current_time - game_over_timer
        # Плавное появление логотипа (2 секунды)
        alpha = min(255, int(255 * (elapsed / 2000)))
        
        temp_img = img_game_over.copy()
        temp_img.set_alpha(alpha)
        go_x = (WIDTH - img_game_over.get_width()) // 2
        go_y = 40 
        screen_surface.blit(temp_img, (go_x, go_y))

        if elapsed > 2500:
            current_state = "GAMEOVER_TEXT"
            dialog_last_tick = current_time

    elif current_state == "GAMEOVER_TEXT":
        screen_surface.fill(BLACK)
        go_x = (WIDTH - img_game_over.get_width()) // 2
        screen_surface.blit(img_game_over, (go_x, 40))

        if gameover_text_index < len(gameover_text):
            if current_time - dialog_last_tick > 120:
                if gameover_text[gameover_text_index] not in [" ", ",", "!"]:
                    if snd_guard:
                        snd_guard.stop()
                        snd_guard.play()
                gameover_text_index += 1
                dialog_last_tick = current_time
        else:
            if current_time - dialog_last_tick > 1000:
                current_state = "GAMEOVER_WAIT_INPUT"

        visible_text = gameover_text[:gameover_text_index]
        txt_surf = font.render(visible_text, True, WHITE)
        screen_surface.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 160))

    elif current_state == "GAMEOVER_WAIT_INPUT":
        screen_surface.fill(BLACK)
        go_x = (WIDTH - img_game_over.get_width()) // 2
        screen_surface.blit(img_game_over, (go_x, 40)) 
        
        txt_surf = font.render(gameover_text, True, WHITE)
        screen_surface.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 160)) 

        # Серая мигающая подсказка в стиле Андертейл
        if (current_time // 500) % 2 == 0:
            if game_data.get("has_saved", False):
                hint_text = "* (ENTER - Загрузить сохранение)"
            else:
                hint_text = "* (ENTER - Начать заново)"
            
            hint = choice_font.render(hint_text, True, (150, 150, 150))
            screen_surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 200))

    elif current_state == "GAMEOVER_FADE_OUT":
        screen_surface.fill(BLACK)
        elapsed = current_time - game_over_timer
        
        # Плавное затухание графики и звука (2 секунды)
        alpha = max(0, 255 - int(255 * (elapsed / 2000)))
        pygame.mixer.music.set_volume(max(0.0, 1.0 - (elapsed / 2000)))

        temp_img = img_game_over.copy()
        temp_img.set_alpha(alpha)
        screen_surface.blit(temp_img, ((WIDTH - img_game_over.get_width()) // 2, 40))

        txt_surf = font.render(gameover_text, True, WHITE)
        txt_surf.set_alpha(alpha)
        screen_surface.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 160))

        if elapsed > 2500:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(1.0) # Возвращаем громкость для самой игры
            current_state = "GAMEOVER_RESTART"

    elif current_state == "GAMEOVER_RESTART":
        # Логика перезагрузки сейва/игры
        current_battle = None
        battle_sound_played = False 
        
        game_data = load_game_data()

        if game_data.get("has_saved", False):
            inventory = game_data.get("inventory", [])
            player_hp = 20
            player_lv = game_data.get("player_lv", 1)
            special_locker_opened = game_data.get("special_locker_opened", False)
            baha_defeated = game_data.get("baha_defeated", False) 
            baha_in_office = False
            
            player_rect.x = SPAWN_SAVE_CONTINUE_X
            player_rect.y = SPAWN_SAVE_CONTINUE_Y
            player_hitbox.centerx = player_rect.centerx
            player_hitbox.bottom = player_rect.bottom
            start_transition(STATE_CORIDORFINAL)
        else:
            game_data["inventory"] = []
            game_data["player_hp"] = 20
            game_data["player_lv"] = 1
            game_data["special_locker_opened"] = False
            save_game_data(game_data)
            
            inventory.clear()
            player_hp = 20
            player_lv = 1
            special_locker_opened = False
            baha_defeated = False 
            
            turniket_closed = True 
            is_behind_turniket = False
            target_turniket_state = 0 
            
            guard_talk_count = 0
            dialog_step = 0
            first_char_index = 0
            post_baha_char_index = 0
            
            baha_event_finished = False
            baha_stage = 0
            baha_x, baha_y = 867, 163
            baha_current_anim = baha_walk_down  
            baha_frame = 0
            
            baha_in_coridor = True
            coridor_baha_x, coridor_baha_y = 399, 522
            coridor_baha_anim = baha_walk_down 
            coridor_baha_frame = 0
            
            baha_in_office = False
            office_baha_dialog_step = 0
            
            player_rect.x = map_rect.width // 2
            player_rect.y = map_rect.height - SCALE_H - 50
            player_hitbox.centerx = player_rect.centerx
            player_hitbox.bottom = player_rect.bottom
            
            # --- Запуск катсцены нового начала ---
            cutscene_step = 0
            cutscene_char_index = 0
            cutscene_text = "...Где я?"
            cutscene_timer = pygame.time.get_ticks()
            dialog_last_tick = pygame.time.get_ticks()
            start_transition("STATE_NEW_GAME_CUTSCENE")
    # === МЕНЮ СТАТИСТИКИ (НА CTRL) ===
    if show_menu and current_state not in [STATE_TITLE, STATE_TITLE_2, STATE_STORY, STATE_MAIN_MENU, STATE_SAVE_MENU, STATE_TRANSITION, STATE_BATTLE, STATE_GAMEOVER_ANIM, "GAMEOVER_FADE_IN_LOGO", "GAMEOVER_TEXT", "GAMEOVER_WAIT_INPUT", "GAMEOVER_FADE_OUT", "GAMEOVER_RESTART", "STATE_NEW_INTRO", "STATE_NEW_GAME_CUTSCENE"]:
        
        box1 = pygame.Rect(4, 4, 80, 60) # ВОТ ЗДЕСЬ ДОБАВЛЕНЫ РАЗМЕРЫ ОКНА
        
        pygame.draw.rect(screen_surface, BLACK, box1)
        pygame.draw.rect(screen_surface, WHITE, box1, 2)
        screen_surface.blit(font.render(player_name, True, WHITE),       (box1.x+4, box1.y+4))
        screen_surface.blit(font.render(f"LV {player_lv}", True, WHITE),  (box1.x+4, box1.y+20))
        screen_surface.blit(font.render(f"HP {player_hp}/{player_max_hp}", True, WHITE), (box1.x+4, box1.y+36))
        
        box2 = pygame.Rect(4, 66, 80, 42)
        pygame.draw.rect(screen_surface, BLACK, box2)
        pygame.draw.rect(screen_surface, WHITE, box2, 2)
        screen_surface.blit(font.render("\u2665 ITEM", True, (255, 60, 60)), (box2.x+4, box2.y+4))
        screen_surface.blit(font.render("  STAT", True, WHITE),             (box2.x+4, box2.y+20))
        
        if inventory:
            inv_box = pygame.Rect(90, 4, 180, 28 + 18 * len(inventory))
            pygame.draw.rect(screen_surface, BLACK, inv_box)
            pygame.draw.rect(screen_surface, WHITE, inv_box, 2)
            screen_surface.blit(font.render("ИНВЕНТАРЬ:", True, AUTUMN_YELLOW), (inv_box.x+4, inv_box.y+4))
            for idx, item in enumerate(inventory):
                screen_surface.blit(font.render(f"* {item}", True, WHITE), (inv_box.x+4, inv_box.y+24 + idx*18))

    scaled = pygame.transform.scale(screen_surface, (WIDTH * SCALE, HEIGHT * SCALE))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    clock.tick(60)