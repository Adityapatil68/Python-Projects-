# VoxWatch v2.0 — iOS Ultra Style UI
# Banaya: Aditya Thakare (Adiyani)

import threading
import time
import csv
import os
import math
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Ellipse, Rectangle,
                           RoundedRectangle, Line, SmoothLine)
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex_c
from kivy.animation import Animation
import pyttsx3

Window.size = (390, 780)

# ── COLORS: iOS Ultra Dark
BG1    = hex_c('#000000')   # Pure black (iOS style)
BG2    = hex_c('#1C1C1E')   # Card dark
BG3    = hex_c('#2C2C2E')   # Separator
BLUE   = hex_c('#0A84FF')   # iOS blue
GREEN  = hex_c('#30D158')   # iOS green
RED    = hex_c('#FF453A')   # iOS red
YELLOW = hex_c('#FFD60A')   # iOS yellow
WHITE  = hex_c('#FFFFFF')
GREY   = hex_c('#8E8E93')   # iOS grey
LGREY  = hex_c('#636366')   # iOS light grey
ORANGE = hex_c('#FF9F0A')   # iOS orange

# ── TTS
try:
    _tts = pyttsx3.init()
    _tts.setProperty('rate', 148)
    TTS_OK = True
except Exception as e:
    print(f"TTS Error: {e}")
    TTS_OK = False

def speak(text):
    if TTS_OK:
        def _r():
            try:
                _tts.say(text)
                _tts.runAndWait()
            except Exception as e:
                print(f"Speak error: {e}")
        threading.Thread(target=_r, daemon=True).start()

alarms = []

def add_alarm(t, label, days, routine):
    alarms.append({
        'time': t, 'label': label,
        'days': days, 'routine': routine,
        'active': True, 'triggered': False
    })

def load_csv():
    path = os.path.join(os.path.dirname(__file__), 'sample_routine.csv')
    if not os.path.exists(path):
        return
    try:
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                add_alarm(
                    row.get('time', '07:00').strip(),
                    row.get('label', 'Alarm').strip(),
                    ['Mon', 'Wed', 'Thu'],
                    row.get('routine', '').strip()
                )
    except Exception as e:
        print(f"CSV Error: {e}")

# ══════════════════════════════════════
# HELPER: iOS Rounded Card Background
# ══════════════════════════════════════
def ios_card(widget, color=None, radius=14):
    col = color or BG2
    with widget.canvas.before:
        Color(*col)
        rect = RoundedRectangle(
            pos=widget.pos,
            size=widget.size,
            radius=[dp(radius)]
        )
    widget.bind(
        pos=lambda w, v: setattr(rect, 'pos', v),
        size=lambda w, v: setattr(rect, 'size', v)
    )
    return rect

def flat_bg(widget, color=None):
    col = color or BG1
    with widget.canvas.before:
        Color(*col)
        rect = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(
        pos=lambda w, v: setattr(rect, 'pos', v),
        size=lambda w, v: setattr(rect, 'size', v)
    )
    return rect

