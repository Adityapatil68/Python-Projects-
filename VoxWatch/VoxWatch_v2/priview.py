

import json
import math
import sys
from datetime import datetime, timedelta
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

BG = (0.018, 0.035, 0.075, 1)
BG_2 = (0.026, 0.055, 0.115, 1)
CARD = (0.050, 0.095, 0.185, 1)
CARD_2 = (0.065, 0.120, 0.230, 1)
WHITE = (0.97, 0.985, 1.0, 1)
MUTED = (0.55, 0.67, 0.84, 1)
ACCENT = (0.20, 0.49, 1.0, 1)
ACCENT_2 = (0.25, 0.56, 1.0, 1)
ORANGE = (1.0, 0.46, 0.08, 1)
DANGER = (0.95, 0.25, 0.30, 1)
BORDER = (0.12, 0.22, 0.38, 1)
GREEN = (0.25, 0.82, 0.48, 1)


# ---------------------------------------------------------------------------
# Small reusable widgets
# ---------------------------------------------------------------------------

class RoundedWidget(Widget):
    def __init__(self, bg_color=CARD, radius=18, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        with self.canvas.before:
            Color(*self.bg_color)
            self.shape = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[dp(radius)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.shape.pos = self.pos
        self.shape.size = self.size


class Card(BoxLayout):
    def __init__(self, bg_color=CARD, radius=18, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.shape = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[dp(radius)])
            Color(*BORDER)
            self.outline = Line(rounded_rectangle=(
                self.x, self.y, self.width, self.height, dp(radius)), width=0.7)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.shape.pos = self.pos
        self.shape.size = self.size
        self.outline.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(18)
        )


class TextButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("border", (0, 0, 0, 0))
        kwargs.setdefault("color", WHITE)
        super().__init__(**kwargs)


class AccentButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", ACCENT)
        kwargs.setdefault("border", (0, 0, 0, 0))
        kwargs.setdefault("color", WHITE)
        kwargs.setdefault("bold", True)
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*ACCENT)
            self.shape = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[dp(17)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.shape.pos = self.pos
        self.shape.size = self.size


class Divider(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(1), **kwargs)
        with self.canvas:
            Color(*BORDER)
            self.line = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.line.pos = self.pos
        self.line.size = self.size


class Toggle(Widget):
    active = BooleanProperty(False)

    def __init__(self, active=False, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(54), dp(32)), **kwargs)
        self.active = active
        self.bind(pos=self._draw, size=self._draw, active=self._draw)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return super().on_touch_down(touch)

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*(ACCENT if self.active else (0.17, 0.22, 0.31, 1)))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            Color(*WHITE)
            x = self.x + self.width - dp(16) if self.active else self.x + dp(16)
            Ellipse(pos=(x - dp(10), self.y + dp(6)), size=(dp(20), dp(20)))


class NavBar(BoxLayout):
    def __init__(self, home_active=True, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(72),
                         padding=(dp(18), dp(8)), spacing=dp(5), **kwargs)
        items = [
            ("◷", "Alarms", "alarms"),
            ("＋", "Add", "new_alarm"),
            ("⚙", "Settings", "settings"),
        ]
        for icon, title, screen in items:
            box = BoxLayout(orientation="vertical")
            b = TextButton(text=icon, font_size=sp(22), size_hint_y=.58)
            lbl = Label(text=title, font_size=sp(11),
                        color=ACCENT if (home_active and screen == "alarms") else MUTED)
            b.bind(on_release=lambda *_a, s=screen: App.get_running_app().show(s))
            box.add_widget(b)
            box.add_widget(lbl)
            self.add_widget(box)


