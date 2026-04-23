import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize


class DashboardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KLIK Admin Dashboard")
        self.setFixedSize(1100, 650)

        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                background-color: #dcdfe3;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)

        # ===== CONTAINER =====
        container = QWidget()
        container.setStyleSheet("""
            background-color: #f1f3f5;
            border-radius: 12px;
        """)

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)

        # ===== HEADER =====
        header = QLabel("K L I K")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(55)
        header.setStyleSheet("""
            background-color: #0d3b66;
            color: white;
            font-size: 20px;
            letter-spacing: 8px;
        """)

        # ===== TITLE =====
        top_title = QLabel("Admin Dashboard")
        top_title.setAlignment(Qt.AlignCenter)
        top_title.setFixedHeight(45)
        top_title.setStyleSheet("""
            background-color: #e5e7eb;
            font-size: 16px;
            font-weight: bold;
        """)

        # ===== BODY =====
        body = QHBoxLayout()
        body.setContentsMargins(15, 10, 15, 10)

        # ===== SIDEBAR =====
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(190)
        sidebar_widget.setStyleSheet("""
            background-color: #0d3b66;
            border-radius: 8px;
        """)

        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(10, 15, 10, 15)
        sidebar.setSpacing(8)

        style = self.style()

        # BUTTON (clickable)
        self.dashboard_btn = QPushButton("  Dashboard")
        self.dashboard_btn.setFixedHeight(38)
        self.dashboard_btn.setIcon(style.standardIcon(QStyle.SP_DesktopIcon))
        self.dashboard_btn.setIconSize(QSize(18, 18))
        self.dashboard_btn.setStyleSheet(self.inactive_style())

        self.dashboard_btn.clicked.connect(self.show_dashboard)

        sidebar.addWidget(self.dashboard_btn)
        sidebar.addStretch()

        footer = QLabel("You're logged in as admin")
        footer.setStyleSheet("color: #adb5bd; font-size: 10px;")
        sidebar.addWidget(footer)

        sidebar_widget.setLayout(sidebar)

        # ===== STACK =====
        self.stack = QStackedWidget()

        # BLANK PAGE FIRST
        self.blank_page = QWidget()
        self.stack.addWidget(self.blank_page)

        # DASHBOARD PAGE
        self.dashboard_page_widget = self.create_dashboard()
        self.stack.addWidget(self.dashboard_page_widget)

        # ===== COMBINE =====
        body.addWidget(sidebar_widget)
        body.addWidget(self.stack)

        container_layout.addWidget(header)
        container_layout.addWidget(top_title)
        container_layout.addLayout(body)

        container.setLayout(container_layout)
        main_layout.addWidget(container)

        self.setLayout(main_layout)

    # ===== STYLES =====
    def active_style(self):
        return """
            QPushButton {
                background-color: #2f6db3;
                color: white;
                text-align: left;
                border-radius: 6px;
            }
        """

    def inactive_style(self):
        return """
            QPushButton {
                color: white;
                text-align: left;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #1d5fa7;
                border-radius: 6px;
            }
        """

    # ===== CLICK EVENT =====
    def show_dashboard(self):
        self.stack.setCurrentIndex(1)
        self.dashboard_btn.setStyleSheet(self.active_style())

    # ===== DASHBOARD =====
    def create_dashboard(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # BLUE BAR
        top_bar = QLabel()
        top_bar.setFixedHeight(40)
        top_bar.setStyleSheet("background-color: #0d3b66; border-radius: 4px;")
        layout.addWidget(top_bar)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "🗑", "ID", "Name", "Contact", "Purpose", "Document", "Date & Time"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # ===== 15+ DATA =====
        data = [
            ("1", "Cyrill", "09123456789", "Cedula", "Cedula", "2026-01-01"),
            ("2", "Maria", "09987654321", "Job", "Brgy ID", "2026-01-02"),
            ("3", "Juan", "09876543210", "Permit", "Permit", "2026-01-03"),
            ("4", "Ana", "09111111111", "School", "ID", "2026-01-04"),
            ("5", "Pedro", "09222222222", "Loan", "Docs", "2026-01-05"),
            ("6", "Luis", "09333333333", "Travel", "Passport", "2026-01-06"),
            ("7", "Mark", "09444444444", "Work", "Resume", "2026-01-07"),
            ("8", "Liza", "09555555555", "Health", "Med Cert", "2026-01-08"),
            ("9", "Paul", "09666666666", "Permit", "Permit", "2026-01-09"),
            ("10", "Rina", "09777777777", "School", "Form", "2026-01-10"),
            ("11", "Tom", "09888888888", "Job", "ID", "2026-01-11"),
            ("12", "Ella", "09999999999", "Cedula", "Cedula", "2026-01-12"),
            ("13", "Noah", "09121212121", "Travel", "Visa", "2026-01-13"),
            ("14", "Mia", "09232323232", "Work", "Contract", "2026-01-14"),
            ("15", "Leo", "09343434343", "Permit", "Permit", "2026-01-15"),
        ]

        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            btn = QPushButton("🗑")
            btn.setStyleSheet("border: none;")
            btn.clicked.connect(lambda _, r=row: self.delete_row(r))
            self.table.setCellWidget(row, 0, btn)

            for col, val in enumerate(item):
                self.table.setItem(row, col + 1, QTableWidgetItem(val))

        layout.addWidget(self.table)

        widget.setLayout(layout)
        return widget

    # ===== DELETE =====
    def delete_row(self, row):
        self.table.removeRow(row)


# ===== RUN =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardUI()
    window.show()
    sys.exit(app.exec_())