# ══════════════════════════════════════
# ANALOG CLOCK — iOS Style
# ══════════════════════════════════════
class AnalogClock(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint = (None, None)
        self.size = (dp(200), dp(200))
        Clock.schedule_interval(self._draw, 1)
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = dp(96)
        now = datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second

        with self.canvas:
            # Outer dark ring
            Color(0.11, 0.11, 0.12, 1)
            Ellipse(pos=(cx-r-dp(6), cy-r-dp(6)),
                    size=(r*2+dp(12), r*2+dp(12)))

            # Inner face — dark grey
            Color(0.17, 0.17, 0.18, 1)
            Ellipse(pos=(cx-r, cy-r), size=(r*2, r*2))

            # Hour dots (12 dots)
            for i in range(12):
                ang = math.radians(90 - i*30)
                dot_r = dp(3) if i % 3 == 0 else dp(1.5)
                dot_x = cx + (r-dp(12)) * math.cos(ang)
                dot_y = cy + (r-dp(12)) * math.sin(ang)
                if i % 3 == 0:
                    Color(*WHITE)
                else:
                    Color(*GREY)
                Ellipse(pos=(dot_x-dot_r, dot_y-dot_r),
                        size=(dot_r*2, dot_r*2))

            # Hour hand — thick white
            ang_h = math.radians(90 - (h*30 + m*0.5))
            Color(*WHITE)
            Line(points=[cx - dp(8)*math.cos(ang_h),
                         cy - dp(8)*math.sin(ang_h),
                         cx + dp(52)*math.cos(ang_h),
                         cy + dp(52)*math.sin(ang_h)],
                 width=dp(4), cap='round')

            # Minute hand — medium white
            ang_m = math.radians(90 - m*6)
            Color(*WHITE)
            Line(points=[cx - dp(10)*math.cos(ang_m),
                         cy - dp(10)*math.sin(ang_m),
                         cx + dp(72)*math.cos(ang_m),
                         cy + dp(72)*math.sin(ang_m)],
                 width=dp(2.5), cap='round')

            # Second hand — iOS orange/red
            ang_s = math.radians(90 - s*6)
            Color(*ORANGE)
            Line(points=[cx - dp(14)*math.cos(ang_s),
                         cy - dp(14)*math.sin(ang_s),
                         cx + dp(80)*math.cos(ang_s),
                         cy + dp(80)*math.sin(ang_s)],
                 width=dp(1.5), cap='round')

            # Center cap
            Color(*ORANGE)
            Ellipse(pos=(cx-dp(5), cy-dp(5)),
                    size=(dp(10), dp(10)))
            Color(0.17, 0.17, 0.18, 1)
            Ellipse(pos=(cx-dp(2), cy-dp(2)),
                    size=(dp(4), dp(4)))

# ══════════════════════════════════════
# HOME SCREEN
# ══════════════════════════════════════
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()
        Clock.schedule_interval(self._refresh, 2)
        Clock.schedule_interval(self._update_time, 1)

    def _build(self):
        self.root_fl = FloatLayout()
        flat_bg(self.root_fl, BG1)

        # ── STATUS BAR area
        status = BoxLayout(
            size_hint=(1, None), height=dp(44),
            pos_hint={'top': 1},
            padding=[dp(20), dp(12)]
        )
        flat_bg(status, BG1)
        self.status_time = Label(
            text=datetime.now().strftime('%H:%M'),
            font_size=sp(15), bold=True,
            color=WHITE, halign='left'
        )
        status.add_widget(self.status_time)
        status.add_widget(Widget())
        status.add_widget(Label(
            text='● ●●', font_size=sp(12),
            color=WHITE, halign='right',
            size_hint_x=None, width=dp(60)
        ))
        self.root_fl.add_widget(status)

        # ── TOP NAV BAR
        nav = BoxLayout(
            size_hint=(1, None), height=dp(52),
            pos_hint={'top': 0.944},
            padding=[dp(20), dp(8)]
        )
        flat_bg(nav, BG1)
        nav.add_widget(Label(
            text='VoxWatch', font_size=sp(20),
            bold=True, color=WHITE, halign='left'
        ))
        nav.add_widget(Widget())

        # Settings btn — iOS circle style
        s_btn = Button(
            text='⚙', font_size=sp(18),
            size_hint=(None, None), size=(dp(36), dp(36)),
            background_color=(0, 0, 0, 0), color=BLUE
        )
        s_btn.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'settings'))
        nav.add_widget(s_btn)

        add_btn = Button(
            text='+', font_size=sp(24),
            size_hint=(None, None), size=(dp(36), dp(36)),
            background_color=(0, 0, 0, 0), color=BLUE
        )
        add_btn.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'add_alarm'))
        nav.add_widget(add_btn)
        self.root_fl.add_widget(nav)

        # ── CLOCK CARD
        clock_card = FloatLayout(
            size_hint=(0.92, None), height=dp(260),
            pos_hint={'center_x': 0.5, 'top': 0.88}
        )
        ios_card(clock_card, BG2, radius=22)

        # Analog clock inside card
        self.clock_w = AnalogClock(
            pos_hint={'center_x': 0.5, 'center_y': 0.58}
        )
        clock_card.add_widget(self.clock_w)

        # Digital time below clock
        self.dig_time = Label(
            text=datetime.now().strftime('%H:%M'),
            font_size=sp(16), bold=True,
            color=GREY, halign='center',
            size_hint=(1, None), height=dp(28),
            pos_hint={'center_x': 0.5, 'y': 0.01}
        )
        clock_card.add_widget(self.dig_time)
        self.root_fl.add_widget(clock_card)

        # ── NEXT ALARM PILL
        self.next_pill = Label(
            text='⏰  No alarms set',
            font_size=sp(13), color=GREY,
            size_hint=(0.92, None), height=dp(36),
            pos_hint={'center_x': 0.5, 'top': 0.555},
            halign='left'
        )
        self.root_fl.add_widget(self.next_pill)

        # ── ALARMS SECTION TITLE
        alm_title = Label(
            text='ALARMS',
            font_size=sp(12), bold=True,
            color=GREY, halign='left',
            size_hint=(0.92, None), height=dp(28),
            pos_hint={'center_x': 0.5, 'top': 0.515}
        )
        self.root_fl.add_widget(alm_title)

        # ── ALARM LIST (rounded card container)
        self.list_card = FloatLayout(
            size_hint=(0.92, None), height=dp(280),
            pos_hint={'center_x': 0.5, 'top': 0.482}
        )
        ios_card(self.list_card, BG2, radius=18)

        self.scroll = ScrollView(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.alarm_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None, spacing=0
        )
        self.alarm_box.bind(
            minimum_height=self.alarm_box.setter('height'))
        self.scroll.add_widget(self.alarm_box)
        self.list_card.add_widget(self.scroll)
        self.root_fl.add_widget(self.list_card)

        self.add_widget(self.root_fl)
        self._refresh()

    def on_enter(self):
        self._refresh()

    def _update_time(self, *_):
        now = datetime.now().strftime('%H:%M')
        self.status_time.text = now
        self.dig_time.text = now

    def _refresh(self, *_):
        self.alarm_box.clear_widgets()
        active = [a for a in alarms if a['active']]

        if active:
            nxt = sorted(active, key=lambda x: x['time'])[0]
            self.next_pill.text = (
                f"⏰  Next — {nxt['time']}  {nxt['label']}")
        else:
            self.next_pill.text = '⏰  No active alarms'

        if not alarms:
            self.alarm_box.add_widget(Label(
                text='Tap + to add an alarm',
                font_size=sp(15), color=GREY,
                halign='center',
                size_hint_y=None, height=dp(80)
            ))
            return

        for i, alarm in enumerate(alarms):
            # Alarm row
            row = BoxLayout(
                size_hint_y=None, height=dp(72),
                padding=[dp(18), dp(10)]
            )

            # Left info
            left = BoxLayout(orientation='vertical')
            t_lbl = Label(
                text=alarm['time'],
                font_size=sp(30), bold=True,
                color=WHITE if alarm['active'] else GREY,
                halign='left',
                size_hint_y=None, height=dp(38)
            )
            t_lbl.bind(size=lambda w, s: setattr(w, 'text_size', s))
            left.add_widget(t_lbl)

            sub = f"{alarm['label']}  ·  "
            sub += ', '.join(alarm['days']) if alarm['days'] else 'Once'
            s_lbl = Label(
                text=sub, font_size=sp(12),
                color=GREY, halign='left',
                size_hint_y=None, height=dp(20)
            )
            s_lbl.bind(size=lambda w, s: setattr(w, 'text_size', s))
            left.add_widget(s_lbl)
            row.add_widget(left)

            # iOS style switch
            sw = Switch(
                active=alarm['active'],
                size_hint=(None, None),
                size=(dp(58), dp(32))
            )
            sw.bind(active=lambda w, val, idx=i: self._tog(idx, val))
            row.add_widget(sw)
            self.alarm_box.add_widget(row)

            # Thin separator (not after last)
            if i < len(alarms) - 1:
                sep = Widget(size_hint_y=None, height=dp(1))
                with sep.canvas:
                    Color(*BG3)
                    rect = Rectangle(pos=sep.pos, size=sep.size)
                sep.bind(
                    pos=lambda w, v: setattr(rect, 'pos', v),
                    size=lambda w, v: setattr(rect, 'size', v)
                )
                self.alarm_box.add_widget(sep)

    def _tog(self, idx, val):
        if 0 <= idx < len(alarms):
            alarms[idx]['active'] = val

