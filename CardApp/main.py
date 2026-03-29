import pandas as pd
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.animation import Animation
import random
import sys

# 🎨 Barve
BG_COLOR = (0.96, 0.93, 0.90, 1)
CARD_COLOR = (1, 0.95, 0.96, 1)
BTN_COLOR = (0.95, 0.75, 0.80, 1)
TEXT_COLOR = (0.6, 0.2, 0.4, 1)

CATEGORY_COLORS = {
    "serious conv": (0.96, 0.93, 0.90, 1),  # bež
    "wild side of us": (1, 0.6, 0.6, 1),     # rdeča
    "fun & games": (0.8, 0.95, 0.9, 1),      # pastelno zelena
    "deep talks": (0.9, 0.85, 1, 1),         # pastelno vijolična
}

class CardApp(App):
    def build(self):
        df = pd.read_csv("cards.csv", encoding="utf-8")
        self.questions = df.groupby("EDITION")["QUESTION"].apply(list).to_dict()
        self.root_layout = BoxLayout(orientation="vertical", padding=20)

        with self.root_layout.canvas.before:
            Color(*BG_COLOR)
            self.bg = RoundedRectangle(pos=self.root_layout.pos, size=self.root_layout.size)

        self.root_layout.bind(pos=self.update_bg, size=self.update_bg)
        self.show_menu()
        return self.root_layout

    def update_bg(self, *args):
        self.bg.pos = self.root_layout.pos
        self.bg.size = self.root_layout.size

    def show_menu(self):
        self.root_layout.clear_widgets()

        title = Label(
            text="IZBERI KATEGORIJO:",
            font_size=40,
            font_name="Patrick_Hand/PatrickHand.ttf",
            size_hint=(1, 0.2),
            color=TEXT_COLOR
        )
        self.root_layout.add_widget(title)

        grid = GridLayout(cols=2, spacing=15, size_hint=(1, 0.8))
        for category in self.questions.keys():
            btn = Button(
                text=category,
                font_size=40,
                font_name="Patrick_Hand/PatrickHand.ttf",  
                background_normal="",
                background_color=BTN_COLOR
            )
            # Pokliče popup za izbiro števila kartic
            btn.bind(on_press=lambda x, c=category: self.choose_card_count(c))
            grid.add_widget(btn)

        self.root_layout.add_widget(grid)

    # Popup za izbiro števila kartic
    def choose_card_count(self, category):
        box = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Izberi število kartic:", 
                      font_size=32,
                      font_name="Patrick_Hand/PatrickHand.ttf", 
                      color=TEXT_COLOR)
        box.add_widget(label)

        for n in [5, 10, 15]:
            btn = Button(
                text=str(n),
                size_hint=(1, None),
                height=60,
                font_size=28,
                font_name="Patrick_Hand/PatrickHand.ttf",
                background_normal="",
                background_color=BTN_COLOR
            )
            btn.bind(on_press=lambda x, n=n: self.start_game_with_count(category, n))
            box.add_widget(btn)

        self.popup = Popup(
            content=box,
            size_hint=(0.7, 0.5),
            auto_dismiss=True,
            title_color=(0.6, 0.2, 0.4, 1),  # barva naslova
            title_align='center'
        )
        self.popup.open()

    # Začetek igre z izbranim številom kartic
    def start_game_with_count(self, category, count):
        self.popup.dismiss()
        self.category = category
        self.deck = random.sample(self.questions[self.category], min(count, len(self.questions[self.category])))
        self.index = 0
        self.current_card_widget = None
        self.show_question()

    # Animacija kartic
    def animate_card(self, old_widget, new_widget):
        anim_out = Animation(x=-self.root_layout.width, duration=0.3)
        anim_out.bind(on_complete=lambda *args: self.root_layout.remove_widget(old_widget))
        anim_out.start(old_widget)

        new_widget.x = self.root_layout.width
        self.root_layout.add_widget(new_widget)
        anim_in = Animation(x=0, duration=0.3)
        anim_in.start(new_widget)

    # Prikaz kartice
    def show_question(self):
        # če smo na koncu, pokaži game_over brez animacije
        if self.index >= len(self.deck):
            self.current_card_widget = None  # reset animacije
            self.show_game_over()
            return

        main_box = BoxLayout(orientation="vertical", spacing=20)

        # info o kategoriji na vrhu
        menu_label = Label(
            text=f"Kategorija: {self.category}",
            font_size=28,
            font_name="Patrick_Hand/PatrickHand.ttf",
            color=TEXT_COLOR,
            size_hint=(1, 0.2)  # 20% višine
        )
        main_box.add_widget(menu_label)

        # kartica
        card = BoxLayout(size_hint=(1, 0.8), padding=20)
        with card.canvas.before:
            Color(*CATEGORY_COLORS.get(self.category, CARD_COLOR))
            self.card_rect = RoundedRectangle(radius=[20], pos=card.pos, size=card.size)
        card.bind(pos=self.update_card, size=self.update_card)

        label = Label(
            text=self.deck[self.index],
            font_size=36,
            font_name="Patrick_Hand/PatrickHand.ttf",
            halign="center",
            valign="middle",
            color=TEXT_COLOR
        )
        label.bind(size=label.setter("text_size"))
        card.add_widget(label)

        # animacija samo če je prejšnja kartica
        if hasattr(self, "current_card_widget") and self.current_card_widget:
            self.animate_card(self.current_card_widget, card)
        else:
            main_box.add_widget(card)

        self.current_card_widget = card

        # gumbi
        btn_box = BoxLayout(size_hint=(1, None), height=100, padding=20)
        prev_btn = Button(text="Prejšnja kartica", size_hint=(None, None), width=250, height=70,
                        font_name="Patrick_Hand/PatrickHand.ttf", font_size=32,
                        background_normal="", background_color=BTN_COLOR)
        prev_btn.bind(on_press=self.prev_question)

        next_btn = Button(text="Naslednja kartica", size_hint=(None, None), width=250, height=70,
                        font_name="Patrick_Hand/PatrickHand.ttf", font_size=32,
                        background_normal="", background_color=BTN_COLOR)
        next_btn.bind(on_press=self.next_question)

        back_btn = Button(text="Zaključi igro", size_hint=(None, None), width=200, height=70,
                        font_name="Patrick_Hand/PatrickHand.ttf", font_size=32,
                        background_normal="", background_color=BTN_COLOR)
        back_btn.bind(on_press=lambda x: self.show_menu())

        btn_box.add_widget(back_btn)
        btn_box.add_widget(Widget())
        btn_box.add_widget(prev_btn)
        btn_box.add_widget(Widget())
        btn_box.add_widget(next_btn)

        main_box.add_widget(btn_box)

        # števec
        counter = Label(text=f"{self.index+1} / {len(self.deck)}", font_size=24,
                        font_name="Patrick_Hand/PatrickHand.ttf", color=TEXT_COLOR, size_hint=(1, 0.1))
        main_box.add_widget(counter)

        self.root_layout.clear_widgets()
        self.root_layout.add_widget(main_box)

    def next_question(self, instance):
        if self.index < len(self.deck) - 1:
            self.index += 1
            self.show_question()

    def prev_question(self, instance):
        if self.index > 0:
            self.index -= 1
            self.show_question()

    def update_card(self, *args):
        if hasattr(self, "card_rect") and self.root_layout.children:
            self.card_rect.pos = self.root_layout.children[0].pos
            self.card_rect.size = self.root_layout.children[0].size


    def show_game_over(self):
        self.root_layout.clear_widgets()
        self.current_card_widget = None  # reset animacije

        label = Label(
            text="Prišla sta do konca igre!",
            font_size=40,
            font_name="Patrick_Hand/PatrickHand.ttf",
            color=TEXT_COLOR,
            halign="center",
            valign="middle"
        )
        label.bind(size=label.setter("text_size"))

        btn_menu = Button(
            text="Nazaj na izbiro kategorije",
            font_size=32,
            font_name="Patrick_Hand/PatrickHand.ttf",
            background_normal="",
            background_color=BTN_COLOR,
            size_hint=(None, None), width=300, height=70
        )
        btn_menu.bind(on_press=lambda x: self.show_menu())

        btn_quit = Button(
            text="Zapusti igro",
            font_size=32,
            font_name="Patrick_Hand/PatrickHand.ttf",
            background_normal="",
            background_color=BTN_COLOR,
            size_hint=(None, None), width=300, height=70
        )
        btn_quit.bind(on_press=lambda x: (App.get_running_app().stop(), sys.exit()))

        btn_box = BoxLayout(size_hint=(1, None), height=80, spacing=20, padding=20)
        btn_box.add_widget(btn_menu)
        btn_box.add_widget(Widget())
        btn_box.add_widget(btn_quit)

        self.root_layout.add_widget(label)
        self.root_layout.add_widget(btn_box)

if __name__ == "__main__":
    CardApp().run()