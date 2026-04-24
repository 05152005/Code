import sys
import sqlite3
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

# ===== DATABASE PATH =====
DB_PATH = os.path.join(os.path.dirname(__file__), "people.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            purpose TEXT,
            document TEXT,
            datetime TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM people")
    if cursor.fetchone()[0] == 0:
        sample = [
            ("Cyrill", "09123456789", "Cedula", "Cedula", "2026-01-01"),
            ("Maria", "09987654321", "Job", "Brgy ID", "2026-01-02"),
            ("Juan", "09876543210", "Permit", "Permit", "2026-01-03"),
        ]
        cursor.executemany("""
            INSERT INTO people (name, contact, purpose, document, datetime)
            VALUES (?, ?, ?, ?, ?)
        """, sample)

    conn.commit()
    conn.close()


class DashboardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KLIK Admin Dashboard")
        self.setFixedSize(1100, 650)

        # 🔥 FIXED GLOBAL STYLE
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                background-color: #dcdfe3;
                color: black;
            }

            QLineEdit {
                background-color: white;
                color: black;
                padding: 5px;
                border-radius: 4px;
            }
        """)

        main_layout = QVBoxLayout()

        container = QWidget()
        container.setStyleSheet("background:#f1f3f5;border-radius:12px;")
        container_layout = QVBoxLayout()

        # HEADER
        header = QLabel("K L I K")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(55)
        header.setStyleSheet("background:#0d3b66;color:white;font-size:20px;")

        # TITLE
        top_title = QLabel("Admin Dashboard")
        top_title.setAlignment(Qt.AlignCenter)
        top_title.setFixedHeight(45)
        top_title.setStyleSheet("background:#e5e7eb;font-weight:bold;")

        # BODY
        body = QHBoxLayout()

        # SIDEBAR
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(190)
        sidebar_widget.setStyleSheet("background:#0d3b66;border-radius:8px;")

        sidebar = QVBoxLayout()

        self.dashboard_btn = QPushButton("  Dashboard")
        self.dashboard_btn.setFixedHeight(38)
        self.dashboard_btn.setIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.dashboard_btn.setIconSize(QSize(18, 18))
        self.dashboard_btn.setCheckable(True)

        self.dashboard_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                text-align: left;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1d5fa7;
            }
            QPushButton:checked {
                background-color: #2f6db3;
            }
        """)

        self.dashboard_btn.clicked.connect(self.show_dashboard)

        sidebar.addWidget(self.dashboard_btn)
        sidebar.addStretch()

        footer = QLabel("You're logged in as admin")
        footer.setStyleSheet("color:#adb5bd;font-size:10px;")
        sidebar.addWidget(footer)

        sidebar_widget.setLayout(sidebar)

        # STACK
        self.stack = QStackedWidget()
        self.stack.addWidget(QWidget())
        self.stack.addWidget(self.create_dashboard())

        body.addWidget(sidebar_widget)
        body.addWidget(self.stack)

        container_layout.addWidget(header)
        container_layout.addWidget(top_title)
        container_layout.addLayout(body)

        container.setLayout(container_layout)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def show_dashboard(self):
        self.stack.setCurrentIndex(1)
        self.dashboard_btn.setChecked(True)
        self.load_data()

    def create_dashboard(self):
        widget = QWidget()
        widget.setStyleSheet("background:#f1f3f5;")

        layout = QVBoxLayout()

        top_bar = QLabel()
        top_bar.setFixedHeight(40)
        top_bar.setStyleSheet("background:#0d3b66;border-radius:4px;")
        layout.addWidget(top_bar)

        box = QFrame()
        box.setStyleSheet("background:white;border-radius:8px;")
        box_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "🗑", "ID", "Name", "Contact", "Purpose", "Document", "Date & Time"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 🔥 FIXED HEADER STYLE
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #0d3b66;
                color: white;
                padding: 5px;
                border: none;
            }
        """)

        self.table.setAlternatingRowColors(True)

        box_layout.addWidget(self.table)
        box.setLayout(box_layout)

        layout.addWidget(box)
        widget.setLayout(layout)

        return widget

    def load_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            record_id = row[0]

            btn = QPushButton("🗑")
            btn.setStyleSheet("border:none;")
            btn.clicked.connect(lambda _, r=record_id: self.delete_row(r))
            self.table.setCellWidget(i, 0, btn)

            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j + 1, item)

    def delete_row(self, record_id):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Delete")
        msg.setText("Are you sure you want to delete this row?")

        delete_btn = msg.addButton("Delete", QMessageBox.AcceptRole)
        msg.addButton("Cancel", QMessageBox.RejectRole)

        msg.exec()

        if msg.clickedButton() == delete_btn:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM people WHERE id=?", (record_id,))
            conn.commit()
            conn.close()

            self.load_data()


# RUN
if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    window = DashboardUI()
    window.show()
    sys.exit(app.exec())