# ══════════════════════════════════════
# ADD ALARM SCREEN
# ══════════════════════════════════════
class AddAlarmScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sel_hour = 7
        self.sel_min  = 0
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical', spacing=0)
        flat_bg(root, BG1)

        # Nav bar
        nav = BoxLayout(
            size_hint_y=None, height=dp(52),
            padding=[dp(8), dp(8)]
        )
        flat_bg(nav, BG1)
        back = Button(
            text='Cancel', font_size=sp(17),
            size_hint=(None, 1), width=dp(80),
            background_color=(0,0,0,0), color=BLUE
        )
        back.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'home'))
        nav.add_widget(back)
        nav.add_widget(Label(
            text='Add Alarm', font_size=sp(17),
            bold=True, color=WHITE
        ))
        save = Button(
            text='Save', font_size=sp(17),
            size_hint=(None, 1), width=dp(60),
            background_color=(0,0,0,0), color=BLUE
        )
        save.bind(on_press=self._save)
        nav.add_widget(save)
        root.add_widget(nav)

        # ── TIME PICKER CARD
        root.add_widget(Widget(size_hint_y=None, height=dp(12)))
        picker_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.92, None), height=dp(190)
        )
        picker_card.pos_hint = {'center_x': 0.5}
        ios_card(picker_card, BG2, radius=18)

        # Up buttons
        up = BoxLayout(size_hint_y=None, height=dp(44),
                       padding=[dp(40), dp(4)])
        for part in ['h', 'm']:
            btn = Button(
                text='▲', font_size=sp(20),
                background_color=(0,0,0,0), color=BLUE
            )
            btn.bind(on_press=lambda _, p=part:
                     self._chg(p, 1))
            up.add_widget(btn)
            if part == 'h':
                up.add_widget(Widget(
                    size_hint_x=None, width=dp(30)))
        picker_card.add_widget(up)

        # Time display
        t_row = BoxLayout(
            size_hint_y=None, height=dp(72),
            padding=[dp(20), 0]
        )
        self.h_lbl = Label(
            text=f'{self.sel_hour:02d}',
            font_size=sp(56), bold=True, color=WHITE
        )
        t_row.add_widget(self.h_lbl)
        t_row.add_widget(Label(
            text=':', font_size=sp(56), bold=True,
            color=WHITE, size_hint_x=None, width=dp(24)
        ))
        self.m_lbl = Label(
            text=f'{self.sel_min:02d}',
            font_size=sp(56), bold=True, color=WHITE
        )
        t_row.add_widget(self.m_lbl)
        picker_card.add_widget(t_row)

        # Down buttons
        dn = BoxLayout(size_hint_y=None, height=dp(44),
                       padding=[dp(40), dp(4)])
        for part in ['h', 'm']:
            btn = Button(
                text='▼', font_size=sp(20),
                background_color=(0,0,0,0), color=BLUE
            )
            btn.bind(on_press=lambda _, p=part:
                     self._chg(p, -1))
            dn.add_widget(btn)
            if part == 'h':
                dn.add_widget(Widget(
                    size_hint_x=None, width=dp(30)))
        picker_card.add_widget(dn)
        root.add_widget(picker_card)

        # ── SETTINGS CARD
        root.add_widget(Widget(size_hint_y=None, height=dp(24)))
        settings_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.92, None), height=dp(180),
            spacing=0
        )
        settings_card.pos_hint = {'center_x': 0.5}
        ios_card(settings_card, BG2, radius=18)

        rows = [
            ('Repeat', 'Every Day', 'repeat', True),
            ('Sound',  'Radar',     None,     True),
            ('Snooze', '',          None,     False),
        ]
        for i, (title, sub, dest, arrow) in enumerate(rows):
            row = BoxLayout(
                size_hint_y=None, height=dp(52),
                padding=[dp(18), dp(10)]
            )
            if dest:
                btn = Button(
                    text='', size_hint=(1, 1),
                    background_color=(0,0,0,0)
                )
                btn.bind(on_press=lambda _, d=dest:
                         setattr(self.manager, 'current', d))
                row.add_widget(btn)

            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(
                text=title, font_size=sp(16),
                color=WHITE, halign='left',
                size_hint_y=None, height=dp(26)
            ))
            if sub:
                info.add_widget(Label(
                    text=sub, font_size=sp(12),
                    color=GREY, halign='left',
                    size_hint_y=None, height=dp(18)
                ))
            row.add_widget(info)

            if arrow:
                row.add_widget(Label(
                    text='›', font_size=sp(20),
                    color=LGREY,
                    size_hint=(None, 1), width=dp(24)
                ))
            else:
                row.add_widget(Switch(
                    active=True,
                    size_hint=(None, None),
                    size=(dp(52), dp(30))
                ))
            settings_card.add_widget(row)

            if i < len(rows) - 1:
                sep = Widget(size_hint_y=None, height=dp(1))
                with sep.canvas:
                    Color(*BG3)
                    sep_r = Rectangle(pos=sep.pos, size=sep.size)
                sep.bind(
                    pos=lambda w, v: setattr(sep_r, 'pos', v),
                    size=lambda w, v: setattr(sep_r, 'size', v)
                )
                settings_card.add_widget(sep)

        root.add_widget(settings_card)
        root.add_widget(Widget())
        self.add_widget(root)

    def _chg(self, part, delta):
        if part == 'h':
            self.sel_hour = (self.sel_hour + delta) % 24
            self.h_lbl.text = f'{self.sel_hour:02d}'
        else:
            self.sel_min = (self.sel_min + delta) % 60
            self.m_lbl.text = f'{self.sel_min:02d}'

    def _save(self, *_):
        t = f'{self.sel_hour:02d}:{self.sel_min:02d}'
        add_alarm(t, f'Alarm {t}',
                  ['Mon', 'Wed', 'Thu'], '')
        speak(f'Alarm set for {t}')
        self.manager.current = 'home'

