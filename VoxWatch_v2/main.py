# VoxWatch v2.0 — Smart Voice Alarm
# Banaya: Aditya Thakare

import threading
import time
import csv
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

import pyttsx3


# ── VOICE ENGINE ──────────────────────
# Yeh class app ko bolne ki taakat deti hai!

class VoiceEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            print("✅ Voice Engine ready!")
        except Exception as e:
            print(f"❌ Voice Error: {e}")
            self.engine = None

    def speak(self, text):
        # Yeh function text ko awaaz mein badalta hai
        if self.engine:
            def _run():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass
            threading.Thread(target=_run, daemon=True).start()
        else:
            print(f"[SPEAK] {text}")

# Global voice object banao
voice = VoiceEngine()


# ── ALARM ENGINE ──────────────────────
# Yeh class alarm ko manage karti hai!

# 




class AlarmEngine:
    def __init__(self, on_trigger):
        self.alarms = []
        self.running = False
        self.on_trigger = on_trigger

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()
        print("✅ Alarm Engine started!")

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            now = datetime.now().strftime("%H:%M")
            for alarm in self.alarms:
                if alarm['active'] and not alarm['triggered']:
                    if alarm['time'] == now:
                        alarm['triggered'] = True
                        Clock.schedule_once(
                            lambda dt, a=alarm: self.on_trigger(a), 0
                        )
            time.sleep(20)
            now2 = datetime.now().strftime("%H:%M")
            for alarm in self.alarms:
                if alarm['triggered'] and alarm['time'] != now2:
                    alarm['triggered'] = False

    def add(self, alarm_time, label, routine):
        self.alarms.append({
            'time':      alarm_time,
            'label':     label,
            'routine':   routine,
            'active':    True,
            'triggered': False
        })
        print(f"✅ Alarm added: {alarm_time} - {label}")

    def load_csv(self, path):
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.add(
                        row['time'].strip(),
                        row['label'].strip(),
                        row['routine'].strip()
                    )
            print("✅ CSV loaded!")
        except Exception as e:
            print(f"❌ CSV Error: {e}")

            # ── MAIN APP ──────────────────────────
# Yeh class poori app banati hai!

