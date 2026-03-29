import pandas as pd
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import random
import os

# --- KONFIGURACIJA ---
FONT_PATH = "Patrick_Hand/PatrickHand.ttf" 
BG_COLOR = (0.96, 0.93, 0.90, 1)
CARD_COLOR = (1, 0.95, 0.96, 1)
BTN_COLOR = (0.95, 0.75, 0.80, 1)
TEXT_COLOR = (0.6, 0.2, 0.4, 1)

ICON_FILLED = "star_filled.png"
ICON_EMPTY = "star_empty.png"
HEART_LOGO = "heart.png" 

CATEGORY_COLORS = {
    "serious conv": (0.96, 0.93, 0.90, 1),
    "wild side of us": (1, 0.6, 0.6, 1),
    "fun & games": (0.8, 0.95, 0.9, 1),
    "deep talks": (0.9, 0.85, 1, 1),
    "PRILJUBLJENE": (1, 0.85, 0.4, 1),
}

FAVORITES_FILE = "favorites.txt"

class CardApp(App):
    def build(self):
        self.load_data()
        self.root_layout = BoxLayout(orientation="vertical", padding=20)

        with self.root_layout.canvas.before:
            Color(*BG_COLOR)
            self.bg = RoundedRectangle(pos=self.root_layout.pos, size=self.root_layout.size)

        self.root_layout.bind(pos=self.update_bg, size=self.update_bg)
        
        # ZAČNEMO NA GLAVNEM IZBIRNEM MENIJU
        self.show_main_selection()
        return self.root_layout

    def load_data(self):
        try:
            df = pd.read_csv("cards.csv", encoding="utf-8")
            self.questions = df.groupby("EDITION")["QUESTION"].apply(list).to_dict()
        except:
            self.questions = {"Info": ["Manjka cards.csv!"]}

        self.favorites = []
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                    self.favorites = [line.strip() for line in f.readlines() if line.strip()]
            except:
                self.favorites = []
        
        if self.favorites:
            self.questions["PRILJUBLJENE"] = self.favorites

    def update_bg(self, *args):
        self.bg.pos = self.root_layout.pos
        self.bg.size = self.root_layout.size

    # --- GLAVNI IZBIRNI MENI ---
    def show_main_selection(self):
        self.root_layout.clear_widgets()
        layout = BoxLayout(orientation="vertical", padding=[30, 50, 30, 50], spacing=30)

        header = BoxLayout(orientation="vertical", size_hint=(1, 0.4), spacing=10)
        heart_img = Image(source=HEART_LOGO, size_hint=(1, 0.7), keep_ratio=True)
        title = Label(
            text="ČAS ZA NAJIN POGOVOR", 
            font_size=42, 
            font_name=FONT_PATH, 
            color=TEXT_COLOR,
            size_hint=(1, 0.2)
        )
        subtitle = Label(
            text="Povežita se na globlji ravni ✨",
            font_size=32,
            font_name=FONT_PATH,
            color=(0.6, 0.2, 0.4, 0.7),
            size_hint=(1, 0.2),
            halign="center",
            valign="middle" # Spremenjeno v middle za boljšo poravnavo
        )
        subtitle.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))

        header.add_widget(heart_img)
        header.add_widget(title)
        header.add_widget(subtitle)
        
        layout.add_widget(header)

        btn_box = BoxLayout(orientation="vertical", spacing=20, size_hint=(1, 0.6))
        
        # Gumb za Vprašanja
        btn_q = Button(text="VPRAŠANJA", font_size=32, font_name=FONT_PATH, color=TEXT_COLOR,
                       background_normal="", background_color=(0,0,0,0), size_hint_y=None, height=100)
        with btn_q.canvas.before:
            Color(*BTN_COLOR)
            btn_q.bg_rect = RoundedRectangle(radius=[25], pos=btn_q.pos, size=btn_q.size)
        btn_q.bind(pos=self.update_btn_rect, size=self.update_btn_rect)
        btn_q.bind(on_press=lambda x: self.show_questions_menu())
        
        # Gumb za Igre
        btn_g = Button(text="IGRE", font_size=32, font_name=FONT_PATH, color=TEXT_COLOR,
                       background_normal="", background_color=(0,0,0,0), size_hint_y=None, height=100)
        with btn_g.canvas.before:
            Color(0.8, 0.9, 0.8, 1) 
            btn_g.bg_rect = RoundedRectangle(radius=[25], pos=btn_g.pos, size=btn_g.size)
        btn_g.bind(pos=self.update_btn_rect, size=self.update_btn_rect)
        btn_g.bind(on_press=lambda x: self.show_games_menu())

        btn_box.add_widget(btn_q)
        btn_box.add_widget(btn_g)
        layout.add_widget(btn_box)
        self.root_layout.add_widget(layout)

    # --- MENI ZA VPRAŠANJA ---
    def show_questions_menu(self):
        self.load_data() 
        self.root_layout.clear_widgets()
        menu_content = BoxLayout(orientation="vertical", padding=[30, 10, 30, 30], spacing=20)

        back_btn = Button(text="< NAZAJ", font_name=FONT_PATH, size_hint=(None, None), size=(100, 40),
                          background_normal="", background_color=(0,0,0,0), color=TEXT_COLOR)
        back_btn.bind(on_press=lambda x: self.show_main_selection())
        menu_content.add_widget(back_btn)

        title = Label(text="IZBERI KATEGORIJO:", font_size=32, font_name=FONT_PATH, color=TEXT_COLOR, size_hint_y=0.1)
        menu_content.add_widget(title)

        grid = GridLayout(cols=1, spacing=15, size_hint=(1, 0.8))
        categories = sorted([c for c in self.questions.keys() if c != "PRILJUBLJENE"])
        for category in categories:
            self.add_menu_button(grid, category, BTN_COLOR)

        if "PRILJUBLJENE" in self.questions:
            grid.add_widget(Widget(size_hint_y=None, height=10))
            self.add_menu_button(grid, "PRILJUBLJENE", CATEGORY_COLORS["PRILJUBLJENE"])

        menu_content.add_widget(grid)
        self.root_layout.add_widget(menu_content)

    # --- MENI ZA IGRE ---
    def show_games_menu(self):
        self.root_layout.clear_widgets()
        layout = BoxLayout(orientation="vertical", padding=[30, 10, 30, 30], spacing=20)

        back_btn = Button(text="< NAZAJ", font_name=FONT_PATH, size_hint=(None, None), size=(100, 40),
                          background_normal="", background_color=(0,0,0,0), color=TEXT_COLOR)
        back_btn.bind(on_press=lambda x: self.show_main_selection())
        layout.add_widget(back_btn)

        title = Label(text="IZBERI IGRO:", font_size=32, font_name=FONT_PATH, color=TEXT_COLOR, size_hint_y=0.1)
        layout.add_widget(title)

        grid = GridLayout(cols=1, spacing=15, size_hint=(1, 0.8))
        self.add_menu_button(grid, "THIS OR THAT (kmalu)", (0.8, 0.8, 0.9, 1))
        layout.add_widget(grid)
        self.root_layout.add_widget(layout)

    # --- POMOŽNE FUNKCIJE ZA GUMBE ---
    def add_menu_button(self, container, category, color):
        btn = Button(text=category.upper(), font_size=26, font_name=FONT_PATH, color=TEXT_COLOR,
                     background_normal="", background_color=(0,0,0,0), size_hint_y=None, height=75)
        with btn.canvas.before:
            Color(*color)
            btn.bg_rect = RoundedRectangle(radius=[20], pos=btn.pos, size=btn.size)
        btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)
        
        if "(kmalu)" not in category:
            btn.bind(on_press=lambda x, c=category: self.choose_card_count(c))
            
        container.add_widget(btn)

    def update_btn_rect(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    # --- LOGIKA ZA VPRAŠANJA (choose, start, show, fav) ---
    def choose_card_count(self, category):
        if category == "PRILJUBLJENE":
            self.start_game_with_count(category, len(self.favorites))
            return
        box = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Izberi število kartic:", font_size=32, font_name=FONT_PATH, color=TEXT_COLOR)
        box.add_widget(label)
        for n in [5, 10, "Vse"]:
            val = len(self.questions[category]) if n == "Vse" else n
            btn = Button(text=str(n), size_hint=(1, None), height=60, font_name=FONT_PATH, font_size=24,
                         background_color=BTN_COLOR, background_normal="")
            btn.bind(on_press=lambda x, count=val: self.start_game_with_count(category, count))
            box.add_widget(btn)
        self.popup = Popup(title="Nastavitve", content=box, size_hint=(0.7, 0.5), title_font=FONT_PATH)
        self.popup.open()

    def start_game_with_count(self, category, count):
        if hasattr(self, 'popup'): self.popup.dismiss()
        self.category = category
        q_list = self.questions.get(category, [])
        self.deck = random.sample(q_list, min(count, len(q_list)))
        self.index = 0
        self.show_question()

    def show_question(self):
        self.root_layout.clear_widgets()
        if self.index >= len(self.deck):
            self.show_game_over()
            return

        current_q = self.deck[self.index]
        main_content = BoxLayout(orientation="vertical", spacing=20, padding=[20, 10, 20, 20])

        # 1. Info Label na vrhu
        info_label = Label(
            text=f"{self.category} ({self.index + 1}/{len(self.deck)})", 
            color=TEXT_COLOR, 
            font_size=32, 
            font_name=FONT_PATH, 
            size_hint=(1, 0.1),
            halign="center",
            valign="middle"
        )
        info_label.bind(size=info_label.setter("text_size"))
        main_content.add_widget(info_label)

        # 2. Kartica z vprašanjem
        card = BoxLayout(padding=30, size_hint=(1, 0.6))
        with card.canvas.before:
            # Barva kartice po kategoriji
            Color(*CATEGORY_COLORS.get(self.category, CARD_COLOR))
            self.card_rect = RoundedRectangle(radius=[25], pos=card.pos, size=card.size)
        card.bind(pos=self.update_card_rect, size=self.update_card_rect)
        
        q_label = Label(
            text=current_q, 
            font_size=34, 
            font_name=FONT_PATH, 
            halign="center", 
            valign="middle", 
            color=TEXT_COLOR
        )
        q_label.bind(size=q_label.setter("text_size"))
        card.add_widget(q_label)
        main_content.add_widget(card)

        # 3. NAVIGACIJSKA VRSTICA (Minimalistični gumbi po vzoru '< NAZAJ')
        # Uporabimo BoxLayout za čistejšo poravnavo minimalnih gumbov
        nav_bar = BoxLayout(orientation="horizontal", size_hint=(1, 0.15), spacing=10)

        # Skupne nastavitve za minimalistični gumb
        minimal_btn_args = {
            "font_name": FONT_PATH,
            "font_size": 32,
            "color": TEXT_COLOR,
            "background_normal": "",        # Odstrani privzeto senco
            "background_color": (0,0,0,0),  # Naredi ozadje prosojno
            "size_hint": (None, 1),         # Gumbi imajo fiksno širino, višina je cela vrstica
            "width": 120,                   # Širina gumba (prilagodi po potrebi)
            "halign": "center",
            "valign": "middle"
        }

        # --- Gumb NAZAJ ---
        btn_prev = Button(text="< NAZAJ", **minimal_btn_args)
        btn_prev.bind(size=btn_prev.setter("text_size"))
        btn_prev.bind(on_press=self.prev_question)
        
        # --- Gumb MENI ---
        btn_menu = Button(text="MENI", **minimal_btn_args)
        btn_menu.bind(size=btn_menu.setter("text_size"))
        btn_menu.bind(on_press=lambda x: self.show_questions_menu())

        # --- Gumb PRILJUBLJENE (Zvezdica) ---
        is_fav = current_q in self.favorites
        fav_container = RelativeLayout(size_hint=(None, 1), width=60) # Kontejner za zvezdico
        self.fav_btn_click = Button(background_color=(0,0,0,0), background_normal="", text="", size_hint=(1,1))
        self.fav_btn_click.bind(on_press=lambda x: self.toggle_favorite(current_q))
        
        self.star_icon = Image(
            source=ICON_FILLED if is_fav else ICON_EMPTY, 
            size_hint=(None, None), 
            size=(40, 40), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        fav_container.add_widget(self.fav_btn_click)
        fav_container.add_widget(self.star_icon)

        # --- Gumb NAPREJ ---
        # Malce širši gumb, da lepo izgleda
        btn_next = Button(text="NAPREJ >", **minimal_btn_args)
        btn_next.width = 130 # Prilagojena širina za daljši tekst
        btn_next.bind(size=btn_next.setter("text_size"))
        btn_next.bind(on_press=self.next_question)

        # Dodajanje elementov v navigacijsko vrstico z dodajanjem praznih Widgetov (spacerjev) za poravnavo
        nav_bar.add_widget(btn_prev)
        nav_bar.add_widget(Widget(size_hint=(1, 1))) # Spacer, da potisne Meni in Zvezdico na sredino
        nav_bar.add_widget(btn_menu)
        nav_bar.add_widget(fav_container)
        nav_bar.add_widget(Widget(size_hint=(1, 1))) # Spacer, da potisne Naprej na desno
        nav_bar.add_widget(btn_next)

        main_content.add_widget(nav_bar)
        
        # Dodajanje vsega v root_layout
        self.root_layout.add_widget(main_content)

    def toggle_favorite(self, question):
        if question in self.favorites:
            self.favorites.remove(question)
            self.star_icon.source = ICON_EMPTY
        else:
            self.favorites.append(question)
            self.star_icon.source = ICON_FILLED
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            for fav in self.favorites: f.write(fav + "\n")

    def update_card_rect(self, instance, value):
        self.card_rect.pos = instance.pos
        self.card_rect.size = instance.size

    def next_question(self, instance):
        self.index += 1
        self.show_question()

    def prev_question(self, instance):
        if self.index > 0:
            self.index -= 1
            self.show_question()

    def show_game_over(self):
        self.root_layout.clear_widgets()
        l = Label(text=f"Prišla sta do konca kategorije!", font_size=36, font_name=FONT_PATH, color=TEXT_COLOR, halign="center")
        b = Button(text="Nazaj Domov", size_hint=(None,None), size=(240,70), font_name=FONT_PATH, font_size=32, pos_hint={'center_x':.5}, background_color=BTN_COLOR, background_normal="")
        b.bind(on_press=lambda x: self.show_questions_menu())
        self.root_layout.add_widget(l)
        self.root_layout.add_widget(b)

if __name__ == "__main__":
    CardApp().run()