"""
╔══════════════════════════════════════════════════════════════════════╗
║           STUDENT MANAGEMENT SYSTEM — Production Ready              ║
║        CustomTkinter + SQLite + OOP — Integrated with MGAHV         ║
╠══════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN:                                                         ║
║  1. Install dependencies:                                            ║
║       pip install customtkinter pillow                               ║
║  2. Run the application:                                             ║
║       python student_management_system.py                            ║
║  3. The SQLite database (students.db) is auto-created on first run.  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import sqlite3
import re
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ─── App-wide appearance ────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Palette & constants ────────────────────────────────────────────────────
COLORS = {
    "bg_primary":     "#0f1117",
    "bg_secondary":   "#1a1d27",
    "bg_card":        "#21263a",
    "bg_hover":       "#2a2f45",
    "accent":         "#4f8ef7",
    "accent_dim":     "#2d5cb8",
    "emerald":        "#34d399",
    "amber":          "#fbbf24",
    "rose":           "#f87171",
    "text_primary":   "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted":     "#64748b",
    "border":         "#2d3350",
    "sidebar":        "#13162a",
    "row_alt":        "#1e2238",
    "success_bg":     "#064e3b",
    "error_bg":       "#450a0a",
    "active_nav":     "#1e3a5f",
}

FONT_HEADING  = ("Helvetica Neue", 22, "bold")
FONT_SUBHEAD  = ("Helvetica Neue", 14, "bold")
FONT_BODY     = ("Helvetica Neue", 13)
FONT_SMALL    = ("Helvetica Neue", 11)
FONT_CODE     = ("Courier New",   12)
FONT_NAV      = ("Helvetica Neue", 13, "bold")
FONT_STAT     = ("Helvetica Neue", 32, "bold")

NAV_ITEMS = [
    ("📊", "Dashboard"),
    ("🎓", "Manage Students"),
    ("⚙️", "Settings"),
]

COURSES = [
    "Computer Science", "Business Administration", "Mechanical Engineering",
    "Data Science", "Electrical Engineering", "Medicine", "Law",
    "Architecture", "Psychology", "Economics", "Mathematics", "Physics",
]

STATUS_OPTIONS = ["Active", "Suspended", "Graduated"]

# Reference Configuration for MGAHV Central University
UNIVERSITY_METADATA = {
    "name": "Mahatma Gandhi Antarrashtriya Hindi Vishwavidyalaya",
    "acronym": "MGAHV",
    "location": "Wardha, Maharashtra",
    "type": "Central University",
    "established": "1997",
    "id_prefix": "MGAHV"
}


# ══════════════════════════════════════════════════════════════════════════════
#  DATABASE LAYER
# ══════════════════════════════════════════════════════════════════════════════

class Database:
    """Handles all SQLite interactions for the Student Management System."""

    def __init__(self, db_path: str = "students.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_university_reference()
        self._seed_demo_data()

    def _create_tables(self):
        """Create tables if they don't already exist."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id    TEXT    UNIQUE NOT NULL,
                full_name     TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                phone         TEXT    NOT NULL,
                course        TEXT    NOT NULL,
                enrolled_date TEXT    NOT NULL,
                status        TEXT    NOT NULL DEFAULT 'Active',
                created_at    TEXT    NOT NULL
            )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def _seed_university_reference(self):
        """Seeds global university metadata into the settings table."""
        for key, value in UNIVERSITY_METADATA.items():
            self.set_setting(f"univ_{key}", value)

    def _seed_demo_data(self):
        """Populate demo students only when the table is empty."""
        count = self.connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        if count > 0:
            return
        demo = [
            ("Aarav Sharma",    "aarav.sharma@uni.edu",    "9876543210", "Computer Science",         "2023-08-15", "Active"),
            ("Priya Patel",     "priya.patel@uni.edu",     "9123456780", "Data Science",             "2023-08-15", "Active"),
            ("Rohan Mehta",     "rohan.mehta@uni.edu",     "8765432109", "Mechanical Engineering",   "2022-07-20", "Graduated"),
            ("Sneha Reddy",     "sneha.reddy@uni.edu",     "9988776655", "Business Administration",  "2024-01-10", "Active"),
            ("Kiran Kumar",     "kiran.kumar@uni.edu",     "7654321098", "Electrical Engineering",   "2023-03-05", "Suspended"),
            ("Ananya Iyer",     "ananya.iyer@uni.edu",     "8123456709", "Psychology",                "2024-01-10", "Active"),
            ("Vikram Singh",    "vikram.singh@uni.edu",    "9345678012", "Law",                       "2022-07-20", "Graduated"),
            ("Divya Nair",      "divya.nair@uni.edu",      "8901234567", "Medicine",                  "2023-08-15", "Active"),
            ("Arjun Desai",     "arjun.desai@uni.edu",     "7890123456", "Mathematics",               "2024-06-01", "Active"),
            ("Meera Joshi",     "meera.joshi@uni.edu",     "9012345678", "Physics",                   "2024-06-01", "Active"),
        ]
        for name, email, phone, course, enroll, status in demo:
            sid = self._generate_student_id()
            self.connection.execute(
                "INSERT INTO students (student_id,full_name,email,phone,course,enrolled_date,status,created_at) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (sid, name, email, phone, course, enroll, status, datetime.now().isoformat())
            )
        self.connection.commit()

    def _generate_student_id(self) -> str:
        """Generates a unique institutional student ID matching the MGAHV format."""
        year = datetime.now().year
        row = self.connection.execute("SELECT MAX(id) FROM students").fetchone()[0]
        seq = (row or 0) + 1
        prefix = self.get_setting("univ_id_prefix", default="MGAHV")
        return f"{prefix}-{year}-{seq:04d}"

    def add_student(self, full_name, email, phone, course, enrolled_date, status) -> str:
        sid = self._generate_student_id()
        self.connection.execute(
            "INSERT INTO students (student_id,full_name,email,phone,course,enrolled_date,status,created_at) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (sid, full_name, email, phone, course, enrolled_date, status, datetime.now().isoformat())
        )
        self.connection.commit()
        return sid

    def update_student(self, student_id, full_name, email, phone, course, enrolled_date, status):
        self.connection.execute(
            "UPDATE students SET full_name=?,email=?,phone=?,course=?,enrolled_date=?,status=? "
            "WHERE student_id=?",
            (full_name, email, phone, course, enrolled_date, status, student_id)
        )
        self.connection.commit()

    def delete_student(self, student_id):
        self.connection.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        self.connection.commit()

    def get_all_students(self, search: str = "") -> list:
        if search:
            q = f"%{search}%"
            rows = self.connection.execute(
                "SELECT * FROM students WHERE full_name LIKE ? OR student_id LIKE ? OR course LIKE ? "
                "ORDER BY id DESC", (q, q, q)
            ).fetchall()
        else:
            rows = self.connection.execute(
                "SELECT * FROM students ORDER BY id DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def get_student_by_id(self, student_id: str) -> dict | None:
        row = self.connection.execute(
            "SELECT * FROM students WHERE student_id=?", (student_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_stats(self) -> dict:
        total     = self.connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        active    = self.connection.execute("SELECT COUNT(*) FROM students WHERE status='Active'").fetchone()[0]
        graduated = self.connection.execute("SELECT COUNT(*) FROM students WHERE status='Graduated'").fetchone()[0]
        suspended = self.connection.execute("SELECT COUNT(*) FROM students WHERE status='Suspended'").fetchone()[0]
        
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        recent = self.connection.execute(
            "SELECT full_name, course, enrolled_date, status FROM students "
            "WHERE enrolled_date >= ? ORDER BY enrolled_date DESC LIMIT 5", (cutoff,)
        ).fetchall()
        
        courses = self.connection.execute(
            "SELECT course, COUNT(*) as cnt FROM students GROUP BY course ORDER BY cnt DESC LIMIT 6"
        ).fetchall()
        return {
            "total": total, "active": active,
            "graduated": graduated, "suspended": suspended,
            "recent": [dict(r) for r in recent],
            "courses": [dict(r) for r in courses],
        }

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.connection.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else default

    def set_setting(self, key: str, value: str):
        self.connection.execute(
            "INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value)
        )
        self.connection.commit()


# ══════════════════════════════════════════════════════════════════════════════
#  VALIDATION HELPERS
# ══════════════════════════════════════════════════════════════════════════════

class Validator:
    @staticmethod
    def email(value: str) -> bool:
        return bool(re.match(r"^[\w.+\-]+@[\w\-]+\.[a-z]{2,}$", value, re.IGNORECASE))

    @staticmethod
    def phone(value: str) -> bool:
        return bool(re.match(r"^\d{7,15}$", value))

    @staticmethod
    def not_empty(*values) -> bool:
        return all(v.strip() for v in values)


# ══════════════════════════════════════════════════════════════════════════════
#  REUSABLE UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

class Toast:
    """Floating toast notification that fades after 3 seconds."""

    def __init__(self, parent, message: str, kind: str = "success"):
        bg = COLORS["success_bg"] if kind == "success" else COLORS["error_bg"]
        icon = "✔" if kind == "success" else "✖"
        color = COLORS["emerald"] if kind == "success" else COLORS["rose"]

        self.win = ctk.CTkToplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)

        px = parent.winfo_rootx() + parent.winfo_width()  - 340
        py = parent.winfo_rooty() + parent.winfo_height() - 80
        self.win.geometry(f"320x56+{px}+{py}")
        self.win.configure(fg_color=bg)

        frame = ctk.CTkFrame(self.win, fg_color=bg, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(frame, text=icon, text_color=color,
                     font=("Helvetica Neue", 18, "bold")).pack(side="left", padx=(14, 6), pady=10)
        ctk.CTkLabel(frame, text=message, text_color=COLORS["text_primary"],
                     font=FONT_BODY, wraplength=240).pack(side="left", pady=10)

        self.win.after(3000, self.win.destroy)


class StatCard(ctk.CTkFrame):
    """A metric card for the dashboard."""

    def __init__(self, parent, icon: str, label: str, value: str, accent: str, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_card"], corner_radius=16, **kwargs)

        ctk.CTkLabel(self, text=icon, font=("Helvetica Neue", 28),
                     text_color=accent).grid(row=0, column=0, padx=(20, 10), pady=(18, 2), sticky="w")
        ctk.CTkLabel(self, text=value, font=FONT_STAT,
                     text_color=COLORS["text_primary"]).grid(row=1, column=0, padx=20, sticky="w")
        ctk.CTkLabel(self, text=label, font=FONT_SMALL,
                     text_color=COLORS["text_secondary"]).grid(row=2, column=0, padx=20, pady=(0, 18), sticky="w")


class SectionHeader(ctk.CTkLabel):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, font=FONT_SUBHEAD,
                         text_color=COLORS["text_primary"], **kwargs)


class Divider(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=1, fg_color=COLORS["border"], **kwargs)


# ══════════════════════════════════════════════════════════════════════════════
#  VIEWS
# ══════════════════════════════════════════════════════════════════════════════

class DashboardView(ctk.CTkFrame):
    """Analytics dashboard: stats, horizontal metrics, recent enrollments."""

    def __init__(self, parent, db: Database):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self._build()

    def _build(self):
        stats = self.db.get_stats()

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(30, 0))
        ctk.CTkLabel(hdr, text="Dashboard Overview", font=FONT_HEADING,
                     text_color=COLORS["text_primary"]).pack(side="left")
        now = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(hdr, text=now, font=FONT_SMALL,
                     text_color=COLORS["text_muted"]).pack(side="right", pady=(8, 0))

        Divider(self).pack(fill="x", padx=30, pady=(16, 20))

        # Stat Cards
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)
        for col in range(4):
            cards_frame.columnconfigure(col, weight=1)

        card_data = [
            ("🎓", "Total Students",  str(stats["total"]),     COLORS["accent"]),
            ("✅", "Active",          str(stats["active"]),    COLORS["emerald"]),
            ("🏛️", "Graduated",       str(stats["graduated"]), COLORS["amber"]),
            ("⛔", "Suspended",       str(stats["suspended"]), COLORS["rose"]),
        ]
        for i, (icon, label, val, color) in enumerate(card_data):
            card = StatCard(cards_frame, icon=icon, label=label, value=val, accent=color)
            card.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="ew", ipady=6)

        # Lower section: chart + recent
        lower = ctk.CTkFrame(self, fg_color="transparent")
        lower.pack(fill="both", expand=True, padx=30, pady=20)
        lower.columnconfigure(0, weight=3)
        lower.columnconfigure(1, weight=2)
        lower.rowconfigure(0, weight=1)

        self._build_bar_chart(lower, stats["courses"])
        self._build_recent(lower, stats["recent"])

    def _build_bar_chart(self, parent, courses: list):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=16)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ctk.CTkLabel(card, text="Students by Course", font=FONT_SUBHEAD,
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=20, pady=(18, 12))

        canvas_frame = ctk.CTkFrame(card, fg_color="transparent")
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        if not courses:
            ctk.CTkLabel(canvas_frame, text="No data yet.",
                         text_color=COLORS["text_muted"]).pack(expand=True)
            return

        max_val = max(c["cnt"] for c in courses) or 1
        BAR_COLORS = [COLORS["accent"], COLORS["emerald"], COLORS["amber"],
                      COLORS["rose"], "#a78bfa", "#fb923c"]

        for idx, row in enumerate(courses):
            row_f = ctk.CTkFrame(canvas_frame, fg_color="transparent")
            row_f.pack(fill="x", pady=4)

            name = row["course"][:22] + ("…" if len(row["course"]) > 22 else "")
            ctk.CTkLabel(row_f, text=name, font=FONT_SMALL, width=180,
                         text_color=COLORS["text_secondary"], anchor="w").pack(side="left")

            ratio = row["cnt"] / max_val
            bar_bg = ctk.CTkFrame(row_f, fg_color=COLORS["bg_hover"],
                                  corner_radius=6, height=18)
            bar_bg.pack(side="left", fill="x", expand=True, padx=(8, 8))
            bar_bg.pack_propagate(False)

            bar = ctk.CTkFrame(bar_bg, fg_color=BAR_COLORS[idx % len(BAR_COLORS)],
                               corner_radius=6, height=18)
            bar.place(relx=0, rely=0, relheight=1, relwidth=ratio)

            ctk.CTkLabel(row_f, text=str(row["cnt"]), font=FONT_SMALL,
                         text_color=COLORS["text_primary"], width=28).pack(side="right")

    def _build_recent(self, parent, recent: list):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=16)
        card.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(card, text="Recent Enrollments", font=FONT_SUBHEAD,
                     text_color=COLORS["text_primary"]).pack(anchor="w", padx=20, pady=(18, 12))

        if not recent:
            ctk.CTkLabel(card, text="No recent enrollments.",
                         text_color=COLORS["text_muted"]).pack(expand=True)
            return

        STATUS_COLOR = {
            "Active": COLORS["emerald"],
            "Graduated": COLORS["amber"],
            "Suspended": COLORS["rose"],
        }

        for i, s in enumerate(recent):
            row_bg = COLORS["bg_hover"] if i % 2 == 0 else COLORS["bg_card"]
            row_f  = ctk.CTkFrame(card, fg_color=row_bg, corner_radius=10)
            row_f.pack(fill="x", padx=14, pady=3)

            initials = "".join(p[0].upper() for p in s["full_name"].split()[:2])
            av = ctk.CTkFrame(row_f, fg_color=COLORS["accent_dim"],
                              width=38, height=38, corner_radius=19)
            av.pack(side="left", padx=(10, 10), pady=10)
            av.pack_propagate(False)
            ctk.CTkLabel(av, text=initials, font=("Helvetica Neue", 12, "bold"),
                         text_color=COLORS["text_primary"]).place(relx=.5, rely=.5, anchor="center")

            info = ctk.CTkFrame(row_f, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True)
            ctk.CTkLabel(info, text=s["full_name"], font=FONT_BODY,
                         text_color=COLORS["text_primary"], anchor="w").pack(anchor="w")
            ctk.CTkLabel(info, text=s["course"][:26], font=FONT_SMALL,
                         text_color=COLORS["text_muted"], anchor="w").pack(anchor="w")

            sc = STATUS_COLOR.get(s["status"], COLORS["text_muted"])
            ctk.CTkLabel(row_f, text=s["status"], font=FONT_SMALL,
                         text_color=sc, width=72).pack(side="right", padx=10)

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()