class ClockFace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)
        Clock.schedule_interval(self.draw, 1)
        self.draw()

    def draw(self, *_):
        self.canvas.clear()
        cx, cy = self.center
        radius = min(self.width, self.height) * 0.40
        if radius <= 0:
            return

        now = datetime.now()
        sec = now.second
        minute = now.minute + sec / 60
        hour = (now.hour % 12) + minute / 60

        with self.canvas:
            Color(0.98, 0.985, 1, 1)
            Ellipse(pos=(cx-radius, cy-radius), size=(2*radius, 2*radius))
            Color(0.73, 0.78, 0.88, 0.50)
            Line(circle=(cx, cy, radius), width=0.9)

            Color(0.15, 0.18, 0.24, 1)
            for n in range(12):
                a = math.radians(n * 30 - 90)
                x1 = cx + math.cos(a) * radius * 0.87
                y1 = cy + math.sin(a) * radius * 0.87
                x2 = cx + math.cos(a) * radius * 0.94
                y2 = cy + math.sin(a) * radius * 0.94
                Line(points=[x1, y1, x2, y2], width=1.0)

            def hand(value_degrees, length, width):
                a = math.radians(value_degrees - 90)
                x = cx + math.cos(a) * length
                y = cy + math.sin(a) * length
                Line(points=[cx, cy, x, y], width=width)

            hand(hour * 30, radius * 0.48, 3.4)
            hand(minute * 6, radius * 0.70, 2.4)

            a = math.radians(sec * 6 - 90)
            sx = cx + math.cos(a) * radius * 0.78
            sy = cy + math.sin(a) * radius * 0.78
            Color(*ORANGE)
            Line(points=[cx, cy, sx, sy], width=1.35)
            Ellipse(pos=(cx-dp(5), cy-dp(5)), size=(dp(10), dp(10)))


class Background(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*BG)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

DEFAULT_ALARMS = [
    {
        "time": "06:00",
        "days": ["Today", "Wednesday", "Thursday"],
        "enabled": True,
        "ringtone": "Ding, Dong, Bong",
        "salutation": "Wake UP, Carl!",
        "repeat_ringtone": True,
    },
    {
        "time": "08:00",
        "days": ["Thursday"],
        "enabled": False,
        "ringtone": "Ding, Dong, Bong",
        "salutation": "Wake UP, Carl!",
        "repeat_ringtone": True,
    },
    {
        "time": "08:40",
        "days": [],
        "enabled": False,
        "ringtone": "Ding, Dong, Bong",
        "salutation": "Wake UP, Carl!",
        "repeat_ringtone": True,
    },
]


# ---------------------------------------------------------------------------
# Base screen
# ---------------------------------------------------------------------------

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = Background()
        self.add_widget(self.root)
        self.body = BoxLayout(orientation="vertical", spacing=0)
        self.root.add_widget(self.body)


class Header(BoxLayout):
    def __init__(self, title, back=False, action_text="", action=None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(64),
                         padding=(dp(14), dp(7)), spacing=dp(4), **kwargs)
        left = TextButton(text="‹" if back else " ", font_size=sp(32),
                          size_hint_x=None, width=dp(44))
        if back:
            left.bind(on_release=lambda *_: App.get_running_app().go_back())
        center = Label(text=title, color=WHITE, font_size=sp(22),
                       bold=True, halign="center")
        right = TextButton(text=action_text or " ", font_size=sp(25),
                           size_hint_x=None, width=dp(44))
        if action:
            right.bind(on_release=action)
        self.add_widget(left)
        self.add_widget(center)
        self.add_widget(right)


# ---------------------------------------------------------------------------
# Home / alarm list
# ---------------------------------------------------------------------------

class AlarmListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.body.clear_widgets()

        top = BoxLayout(size_hint_y=None, height=dp(58), padding=(dp(18), dp(7)))
        settings = TextButton(text="⚙", font_size=sp(22), size_hint_x=None, width=dp(42))
        settings.bind(on_release=lambda *_: App.get_running_app().show("settings"))
        brand = Label(text="WakeUp", color=WHITE, bold=True, font_size=sp(17), halign="left")
        live = Label(text="", color=MUTED, font_size=sp(13), halign="right")
        self.live_label = live
        plus = AccentButton(text="+", font_size=sp(24), size_hint_x=None, width=dp(44))
        plus.bind(on_release=lambda *_: App.get_running_app().new_alarm())
        top.add_widget(settings)
        top.add_widget(brand)
        top.add_widget(live)
        top.add_widget(plus)
        self.body.add_widget(top)

        hero = Card(orientation="vertical", padding=(dp(18), dp(10)), spacing=dp(2),
                    size_hint_y=None, height=dp(350), bg_color=BG_2)
        hero.add_widget(ClockFace())
        self.countdown = Label(text="", color=WHITE, font_size=sp(14),
                               size_hint_y=None, height=dp(34))
        hero.add_widget(self.countdown)
        self.body.add_widget(hero)

        title_row = BoxLayout(size_hint_y=None, height=dp(54), padding=(dp(18), 0))
        title_row.add_widget(Label(text="Your alarms", color=WHITE, font_size=sp(20),
                                   bold=True, halign="left"))
        count = len([a for a in App.get_running_app().alarms if a.get("enabled")])
        title_row.add_widget(Label(text=f"{count} active", color=MUTED, font_size=sp(13),
                                   halign="right"))
        self.body.add_widget(title_row)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3), effect_cls="ScrollEffect")
        self.rows = BoxLayout(orientation="vertical", size_hint_y=None,
                              spacing=dp(10), padding=(dp(14), dp(2), dp(14), dp(14)))
        self.rows.bind(minimum_height=self.rows.setter("height"))
        scroll.add_widget(self.rows)
        self.body.add_widget(scroll)

        self.body.add_widget(NavBar(home_active=True))
        self.refresh_data()

    def refresh_data(self):
        if not hasattr(self, "rows"):
            return
        self.live_label.text = datetime.now().strftime("%I:%M %p")
        self.countdown.text = App.get_running_app().next_alarm_text()
        self.rows.clear_widgets()
        alarms = App.get_running_app().alarms
        if not alarms:
            self.rows.add_widget(
                Label(text="No alarms yet\nTap + to create one",
                      color=MUTED, font_size=sp(16), halign="center",
                      size_hint_y=None, height=dp(100))
            )
            return
        for idx, alarm in enumerate(alarms):
            self.rows.add_widget(AlarmCard(alarm, idx))

    def on_pre_enter(self, *_):
        self.refresh_data()


class AlarmCard(Card):
    def __init__(self, alarm, index, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(88),
                         padding=(dp(15), dp(10)), spacing=dp(10), **kwargs)
        self.index = index
        self.alarm = alarm

        left = BoxLayout(orientation="vertical", spacing=0)
        time = Label(text=alarm["time"], color=WHITE, font_size=sp(28),
                     bold=True, halign="left", valign="middle")
        days = ", ".join(alarm.get("days", [])) or "Every day"
        sub = Label(text=days, color=MUTED, font_size=sp(12),
                    halign="left", valign="middle")
        left.add_widget(time)
        left.add_widget(sub)

        right = BoxLayout(spacing=dp(4), size_hint_x=None, width=dp(105))
        toggle = Toggle(active=bool(alarm.get("enabled")))
        toggle.bind(active=self.set_active)
        edit = TextButton(text="›", font_size=sp(30), size_hint_x=None, width=dp(30))
        edit.bind(on_release=lambda *_: App.get_running_app().edit_alarm(self.index))
        right.add_widget(toggle)
        right.add_widget(edit)

        self.add_widget(left)
        self.add_widget(right)

    def set_active(self, widget, value):
        app = App.get_running_app()
        app.alarms[self.index]["enabled"] = bool(value)
        app.save_data()


# ---------------------------------------------------------------------------
# New / edit alarm
# ---------------------------------------------------------------------------

class NewAlarmScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.edit_index = None
        self.ringtone_value = "Ding, Dong, Bong"
        self.salutation_value = "Wake UP, Carl!"
        self.build()

    def build(self):
        self.body.clear_widgets()
        self.body.add_widget(
            Header("New Alarm", back=True, action_text="✓",
                   action=lambda *_: App.get_running_app().save_alarm_from_editor())
        )

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        content = BoxLayout(orientation="vertical", spacing=dp(14),
                            padding=(dp(15), dp(10), dp(15), dp(22)),
                            size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        time_card = Card(orientation="vertical", size_hint_y=None, height=dp(205),
                         padding=(dp(18), dp(16)), spacing=dp(4), bg_color=BG_2)
        time_card.add_widget(Label(text="Choose time", color=MUTED, font_size=sp(13),
                                   size_hint_y=None, height=dp(25)))
        times = BoxLayout(size_hint_y=None, height=dp(86), spacing=dp(10))
        self.hour = Spinner(text="07",
                            values=tuple(f"{i:02d}" for i in range(24)),
                            background_normal="", background_color=CARD_2,
                            color=WHITE, font_size=sp(29))
        self.minute = Spinner(text="00",
                              values=tuple(f"{i:02d}" for i in range(60)),
                              background_normal="", background_color=CARD_2,
                              color=WHITE, font_size=sp(29))
        times.add_widget(self.hour)
        times.add_widget(Label(text=":", color=ACCENT, font_size=sp(32),
                               size_hint_x=None, width=dp(25)))
        times.add_widget(self.minute)
        time_card.add_widget(times)
        time_card.add_widget(Label(text="24-hour format • Tap the values to change",
                                   color=MUTED, font_size=sp(12)))
        content.add_widget(time_card)

        self.repeat_card = self.setting_card(
            "Repeat", self.repeat_summary(),
            lambda *_: App.get_running_app().show("repeat")
        )
        content.add_widget(self.repeat_card)

        self.ringtone_card = self.setting_card(
            "Ringtone", self.ringtone_value,
            lambda *_: self.choose_ringtone()
        )
        content.add_widget(self.ringtone_card)

        self.salutation_card = self.setting_card(
            "Salutation", self.salutation_value,
            lambda *_: self.edit_salutation()
        )
        content.add_widget(self.salutation_card)

        rr = Card(orientation="horizontal", size_hint_y=None, height=dp(72),
                  padding=(dp(18), dp(10)))
        rr.add_widget(BoxLayout(orientation="vertical",
                                children=[
                                    Label(text="Repeat ringtone", color=WHITE, font_size=sp(16)),
                                    Label(text="Continue until the alarm is dismissed",
                                          color=MUTED, font_size=sp(12))
                                ]))
        self.repeat_switch = Toggle(active=True)
        rr.add_widget(self.repeat_switch)
        content.add_widget(rr)

        delete = AccentButton(text="Delete alarm", background_color=DANGER,
                              size_hint_y=None, height=dp(52), font_size=sp(16))
        # AccentButton draws ACCENT internally; replace its canvas color.
        delete.bind(on_release=lambda *_: App.get_running_app().delete_current_alarm())
        self.delete_button = delete
        content.add_widget(delete)

        scroll.add_widget(content)
        self.body.add_widget(scroll)
        self.body.add_widget(NavBar(home_active=False))

    def setting_card(self, title, subtitle, callback):
        card = Card(orientation="horizontal", size_hint_y=None, height=dp(74),
                    padding=(dp(18), dp(8)))
        text = BoxLayout(orientation="vertical")
        text.add_widget(Label(text=title, color=WHITE, font_size=sp(16),
                              halign="left", valign="middle"))
        label = Label(text=subtitle, color=MUTED, font_size=sp(12),
                      halign="left", valign="middle")
        text.add_widget(label)
        arrow = TextButton(text="›", font_size=sp(26), size_hint_x=None, width=dp(30))
        for w in (card, arrow):
            w.bind(on_touch_down=lambda *args: None)
        card.bind(on_release=callback) if hasattr(card, "bind") else None
        # Card is not a Button, so put a transparent button over the card.
        overlay = TextButton(size_hint_x=1)
        overlay.bind(on_release=callback)
        outer = FloatLayout(size_hint_y=None, height=dp(74))
        outer.add_widget(card)
        outer.add_widget(overlay)
        card.add_widget(text)
        card.add_widget(arrow)
        self._setting_labels = getattr(self, "_setting_labels", {})
        self._setting_labels[title] = label
        return outer

    def refresh_cards(self):
        try:
            self._setting_labels["Repeat"].text = self.repeat_summary()
            self._setting_labels["Ringtone"].text = self.ringtone_value
            self._setting_labels["Salutation"].text = self.salutation_value
        except Exception:
            pass

    def repeat_summary(self):
        days = App.get_running_app().editor_days
        return ", ".join(days) if days else "Every day"

    def load_alarm(self, index):
        self.edit_index = index
        app = App.get_running_app()
        if index is None:
            self.hour.text = "07"
            self.minute.text = "00"
            app.editor_days = []
            self.ringtone_value = "Ding, Dong, Bong"
            self.salutation_value = "Wake UP, Carl!"
            self.repeat_switch.active = True
            self.delete_button.opacity = 0
            self.delete_button.disabled = True
        else:
            a = app.alarms[index]
            h, m = a["time"].split(":")
            self.hour.text = h
            self.minute.text = m
            app.editor_days = list(a.get("days", []))
            self.ringtone_value = a.get("ringtone", "Ding, Dong, Bong")
            self.salutation_value = a.get("salutation", "Wake UP, Carl!")
            self.repeat_switch.active = a.get("repeat_ringtone", True)
            self.delete_button.opacity = 1
            self.delete_button.disabled = False
        self.refresh_cards()

    def choose_ringtone(self):
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(8))
        popup = Popup(title="Choose ringtone", content=box,
                      size_hint=(.84, .55), separator_color=ACCENT)
        options = ["Ding, Dong, Bong", "Classic Bell", "Digital Beep", "Gentle Wake"]
        for name in options:
            b = AccentButton(text=name, size_hint_y=None, height=dp(46))
            b.bind(on_release=lambda btn, p=popup: self.pick_ringtone(btn.text, p))
            box.add_widget(b)
        popup.open()

    def pick_ringtone(self, name, popup):
        self.ringtone_value = name
        popup.dismiss()
        self.refresh_cards()

    def edit_salutation(self):
        inp = TextInput(text=self.salutation_value, multiline=False,
                        foreground_color=WHITE, background_color=CARD_2,
                        cursor_color=ACCENT, font_size=sp(16))
        save = AccentButton(text="Save", size_hint_y=None, height=dp(46))
        box = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        box.add_widget(inp)
        box.add_widget(save)
        popup = Popup(title="Wake-up message", content=box,
                      size_hint=(.88, .34), separator_color=ACCENT)
        save.bind(on_release=lambda *_: self.save_salutation(inp.text, popup))
        popup.open()

    def save_salutation(self, text, popup):
        self.salutation_value = text.strip() or "Wake UP!"
        popup.dismiss()
        self.refresh_cards()

    def on_pre_enter(self, *_):
        self.refresh_cards()


