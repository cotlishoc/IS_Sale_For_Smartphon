from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QHBoxLayout

class AddSmartphoneWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить смартфон")
        self.setFixedSize(400, 600)

        layout = QVBoxLayout()

        # Артикул
        article_label = QLabel("Артикул")
        self.article_input = QLineEdit()
        layout.addWidget(article_label)
        layout.addWidget(self.article_input)

        # Модель
        model_label = QLabel("Модель")
        self.model_input = QLineEdit()
        layout.addWidget(model_label)
        layout.addWidget(self.model_input)

        # Описание
        description_label = QLabel("Описание")
        self.description_input = QTextEdit()
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)

        # Загрузить фотографии
        photo_button = QPushButton("Загрузить фотографии")
        photo_button.clicked.connect(self.upload_photos)
        layout.addWidget(photo_button)

        # Наличие
        stock_label = QLabel("Наличие")
        self.stock_input = QLineEdit()
        layout.addWidget(stock_label)
        layout.addWidget(self.stock_input)

        # Цена
        price_label = QLabel("Цена")
        self.price_input = QLineEdit()
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)

        # Кнопки Сохранить и Отмена
        button_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def upload_photos(self):
        # Функция загрузки фотографий
        QFileDialog.getOpenFileName(self, "Выбрать фотографии", "", "Images (*.png *.xpm *.jpg)")

