import os
import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.mash = 0.005
        self.l1 = None
        self.l2 = None
        self.map_file = "map.png"

        self.init_ui()
        self.set_image(self.mash)

    def set_image(self, mash: float = 0.02, l1: float = 37.530887, l2: float = 55.703118):
        m = f'{mash},{mash}'

        self.l1 = l1
        self.l2 = l2

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.l1},{self.l2}&spn={m}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def update_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        self.image.show()

    def init_ui(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.update_image()

    def close_event(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        clicked = False

        if event.key() == Qt.Key.Key_A or event.key() == Qt.Key.Key_Left:
            self.l1 -= self.l1 / 1000
            clicked = True
        elif event.key() == Qt.Key.Key_S or event.key() == Qt.Key.Key_Down:
            self.l2 += self.l1 / 1000
            clicked = True
        if clicked:
            self.set_image(self.mash, self.l1, self.l2)
            self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec())