# ══════════════════════════════════════
# REPEAT SCREEN
# ══════════════════════════════════════
class RepeatScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.selected = {'Sunday'}
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical')
        flat_bg(root, BG1)

        nav = BoxLayout(
            size_hint_y=None, height=dp(52),
            padding=[dp(8), dp(8)]
        )
        flat_bg(nav, BG1)
        back = Button(
            text='‹  Back', font_size=sp(17),
            size_hint=(None, 1), width=dp(90),
            background_color=(0,0,0,0), color=BLUE
        )
        back.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'add_alarm'))
        nav.add_widget(back)
        nav.add_widget(Label(
            text='Repeat', font_size=sp(17),
            bold=True, color=WHITE
        ))
        nav.add_widget(Widget(size_hint_x=None, width=dp(90)))
        root.add_widget(nav)

        root.add_widget(Widget(size_hint_y=None, height=dp(16)))

        # Days card
        days_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.92, None), height=dp(400),
            spacing=0
        )
        days_card.pos_hint = {'center_x': 0.5}
        ios_card(days_card, BG2, radius=18)

        days = ['Sunday','Monday','Tuesday','Wednesday',
                'Thursday','Friday','Saturday']

        for i, day in enumerate(days):
            row = BoxLayout(
                size_hint_y=None, height=dp(52),
                padding=[dp(18), dp(10)]
            )
            d_lbl = Label(
                text=day, font_size=sp(16),
                color=WHITE, halign='left'
            )
            d_lbl.bind(
                size=lambda w, s: setattr(w, 'text_size', s))
            row.add_widget(d_lbl)

            check = Label(
                text='✓' if day in self.selected else '',
                font_size=sp(18), color=BLUE,
                size_hint=(None, 1), width=dp(30)
            )
            row.add_widget(check)

            btn = Button(
                text='', size_hint=(1, 1),
                background_color=(0,0,0,0),
                pos=row.pos, size=row.size
            )
            btn.bind(on_press=lambda w,
                     dy=day, ch=check: self._tog(dy, ch))
            row.add_widget(btn)
            days_card.add_widget(row)

            if i < len(days)-1:
                sep = Widget(size_hint_y=None, height=dp(1))
                with sep.canvas:
                    Color(*BG3)
                    sr = Rectangle(pos=sep.pos, size=sep.size)
                sep.bind(
                    pos=lambda w, v: setattr(sr, 'pos', v),
                    size=lambda w, v: setattr(sr, 'size', v)
                )
                days_card.add_widget(sep)

        root.add_widget(days_card)
        root.add_widget(Widget())
        self.add_widget(root)

    def _tog(self, day, ch):
        if day in self.selected:
            self.selected.discard(day)
            ch.text = ''
        else:
            self.selected.add(day)
            ch.text = '✓'

