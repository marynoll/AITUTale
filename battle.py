# battle.py
import pygame
import os
import random
from settings import *

def load_texture(filename):
    path = os.path.join("textures", filename)
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        surf = pygame.Surface((30, 30))
        surf.fill((100, 100, 100))
        return surf

def load_sound(filename):
    path = os.path.join("sounds", filename)
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

MENU_RECT = pygame.Rect(15, 120, 290, 65)
ARENA_RECT = pygame.Rect(WIDTH//2 - 60, 110, 120, 120)
TINY_RECT = pygame.Rect(WIDTH//2 - 20, 151, 40, 40)

class Battle:
    def __init__(self, font, player_name, hp, max_hp, lv, inventory):
        try:
            self.font = pygame.font.Font(os.path.join("textures", "determination.ttf"), 12)
            self.bubble_font = pygame.font.Font(os.path.join("textures", "determination.ttf"), 11)
        except:
            self.font = pygame.font.SysFont("arial", 16)
            self.bubble_font = pygame.font.SysFont("arial", 12)
            
        self.player_name = player_name
        self.hp = hp
        self.max_hp = max_hp
        self.lv = lv
        self.inventory = inventory
        
        self.snd_squeak = load_sound("snd_squeak.ogg")
        self.snd_select = load_sound("snd_select.ogg")
        self.snd_txt2 = load_sound("snd_txt2.ogg")
        self.snd_baha = load_sound("snd_baha.ogg")
        self.snd_logappear = load_sound("logappear.ogg")
        self.snd_logkataetsa = load_sound("logkataetsa.ogg")
        self.snd_hurt = load_sound("snd_arrow.ogg") 

        self.snd_bomb = load_sound("snd_bomb.ogg") 
        self.snd_stomp = load_sound("heavy_footstep.ogg")
        self.bg_music_path = os.path.join("sounds", "You messed with the wrong one.ogg") 
        
        # --- СИСТЕМА АНИМАЦИИ БАХИ ---
        self.bpm = 130
        self.ms_per_beat = 60000 / self.bpm 
        self.baha_frame = 0
        self.baha_last_tick = pygame.time.get_ticks()
        self.baha_alpha = 255
        
        self.baha_animations = {}
        filenames = ["BahaAnim_1.png", "BahaAnim_2.png", "BahaAnim_3.png", "BahaAnim_4.png"]
        
        for idx, fname in enumerate(filenames):
            frames = []
            path = os.path.join("textures", fname)
            try:
                sheet = pygame.image.load(path).convert_alpha()
                w = sheet.get_width() // 4
                h = sheet.get_height()
                for i in range(4):
                    frame = sheet.subsurface(pygame.Rect(i * w, 0, w, h))
                    frames.append(frame)
            except:
                for i in range(4):
                    surf = pygame.Surface((30, 40))
                    surf.fill((50 * idx, 255 - i * 50, 100)) 
                    frames.append(surf)
            self.baha_animations[idx + 1] = frames

        self.current_baha_anim = 1
        
        self.img_attack_bg = load_texture("atackpolosa.png")
        self.img_attack_bg = pygame.transform.scale(self.img_attack_bg, (280, 55)) 
        self.img_cursor1 = load_texture("atackletit.png")
        self.img_cursor1 = pygame.transform.scale(self.img_cursor1, (14, 55))
        self.img_cursor2 = load_texture("atack_loop.png")
        self.img_cursor2 = pygame.transform.scale(self.img_cursor2, (14, 55))
        self.img_zero = load_texture("zero.png")
        self.img_zero = pygame.transform.scale(self.img_zero, (25, 25))

        self.img_bubble = load_texture("textbubbles.png")
        self.img_bubble = pygame.transform.scale(self.img_bubble, (110, 65))
        
        log_sheet = load_texture("log.png") 
        self.log_frames = []
        try:
            w = log_sheet.get_width() // 3
            h = log_sheet.get_height()
            for i in range(3):
                frame_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                frame_surf.blit(log_sheet, (0, 0), (i * w, 0, w, h))
                frame_surf = pygame.transform.scale(frame_surf, (45, 15)) 
                self.log_frames.append(frame_surf)
        except:
            for i in range(3):
                dummy = pygame.Surface((45, 15))
                dummy.fill((200, 200, 0))
                self.log_frames.append(dummy)
                
        self.img_warning = load_texture("warningarrow.png")
        self.img_warning = pygame.transform.scale(self.img_warning, (16, 16))
        
        self.img_arrow = load_texture("arrow.png")
        self.img_arrow = pygame.transform.scale(self.img_arrow, (14, 40)) 

        self.img_bomb = load_texture("gasbomb.png")
        self.img_bomb = pygame.transform.scale(self.img_bomb, (20, 20))
        self.img_fart = load_texture("fart.png")
        self.img_fart = pygame.transform.scale(self.img_fart, (40, 40)) 

        self.img_leg_warn = load_texture("warningforlegs.png")
        self.img_leg_warn = pygame.transform.scale(self.img_leg_warn, (60, 118)) 
        self.img_leg_left = load_texture("leftleg.png")
        self.img_leg_left = pygame.transform.scale(self.img_leg_left, (117, 118))
        img_r = load_texture("righleg.png")
        if img_r.get_width() == 30: img_r = load_texture("rightleg.png")
        self.img_leg_right = pygame.transform.scale(img_r, (117, 118))
                
        heart_path = os.path.join("textures", "heart.png")
        try:
            self.heart_sprite = pygame.image.load(heart_path).convert_alpha()
        except:
            self.heart_sprite = pygame.Surface((12, 12))
            self.heart_sprite.fill((255, 0, 0))
        self.heart_sprite = pygame.transform.scale(self.heart_sprite, (12, 12))
        
        self.btn_sprites = {
            0: [load_texture("fight_0.png"), load_texture("fight_1.png")],
            1: [load_texture("act_0.png"),   load_texture("act_1.png")],
            2: [load_texture("item_0.png"),  load_texture("item_1.png")],
            3: [load_texture("mercy_0.png"), load_texture("mercy_1.png")]
        }
        for key in self.btn_sprites:
            self.btn_sprites[key][0] = pygame.transform.scale(self.btn_sprites[key][0], (70, 24))
            self.btn_sprites[key][1] = pygame.transform.scale(self.btn_sprites[key][1], (70, 24))
        
        # --- ПЕРЕМЕННЫЕ ЛОГИКИ И СЮЖЕТА ---
        self.turn_count = 0 
        self.act_phase = 0 
        self.correct_act_selected = False
        self.turns_survived_since_act = 0
        self.win_step = 0
        self.cutscene_timer = 0
        
        # ПЕРЕМЕННЫЕ ПОЩАДЫ
        self.can_spare = False
        self.ui_fade_alpha = 0
        
        self.is_enraged = False 
        self.enrage_dialogue_done = False
        # ----------------------------------------

        self.state = "PRE_BATTLE_BUBBLE" 
        self.current_box = pygame.Rect(ARENA_RECT)
        self.selected_button = 0 
        self.sub_selected = 0 
        self.bar_x = 20
        self.bar_speed = 6
        self.flash_start = 0
        self.zero_y = 0
        self.turn_start = 0
        self.heart_x = WIDTH//2 - 6 
        self.heart_y = 165
        self.heart_speed = 2         
        self.transition_start = 0
        self.transition_duration = 300 
        self.dialog_text = "Ну че\nначнем?"
        self.char_index = 0
        self.last_tick = pygame.time.get_ticks()
        self.invincible_timer = 0  
        self.attack_type = 1
        self.logs = []
        self.arrows = []
        self.arrow_spawn_timer = 0

    def play_sound(self, sound, stop_previous=False):
        if sound:
            if stop_previous: sound.stop()
            sound.play()

    def get_act_options(self):
        if getattr(self, 'is_enraged', False):
            return ["Статистика"]
            
        # ЕСЛИ БАХА ГОТОВ К ПОЩАДЕ (имя желтое), ОСТАВЛЯЕМ ТОЛЬКО СТАТИСТИКУ
        if self.can_spare:
            return ["Статистика"]
            
        if self.correct_act_selected or self.act_phase == 0: 
            return ["Статистика"] 
        
        if self.act_phase == 1: 
            return ["Увлечения", "О дискретке", "Об охраннике"]
        elif self.act_phase == 2: 
            return ["Дота 2", "Решать дискретку", "Купить колу"]
        elif self.act_phase == 3: 
            return ["Секретный файл"]
            
        return []

    def handle_event(self, event):
        if self.state in ["PRE_BATTLE_BUBBLE", "POST_ATTACK_BUBBLE"]:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_z):
                if self.char_index >= len(self.dialog_text):
                    self.play_sound(self.snd_select)
                    if self.state == "PRE_BATTLE_BUBBLE":
                        self.state = "TRANSITION_PRE_TO_MENU"
                        self.transition_start = pygame.time.get_ticks()
                        try:
                            pygame.mixer.music.load(self.bg_music_path)
                            pygame.mixer.music.play(-1)
                            self.music_start_time = pygame.time.get_ticks() 
                        except:
                            self.music_start_time = pygame.time.get_ticks()
                    else:
                        self.state = "MENU"
                        self.dialog_text = "* Баха ждет вашего хода."
                        self.char_index = len(self.dialog_text)

        elif self.state == "ENRAGE_BUBBLE":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_z):
                if self.char_index >= len(self.dialog_text):
                    self.play_sound(self.snd_select)
                    # ПРОПУСКАЕМ МЕНЮ ИГРОКА И ИДЕМ СРАЗУ В АТАКУ
                    self.state = "TRANSITION_TO_ARENA"
                    self.transition_start = pygame.time.get_ticks()

        elif self.state == "WIN_CUTSCENE":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_z):
                if self.win_step < 3 and self.char_index >= len(self.dialog_text):
                    self.win_step += 1
                    self.char_index = 0
                    self.last_tick = pygame.time.get_ticks()
                elif self.win_step == 3:
                    # ПОСЛЕ ДИАЛОГА ВКЛЮЧАЕМ ПОЩАДУ
                    self.can_spare = True
                    self.state = "MENU"
                    self.dialog_text = "* Баха больше не хочет драться."
                    self.char_index = 0
                    
        elif self.state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.selected_button > 0:
                        self.selected_button -= 1
                        self.play_sound(self.snd_squeak)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_button < 3:
                        self.selected_button += 1
                        self.play_sound(self.snd_squeak)
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    if self.selected_button == 0: 
                        self.play_sound(self.snd_select)
                        self.state = "ATTACK_BAR"
                        self.bar_x = 20
                    elif self.selected_button == 1: 
                        self.play_sound(self.snd_select)
                        self.state = "ACT_MENU"
                        self.sub_selected = 0
                    elif self.selected_button == 2: 
                        if len(self.inventory) > 0:
                            self.play_sound(self.snd_select)
                            self.state = "ITEM_MENU"
                            self.sub_selected = 0
                    elif self.selected_button == 3: 
                        self.play_sound(self.snd_select)
                        self.state = "MERCY_MENU"
                        self.sub_selected = 0
                        
        elif self.state == "ACT_MENU":
            options = self.get_act_options()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    if self.sub_selected > 0:
                        self.sub_selected -= 1
                        self.play_sound(self.snd_squeak)
                elif event.key == pygame.K_RIGHT: 
                    if len(options) > 0 and self.sub_selected < len(options) - 1:
                        self.sub_selected += 1
                        self.play_sound(self.snd_squeak)
                elif event.key == pygame.K_ESCAPE: 
                    self.state = "MENU"
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    self.play_sound(self.snd_select)
                    self.state = "DIALOG"
                    self.char_index = 0
                    
                    if not options or options == ["Статистика"]:
                        self.dialog_text = "* БАХА - 999 ATK 999 DEF\n* Клэш рояль про"
                    else:
                        if self.act_phase == 1:
                            if self.sub_selected == 0:
                                self.dialog_text = "* Баха сделал вид что\nему не интересно."
                                self.correct_act_selected = True 
                            elif self.sub_selected == 1:
                                self.dialog_text = "* Бахе не интересно было\nэто слушать."
                            elif self.sub_selected == 2:
                                self.dialog_text = "* Баха осужденно посмотрел\nна вас."
                        elif self.act_phase == 2:
                            if self.sub_selected == 0:
                                self.dialog_text = "* Баха не понял зачем и\nсмотрит с непониманием."
                            elif self.sub_selected == 1:
                                self.dialog_text = "* Баха не понял зачем и\nсмотрит с непониманием."
                            elif self.sub_selected == 2:
                                self.dialog_text = "* Баха загорелся глазами и\nодобрительно кивнул."
                                self.correct_act_selected = True 
                                
                        elif self.act_phase == 3:
                            if self.sub_selected == 0:
                                self.state = "WIN_CUTSCENE"
                                self.win_step = 0
                                self.dialog_text = ""
                                self.char_index = 0
                                self.cutscene_timer = pygame.time.get_ticks()
                                pygame.mixer.music.stop()
                        
        elif self.state == "ITEM_MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.state = "MENU"
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    self.play_sound(self.snd_select)
                    if "Секретные файлы" in self.inventory:
                        self.state = "DIALOG"
                        self.char_index = 0
                        self.dialog_text = "* Вам страшно смотреть на секретный \nфайл."
                    else:
                        self.state = "MENU"
                        
        elif self.state == "MERCY_MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.state = "MENU"
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    self.play_sound(self.snd_select)
                    # Нет выбора (сбежать убрано), поэтому всегда проверяем пощаду
                    if self.can_spare:
                        self.state = "SPARING_BAHA"
                        self.dialog_text = ""
                    else:
                        self.state = "DIALOG"
                        self.char_index = 0
                        self.dialog_text = "* Охранника не пощадить.."

        elif self.state == "ATTACK_BAR":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_z):
                    self.play_sound(self.snd_select)
                    self.state = "ATTACK_HIT_FLASH"
                    self.flash_start = pygame.time.get_ticks()
                    self.zero_y = 60 

        elif self.state in ["DIALOG", "ATTACK_MESSAGE"]:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_z):
                    if self.char_index >= len(self.dialog_text):
                        self.state = "TRANSITION_TO_ARENA"
                        self.transition_start = pygame.time.get_ticks()

    def update_and_draw(self, surface, current_time):
        surface.fill(BLACK)
        
        if hasattr(self, 'music_start_time'):
            elapsed_music_time = current_time - self.music_start_time
        else:
            elapsed_music_time = current_time

        ms_per_beat = 60000 / self.bpm 
        ms_for_two_beats = ms_per_beat * 2 
        ms_per_anim_frame = ms_for_two_beats / 4 

        self.baha_frame = int(elapsed_music_time / ms_per_anim_frame) % 4
        cycles_passed = int(elapsed_music_time / ms_for_two_beats)
        self.current_baha_anim = (cycles_passed % 4) + 1
        
        # --- ЛОГИКА КАТСЦЕНЫ ПОБЕДЫ ---
        if self.state == "WIN_CUTSCENE":
            self.current_baha_anim = 1
            self.baha_frame = 0 
            
            if self.win_step == 0:
                if current_time - self.cutscene_timer > 1000:
                    self.win_step = 1
                    self.dialog_text = "Неужели..."
                    self.char_index = 0
                    self.last_tick = current_time
            elif self.win_step == 1 and self.dialog_text != "Неужели...":
                self.dialog_text = "Неужели..."
            elif self.win_step == 2 and self.dialog_text != "Я смог...":
                self.dialog_text = "Я смог..."
            elif self.win_step == 3 and self.dialog_text != "найти\nбрата?":
                self.dialog_text = "найти\nбрата?"

        # --- ЛОГИКА ИСЧЕЗНОВЕНИЯ БАХИ ---
        if self.state == "SPARING_BAHA":
            self.current_baha_anim = 1
            self.baha_frame = 0
            self.baha_alpha = max(0, self.baha_alpha - 3)
            if self.baha_alpha <= 0:
                self.state = "SPARING_UI_FADE"

        if self.state == "TRANSITION_PRE_TO_MENU":
            progress = (current_time - self.transition_start) / self.transition_duration
            if progress > 1.0: 
                progress = 1.0
            
            self.current_box.x = int(TINY_RECT.x + (MENU_RECT.x - TINY_RECT.x) * progress)
            self.current_box.y = int(TINY_RECT.y + (MENU_RECT.y - TINY_RECT.y) * progress)
            self.current_box.width = int(TINY_RECT.width + (MENU_RECT.width - TINY_RECT.width) * progress)
            self.current_box.height = int(TINY_RECT.height + (MENU_RECT.height - TINY_RECT.height) * progress)
            
            if progress == 1.0:
                self.state = "INTRO" 
                self.dialog_text = "* Баха преграждает путь!"
                self.char_index = 0
                self.last_tick = current_time

        elif self.state == "TRANSITION_TO_ARENA":
            progress = (current_time - self.transition_start) / self.transition_duration
            if progress > 1.0: 
                progress = 1.0
            
            self.current_box.x = int(MENU_RECT.x + (ARENA_RECT.x - MENU_RECT.x) * progress)
            self.current_box.y = int(MENU_RECT.y + (ARENA_RECT.y - MENU_RECT.y) * progress)
            self.current_box.width = int(MENU_RECT.width + (ARENA_RECT.width - MENU_RECT.width) * progress)
            self.current_box.height = int(MENU_RECT.height + (ARENA_RECT.height - MENU_RECT.height) * progress)
            
            if progress == 1.0:
                self.state = "ENEMY_TURN"
                self.turn_start = current_time
                self.heart_x = WIDTH//2 - 6
                self.heart_y = 165
                
                if self.can_spare:
                    self.attack_type = 0 # Пустая атака (0)
                elif self.is_enraged:
                    self.attack_type = 5
                elif self.turn_count == 0: 
                    self.attack_type = 1
                elif self.turn_count == 1: 
                    self.attack_type = 2
                elif self.turn_count == 2: 
                    self.attack_type = 3
                elif self.turn_count == 3: 
                    self.attack_type = 4
                else: 
                    self.attack_type = random.choice([1, 2, 3, 4])
                
                if self.attack_type == 1:
                    self.attack_wave = 1
                    self.play_sound(self.snd_logappear)
                    self.logs = [
                        {"x": WIDTH//2 - 50, "y": 10, "state": "falling", "dir": 1, "frame": 0, "sound_played": False, "anim_timer": current_time},
                        {"x": WIDTH//2 + 5, "y": -40, "state": "falling", "dir": -1, "frame": 0, "sound_played": False, "anim_timer": current_time},
                        {"x": WIDTH//2 - 30, "y": -90, "state": "falling", "dir": 1, "frame": 0, "sound_played": False, "anim_timer": current_time}
                    ]
                elif self.attack_type == 2:
                    self.arrows = []
                    self.arrow_wave_timer = current_time
                    self.play_sound(self.snd_squeak)
                    for i in range(5):
                        target_x = random.randint(self.current_box.left + 5, self.current_box.right - 20)
                        target_y = random.randint(self.current_box.top + 5, self.current_box.bottom - 45)
                        self.arrows.append({
                            "x": target_x, "y": -50, "target_y": target_y,
                            "state": "warning", "wave_start": current_time, 
                            "fire_delay": i * 200, "speed": 2.0
                        })

                elif self.attack_type == 3:
                    self.bombs = []
                    self.bomb_timer = current_time
                    self.play_sound(self.snd_squeak)

                elif self.attack_type == 4:
                    self.leg_state = "warning"
                    self.leg_timer = current_time
                    self.leg_side = random.choice(["left", "right"])
                    self.leg_stomps_done = 0
                    self.play_sound(self.snd_squeak)
                    
                elif self.attack_type == 5:
                    self.leg_state = "warning"
                    self.leg_timer = current_time
                    self.play_sound(self.snd_squeak)

        elif self.state == "TRANSITION_TO_MENU":
            progress = (current_time - self.transition_start) / self.transition_duration
            if progress > 1.0: 
                progress = 1.0
            
            self.current_box.x = int(ARENA_RECT.x + (MENU_RECT.x - ARENA_RECT.x) * progress)
            self.current_box.y = int(ARENA_RECT.y + (MENU_RECT.y - ARENA_RECT.y) * progress)
            self.current_box.width = int(ARENA_RECT.width + (MENU_RECT.width - ARENA_RECT.width) * progress)
            self.current_box.height = int(ARENA_RECT.height + (MENU_RECT.height - ARENA_RECT.height) * progress)
            
            if progress == 1.0:
                self.logs.clear()
                self.arrows.clear()
                
                self.turn_count += 1
                
                if self.turn_count == 1 and self.act_phase == 0:
                    self.act_phase = 1
                
                if self.correct_act_selected:
                    self.turns_survived_since_act += 1
                    if self.turns_survived_since_act >= 3:
                        # ПРОВЕРКА НА НАЛИЧИЕ СЕКРЕТНОГО ФАЙЛА
                        if self.act_phase == 2 and "Секретные файлы" not in self.inventory:
                            self.is_enraged = True
                            self.correct_act_selected = False
                        else:
                            self.act_phase += 1
                            self.correct_act_selected = False
                            self.turns_survived_since_act = 0

                # ВМЕСТО МЕНЮ ИДЕМ В СПЕЦИАЛЬНЫЙ БАББЛ, ЕСЛИ БАХА РАЗОЗЛЕН
                if self.is_enraged and not self.enrage_dialogue_done:
                    self.state = "ENRAGE_BUBBLE"
                    self.dialog_text = "Ты мне\nнадоел!"
                    self.char_index = 0
                    self.last_tick = current_time
                    self.enrage_dialogue_done = True
                else:
                    self.state = "POST_ATTACK_BUBBLE"
                    self.char_index = 0
                    self.last_tick = current_time
                    
                    # Если пощада доступна, он просто молчит
                    if self.can_spare:
                        self.dialog_text = "..."
                    elif self.turn_count == 1: 
                        self.dialog_text = "Ну как тебе\nБРЕВНА?"
                    elif self.turn_count == 2: 
                        self.dialog_text = "Ойёй,\nстрелы."
                    elif self.turn_count == 3: 
                        self.dialog_text = "четкий запах,\nда?"
                    elif self.turn_count == 4: 
                        self.dialog_text = "ноги."
                    else: 
                        self.dialog_text = "Хехе..." 

        elif self.state in ["ENEMY_TURN", "PRE_BATTLE_BUBBLE"]:
            self.current_box = pygame.Rect(ARENA_RECT)
        else:
            self.current_box = pygame.Rect(MENU_RECT)

        # --- ОТРИСОВКА БАХИ ---
        current_baha_img = self.baha_animations[self.current_baha_anim][self.baha_frame].copy()
        current_baha_img.set_alpha(self.baha_alpha)
        spr_x = WIDTH // 2 - current_baha_img.get_width() // 2
        spr_y = 0
        surface.blit(current_baha_img, (spr_x, spr_y))

        text_speed = 30 
        show_bubble = False
        
        # ДОБАВЛЯЕМ ENRAGE_BUBBLE В СПИСОК ПУЗЫРЕЙ
        if self.state in ["PRE_BATTLE_BUBBLE", "POST_ATTACK_BUBBLE", "WIN_CUTSCENE", "ENRAGE_BUBBLE"]:
            show_bubble = True

        if show_bubble:
            bubble_x = spr_x + 50
            bubble_y = spr_y + 10 
            surface.blit(self.img_bubble, (bubble_x, bubble_y))

            if current_time - self.last_tick > text_speed:
                if self.char_index < len(self.dialog_text):
                    new_char = self.dialog_text[self.char_index]
                    self.char_index += 1
                    if new_char not in [" ", "\n"]:
                        self.play_sound(self.snd_baha, stop_previous=True) 
                self.last_tick = current_time
            
            vis_text = self.dialog_text[:self.char_index] 
            for i, line in enumerate(vis_text.split('\n')):
                text_x = bubble_x + 21
                text_y = bubble_y + 12 + (i * 12) 
                surface.blit(self.bubble_font.render(line, True, BLACK), (text_x, text_y))

        # Отрисовка арены, меню и UI всегда, пока интерфейс полностью не исчез
        pygame.draw.rect(surface, BLACK, self.current_box)
        pygame.draw.rect(surface, WHITE, self.current_box, 2)

        if self.state == "PRE_BATTLE_BUBBLE":
            surface.blit(self.heart_sprite, (WIDTH//2 - 6, 165))

        menu_states = ["INTRO", "INTRO_WAIT", "MENU", "DIALOG", "ACT_MENU", "ITEM_MENU", "MERCY_MENU", "ATTACK_BAR", "ATTACK_HIT_FLASH", "ATTACK_MESSAGE", "POST_ATTACK_BUBBLE", "ENRAGE_BUBBLE"]
        
        if self.state in menu_states:
            if self.state in ["INTRO", "DIALOG", "ATTACK_MESSAGE"]:
                if current_time - self.last_tick > text_speed:
                    if self.char_index < len(self.dialog_text):
                        new_char = self.dialog_text[self.char_index]
                        self.char_index += 1
                        if new_char not in [" ", "\n"]:
                            self.play_sound(self.snd_txt2, stop_previous=True) 
                    else:
                        if self.state == "INTRO":
                            self.state = "INTRO_WAIT"
                            self.intro_wait_start = current_time
                    self.last_tick = current_time
                visible_text = self.dialog_text[:self.char_index]
                for i, line in enumerate(visible_text.split('\n')):
                    surface.blit(self.font.render(line, True, WHITE), (25, 130 + i * 20)) 

            elif self.state == "INTRO_WAIT":
                for i, line in enumerate(self.dialog_text.split('\n')):
                    surface.blit(self.font.render(line, True, WHITE), (25, 130 + i * 20))
                if current_time - self.intro_wait_start > 1000:
                    self.state = "MENU"
                    
            elif self.state in ["MENU", "POST_ATTACK_BUBBLE"]:
                if self.state == "MENU":
                    for i, line in enumerate(self.dialog_text.split('\n')):
                        surface.blit(self.font.render(line, True, WHITE), (25, 130 + i * 20))
                    
            elif self.state == "ACT_MENU":
                opts = self.get_act_options()
                positions = [(55, 130), (175, 130), (55, 150), (175, 150)]
                if opts: 
                    for i, opt in enumerate(opts):
                        surface.blit(self.font.render(opt, True, WHITE), positions[i])
                        if i == self.sub_selected:
                            surface.blit(self.heart_sprite, (positions[i][0] - 20, positions[i][1] - 1))
                
            elif self.state == "ITEM_MENU":
                if "Секретные файлы" in self.inventory:
                    surface.blit(self.font.render("Секретные файлы", True, WHITE), (55, 130))
                surface.blit(self.heart_sprite, (35, 129))
                    
            elif self.state == "MERCY_MENU":
                # УБРАНА КНОПКА СБЕЖАТЬ (Осталась только Пощада)
                spare_color = (255, 255, 0) if self.can_spare else WHITE
                surface.blit(self.font.render("Пощада", True, spare_color), (55, 130))
                surface.blit(self.heart_sprite, (35, 129))

            elif self.state == "ATTACK_BAR":
                surface.blit(self.img_attack_bg, (20, 125))
                self.bar_x += self.bar_speed
                if self.bar_x > 280: 
                    self.state = "ATTACK_HIT_FLASH"
                    self.flash_start = current_time
                    self.zero_y = 60
                surface.blit(self.img_cursor1, (self.bar_x, 125))
                
            elif self.state == "ATTACK_HIT_FLASH":
                surface.blit(self.img_attack_bg, (20, 125))
                if ((current_time - self.flash_start) // 100) % 2 == 0:
                    surface.blit(self.img_cursor1, (self.bar_x, 125))
                else:
                    surface.blit(self.img_cursor2, (self.bar_x, 125))
                self.zero_y -= 0.5 
                surface.blit(self.img_zero, (WIDTH // 2 - 12, self.zero_y))
                if current_time - self.flash_start > 1000:
                    self.state = "ATTACK_MESSAGE"
                    self.dialog_text = "* По Бахе невозможно попасть."
                    self.char_index = 0
                    self.last_tick = current_time

            stat_y = 190
            surface.blit(self.font.render(f"{self.player_name}   LV {self.lv}", True, WHITE), (20, stat_y))
            surface.blit(self.font.render("HP", True, WHITE), (120, stat_y))
            pygame.draw.rect(surface, (255, 0, 0), (140, stat_y, self.max_hp * 2.0, 11)) 
            pygame.draw.rect(surface, (255, 255, 0), (140, stat_y, self.hp * 2.0, 11))  
            surface.blit(self.font.render(f"{self.hp} / {self.max_hp}", True, WHITE), (140 + int(self.max_hp * 2.0) + 10, stat_y))

            btn_y = 210
            btn_spacing = 74 
            for i in range(4):
                x = 12 + i * btn_spacing
                is_selected = (i == self.selected_button and self.state in ["MENU", "POST_ATTACK_BUBBLE", "ENRAGE_BUBBLE"])
                frame = 1 if is_selected else 0
                btn_img = self.btn_sprites[i][frame]
                
                # ЕСЛИ ДОСТУПНА ПОЩАДА, КНОПКА MERCY СЛЕГКА ПОДСВЕЧИВАЕТСЯ ЖЕЛТЫМ
                surface.blit(btn_img, (x, btn_y))
                    
                if is_selected and self.state == "MENU": 
                    surface.blit(self.heart_sprite, (x + 6, btn_y + 6))

        # --- ЛОГИКА ХОДА ВРАГА ---
        elif self.state == "ENEMY_TURN":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  
                self.heart_x -= self.heart_speed
            if keys[pygame.K_RIGHT]: 
                self.heart_x += self.heart_speed
            if keys[pygame.K_UP]:    
                self.heart_y -= self.heart_speed
            if keys[pygame.K_DOWN]:  
                self.heart_y += self.heart_speed
                
            if self.heart_x < self.current_box.left + 2: 
                self.heart_x = self.current_box.left + 2
            if self.heart_x > self.current_box.right - 14: 
                self.heart_x = self.current_box.right - 14
            if self.heart_y < self.current_box.top + 2: 
                self.heart_y = self.current_box.top + 2
            if self.heart_y > self.current_box.bottom - 14: 
                self.heart_y = self.current_box.bottom - 14

            heart_hitbox = pygame.Rect(self.heart_x + 2, self.heart_y + 2, 8, 8) 

            # --- ПУСТАЯ АТАКА (если можно пощадить, но игрок выбрал что-то другое) ---
            if self.attack_type == 0:
                if current_time - self.turn_start > 3000: # Просто 3 секунды ожидания
                    self.state = "TRANSITION_TO_MENU"
                    self.transition_start = current_time

            elif self.attack_type == 1:
                if self.attack_wave == 1 and current_time - self.turn_start > 3500:
                    self.attack_wave = 2
                    self.play_sound(self.snd_logappear)
                    self.logs = [
                        {"x": WIDTH//2 + 10, "y": 10, "state": "falling", "dir": -1, "frame": 0, "sound_played": False, "anim_timer": current_time},
                        {"x": WIDTH//2 - 40, "y": -40, "state": "falling", "dir": 1, "frame": 0, "sound_played": False, "anim_timer": current_time},
                        {"x": WIDTH//2 + 30, "y": -90, "state": "falling", "dir": -1, "frame": 0, "sound_played": False, "anim_timer": current_time}
                    ]

                for log in self.logs:
                    if log["state"] == "falling":
                        log["y"] += 2.0 
                        if log["y"] >= self.current_box.bottom - 18:
                            log["y"] = self.current_box.bottom - 18
                            log["state"] = "rolling"
                            if not log["sound_played"]:
                                self.play_sound(self.snd_logkataetsa)
                                log["sound_played"] = True
                    elif log["state"] == "rolling":
                        log["x"] += 1.8 * log["dir"] 
                        if current_time - log["anim_timer"] > 100:
                            log["frame"] = (log["frame"] + 1) % 3
                            log["anim_timer"] = current_time

                    if log["y"] > self.current_box.top - 15 and log["y"] < self.current_box.bottom:
                        log_img = self.log_frames[0 if log["state"] == "falling" else log["frame"]]
                        surface.blit(log_img, (log["x"], log["y"]))
                    
                    log_hitbox = pygame.Rect(log["x"] + 2, log["y"] + 2, 41, 11)
                    if heart_hitbox.colliderect(log_hitbox):
                        if current_time - self.invincible_timer > 1000: 
                            self.hp -= 4
                            self.play_sound(self.snd_hurt)
                            self.invincible_timer = current_time
                            if self.hp < 0: 
                                self.hp = 0

                if current_time - self.turn_start > 7000:
                    self.state = "TRANSITION_TO_MENU"
                    self.transition_start = current_time

            elif self.attack_type == 2:
                if current_time - self.arrow_wave_timer > 3000:
                    self.arrow_wave_timer = current_time
                    self.play_sound(self.snd_squeak)
                    for i in range(5):
                        target_x = random.randint(self.current_box.left + 5, self.current_box.right - 20)
                        target_y = random.randint(self.current_box.top + 5, self.current_box.bottom - 45)
                        self.arrows.append({
                            "x": target_x, "y": -50, "target_y": target_y,
                            "state": "warning", "wave_start": current_time,
                            "fire_delay": i * 200 
                        })

                warning_duration = 1000 

                for arr in self.arrows:
                    if arr["state"] == "warning":
                        if current_time - arr["wave_start"] < warning_duration:
                            if ((current_time - arr["wave_start"]) // 100) % 2 == 0:
                                surface.blit(self.img_warning, (arr["x"], arr["target_y"] + 12))
                        else:
                            arr["state"] = "waiting"

                    elif arr["state"] == "waiting":
                        time_since_warning_end = current_time - (arr["wave_start"] + warning_duration)
                        if time_since_warning_end >= arr["fire_delay"]:
                            arr["state"] = "flying"

                    elif arr["state"] == "flying":
                        arr["speed"] = arr.get("speed", 2.0) + 1.5 
                        arr["y"] += arr["speed"]
                        
                        if arr["y"] >= arr["target_y"]:
                            arr["y"] = arr["target_y"]
                            arr["state"] = "stuck"
                            arr["stuck_time"] = current_time 
                            self.play_sound(self.snd_hurt)
                        surface.blit(self.img_arrow, (arr["x"], arr["y"]))

                    elif arr["state"] == "stuck":
                        surface.blit(self.img_arrow, (arr["x"], arr["y"]))
                        if current_time - arr["stuck_time"] > 1000:
                            arr["state"] = "fading"
                            arr["alpha"] = 255 

                    elif arr["state"] == "fading":
                        arr["alpha"] -= 15
                        if arr["alpha"] > 0:
                            temp_arrow = self.img_arrow.copy()
                            temp_arrow.set_alpha(arr["alpha"])
                            surface.blit(temp_arrow, (arr["x"], arr["y"]))
                        else:
                            arr["state"] = "dead" 

                    if arr["state"] in ["flying", "stuck"]:
                        arr_hitbox = pygame.Rect(arr["x"] + 2, arr["y"] + 2, 10, 36)
                        if heart_hitbox.colliderect(arr_hitbox):
                            if current_time - self.invincible_timer > 1000: 
                                self.hp -= 3
                                self.play_sound(self.snd_hurt)
                                self.invincible_timer = current_time
                                if self.hp < 0: 
                                    self.hp = 0

                self.arrows = [arr for arr in self.arrows if arr["state"] != "dead"]

                if current_time - self.turn_start > 6500:
                    self.state = "TRANSITION_TO_MENU"
                    self.transition_start = current_time

            elif self.attack_type == 3:
                if current_time - self.bomb_timer > 1500:
                    self.bomb_timer = current_time
                    self.play_sound(self.snd_squeak)

                    spawn_side = random.choice(["top", "bottom", "left", "right"])
                    
                    if spawn_side == "top":
                        start_x = random.randint(self.current_box.left + 5, self.current_box.right - 25)
                        start_y = self.current_box.top
                        gx, gy = 0, 0.05  
                        vx, vy = random.uniform(-0.8, 0.8), random.uniform(0.2, 0.6) 
                    elif spawn_side == "bottom":
                        start_x = random.randint(self.current_box.left + 5, self.current_box.right - 25)
                        start_y = self.current_box.bottom - 20
                        gx, gy = 0, -0.05 
                        vx, vy = random.uniform(-0.8, 0.8), random.uniform(-0.6, -0.2)
                    elif spawn_side == "left":
                        start_x = self.current_box.left
                        start_y = random.randint(self.current_box.top + 5, self.current_box.bottom - 25)
                        gx, gy = 0.05, 0 
                        vx, vy = random.uniform(0.2, 0.6), random.uniform(-0.8, 0.8)
                    else: 
                        start_x = self.current_box.right - 20
                        start_y = random.randint(self.current_box.top + 5, self.current_box.bottom - 25)
                        gx, gy = -0.05, 0 
                        vx, vy = random.uniform(-0.6, -0.2), random.uniform(-0.8, 0.8)

                    self.bombs.append({
                        "x": start_x, "y": start_y,
                        "vx": vx, "vy": vy,
                        "gx": gx, "gy": gy,
                        "state": "flying",
                        "scale": 0.5, 
                        "alpha": 255
                    })

                for bomb in self.bombs:
                    if bomb["state"] == "flying":
                        bomb["vx"] += bomb["gx"]
                        bomb["vy"] += bomb["gy"]
                        bomb["x"] += bomb["vx"]
                        bomb["y"] += bomb["vy"]

                        hit_wall = False
                        
                        if bomb["x"] <= self.current_box.left + 5 and bomb["vx"] < 0:
                            bomb["x"] = self.current_box.left + 5
                            hit_wall = True
                        elif bomb["x"] >= self.current_box.right - 25 and bomb["vx"] > 0:
                            bomb["x"] = self.current_box.right - 25
                            hit_wall = True

                        if bomb["y"] <= self.current_box.top + 5 and bomb["vy"] < 0:
                            bomb["y"] = self.current_box.top + 5
                            hit_wall = True
                        elif bomb["y"] >= self.current_box.bottom - 25 and bomb["vy"] > 0:
                            bomb["y"] = self.current_box.bottom - 25
                            hit_wall = True

                        if hit_wall:
                            bomb["state"] = "exploding"
                            self.play_sound(self.snd_bomb) 

                        surface.blit(self.img_bomb, (bomb["x"], bomb["y"]))
                        
                        bomb_hitbox = pygame.Rect(bomb["x"], bomb["y"], 20, 20)
                        if heart_hitbox.colliderect(bomb_hitbox):
                            if current_time - self.invincible_timer > 1000:
                                self.hp -= 1
                                self.play_sound(self.snd_hurt)
                                self.invincible_timer = current_time

                    elif bomb["state"] == "exploding":
                        bomb["scale"] += 0.025  
                        bomb["alpha"] -= 1.5    

                        if bomb["alpha"] > 0:
                            base_w, base_h = 40, 40
                            new_w = int(base_w * bomb["scale"])
                            new_h = int(base_h * bomb["scale"])

                            fart_scaled = pygame.transform.scale(self.img_fart, (new_w, new_h))
                            fart_scaled.set_alpha(int(bomb["alpha"]))

                            cx = bomb["x"] + 10
                            cy = bomb["y"] + 10
                            draw_x = cx - new_w // 2
                            draw_y = cy - new_h // 2

                            surface.blit(fart_scaled, (draw_x, draw_y))

                            offset_x = int(new_w * 0.32)
                            offset_y = int(new_h * 0.32)
                            hit_w = int(new_w * 0.36)
                            hit_h = int(new_h * 0.36)
                            
                            gas_hitbox = pygame.Rect(draw_x + offset_x, draw_y + offset_y, hit_w, hit_h)
                            
                            if heart_hitbox.colliderect(gas_hitbox):
                                if current_time - self.invincible_timer > 1000:
                                    self.hp -= 4
                                    self.play_sound(self.snd_hurt)
                                    self.invincible_timer = current_time
                                    if self.hp < 0: 
                                        self.hp = 0
                        else:
                            bomb["state"] = "dead"

                self.bombs = [b for b in self.bombs if b["state"] != "dead"]

                if current_time - self.turn_start > 9000:
                    self.state = "TRANSITION_TO_MENU"
                    self.transition_start = current_time

            elif self.attack_type == 4:
                half_width = self.current_box.width // 2
                
                if self.leg_side == "left":
                    zone_rect = pygame.Rect(self.current_box.left, self.current_box.top, half_width, self.current_box.height)
                    leg_img = self.img_leg_left
                else:
                    zone_rect = pygame.Rect(self.current_box.left + half_width, self.current_box.top, half_width, self.current_box.height)
                    leg_img = self.img_leg_right

                time_in_state = current_time - self.leg_timer

                if self.leg_state == "warning":
                    if (current_time // 100) % 2 == 0:
                        surface.blit(self.img_leg_warn, (zone_rect.x, zone_rect.y + 1)) 
                    
                    if time_in_state > 600:
                        self.leg_state = "falling"
                        self.leg_timer = current_time
                        
                        self.current_leg_y = self.current_box.top - leg_img.get_height()
                        self.target_leg_y = self.current_box.bottom - leg_img.get_height() - 2
                        
                        self.play_sound(self.snd_squeak) 

                elif self.leg_state == "falling":
                    self.current_leg_y += 18 
                    
                    if self.current_leg_y >= self.target_leg_y:
                        self.current_leg_y = self.target_leg_y
                        self.leg_state = "stomp"
                        self.leg_timer = current_time
                        self.play_sound(self.snd_stomp) 

                    leg_x = zone_rect.x + (zone_rect.width - leg_img.get_width()) // 2
                    if self.leg_side == "left": 
                        leg_x -= 30  
                    else: 
                        leg_x += 30  
                    
                    surface.blit(leg_img, (leg_x, self.current_leg_y))
                    
                    if heart_hitbox.colliderect(zone_rect):
                        if current_time - self.invincible_timer > 1000:
                            self.hp -= 5
                            self.play_sound(self.snd_hurt)
                            self.invincible_timer = current_time
                            if self.hp < 0: 
                                self.hp = 0

                elif self.leg_state == "stomp":
                    leg_x = zone_rect.x + (zone_rect.width - leg_img.get_width()) // 2
                    if self.leg_side == "left": 
                        leg_x -= 30  
                    else: 
                        leg_x += 30  
                    
                    surface.blit(leg_img, (leg_x, self.target_leg_y))
                    
                    if heart_hitbox.colliderect(zone_rect):
                        if current_time - self.invincible_timer > 1000:
                            self.hp -= 5
                            self.play_sound(self.snd_hurt)
                            self.invincible_timer = current_time
                            if self.hp < 0: 
                                self.hp = 0

                    if time_in_state > 400:
                        self.leg_state = "cooldown"
                        self.leg_timer = current_time
                        self.leg_stomps_done += 1

                elif self.leg_state == "cooldown":
                    if time_in_state > 200:
                        if self.leg_stomps_done >= 6:
                            self.state = "TRANSITION_TO_MENU"
                            self.transition_start = current_time
                        else:
                            self.leg_state = "warning"
                            self.leg_timer = current_time
                            self.leg_side = random.choice(["left", "right"])
                            self.play_sound(self.snd_squeak)

            elif self.attack_type == 5:
                half_width = self.current_box.width // 2
                
                zone_left = pygame.Rect(self.current_box.left, self.current_box.top, half_width, self.current_box.height)
                zone_right = pygame.Rect(self.current_box.left + half_width, self.current_box.top, half_width, self.current_box.height)

                time_in_state = current_time - self.leg_timer

                if self.leg_state == "warning":
                    if (current_time // 50) % 2 == 0: 
                        surface.blit(self.img_leg_warn, (zone_left.x, zone_left.y + 1)) 
                        surface.blit(self.img_leg_warn, (zone_right.x, zone_right.y + 1)) 
                    
                    if time_in_state > 200: 
                        self.leg_state = "falling"
                        self.leg_timer = current_time
                        self.current_leg_y = self.current_box.top - self.img_leg_left.get_height()
                        self.target_leg_y = self.current_box.bottom - self.img_leg_left.get_height() - 2
                        self.play_sound(self.snd_squeak) 

                elif self.leg_state == "falling":
                    self.current_leg_y += 45 
                    
                    if self.current_leg_y >= self.target_leg_y:
                        self.current_leg_y = self.target_leg_y
                        self.leg_state = "stomp"
                        self.leg_timer = current_time
                        self.play_sound(self.snd_stomp) 

                    l_x = zone_left.x + (zone_left.width - self.img_leg_left.get_width()) // 2 - 30  
                    r_x = zone_right.x + (zone_right.width - self.img_leg_right.get_width()) // 2 + 30  
                    
                    surface.blit(self.img_leg_left, (l_x, self.current_leg_y))
                    surface.blit(self.img_leg_right, (r_x, self.current_leg_y))
                    
                    if heart_hitbox.colliderect(zone_left) or heart_hitbox.colliderect(zone_right):
                        self.hp -= 999
                        if self.hp < 0: self.hp = 0

                elif self.leg_state == "stomp":
                    l_x = zone_left.x + (zone_left.width - self.img_leg_left.get_width()) // 2 - 30  
                    r_x = zone_right.x + (zone_right.width - self.img_leg_right.get_width()) // 2 + 30  
                    
                    surface.blit(self.img_leg_left, (l_x, self.target_leg_y))
                    surface.blit(self.img_leg_right, (r_x, self.target_leg_y))
                    
                    if heart_hitbox.colliderect(zone_left) or heart_hitbox.colliderect(zone_right):
                        self.hp -= 999
                        if self.hp < 0: self.hp = 0

            # --- ОТРИСОВКА СЕРДЕЧКА ---
            if current_time - self.invincible_timer < 1000:
                if (current_time // 100) % 2 == 0:
                    surface.blit(self.heart_sprite, (self.heart_x, self.heart_y))
            else:
                surface.blit(self.heart_sprite, (self.heart_x, self.heart_y))

        # === ЗАТЕМНЕНИЕ ИНТЕРФЕЙСА ПОСЛЕ ИСЧЕЗНОВЕНИЯ БАХИ ===
        if self.state == "SPARING_UI_FADE":
            self.ui_fade_alpha = min(255, self.ui_fade_alpha + 4)
            fade_surf = pygame.Surface((WIDTH, HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.ui_fade_alpha)
            surface.blit(fade_surf, (0, 0))
            if self.ui_fade_alpha >= 255:
                return "WIN_BATTLE"

        # === ПРОВЕРКА НА СМЕРТЬ ===
        if self.hp <= 0:
            return "GAMEOVER_ANIM"
            
        return STATE_BATTLE