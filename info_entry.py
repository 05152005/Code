import sys
import sqlite3
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

DB_PATH = os.path.join(os.path.dirname(__file__), "people.db")


class CedulaUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cedula")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #dcdfe3;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # HEADER
        header = QLabel("K L I K")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background-color: #0d3b66;
            color: white;
            font-size: 20px;
            letter-spacing: 8px;
        """)

        # MAIN CARD
        card = QFrame()
        card.setStyleSheet("background:#f1f3f5;border-radius:12px;")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 10, 20, 10)

        # TOP BAR
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("background:#0d3b66;border-radius:8px;")

        top_layout = QVBoxLayout()

        title_main = QLabel("Request For Cedula")
        title_main.setAlignment(Qt.AlignCenter)
        title_main.setStyleSheet("color:white;font-size:16px;font-weight:bold;")

        title_sub = QLabel("(Community Tax Certificate)")
        title_sub.setAlignment(Qt.AlignCenter)
        title_sub.setStyleSheet("color:#dbeafe;font-size:11px;font-weight:bold;")

        top_layout.addWidget(title_main)
        top_layout.addWidget(title_sub)
        top_bar.setLayout(top_layout)

        # ===== REQUIREMENTS (FIXED ALIGNMENT) =====
        req_title = QLabel("Requirements:")
        req_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: black;
        """)

        req_list = QLabel(
            "• Valid Government ID\n"
            "• Proof of Residency (Barangay Certificate or ID)\n"
            "• Taxpayer Information / Income Details\n"
            "• Age 18 years old and above\n"
            "• Personal Appearance\n"
            "• Payment Fee"
        )

        req_list.setStyleSheet("""
            font-family: sans-serif;
            font-weight: bold;
            font-size: 14px;
            color: black;
            margin-left: 25px;
        """)
        req_list.setAlignment(Qt.AlignLeft)

        req_container = QVBoxLayout()
        req_container.setAlignment(Qt.AlignLeft)
        req_container.setContentsMargins(30, 0, 0, 0)

        req_container.addWidget(req_title)
        req_container.addWidget(req_list)

        # FORM CARD
        form_card = QFrame()
        form_card.setFixedWidth(400)
        form_card.setStyleSheet("background:#0d3b66;border-radius:12px;")

        form_layout = QVBoxLayout()

        form_title = QLabel("Please Fill the Details Below")
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setStyleSheet("color:white;font-size:13px;font-weight:bold;")

        label_style = "color:white;font-size:11px;"

        input_style = """
            QLineEdit {
                background-color: white;
                color: black;
                border-radius: 6px;
                padding: 5px;
                font-size: 11px;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """

        # INPUTS
        name_label = QLabel("Full Name")
        name_label.setStyleSheet(label_style)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Juan Dela Cruz")
        self.name.setStyleSheet(input_style)

        contact_label = QLabel("Contact Number")
        contact_label.setStyleSheet(label_style)
        self.contact = QLineEdit()
        self.contact.setPlaceholderText("09XX XXX XXXX")
        self.contact.setStyleSheet(input_style)

        purpose_label = QLabel("Purpose")
        purpose_label.setStyleSheet(label_style)
        self.purpose = QLineEdit()
        self.purpose.setPlaceholderText("Application for Cedula")
        self.purpose.setStyleSheet(input_style)

        # BUTTON
        btn = QPushButton("Enter Details and Print")
        btn.setFixedHeight(35)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2f6db3;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
        """)
        btn.clicked.connect(self.save_data)

        # ADD FORM
        form_layout.addWidget(form_title)
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name)
        form_layout.addWidget(contact_label)
        form_layout.addWidget(self.contact)
        form_layout.addWidget(purpose_label)
        form_layout.addWidget(self.purpose)
        form_layout.addWidget(btn)

        form_card.setLayout(form_layout)

        # CENTER FORM
        form_container = QHBoxLayout()
        form_container.addStretch()
        form_container.addWidget(form_card)
        form_container.addStretch()

        # FOOTER
        footer = QLabel("Next Step: Proceed to Barangay Treasurer’s Office ➡")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size:11px;color:black;")

        # ADD TO CARD
        card_layout.addWidget(top_bar)
        card_layout.addLayout(req_container)
        card_layout.addLayout(form_container)
        card_layout.addWidget(footer)

        card.setLayout(card_layout)

        main_layout.addWidget(header)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    def save_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO people (name, contact, purpose, document, datetime)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (
            self.name.text(),
            self.contact.text(),
            self.purpose.text(),
            "Cedula"
        ))

        conn.commit()
        conn.close()

        msg = QMessageBox(self)
        msg.setWindowTitle("Saved")
        msg.setText("Data saved successfully!")
        msg.setStyleSheet("""
            QMessageBox { background-color: white; }
            QLabel { color: black; font-size: 12px; }
            QPushButton {
                background-color: #2f6db3;
                color: white;
                padding: 5px 15px;
                border-radius: 6px;
            }
        """)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CedulaUI()
    window.show()
    sys.exit(app.exec())