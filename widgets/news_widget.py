# widgets/news_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from services.news_fetcher import NewsFetcher

class NewsWidget(QWidget):
    def __init__(self, game_name=""):
        super().__init__()
        self.game_name = game_name
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.title_label = QLabel("Новости игры")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.news_list = QListWidget()
        self.news_list.itemClicked.connect(self.open_news)
        layout.addWidget(self.title_label)
        layout.addWidget(self.news_list)

    def set_game(self, game_name):
        self.game_name = game_name
        self.title_label.setText(f"Новости {game_name}")
        self.news_list.clear()
        news_items = NewsFetcher.fetch_news(game_name)
        if not news_items:
            self.news_list.addItem("Нет новостей")
        else:
            for item in news_items:
                list_item = QListWidgetItem(item["title"])
                list_item.setData(Qt.ItemDataRole.UserRole, item["link"])
                self.news_list.addItem(list_item)

    def open_news(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            QDesktopServices.openUrl(QUrl(url))