# ---------------------------------------------------------------------------
# Repeat
# ---------------------------------------------------------------------------

class RepeatScreen(BaseScreen):
    DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.body.clear_widgets()
        self.body.add_widget(Header("Repeat", back=True))

        scroll = ScrollView(do_scroll_x=False)
        box = BoxLayout(orientation="vertical", size_hint_y=None,
                        spacing=dp(8), padding=(dp(15), dp(12)))
        box.bind(minimum_height=box.setter("height"))

        selected = App.get_running_app().editor_days
        for day in self.DAYS:
            row = Card(orientation="horizontal", size_hint_y=None, height=dp(58),
                       padding=(dp(18), 0))
            row.add_widget(Label(text=day, color=WHITE, font_size=sp(16), halign="left"))
            check = CheckBox(active=(day in selected), size_hint_x=None, width=dp(48))
            check.color = ACCENT
            check.bind(active=lambda inst, val, d=day: self.changed(d, val))
            row.add_widget(check)
            box.add_widget(row)
        scroll.add_widget(box)
        self.body.add_widget(scroll)
        self.body.add_widget(
            AccentButton(text="Done", size_hint_y=None, height=dp(52), font_size=sp(16),
                         on_release=lambda *_: App.get_running_app().show("new_alarm"))
        )
        self.body.add_widget(NavBar(home_active=False))

    def changed(self, day, value):
        days = App.get_running_app().editor_days
        if value and day not in days:
            days.append(day)
        elif not value and day in days:
            days.remove(day)


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class SettingsScreen(BaseScreen):
    def build(self):
        self.body.clear_widgets()
        self.body.add_widget(Header("Settings", back=True))

        scroll = ScrollView(do_scroll_x=False)
        box = BoxLayout(orientation="vertical", size_hint_y=None,
                        padding=(dp(15), dp(12)), spacing=dp(12))
        box.bind(minimum_height=box.setter("height"))

        theme = Card(orientation="vertical", size_hint_y=None, height=dp(114),
                     padding=(dp(18), dp(12)))
        theme.add_widget(Label(text="Theme color", color=WHITE, font_size=sp(16),
                               halign="left", size_hint_y=None, height=dp(28)))
        colors = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(46))
        blue = AccentButton(text="Blue", font_size=sp(14))
        orange = AccentButton(text="Orange", font_size=sp(14))
        blue.bind(on_release=lambda *_: App.get_running_app().set_theme("blue"))
        orange.bind(on_release=lambda *_: App.get_running_app().set_theme("orange"))
        colors.add_widget(blue)
        colors.add_widget(orange)
        theme.add_widget(colors)
        box.add_widget(theme)

        volume = Card(orientation="vertical", size_hint_y=None, height=dp(102),
                      padding=(dp(18), dp(10)))
        volume.add_widget(Label(text="Alarm volume", color=WHITE, font_size=sp(16),
                                halign="left", size_hint_y=None, height=dp(24)))
        slider = Slider(min=0, max=100, value=App.get_running_app().volume,
                        cursor_size=(dp(24), dp(24)))
        slider.bind(value=lambda inst, val: App.get_running_app().set_volume(val))
        volume.add_widget(slider)
        box.add_widget(volume)

        for title, subtitle in [
            ("Developers", "Python + Kivy implementation"),
            ("Donation", "Support future development"),
            ("About", "WakeUp Alarm • polished single-file edition"),
        ]:
            c = Card(orientation="horizontal", size_hint_y=None, height=dp(70),
                     padding=(dp(18), dp(8)))
            txt = BoxLayout(orientation="vertical")
            txt.add_widget(Label(text=title, color=WHITE, font_size=sp(16), halign="left"))
            txt.add_widget(Label(text=subtitle, color=MUTED, font_size=sp(12), halign="left"))
            b = TextButton(text="›", font_size=sp(25), size_hint_x=None, width=dp(30))
            b.bind(on_release=lambda *_a, t=title, s=subtitle:
                   App.get_running_app().info_popup(t, s))
            c.add_widget(txt)
            c.add_widget(b)
            box.add_widget(c)

        scroll.add_widget(box)
        self.body.add_widget(scroll)
        self.body.add_widget(NavBar(home_active=False))

    def on_pre_enter(self, *_):
        self.build()


