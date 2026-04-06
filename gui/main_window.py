from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QSizePolicy, QFrame, QButtonGroup
)
from PySide6.QtGui import QGuiApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RF & Acoustic Analyser")
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)

        # MAIN LAYOUT
        self.main_layout = QHBoxLayout(central)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= LEFT PANEL =================
        self.left_panel = QFrame()
        self.left_panel.setObjectName("sidePanel")
        self.left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(10, 10, 10, 10)

        self.left_inner = QWidget()
        self.left_inner.setObjectName("innerPanel")
        self.left_inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        left_layout.addWidget(self.left_inner)

        # ================= CENTER =================
        self.center_container = QWidget()
        self.center_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        center_layout = QVBoxLayout(self.center_container)
        center_layout.setSpacing(0)
        center_layout.setContentsMargins(0, 0, 0, 0)

        # TOP BAR
        top_bar = QHBoxLayout()
        top_bar.setSpacing(0)
        top_bar.setContentsMargins(0, 0, 0, 0)

        top_bar.addStretch()

        self.rf_btn = QPushButton("RF")
        self.acoustic_btn = QPushButton("Acoustic")

        for b in (self.rf_btn, self.acoustic_btn):
            b.setMinimumWidth(120)
            b.setCheckable(True)

        self.rf_btn.setChecked(True)

        # BUTTON GROUP (exclusive)
        self.group = QButtonGroup()
        self.group.setExclusive(True)
        self.group.addButton(self.rf_btn)
        self.group.addButton(self.acoustic_btn)

        top_bar.addWidget(self.rf_btn)
        top_bar.addWidget(self.acoustic_btn)

        top_bar.addStretch()

        # CENTER STACK
        self.center_stack = QStackedWidget()
        self.center_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.center_rf = QWidget()
        self.center_rf.setObjectName("centerPanel")

        self.center_acoustic = QWidget()
        self.center_acoustic.setObjectName("centerPanel")

        self.center_stack.addWidget(self.center_rf)
        self.center_stack.addWidget(self.center_acoustic)

        center_layout.addLayout(top_bar)
        center_layout.addWidget(self.center_stack)

        # ================= RIGHT PANEL =================
        self.right_panel = QFrame()
        self.right_panel.setObjectName("sidePanel")
        self.right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(10, 10, 10, 10)

        self.right_inner = QWidget()
        self.right_inner.setObjectName("innerPanel")
        self.right_inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        right_layout.addWidget(self.right_inner)

        # ================= ADD =================
        self.main_layout.addWidget(self.left_panel)
        self.main_layout.addWidget(self.center_container)
        self.main_layout.addWidget(self.right_panel)

        # ================= LOGIC =================
        def select_tab(index):
            self.center_stack.setCurrentIndex(index)
            self.rf_btn.setChecked(index == 0)
            self.acoustic_btn.setChecked(index == 1)

        self.rf_btn.clicked.connect(lambda: select_tab(0))
        self.acoustic_btn.clicked.connect(lambda: select_tab(1))

        # INITIAL RESPONSIVE SETUP
        self.apply_responsive_layout()

    # ================= RESPONSIVE =================
    def apply_responsive_layout(self):
        width = self.width()

        if width <= 800:
            # SMALL (Raspberry Pi)
            self.left_panel.hide()
            self.right_panel.hide()

            self.main_layout.setStretch(0, 0)
            self.main_layout.setStretch(1, 1)
            self.main_layout.setStretch(2, 0)

        else:
            # MEDIUM + LARGE → 1:7:1
            self.left_panel.show()
            self.right_panel.show()

            self.main_layout.setStretch(0, 1)
            self.main_layout.setStretch(1, 7)
            self.main_layout.setStretch(2, 1)

    def resizeEvent(self, event):
        self.apply_responsive_layout()
        super().resizeEvent(event)


def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    app.setStyleSheet("""
    QWidget {
        background-color: #121212;
        color: #E0E0E0;
    }

    QPushButton {
        background-color: #FFFFFF;
        color: #000000;
        padding: 8px 0px;
        border: none;
    }

    QPushButton:checked {
        background-color: #5A5A5A;
        color: #FFFFFF;
    }

    QPushButton:hover {
        background-color: #FFFFFF;
        color: #000000;
    }

    QPushButton:checked:hover {
        background-color: #5A5A5A;
        color: #FFFFFF;
    }

    #sidePanel {
        background-color: #5F5F5F;
    }

    #innerPanel {
        background-color: #CFCFCF;
        border-radius: 4px;
    }

    #centerPanel {
        background-color: #CFCFCF;
    }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()