# ─────────────────────────────────────────────────────────────────────────────

class StudentFormDialog(ctk.CTkToplevel):
    """Modal dialog for Add / Edit student."""

    def __init__(self, parent, db: Database, on_save, student: dict = None):
        super().__init__(parent)
        self.db        = db
        self.on_save   = on_save
        self.student   = student
        self.editing   = student is not None

        self.title("Edit Student" if self.editing else "Add New Student")
        self.geometry("540x620")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_secondary"])
        self.grab_set()
        self.attributes("-topmost", True)
        self._center()
        self._build()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - 540) // 2
        y = (sh - 620) // 2
        self.geometry(f"540x620+{x}+{y}")

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=0)
        hdr.pack(fill="x")
        title = "✏️  Edit Student" if self.editing else "➕  Add New Student"
        ctk.CTkLabel(hdr, text=title, font=FONT_SUBHEAD,
                     text_color=COLORS["text_primary"]).pack(side="left", padx=24, pady=16)

        body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=16)

        def field(label, row, placeholder="", default=""):
            ctk.CTkLabel(body, text=label, font=FONT_SMALL,
                         text_color=COLORS["text_secondary"]).grid(
                row=row*2, column=0, sticky="w", pady=(8, 2))
            e = ctk.CTkEntry(body, placeholder_text=placeholder,
                             fg_color=COLORS["bg_card"], border_color=COLORS["border"],
                             text_color=COLORS["text_primary"], height=40, corner_radius=8)
            e.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 4))
            if default:
                e.insert(0, default)
            return e

        body.columnconfigure(0, weight=1)

        s = self.student or {}
        self.e_name   = field("Full Name *",    0, "e.g. Rahul Verma",         s.get("full_name",""))
        self.e_email  = field("Email *",        1, "e.g. rahul@uni.edu",        s.get("email",""))
        self.e_phone  = field("Phone Number *", 2, "10–15 digits",              s.get("phone",""))

        ctk.CTkLabel(body, text="Course / Major *", font=FONT_SMALL,
                     text_color=COLORS["text_secondary"]).grid(row=6, column=0, sticky="w", pady=(8,2))
        self.dd_course = ctk.CTkOptionMenu(
            body, values=COURSES,
            fg_color=COLORS["bg_card"], button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_dim"],
            text_color=COLORS["text_primary"], corner_radius=8, height=40,
        )
        self.dd_course.grid(row=7, column=0, sticky="ew", pady=(0,4))
        self.dd_course.set(s.get("course", COURSES[0]))

        ctk.CTkLabel(body, text="Enrollment Date *", font=FONT_SMALL,
                     text_color=COLORS["text_secondary"]).grid(row=8, column=0, sticky="w", pady=(8,2))
        self.e_date = ctk.CTkEntry(body, placeholder_text="YYYY-MM-DD",
                                   fg_color=COLORS["bg_card"], border_color=COLORS["border"],
                                   text_color=COLORS["text_primary"], height=40, corner_radius=8)
        self.e_date.grid(row=9, column=0, sticky="ew", pady=(0,4))
        self.e_date.insert(0, s.get("enrolled_date", datetime.now().strftime("%Y-%m-%d")))

        ctk.CTkLabel(body, text="Status *", font=FONT_SMALL,
                     text_color=COLORS["text_secondary"]).grid(row=10, column=0, sticky="w", pady=(8,2))
        self.dd_status = ctk.CTkOptionMenu(
            body, values=STATUS_OPTIONS,
            fg_color=COLORS["bg_card"], button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_dim"],
            text_color=COLORS["text_primary"], corner_radius=8, height=40,
        )
        self.dd_status.grid(row=11, column=0, sticky="ew", pady=(0,4))
        self.dd_status.set(s.get("status", "Active"))

        self.lbl_err = ctk.CTkLabel(body, text="", font=FONT_SMALL,
                                    text_color=COLORS["rose"], wraplength=480)
        self.lbl_err.grid(row=12, column=0, sticky="w", pady=(8, 0))

        btn_row = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=0)
        btn_row.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_row, text="Cancel", command=self.destroy,
                      fg_color=COLORS["bg_hover"], hover_color=COLORS["border"],
                      text_color=COLORS["text_secondary"], corner_radius=8,
                      font=FONT_BODY, width=120, height=42).pack(side="right", padx=(8,20), pady=16)

        ctk.CTkButton(btn_row, text="Save Student", command=self._save,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dim"],
                      text_color="#ffffff", corner_radius=8,
                      font=FONT_NAV, width=160, height=42).pack(side="right", pady=16)

    def _save(self):
        name   = self.e_name.get().strip()
        email  = self.e_email.get().strip()
        phone  = self.e_phone.get().strip()
        course = self.dd_course.get()
        date   = self.e_date.get().strip()
        status = self.dd_status.get()

        if not Validator.not_empty(name, email, phone, date):
            self._err("All fields are required.")
            return
        if not Validator.email(email):
            self._err("Please enter a valid email address.")
            return
        if not Validator.phone(phone):
            self._err("Phone must contain 7–15 digits only.")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self._err("Date must be in YYYY-MM-DD format.")
            return

        try:
            if self.editing:
                self.db.update_student(self.student["student_id"], name, email, phone, course, date, status)
            else:
                self.db.add_student(name, email, phone, course, date, status)
            self.on_save()
            self.destroy()
        except sqlite3.IntegrityError as e:
            if "email" in str(e):
                self._err("This email is already registered.")
            else:
                self._err(f"Database error: {e}")

    def _err(self, msg: str):
        self.lbl_err.configure(text=f"⚠  {msg}")


