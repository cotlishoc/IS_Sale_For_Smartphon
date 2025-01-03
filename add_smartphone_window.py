from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QHBoxLayout, QComboBox, QInputDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QByteArray, QBuffer
from model import db

class AddSmartphoneWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить смартфон")
        self.setFixedSize(400, 600)
        self.photos = []
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для ввода артикула
        layout.addWidget(QLabel("Артикул"))
        self.article_input = QLineEdit()
        layout.addWidget(self.article_input)

        # Поле для выбора бренда
        layout.addLayout(self.create_brand_selection_layout())

        # Поле для ввода модели
        layout.addWidget(QLabel("Модель"))
        self.model_input = QLineEdit()
        layout.addWidget(self.model_input)

        # Поле для ввода описания
        layout.addWidget(QLabel("Описание"))
        self.description_input = QTextEdit()
        layout.addWidget(self.description_input)

        photo_button = QPushButton("Загрузить фотографии")
        photo_button.clicked.connect(self.upload_photos)
        layout.addWidget(photo_button)

        layout.addWidget(QLabel("Наличие"))
        self.stock_input = QLineEdit()
        layout.addWidget(self.stock_input)

        layout.addWidget(QLabel("Цена"))
        self.price_input = QLineEdit()
        layout.addWidget(self.price_input)

        layout.addLayout(self.create_action_buttons_layout())

        self.setLayout(layout)

    def create_brand_selection_layout(self):
        brand_layout = QHBoxLayout()

        # Метка и выпадающий список для бренда
        brand_layout.addWidget(QLabel("Бренд"))
        self.brand_input = QComboBox()
        self.load_brands()
        brand_layout.addWidget(self.brand_input)

        # Кнопка добавления нового бренда
        add_brand_button = QPushButton("+")
        add_brand_button.setFixedSize(30, 30)
        add_brand_button.clicked.connect(self.add_new_brand)
        brand_layout.addWidget(add_brand_button)

        return brand_layout

    def create_action_buttons_layout(self):
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_smartphone)
        button_layout.addWidget(self.save_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        return button_layout

    def load_brands(self):
        # Загрузка списка брендов из базы данных
        brands = db.fetch_query('SELECT `name` FROM `brand`')
        self.brand_input.clear()
        self.brand_input.addItems([brand[0] for brand in brands])

    def add_new_brand(self):
        # Добавление нового бренда
        brand_name, ok = QInputDialog.getText(self, "Добавить бренд", "Введите название бренда:")
        if ok and brand_name.strip():
            db.execute_query('INSERT INTO `brand` (`name`) VALUES (%s)', (brand_name.strip(),))
            db.commit()
            self.load_brands()
            self.brand_input.setCurrentText(brand_name.strip())

    def save_smartphone(self, smartphone_id=None):
        try:
            # Получение данных из формы
            brand_name = self.brand_input.currentText()
            brand_id = db.fetch_query('SELECT `brand_id` FROM `brand` WHERE `name` = %s', (brand_name,))[0][0]

            article = self.article_input.text().strip()
            model = self.model_input.text().strip()
            price = float(self.price_input.text())
            description = self.description_input.toPlainText().strip()
            stock = int(self.stock_input.text())

            if smartphone_id:  # Редактирование существующего смартфона
                db.execute_query(
                    'UPDATE `smartphone` SET `article` = %s, `model` = %s, `price` = %s, `brand_id` = %s, `characteristic` = %s, `in_stock` = %s WHERE `smartphone_id` = %s',
                    (article, model, price, brand_id, description, stock, smartphone_id)
                )
                self.save_photos(smartphone_id, is_editing=True)
                QMessageBox.information(self, "Успех", "Смартфон успешно обновлен.")
            else:  # Добавление нового смартфона
                db.execute_query(
                    'INSERT INTO `smartphone` (`article`, `model`, `price`, `brand_id`, `characteristic`, `in_stock`) VALUES (%s, %s, %s, %s, %s, %s)',
                    (article, model, price, brand_id, description, stock)
                )
                # Получаем ID добавленного смартфона
                smartphone_id = db.fetch_query('SELECT LAST_INSERT_ID()')[0][0]

                self.save_photos(smartphone_id)

                QMessageBox.information(self, "Успех", "Смартфон успешно добавлен.")

            db.commit()
            self.accept()  # Закрытие окна
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить смартфон: {str(e)}")


        

    def upload_photos(self):
        # Функция загрузки фотографий
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Выбрать фотографии", "", "Images (*.png *.xpm *.jpg)")

        if file_paths:
            if not hasattr(self, 'photos'):
                self.photos = []  # Инициализация списка фотографий, если его нет
            for path in file_paths:
                # Конвертируем изображение в формат BLOB
                image = QImage(path)
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                image.save(buffer, "PNG")
                self.photos.append(byte_array)  # Добавляем изображение в список

            # Обновляем текст кнопки
            photo_count = len(self.photos)
            self.sender().setText(f"Добавлена {photo_count} фотография" if photo_count == 1 else f"Добавлено {photo_count} фотографий")

            QMessageBox.information(self, "Фотографии загружены", "Фотографии успешно загружены.")
            
    def save_photos(self, smartphone_id, is_editing=False):
        if not hasattr(self, 'photos') or not self.photos:
            # Если фотографий нет, ничего не делаем
            return

        if is_editing:
            # Удаляем старые фотографии, связанные с этим смартфоном
            db.execute_query('DELETE FROM `photosmartphone` WHERE `smartphone_id` = %s', (smartphone_id,))
            db.commit()

        # Сохраняем новые фотографии в базу данных
        for photo in self.photos:
            photo_data = bytes(photo)  # Преобразуем QByteArray в bytes

            # Сохраняем фото как BLOB в таблицу `photo`
            db.execute_query('INSERT INTO `photo` (`photo`) VALUES (%s)', (photo_data,))
            
            # Получаем ID вставленной фотографии
            photo_id = db.fetch_query('SELECT LAST_INSERT_ID()')[0][0]

            # Связываем фотографию с конкретным смартфоном
            db.execute_query('INSERT INTO `photosmartphone` (`smartphone_id`, `photo_id`) VALUES (%s, %s)', (smartphone_id, photo_id))
            
        db.commit()
            
        db.commit()

            
        db.commit()