# ---------------------------------------------------------------------------
# Ringing screen
# ---------------------------------------------------------------------------

class RingingScreen(BaseScreen):
    def build(self):
        self.body.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=(dp(28), dp(46)), spacing=dp(15))
        box.add_widget(Label(text="ALARM", color=ORANGE, font_size=sp(14), bold=True,
                             size_hint_y=None, height=dp(28)))
        self.time_label = Label(text=App.get_running_app().ringing_time,
                                color=WHITE, font_size=sp(64), bold=True,
                                size_hint_y=None, height=dp(120))
        box.add_widget(self.time_label)
        box.add_widget(Label(text=App.get_running_app().ringing_text,
                             color=MUTED, font_size=sp(20), size_hint_y=None, height=dp(48)))
        box.add_widget(Widget())
        shut = AccentButton(text="Shut down", font_size=sp(19),
                            size_hint_y=None, height=dp(62))
        shut.bind(on_release=lambda *_: App.get_running_app().stop_alarm())
        snooze = Button(text="Snooze 5 minutes", background_normal="",
                        background_color=CARD_2, color=WHITE, font_size=sp(16),
                        size_hint_y=None, height=dp(52))
        snooze.bind(on_release=lambda *_: App.get_running_app().snooze_alarm())
        box.add_widget(shut)
        box.add_widget(snooze)
        self.body.add_widget(box)

    def on_pre_enter(self, *_):
        self.build()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

