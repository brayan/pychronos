import sys

from PyQt5.QtWidgets import QApplication

from pychronos.ui import ChronosWindow


def main():
    app = QApplication(sys.argv)
    window = ChronosWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