class VoxWatchApp(App):
    def build(self):
        # Window setup
        Window.clearcolor = (0.04, 0.06, 0.10, 1)  # Dark background
        self.title = "VoxWatch v2.0"

        # Alarm engine shuru karo
        self.alarm_engine = AlarmEngine(
            on_trigger=self._on_alarm
        )
        self.alarm_engine.start()

        # CSV load karo
        csv_path = os.path.join(
            os.path.dirname(__file__),
            "sample_routine.csv"
        )
        if os.path.exists(csv_path):
            self.alarm_engine.load_csv(csv_path)

        # Main layout banao
        root = BoxLayout(orientation='vertical')

        # ── HEADER ──
        header = Label(
            text="⌚ VoxWatch v2.0",
            font_size=24,
            size_hint_y=None,
            height=60,
            color=(0.31, 0.56, 0.97, 1)  # Blue color
        )
        root.add_widget(header)

        # ── CLOCK ──
        self.clock_label = Label(
            text="00:00",
            font_size=52,
            size_hint_y=None,
            height=80,
            color=(0.31, 0.56, 0.97, 1)
        )
        root.add_widget(self.clock_label)

        # ── DATE ──
        self.date_label = Label(
            text="",
            font_size=14,
            size_hint_y=None,
            height=30,
            color=(0.53, 0.54, 0.64, 1)  # Grey color
        )
        root.add_widget(self.date_label)

        # Clock update shuru karo
        Clock.schedule_interval(self._update_clock, 1)

        # ── ADD ALARM SECTION ──
        root.add_widget(Label(
            text="── Add Alarm ──",
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        ))

        # Time input
        self.time_input = TextInput(
            hint_text="Time (HH:MM) — jaise 07:30",
            size_hint_y=None,
            height=44,
            font_size=16,
            multiline=False
        )
        root.add_widget(self.time_input)

        # Label input
        self.label_input = TextInput(
            hint_text="Label — jaise Morning Alarm",
            size_hint_y=None,
            height=44,
            font_size=16,
            multiline=False
        )
        root.add_widget(self.label_input)

        # Routine input
        self.routine_input = TextInput(
            hint_text="Routine — DSA | Java | Breakfast",
            size_hint_y=None,
            height=44,
            font_size=16,
            multiline=False
        )
        root.add_widget(self.routine_input)

        # Save button
        save_btn = Button(
            text="✅ Save Alarm",
            size_hint_y=None,
            height=50,
            font_size=18,
            background_color=(0.31, 0.56, 0.97, 1)
        )
        save_btn.bind(on_press=self._save_alarm)
        root.add_widget(save_btn)

        # ── ALARM LIST ──
        root.add_widget(Label(
            text="── Your Alarms ──",
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        ))

        # Scroll view for alarms
        scroll = ScrollView()
        self.alarm_list = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=8,
            padding=8
        )
        self.alarm_list.bind(
            minimum_height=self.alarm_list.setter('height')
        )
        scroll.add_widget(self.alarm_list)
        root.add_widget(scroll)

        # Alarm list refresh karo
        self._refresh_alarms()

        # Welcome message bolao
        Clock.schedule_once(
            lambda dt: voice.speak("VoxWatch ready hai!"), 1
        )

        return root

    def _update_clock(self, dt):
        # Clock update karo har second
        now = datetime.now()
        self.clock_label.text = now.strftime("%H:%M")
        self.date_label.text = now.strftime("%A, %d %B %Y")

    def _save_alarm(self, instance):
        # Alarm save karo
        t = self.time_input.text.strip()
        l = self.label_input.text.strip() or "Alarm"
        r = self.routine_input.text.strip()

        # Time validate karo
        if not t or len(t) != 5 or t[2] != ':':
            voice.speak("Time format galat hai! HH MM format use karo")
            return

        # Alarm add karo
        self.alarm_engine.add(t, l, r)
        voice.speak(f"Alarm set ho gaya {l} ke liye {t} baje")

        # Fields clear karo
        self.time_input.text = ""
        self.label_input.text = ""
        self.routine_input.text = ""

        # List refresh karo
        self._refresh_alarms()

    def _refresh_alarms(self):
        # Alarm list clear karke dobara banao
        self.alarm_list.clear_widgets()

        if not self.alarm_engine.alarms:
            self.alarm_list.add_widget(Label(
                text="Koi alarm nahi — upar se add karo!",
                font_size=14,
                color=(0.53, 0.54, 0.64, 1),
                size_hint_y=None,
                height=50
            ))
            return

        for alarm in self.alarm_engine.alarms:
            # Har alarm ka row banao
            row = BoxLayout(
                size_hint_y=None,
                height=60,
                spacing=8
            )

            # Time + Label
            info = Label(
                text=f"⏰ {alarm['time']}  {alarm['label']}",
                font_size=16,
                color=(1, 1, 1, 1),
                halign='left'
            )
            row.add_widget(info)

            self.alarm_list.add_widget(row)

    def _on_alarm(self, alarm):
        # Alarm bajne par yeh chalta hai!
        routine_items = alarm['routine'].split('|')
        spoken = f"It's {alarm['time']} — {alarm['label']}. "
        spoken += "Teri routine hai: "
        spoken += ", phir ".join(
            [r.strip() for r in routine_items[:4]]
        )
        voice.speak(spoken)
        print(f"🔔 ALARM: {alarm['label']} at {alarm['time']}")

    def on_stop(self):
        self.alarm_engine.stop()


# ── APP CHALAO ─────────────────────────
if __name__ == '__main__':
    VoxWatchApp().run()