class WakeUpAlarmApp(App):
    title = "WakeUp Alarm"

    def build(self):
        Window.clearcolor = BG
        Window.minimum_width = 340
        Window.minimum_height = 640

        self.data_file = Path.home() / ".wakeup_alarm.json"
        self.alarms = []
        self.editor_days = []
        self.volume = 80
        self.theme = "blue"
        self.ringing_time = "07:00"
        self.ringing_text = "Time to wake UP!"
        self.current_ringing_index = None
        self._last_trigger = {}
        self.load_data()

        self.sm = ScreenManager(transition=SlideTransition(duration=.16))
        self.sm.add_widget(AlarmListScreen(name="alarms"))
        self.sm.add_widget(NewAlarmScreen(name="new_alarm"))
        self.sm.add_widget(RepeatScreen(name="repeat"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(RingingScreen(name="ringing"))

        Clock.schedule_interval(self.tick, 1)
        return self.sm

    def load_data(self):
        try:
            if self.data_file.exists():
                data = json.loads(self.data_file.read_text(encoding="utf-8"))
                self.alarms = data.get("alarms") or [dict(x) for x in DEFAULT_ALARMS]
                self.volume = int(data.get("volume", 80))
                self.theme = data.get("theme", "blue")
            else:
                self.alarms = [dict(x) for x in DEFAULT_ALARMS]
        except Exception:
            self.alarms = [dict(x) for x in DEFAULT_ALARMS]

    def save_data(self):
        try:
            payload = {
                "alarms": self.alarms,
                "volume": self.volume,
                "theme": self.theme,
            }
            self.data_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception:
            pass

    def show(self, name):
        self.sm.current = name

    def go_back(self):
        current = self.sm.current
        if current == "repeat":
            self.show("new_alarm")
        elif current in ("new_alarm", "settings"):
            self.show("alarms")
        else:
            self.show("alarms")

    def new_alarm(self):
        self.editor_days = []
        editor = self.sm.get_screen("new_alarm")
        editor.load_alarm(None)
        self.show("new_alarm")

    def edit_alarm(self, index):
        editor = self.sm.get_screen("new_alarm")
        editor.load_alarm(index)
        self.show("new_alarm")

    def save_alarm_from_editor(self):
        editor = self.sm.get_screen("new_alarm")
        hour = int(editor.hour.text)
        minute = int(editor.minute.text)
        item = {
            "time": f"{hour:02d}:{minute:02d}",
            "days": list(self.editor_days),
            "enabled": True,
            "ringtone": editor.ringtone_value,
            "salutation": editor.salutation_value,
            "repeat_ringtone": editor.repeat_switch.active,
        }
        if editor.edit_index is None:
            self.alarms.append(item)
        else:
            old_enabled = self.alarms[editor.edit_index].get("enabled", True)
            item["enabled"] = old_enabled
            self.alarms[editor.edit_index] = item
        self.save_data()
        self.show("alarms")

    def delete_current_alarm(self):
        editor = self.sm.get_screen("new_alarm")
        if editor.edit_index is None:
            return
        idx = editor.edit_index
        if 0 <= idx < len(self.alarms):
            self.alarms.pop(idx)
        self.save_data()
        self.show("alarms")

    def next_alarm_text(self):
        active = [a for a in self.alarms if a.get("enabled")]
        if not active:
            return "No active alarms"
        now = datetime.now()
        best = None
        for alarm in active:
            try:
                hh, mm = map(int, alarm["time"].split(":"))
            except Exception:
                continue
            candidate = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            if candidate <= now:
                candidate += timedelta(days=1)
            if best is None or candidate < best:
                best = candidate
        if best is None:
            return "No active alarms"
        seconds = max(0, int((best - now).total_seconds()))
        h, rem = divmod(seconds, 3600)
        m = rem // 60
        return f"Next alarm in  {h:02d}h {m:02d}m"

    def tick(self, *_):
        if self.sm.current == "alarms":
            screen = self.sm.get_screen("alarms")
            screen.refresh_data()
        self.check_alarms()

    def check_alarms(self):
        now = datetime.now()
        current = now.strftime("%H:%M")
        today = now.strftime("%A")
        stamp = now.strftime("%Y-%m-%d %H:%M")

        for index, alarm in enumerate(self.alarms):
            if not alarm.get("enabled") or alarm.get("time") != current:
                continue
            if self._last_trigger.get(index) == stamp:
                continue
            days = alarm.get("days", [])
            if days and today not in days and "Today" not in days:
                continue
            self._last_trigger[index] = stamp
            self.current_ringing_index = index
            self.ringing_time = current
            self.ringing_text = alarm.get("salutation", "Time to wake UP!")
            self.play_alarm_sound()
            self.show("ringing")
            break

    def play_alarm_sound(self):
        try:
            if sys.platform.startswith("win"):
                import winsound
                winsound.Beep(880, 280)
                winsound.Beep(660, 280)
            else:
                print("\a", end="", flush=True)
        except Exception:
            pass

    def stop_alarm(self):
        self.current_ringing_index = None
        self.show("alarms")

    def snooze_alarm(self):
        if self.current_ringing_index is not None:
            alarm = self.alarms[self.current_ringing_index]
            future = datetime.now() + timedelta(minutes=5)
            alarm["time"] = future.strftime("%H:%M")
            alarm["days"] = []
            alarm["enabled"] = True
            self.save_data()
        self.current_ringing_index = None
        self.show("alarms")

    def set_volume(self, value):
        self.volume = int(value)
        self.save_data()

    def set_themet(self, name):
        self.theme = name
        self.save_data()
        self.info_popup("Theme", f"{name.title()} theme selected.")

    def info_popup(self, title, message):
        text = Label(text=message, color=WHITE, halign="center", valign="middle")
        Popup(title=title, content=text, size_hint=(.82, .30),
              separator_color=ACCENT).open()


if __name__ == "__main__":
    WakeUpAlarmApp().run()