# ══════════════════════════════════════
# SETTINGS SCREEN
# ══════════════════════════════════════
class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical')
        flat_bg(root, BG1)

        nav = BoxLayout(
            size_hint_y=None, height=dp(52),
            padding=[dp(8), dp(8)]
        )
        flat_bg(nav, BG1)
        back = Button(
            text='‹  Back', font_size=sp(17),
            size_hint=(None, 1), width=dp(90),
            background_color=(0,0,0,0), color=BLUE
        )
        back.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'home'))
        nav.add_widget(back)
        nav.add_widget(Label(
            text='Settings', font_size=sp(17),
            bold=True, color=WHITE
        ))
        nav.add_widget(Widget(size_hint_x=None, width=dp(90)))
        root.add_widget(nav)

        root.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Theme card
        theme_card = BoxLayout(
            size_hint=(0.92, None), height=dp(62),
            padding=[dp(18), dp(10)]
        )
        theme_card.pos_hint = {'center_x': 0.5}
        ios_card(theme_card, BG2, radius=14)
        theme_card.add_widget(Label(
            text='Appearance', font_size=sp(16),
            color=WHITE, halign='left'
        ))
        circles = BoxLayout(
            size_hint=(None, 1), width=dp(80), spacing=dp(10))
        for col in [BLUE, ORANGE]:
            circles.add_widget(Button(
                size_hint=(None, None), size=(dp(28), dp(28)),
                background_color=col,
                border=(dp(14),)*4
            ))
        theme_card.add_widget(circles)
        root.add_widget(theme_card)

        root.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Volume card
        vol_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.92, None), height=dp(88),
            padding=[dp(18), dp(12)]
        )
        vol_card.pos_hint = {'center_x': 0.5}
        ios_card(vol_card, BG2, radius=14)
        vol_card.add_widget(Label(
            text='Volume', font_size=sp(16),
            color=WHITE, halign='left',
            size_hint_y=None, height=dp(26)
        ))
        sl = Slider(
            min=0, max=100, value=65,
            size_hint_y=None, height=dp(36),
            cursor_size=(dp(22), dp(22))
        )
        vol_card.add_widget(sl)
        root.add_widget(vol_card)

        root.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Info card
        info_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.92, None), height=dp(110),
            spacing=0
        )
        info_card.pos_hint = {'center_x': 0.5}
        ios_card(info_card, BG2, radius=14)

        for i, (title, val) in enumerate([
            ('Developer', 'Aditya Thakare (Adiyani)'),
            ('Version',   'VoxWatch v2.0'),
        ]):
            row = BoxLayout(
                size_hint_y=None, height=dp(52),
                padding=[dp(18), dp(12)]
            )
            row.add_widget(Label(
                text=title, font_size=sp(16),
                color=WHITE, halign='left'
            ))
            row.add_widget(Label(
                text=val, font_size=sp(13),
                color=GREY, halign='right'
            ))
            info_card.add_widget(row)
            if i == 0:
                sep = Widget(size_hint_y=None, height=dp(1))
                with sep.canvas:
                    Color(*BG3)
                    sr = Rectangle(pos=sep.pos, size=sep.size)
                sep.bind(
                    pos=lambda w, v: setattr(sr, 'pos', v),
                    size=lambda w, v: setattr(sr, 'size', v)
                )
                info_card.add_widget(sep)

        root.add_widget(info_card)
        root.add_widget(Widget())
        self.add_widget(root)