# ─────────────────────────────────────────────────────────────────────────────

class ManageStudentsView(ctk.CTkFrame):
    """Full CRUD table view with search & filter functionality."""

    COL_IDS   = ("student_id", "full_name", "email", "phone", "course", "enrolled_date", "status")
    COL_HEADS = ("Student ID", "Full Name", "Email", "Phone", "Course", "Enrolled", "Status")
    COL_WIDTHS= (115, 160, 200, 110, 175, 100, 88)

    def __init__(self, parent, db: Database, show_toast):
        super().__init__(parent, fg_color="transparent")
        self.db         = db
        self.show_toast = show_toast
        self._selected  = None
        self._build()
        self._load()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(30, 0))

        ctk.CTkLabel(top, text="Manage Students", font=FONT_HEADING,
                     text_color=COLORS["text_primary"]).pack(side="left")

        ctk.CTkButton(top, text="＋  Add Student", command=self._open_add,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_dim"],
                      text_color="#ffffff", corner_radius=8, font=FONT_NAV,
                      height=40, width=150).pack(side="right")

        Divider(self).pack(fill="x", padx=30, pady=(14, 0))

        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=12)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._load())
        search_entry = ctk.CTkEntry(
            bar, textvariable=self.search_var,
            placeholder_text="🔍  Search by name, ID, or course…",
            fg_color=COLORS["bg_card"], border_color=COLORS["border"],
            text_color=COLORS["text_primary"], height=40, corner_radius=8, width=340,
        )
        search_entry.pack(side="left")

        ctk.CTkLabel(bar, text="Filter:", font=FONT_SMALL,
                     text_color=COLORS["text_muted"]).pack(side="left", padx=(20, 6))
        self.filter_var = ctk.StringVar(value="All")
        for opt in ["All", "Active", "Graduated", "Suspended"]:
            ctk.CTkRadioButton(
                bar, text=opt, variable=self.filter_var, value=opt,
                command=self._load, font=FONT_SMALL,
                text_color=COLORS["text_secondary"],
                fg_color=COLORS["accent"], hover_color=COLORS["accent_dim"],
            ).pack(side="left", padx=6)

        self.lbl_count = ctk.CTkLabel(bar, text="", font=FONT_SMALL,
                                      text_color=COLORS["text_muted"])
        self.lbl_count.pack(side="right")

        tree_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], corner_radius=14)
        tree_frame.pack(fill="both", expand=True, padx=30, pady=(0, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("SMS.Treeview",
                         background=COLORS["bg_card"],
                         foreground=COLORS["text_primary"],
                         fieldbackground=COLORS["bg_card"],
                         bordercolor=COLORS["border"],
                         rowheight=42,
                         font=("Helvetica Neue", 12))
        style.configure("SMS.Treeview.Heading",
                         background=COLORS["bg_secondary"],
                         foreground=COLORS["text_secondary"],
                         relief="flat",
                         font=("Helvetica Neue", 11, "bold"))
        style.map("SMS.Treeview",
                  background=[("selected", COLORS["active_nav"])],
                  foreground=[("selected", COLORS["text_primary"])])
        style.layout("SMS.Treeview", [("SMS.Treeview.treearea", {"sticky": "nswe"})])

        self.tree = ttk.Treeview(
            tree_frame,
            columns=self.COL_IDS,
            show="headings",
            style="SMS.Treeview",
            selectmode="browse",
        )
        for cid, head, w in zip(self.COL_IDS, self.COL_HEADS, self.COL_WIDTHS):
            self.tree.heading(cid, text=head)
            self.tree.column(cid, width=w, minwidth=60, anchor="w")

        self.tree.tag_configure("alt",    background=COLORS["row_alt"])
        self.tree.tag_configure("Active", foreground=COLORS["emerald"])
        self.tree.tag_configure("Graduated", foreground=COLORS["amber"])
        self.tree.tag_configure("Suspended", foreground=COLORS["rose"])

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>",         self._open_edit)

        action = ctk.CTkFrame(self, fg_color="transparent")
        action.pack(fill="x", padx=30, pady=(0, 20))

        self.btn_edit = ctk.CTkButton(
            action, text="✏  Edit Selected", command=self._open_edit,
            fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_secondary"], border_color=COLORS["border"],
            border_width=1, corner_radius=8, font=FONT_BODY, height=38, state="disabled"
        )
        self.btn_edit.pack(side="left", padx=(0, 10))

        self.btn_delete = ctk.CTkButton(
            action, text="🗑  Delete Selected", command=self._delete,
            fg_color=COLORS["bg_card"], hover_color=COLORS["error_bg"],
            text_color=COLORS["rose"], border_color=COLORS["border"],
            border_width=1, corner_radius=8, font=FONT_BODY, height=38, state="disabled"
        )
        self.btn_delete.pack(side="left")

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        search = self.search_var.get().strip()
        f_status = self.filter_var.get()

        students = self.db.get_all_students(search)
        count = 0

        for idx, s in enumerate(students):
            if f_status != "All" and s["status"] != f_status:
                continue

            tags = (s["status"],)
            if idx % 2 == 1:
                tags = tags + ("alt",)

            self.tree.insert("", "end", iid=s["student_id"], values=(
                s["student_id"], s["full_name"], s["email"], s["phone"],
                s["course"], s["enrolled_date"], s["status"]
            ), tags=tags)
            count += 1

        self.lbl_count.configure(text=f"Showing {count} entries")
        self._clear_selection()

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if sel:
            self._selected = sel[0]
            self.btn_edit.configure(state="normal", text_color=COLORS["text_primary"])
            self.btn_delete.configure(state="normal")
        else:
            self._clear_selection()

    def _clear_selection(self):
        self._selected = None
        self.btn_edit.configure(state="disabled", text_color=COLORS["text_secondary"])
        self.btn_delete.configure(state="disabled")

    def _open_add(self):
        StudentFormDialog(self.winfo_toplevel(), self.db, on_save=self._on_save_success)

    def _open_edit(self, _=None):
        if not self._selected:
            return
        student = self.db.get_student_by_id(self._selected)
        if student:
            StudentFormDialog(self.winfo_toplevel(), self.db, on_save=self._on_save_success, student=student)

    def _delete(self):
        if not self._selected:
            return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to completely remove record {self._selected}?"):
            self.db.delete_student(self._selected)
            self.show_toast(f"Record {self._selected} successfully deleted.", "success")
            self._load()

    def _on_save_success(self):
        self.show_toast("Student data recorded successfully.", "success")
        self._load()

    def refresh(self):
        self._load()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION ROOT
# ══════════════════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    """Main window and navigation controller initialized with custom university values."""

    def __init__(self):
        super().__init__()
        self.db = Database()

        # Window properties
        self.title(f"{self.db.get_setting('univ_name')} — SMS Pro")
        self.geometry("1280x740")
        self.minimum_size = (1100, 640)
        self.configure(fg_color=COLORS["bg_primary"])

        self._build_layout()
        self.show_view("Dashboard")

    def _build_layout(self):
        # Sidebar Panel
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Dynamic Institutional Branding
        univ_acronym = self.db.get_setting("univ_acronym", "MGAHV")
        univ_type = self.db.get_setting("univ_type", "Central University")

        brand_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_f.pack(fill="x", padx=24, pady=28)
        ctk.CTkLabel(brand_f, text=f"🎓  {univ_acronym} SMS", font=FONT_HEADING,
                     text_color=COLORS["text_primary"]).pack(anchor="w")
        ctk.CTkLabel(brand_f, text=univ_type, font=FONT_SMALL,
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=4)

        Divider(self.sidebar).pack(fill="x", padx=16, pady=(0, 20))

        # Main Workspace Container
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.pack(side="right", fill="both", expand=True)

        # Construct System Views
        self.views = {
            "Dashboard": DashboardView(self.view_container, self.db),
            "Manage Students": ManageStudentsView(self.view_container, self.db, self.show_toast),
            "Settings": ctk.CTkLabel(
                self.view_container, 
                text=f"⚙️ {self.db.get_setting('univ_name')} Configuration Menu Profile\nLocation: {self.db.get_setting('univ_location')}\nEstablished: {self.db.get_setting('univ_established')}", 
                font=FONT_SUBHEAD, text_color=COLORS["text_secondary"]
            ),
        }

        # Setup Menu Buttons
        self.nav_buttons = {}
        for icon, name in NAV_ITEMS:
            btn = ctk.CTkButton(
                self.sidebar, text=f"   {icon}     {name}", font=FONT_NAV,
                anchor="w", height=46, corner_radius=10,
                fg_color="transparent", text_color=COLORS["text_secondary"],
                hover_color=COLORS["bg_hover"],
                command=lambda n=name: self.show_view(n)
            )
            btn.pack(fill="x", padx=14, pady=3)
            self.nav_buttons[name] = btn

    def show_view(self, target_view_name: str):
        """Switches visibility context among UI sub-frames."""
        for name, view in self.views.items():
            if name == target_view_name:
                view.pack(fill="both", expand=True)
                if hasattr(view, "refresh"):
                    view.refresh()
                self.nav_buttons[name].configure(fg_color=COLORS["active_nav"], text_color=COLORS["text_primary"])
            else:
                view.pack_forget()
                self.nav_buttons[name].configure(fg_color="transparent", text_color=COLORS["text_secondary"])

    def show_toast(self, message: str, kind: str = "success"):
        Toast(self, message, kind)


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()