# ══════════════════════════════════════
# ALARM TRIGGER SCREEN
# ══════════════════════════════════════
class AlarmTriggerScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def _build(self):
        fl = FloatLayout()
        flat_bg(fl, BG1)

        # Big time
        self.time_lbl = Label(
            text='07:00',
            font_size=sp(80), bold=True, color=WHITE,
            size_hint=(1, None), height=dp(110),
            pos_hint={'center_x': 0.5, 'center_y': 0.60}
        )
        fl.add_widget(self.time_lbl)

        # Label
        self.name_lbl = Label(
            text='Alarm',
            font_size=sp(20), color=GREY,
            size_hint=(1, None), height=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.50}
        )
        fl.add_widget(self.name_lbl)

        # Routine card
        self.routine_card = BoxLayout(
            orientation='vertical',
            size_hint=(0.88, None), height=dp(140),
            pos_hint={'center_x': 0.5, 'center_y': 0.34},
            padding=[dp(18), dp(14)], spacing=dp(6)
        )
        ios_card(self.routine_card, BG2, radius=18)
        self.routine_lbl = Label(
            text='',
            font_size=sp(14), color=WHITE,
            halign='left', valign='top',
            text_size=(dp(320), dp(110))
        )
        self.routine_card.add_widget(self.routine_lbl)
        fl.add_widget(self.routine_card)

        # Shut down btn — iOS red pill
        shut = Button(
            text='Stop Alarm',
            font_size=sp(18), bold=True,
            size_hint=(0.82, None), height=dp(58),
            pos_hint={'center_x': 0.5, 'y': 0.06},
            background_color=RED,
            border=(dp(29),)*4
        )
        shut.bind(on_press=lambda _: setattr(
            self.manager, 'current', 'home'))
        fl.add_widget(shut)
        self.add_widget(fl)

    def show_alarm(self, alarm):
        self.time_lbl.text = alarm['time']
        self.name_lbl.text = alarm['label']
        items = [i.strip() for i in
                 alarm.get('routine', '').split('|') if i.strip()]
        if items:
            self.routine_lbl.text = '\n'.join(
                [f"  {i+1}.  {t}" for i, t in enumerate(items[:5])])
        else:
            self.routine_lbl.text = 'No routine set'
        self.manager.current = 'trigger'
        msg = f"It's {alarm['time']}. {alarm['label']}. "
        if items:
            msg += "Your routine: " + ", then ".join(items[:4])
        speak(msg)

# ══════════════════════════════════════
# ALARM CHECKER
# ══════════════════════════════════════
class AlarmChecker:
    def __init__(self, trigger):
        self.ts = trigger

    def start(self):
        threading.Thread(
            target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            now = datetime.now().strftime('%H:%M')
            for a in alarms:
                if (a['active'] and
                        not a['triggered'] and
                        a['time'] == now):
                    a['triggered'] = True
                    Clock.schedule_once(
                        lambda dt, al=a:
                        self.ts.show_alarm(al), 0)
            time.sleep(10)
            now2 = datetime.now().strftime('%H:%M')
            for a in alarms:
                if a['triggered'] and a['time'] != now2:
                    a['triggered'] = False

# ══════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════
class VoxWatchApp(App):
    def build(self):
        self.title = 'VoxWatch v2.0'
        Window.clearcolor = (0, 0, 0, 1)
        sm = ScreenManager(transition=SlideTransition())
        trigger = AlarmTriggerScreen(name='trigger')
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddAlarmScreen(name='add_alarm'))
        sm.add_widget(RepeatScreen(name='repeat'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(trigger)
        load_csv()
        AlarmChecker(trigger).start()
        speak('VoxWatch ready hai!')
        return sm

if __name__ == '__main__':
    VoxWatchApp().run()