from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSplitter,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QImage, QPixmap
from add_smartphone_window import AddSmartphoneWindow
from model import db
import uuid
from receipt import generate_receipt
from datetime import datetime
from report import ReportWidget

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SELL FOR SMARTPHONE')
        self.setMinimumSize(1200, 900)
        self.resize(1200, 900)

        self.setStyleSheet("""
            QPushButton { height: 50px; font-size: 16px; }
            QLabel { font-size: 52px; font-family: Arial; }
            QLineEdit { font-size: 16px; height: 50px; }
        """)

        self.catalog_button = QPushButton('Каталог')
        self.catalog_button.clicked.connect(self.show_catalog)
        
        self.client_button = QPushButton('Покупатели')
        self.client_button.clicked.connect(self.show_clients)
        
        self.cart_button = QPushButton('Корзина')
        self.cart_button.clicked.connect(self.show_cart)
        
        self.management_button = QPushButton('Управление')
        self.management_button.clicked.connect(self.show_management)
        
        self.sell_button = QPushButton('Продажи')
        self.sell_button.clicked.connect(self.show_sales)
        
        self.report_button = QPushButton('Отчет')
        self.report_button.clicked.connect(self.show_report)

        # Создание вертикального макета для кнопок
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.catalog_button)
        button_layout.addWidget(self.client_button)
        button_layout.addWidget(self.cart_button)
        button_layout.addWidget(self.management_button)
        button_layout.addWidget(self.sell_button)
        button_layout.addWidget(self.report_button)
        button_layout.addStretch()

        # Контейнер с кнопками разделов
        self.section_button_widget = QWidget()
        self.section_button_widget.setLayout(button_layout)
        self.section_button_widget.setFixedWidth(200)

        # Основной сплиттер для разделения кнопок разделов и содержимого
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.section_button_widget)

        # Инициализация текущего виджета содержимого
        self.content_widget = QWidget()
        self.main_splitter.addWidget(self.content_widget)
        self.main_splitter.setSizes([200, 1720])

        self.setCentralWidget(self.main_splitter)
        self.show_catalog()

    def show_report(self):
        report_widget = ReportWidget()
        self.replace_content_widget(report_widget)

    def show_catalog(self):
        catalog_layout = QHBoxLayout()

        left_container = QWidget()
        left_layout = QVBoxLayout()

        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        catalog_top_button = QLabel('Каталог')

        search_bar = QLineEdit()
        search_bar.setPlaceholderText('Поиск по каталогу...')

        def filter_catalog(text): 
            for row in range(table_widget_catalog.rowCount()): 
                match = False 
                for col in range(table_widget_catalog.columnCount()): 
                    item = table_widget_catalog.item(row, col) 
                    if item and text.lower() in item.text().lower(): 
                        match = True 
                        break 
                table_widget_catalog.setRowHidden(row, not match)

        search_bar.textChanged.connect(filter_catalog)

        top_layout.addWidget(catalog_top_button)
        top_layout.addWidget(search_bar)
        top_container.setLayout(top_layout)

        table_widget_catalog = QTableWidget()
        table_widget_catalog.setColumnCount(5)
        table_widget_catalog.setHorizontalHeaderLabels([
            'Название', 'Артикул', 'В наличии', 'Цена', 'pk'
        ])
        table_widget_catalog.setColumnHidden(4, True)
        table_widget_catalog.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget_catalog.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget_catalog.setEditTriggers(QTableWidget.NoEditTriggers)

        phones = db.fetch_query('SELECT `model`, `article`, `in_stock`, `price`, `smartphone_id` FROM `smartphone`')
        if phones:
            for row_data in phones:
                row_position = table_widget_catalog.rowCount()
                table_widget_catalog.insertRow(row_position)
                for col, value in enumerate(row_data):
                    table_widget_catalog.setItem(row_position, col, QTableWidgetItem(str(value)))

        left_layout.addWidget(top_container)
        left_layout.addWidget(table_widget_catalog)
        left_container.setLayout(left_layout)

        right_container = QWidget()
        right_container.setFixedWidth(400)
        right_layout = QVBoxLayout()

        title_label = QLabel('Название')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 42px;")
        right_layout.addWidget(title_label)

        title_to_photo_spacer = QWidget()
        title_to_photo_spacer.setFixedHeight(50)
        right_layout.addWidget(title_to_photo_spacer)

        photo_layout = QHBoxLayout()
        previous_photo_button = QPushButton('<')
        previous_photo_button.setFixedSize(50, 50)
        
        next_photo_button = QPushButton('>')
        next_photo_button.setFixedSize(50, 50)

        photo_placeholder = QLabel()
        photo_placeholder.setFixedSize(225, 225)
        photo_placeholder.setStyleSheet("border: 1px solid black;")
        photo_placeholder.setAlignment(Qt.AlignCenter)

        photo_layout.addWidget(previous_photo_button)
        photo_layout.addWidget(photo_placeholder)
        photo_layout.addWidget(next_photo_button)

        photo_container = QWidget()
        photo_container.setLayout(photo_layout)
        right_layout.addWidget(photo_container)

        price_label = QLabel('Цена')
        price_label.setAlignment(Qt.AlignLeft)
        price_label.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(price_label)

        price_value = QLabel('')
        price_value.setAlignment(Qt.AlignLeft)
        price_value.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(price_value)

        article_label = QLabel('Артикул')
        article_label.setAlignment(Qt.AlignLeft)
        article_label.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(article_label)

        article_value = QLabel('')
        article_value.setAlignment(Qt.AlignLeft)
        article_value.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(article_value)

        characteristics_label = QLabel('Описание характеристик')
        characteristics_label.setAlignment(Qt.AlignLeft)
        characteristics_label.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(characteristics_label)

        characteristics_value = QLabel('')
        characteristics_value.setAlignment(Qt.AlignLeft)
        characteristics_value.setStyleSheet("font-size: 20px;")
        right_layout.addWidget(characteristics_value)

        right_layout.addStretch()

        availability_label = QLabel('В наличии')
        availability_label.setAlignment(Qt.AlignLeft)
        availability_label.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(availability_label)

        availability_value = QLabel('')
        availability_value.setAlignment(Qt.AlignLeft)
        availability_value.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(availability_value)

        add_to_cart_button = QPushButton('В корзину')
        add_to_cart_button.setFixedHeight(50)
        add_to_cart_button.setStyleSheet("font-size: 24px;")
        right_layout.addWidget(add_to_cart_button)
        add_to_cart_button.clicked.connect(lambda: self.add_selected_to_cart(table_widget_catalog))

        right_container.setLayout(right_layout)

        catalog_layout.addWidget(left_container)
        catalog_layout.addWidget(right_container)

        new_content_widget = QWidget()
        new_content_layout = QVBoxLayout()
        new_content_widget.setLayout(new_content_layout)
        new_content_layout.addLayout(catalog_layout)

        self.replace_content_widget(new_content_widget)

                # отображения и переключения фотографий
        def display_photos(smartphone_id):
            photo_list = [] 
            current_index = 0 

            photos = db.fetch_query('''
                SELECT p.Photo 
                FROM Photo p
                JOIN PhotoSmartphone ps ON p.Photo_ID = ps.Photo_ID
                WHERE ps.Smartphone_ID = %s
            ''', (smartphone_id,))

            if photos:
                photo_list.extend([QImage.fromData(photo[0]) for photo in photos])

                def update_photo(): # Отображение текущей фотографии
                    photo_placeholder.setPixmap(QPixmap(photo_list[current_index]).scaled(225, 225, Qt.KeepAspectRatio))

                def show_next_photo():
                    nonlocal current_index
                    current_index = (current_index + 1) % len(photo_list)  # Переключаем по кругу
                    update_photo()

                def show_previous_photo():
                    nonlocal current_index
                    current_index = (current_index - 1) % len(photo_list)  # Переключаем по кругу
                    update_photo()
                update_photo()

                # Подключаем кнопки для переключения фотографий
                next_photo_button.setEnabled(True)
                previous_photo_button.setEnabled(True)
                next_photo_button.clicked.connect(show_next_photo)
                previous_photo_button.clicked.connect(show_previous_photo)
            else:
                photo_placeholder.setText('Нет фото')
                next_photo_button.setEnabled(False)
                previous_photo_button.setEnabled(False)

        def get_selected_id(): #получения выбранного смартфона и отображения его данных
            selected_row = table_widget_catalog.currentRow()
            
            if selected_row != -1:
                smartphone_id = table_widget_catalog.item(selected_row, 4).text()

                params = db.fetch_query('''
                    SELECT s.model, s.article, s.price, s.in_stock, s.characteristic 
                    FROM smartphone s 
                    WHERE s.smartphone_id = %s
                ''', (smartphone_id,))[0]

                title_label.setText(params[0]) 
                price_value.setText(f"{params[2]:.2f} ₽") 
                article_value.setText(params[1]) 
                characteristics_value.setText(params[4])  
                availability_value.setText(str(params[3]))

                display_photos(smartphone_id)

        table_widget_catalog.itemSelectionChanged.connect(get_selected_id)


    def add_selected_to_cart(self, table_widget_catalog):
        """Добавление выделенного смартфона в корзину"""
        try:
            selected_row = table_widget_catalog.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Ошибка", "Выберите смартфон для добавления в корзину.")
                return

            smartphone_id_item = table_widget_catalog.item(selected_row, 4) 
            if not smartphone_id_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID смартфона.")
                return

            smartphone_id = int(smartphone_id_item.text())

            self.add_to_cart(smartphone_id)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить добавление в корзину: {str(e)}")

    def add_to_cart(self, smartphone_id=None, quantity=1):
        """Добавление смартфона в корзину с учетом остатка in_stock"""
        try:
            if smartphone_id is None:
                QMessageBox.warning(self, "Ошибка", "Не выбран смартфон для добавления в корзину.")
                return

            smartphone_data = db.fetch_query(
                "SELECT in_stock, model FROM smartphone WHERE smartphone_id = %s",
                (smartphone_id,)
            )
            
            if not smartphone_data:
                QMessageBox.warning(self, "Ошибка", "Смартфон не найден.")
                return

            in_stock, model = smartphone_data[0]

            if in_stock < quantity:
                QMessageBox.warning(self,"Ошибка","Недостаточно товара на складе.")
                return

            cart_id = self.get_or_create_cart_id()
            if not cart_id:
                QMessageBox.critical(self, "Ошибка", "Не удалось создать корзину.")
                return

            existing_item = db.fetch_query(
                "SELECT quantity FROM cart_smartphone WHERE cart_id = %s AND smartphone_id = %s",
                (cart_id, smartphone_id)
            )

            if existing_item:   # Если товар уже в корзине, обновляем количество
                new_quantity = existing_item[0][0] + quantity
                db.execute_query(
                    "UPDATE cart_smartphone SET quantity = %s WHERE cart_id = %s AND smartphone_id = %s",
                    (new_quantity, cart_id, smartphone_id)
                )
            else:
                db.execute_query(
                    "INSERT INTO cart_smartphone (cart_id, smartphone_id, quantity) VALUES (%s, %s, %s)",
                    (cart_id, smartphone_id, quantity)
                )
            db.execute_query(
                "UPDATE smartphone SET in_stock = in_stock - %s WHERE smartphone_id = %s",
                (quantity, smartphone_id)
            )

            db.commit()
            QMessageBox.information(self, "Успех", f"{model} добавлен в корзину.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить смартфон в корзину: {str(e)}")




    def get_or_create_cart_id(self):
        """Создание или получение ID корзины для текущего устройства"""
        try:
            device_id = "default_device_id"  # ой не доделано, надо чтоб устройство распазновалось а то вдруг с разных касс зайдут 
            cart = db.fetch_query("SELECT cart_id FROM cart WHERE device_id = %s LIMIT 1", (device_id,))

            if cart:
                return cart[0][0] 
            else:
                db.execute_query("INSERT INTO cart (device_id) VALUES (%s)", (device_id,))
                db.commit()
                return db.fetch_query("SELECT LAST_INSERT_ID()")[0][0]
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать или получить корзину: {str(e)}")
            return None

    def show_clients(self):
        clients_layout = QVBoxLayout()

        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        clients_label = QLabel('Покупатели')
        top_layout.addWidget(clients_label)
        top_container.setLayout(top_layout)

        bottom_container = QWidget()
        bottom_layout = QVBoxLayout()

        table_widget_clients = QTableWidget()
        table_widget_clients.setColumnCount(2)

        clients = db.fetch_query('SELECT CONCAT(`lastname`, " ", `firstname`, " ", `patronymic`), `phone_number` FROM `client`')

        table_widget_clients.setHorizontalHeaderLabels([
            'ФИО', 'Номер телефона'
        ])
        table_widget_clients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget_clients.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget_clients.setEditTriggers(QTableWidget.NoEditTriggers)

        for client in clients:
            row_position = table_widget_clients.rowCount()
            table_widget_clients.insertRow(row_position)
            
            for col, value in enumerate(client):
                table_widget_clients.setItem(row_position, col, QTableWidgetItem(str(value)))

        bottom_layout.addWidget(table_widget_clients)
        bottom_container.setLayout(bottom_layout)

        clients_layout.addWidget(top_container)
        clients_layout.addWidget(bottom_container)

        new_content_widget = QWidget()
        new_content_layout = QVBoxLayout()
        new_content_widget.setLayout(new_content_layout)
        new_content_layout.addLayout(clients_layout)

        self.replace_content_widget(new_content_widget)

    def show_cart(self):
        cart_layout = QHBoxLayout()

        # Левый контейнер с таблицей
        left_container = QWidget()
        left_layout = QVBoxLayout()

        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        cart_label = QLabel('Корзина')
        cart_label.setAlignment(Qt.AlignLeft)

        clear_button = QPushButton('')
        clear_button.setFixedSize(50, 50)
        clear_button.setIcon(QIcon('image/clear.png'))
        clear_button.setIconSize(clear_button.size())

        def clear_cart():
            cart_id = self.get_or_create_cart_id()
            if not cart_id:
                QMessageBox.information(self, "Корзина", "Корзина пуста.")
                return

            cart_items = db.fetch_query('''
                SELECT smartphone_id, quantity 
                FROM cart_smartphone 
                WHERE cart_id = %s
            ''', (cart_id,))

            for item in cart_items:
                smartphone_id, quantity = item
                db.execute_query(
                    "UPDATE smartphone SET in_stock = in_stock + %s WHERE smartphone_id = %s",
                    (quantity, smartphone_id)
                )
            db.execute_query('DELETE FROM cart_smartphone WHERE cart_id = %s', (cart_id,))

            db.commit()
            QMessageBox.information(self, "Успех", "Корзина очищена.")
            self.show_cart() 

        clear_button.clicked.connect(clear_cart)

        top_layout.addWidget(cart_label)
        top_layout.addStretch()
        top_layout.addWidget(clear_button)
        top_container.setLayout(top_layout)

        table_widget_cart = QTableWidget()
        table_widget_cart.setColumnCount(5) 
        table_widget_cart.setHorizontalHeaderLabels([
            ' ', 'Название', 'Артикул', 'Количество', 'Цена'
        ])

        cart_id = self.get_or_create_cart_id()
        if not cart_id:
            QMessageBox.information(self, "Корзина", "Корзина пуста.")
            return

        carts = db.fetch_query('''
            SELECT 
                s.model AS smartphone_name, 
                s.article AS smartphone_article, 
                cs.quantity, 
                s.price, 
                (cs.quantity * s.price) AS total_price,
                cs.smartphone_id
            FROM cart_smartphone cs
            JOIN smartphone s ON cs.smartphone_id = s.smartphone_id
            WHERE cs.cart_id = %s
        ''', (cart_id,))

        if not carts:
            QMessageBox.information(self, "Корзина", "Корзина пуста.")
            return

        for row_index, cart_item in enumerate(carts):
            model, article, quantity, price, total_price, smartphone_id = cart_item

            row_position = table_widget_cart.rowCount()
            table_widget_cart.insertRow(row_position)

            # Кнопка для удаления товара из корзины
            remove_button = QPushButton('X')
            remove_button.setFixedSize(30, 30)
            remove_button.clicked.connect(lambda _, sid=smartphone_id, qty=quantity: remove_item(smartphone_id=sid, cart_id=cart_id, quantity=qty))

            # Заполняем данные в таблице
            table_widget_cart.setCellWidget(row_position, 0, remove_button)  # Кнопка удаления
            table_widget_cart.setItem(row_position, 1, QTableWidgetItem(model))  # Название
            table_widget_cart.setItem(row_position, 2, QTableWidgetItem(article))  # Артикул
            table_widget_cart.setItem(row_position, 3, QTableWidgetItem(str(quantity)))  # Количество
            table_widget_cart.setItem(row_position, 4, QTableWidgetItem(f"{total_price:.2f}"))  # Цена

        table_widget_cart.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget_cart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget_cart.setEditTriggers(QTableWidget.NoEditTriggers)


        def remove_item(smartphone_id=smartphone_id, cart_id=cart_id, quantity=quantity):
            try:
                db.execute_query(
                    "UPDATE smartphone SET in_stock = in_stock + %s WHERE smartphone_id = %s",
                    (quantity, smartphone_id)
                )
    
                db.execute_query(
                    "DELETE FROM cart_smartphone WHERE cart_id = %s AND smartphone_id = %s",
                    (cart_id, smartphone_id)
                )

                db.commit()
                QMessageBox.information(self, "Корзина", "Товар удален из корзины.")
                self.show_cart()  # Перезагрузка интерфейса корзины
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")

        left_layout.addWidget(top_container)
        left_layout.addWidget(table_widget_cart)
        left_container.setLayout(left_layout)

        right_container = QWidget()
        right_container.setFixedWidth(400)
        right_layout = QVBoxLayout()

        title_label = QLabel(f"Заказ №{cart_id}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 46px;")

        price_label = QLabel("Цена со скидки:")
        price_label.setStyleSheet("font-size: 30px;")

        total_price_field = QLabel(f"{sum(item[2] * item[3] for item in carts):.2f} ₽")
        total_price_field.setStyleSheet("font-size: 30px;")
        discount_label = QLabel("Скидка:")
        discount_label.setStyleSheet("font-size: 24px;")

        discount_combo = QComboBox()
        discount_combo.addItems(["0%", "5%", "10%", "15%", "20%"])
        discount_combo.setStyleSheet("font-size: 20px;")
        discount_combo.setFixedHeight(40)

        def update_total_with_discount():
            """Обновляет итоговую цену с учетом выбранной скидки."""
            discount_percentage = int(discount_combo.currentText().strip('%'))
            total_without_discount = sum(item[2] * item[3] for item in carts)
            discount_value = total_without_discount * discount_percentage / 100
            total_with_discount = total_without_discount - discount_value
            total_price_field.setText(f"{total_with_discount:.2f} ₽")

        discount_combo.currentIndexChanged.connect(update_total_with_discount)

        discount_field = QLabel('')
        discount_field.setStyleSheet("font-size: 24px;")

        customer_data_label = QLabel('Данные покупателя')
        customer_data_label.setStyleSheet("font-size: 24px;")

        name_input = QLineEdit()
        name_input.setPlaceholderText('ФИО')

        phone_input = QLineEdit()
        phone_input.setInputMask('+0-(000)-000-0000')
        # Создаем выпадающий список для существующих клиентов
        client_list = QComboBox()
        client_list.setFixedHeight(50)
        client_list.setStyleSheet("font-size: 16px;")
        client_list.hide()  # Изначально скрыт

        def search_clients(phone_text):
   
            digits = ''.join(filter(str.isdigit, phone_text))

            if len(digits) >= 3:  # Начинаем поиск после ввода минимум 3 цифр
                search_pattern = f"%{digits}%"
                clients = db.fetch_query("""
                    SELECT 
                        client_id,
                        CONCAT(lastname, ' ', firstname, ' ', COALESCE(patronymic, '')) as full_name,
                        phone_number
                    FROM client 
                    WHERE REPLACE(REPLACE(REPLACE(REPLACE(phone_number, '+', ''), '(', ''), ')', ''), '-', '') LIKE %s
                    LIMIT 5
                """, (search_pattern,))

                if clients:
                    client_list.clear()
                    client_list.addItem("Выберите клиента...", None) 
                    for client_id, full_name, phone in clients:
                        client_list.addItem(f"{full_name} ({phone})", client_id)  #client_id как данные
                    client_list.show()
                else:
                    client_list.hide()
            else:
                client_list.hide()

        def on_phone_text_changed(text):
            search_clients(text)

        def on_client_selected(index):  # Обработчик выбора клиента из списка
            if index > 0: 
                try:
                    client_id = client_list.itemData(index)
                    if not client_id:
                        raise ValueError("Некорректный идентификатор клиента.")

                    client_data = db.fetch_query("SELECT lastname, firstname, patronymic, phone_number FROM client WHERE client_id = %s", (client_id,))

                    if not client_data:
                        raise ValueError("Клиент с указанным ID не найден в базе данных.")
                    
                    lastname, firstname, patronymic, phone_number = client_data[0]
                    full_name = f"{lastname} {firstname} {patronymic or ''}".strip()

                    name_input.setText(full_name)
                    phone_input.setText(phone_number)
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки данных клиента: {str(e)}")
                finally:
                    client_list.hide()


        phone_input.textChanged.connect(on_phone_text_changed)
        client_list.currentIndexChanged.connect(on_client_selected)

        receipt_button = QPushButton('Чек')
        receipt_button.clicked.connect(lambda: self.generate_receipt_preview(cart_id))

        payment_button = QPushButton('Оплата')
        payment_button.clicked.connect(lambda: self.process_payment(cart_id, name_input.text(), phone_input.text()))

        right_layout.addWidget(title_label)  # Добавлен отступ
        right_layout.addWidget(price_label)
        right_layout.addWidget(total_price_field)
        right_layout.addWidget(discount_label)
        right_layout.addWidget(discount_combo)
        right_layout.addWidget(discount_field)
        right_layout.addWidget(customer_data_label)
        right_layout.addWidget(name_input)
        right_layout.addWidget(phone_input)
        right_layout.addWidget(client_list)
        right_layout.addStretch()
        right_layout.addWidget(receipt_button)
        right_layout.addWidget(payment_button)

        right_container.setLayout(right_layout)

        cart_layout.addWidget(left_container)
        cart_layout.addWidget(right_container)

        new_content_widget = QWidget()
        new_content_widget.setLayout(cart_layout)

        self.replace_content_widget(new_content_widget)

        # Функция для обновления количества в корзине
        def update_quantity(cart_item_id, smartphone_id, new_quantity):
            # Получаем текущее количество в корзине
            current_quantity = db.fetch_query(
                "SELECT quantity FROM cart_smartphone WHERE cart_item_id = %s", 
                (cart_item_id,)
            )[0][0]

            difference = new_quantity - current_quantity

            db.execute_query(
                "UPDATE cart_smartphone SET quantity = %s WHERE cart_item_id = %s",
                (new_quantity, cart_item_id)
            )

            db.execute_query(
                "UPDATE smartphone SET in_stock = in_stock - %s WHERE smartphone_id = %s",
                (-difference, smartphone_id)
            )
            self.show_cart()

        def on_quantity_changed(row):
            cart_item_id = int(table_widget_cart.item(row, 0).text()) 
            smartphone_id = int(table_widget_cart.item(row, 2).text()) 
            new_quantity = int(table_widget_cart.item(row, 3).text())  

            update_quantity(cart_item_id, smartphone_id, new_quantity)

        table_widget_cart.cellChanged.connect(lambda row, _ : on_quantity_changed(row))  

    def process_payment(self, cart_id, full_name, phone_number):
        #обработка оплаты и запись данных клиента и продажи в БД
        try:
            name_parts = full_name.strip().split()
            if len(name_parts) < 2 or len(name_parts) > 3:
                QMessageBox.warning(self, "Ошибка", "Введите ФИО в формате: Фамилия Имя Отчество.")
                return

            lastname = name_parts[0]
            firstname = name_parts[1]
            patronymic = name_parts[2] if len(name_parts) == 3 else None
            import re
            phone_pattern = re.compile(r"^\+\d-\(\d{3}\)-\d{3}-\d{4}$")
            if not phone_pattern.match(phone_number):
                QMessageBox.warning(self, "Ошибка", "Введите номер телефона в формате: +0-(000)-000-0000.")
                return
            existing_client = db.fetch_query(
                "SELECT client_id FROM client WHERE phone_number = %s",
                (phone_number,)
            )

            if existing_client:
                client_id = existing_client[0][0]
            else:
                db.execute_query(
                    "INSERT INTO client (lastname, firstname, patronymic, phone_number) VALUES (%s, %s, %s, %s)",
                    (lastname, firstname, patronymic, phone_number)
                )
                db.commit()
                client_id = db.fetch_query("SELECT LAST_INSERT_ID()")[0][0]

            db.execute_query(
                "UPDATE cart SET client_id = %s WHERE cart_id = %s",
                (client_id, cart_id)
            )
            db.commit()

            total_price = db.fetch_query(
                "SELECT SUM(cs.quantity * s.price) FROM cart_smartphone cs "
                "JOIN smartphone s ON cs.smartphone_id = s.smartphone_id WHERE cs.cart_id = %s",
                (cart_id,)
            )[0][0]

            db.execute_query(
                "INSERT INTO sell (date_sell, client_id, total_price) VALUES (NOW(), %s, %s)",
                (client_id, total_price)
            )
            db.commit()

            sell_id = db.fetch_query("SELECT LAST_INSERT_ID()")[0][0]

            cart_items = db.fetch_query(
                "SELECT cs.smartphone_id, cs.quantity, s.price "
                "FROM cart_smartphone cs "
                "JOIN smartphone s ON cs.smartphone_id = s.smartphone_id "
                "WHERE cs.cart_id = %s",
                (cart_id,)
            )

            for smartphone_id, quantity, price in cart_items:
                db.execute_query(
                    "INSERT INTO sell_smartphone (sell_id, smartphone_id, quantity, price) "
                    "VALUES (%s, %s, %s, %s)",
                    (sell_id, smartphone_id, quantity, price)
                )
            db.commit()

            db.execute_query("DELETE FROM cart_smartphone WHERE cart_id = %s", (cart_id,))
            db.commit()
            receipt_data = {
                "receipt_number": str(uuid.uuid4())[:8],
                "date_time": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "location": "г. Киров, ул. Свободы, д. 172",
                "inn": "1234567890",
                "tax_system": "УСН",
                "seller_name": "ООО 'ZsellZphone'",
                "buyer_name": full_name,
                "buyer_phone": phone_number,
                "items": [{"name": item[0], "quantity": item[1], "price": item[2]} for item in cart_items],
                "total_without_discount": sum(item[1] * item[2] for item in cart_items),
                "total_with_discount": total_price,  # Цена с учетом скидки
                "payment_method": "Банковская карта"  # Или другой метод оплаты
            }

            receipt_path = generate_receipt(receipt_data)
            QMessageBox.information(self, "Оплата завершена", f"Чек сохранён: {receipt_path}")


        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обработать оплату: {str(e)}")



    def show_management(self):
        management_layout = QVBoxLayout()
        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        management_top_button = QLabel('Управление')

        search_bar = QLineEdit()
        search_bar.setPlaceholderText('Поиск по каталогу...')
        def filter_catalog(text): 
            for row in range(table_widget_management.rowCount()): 
                match = False 
                for col in range(table_widget_management.columnCount()): 
                    item = table_widget_management.item(row, col) 
                    if item and text.lower() in item.text().lower(): 
                        match = True 
                        break 
                table_widget_management.setRowHidden(row, not match)

        search_bar.textChanged.connect(filter_catalog)

        # Кнопка добавления рядом с строкой поиска
        add_button = QPushButton()
        add_button.setFixedSize(50, 50)
        add_button.setIcon(QIcon('image/add_smatphone.png'))
        add_button.setIconSize(add_button.size())
        add_button.clicked.connect(self.open_add_smartphone_window)  # Подключение к новой функции

        top_layout.addWidget(management_top_button)
        top_layout.addWidget(search_bar)
        top_layout.addWidget(add_button)
        top_container.setLayout(top_layout)

        # Нижняя часть: таблица
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout()

        managments = db.fetch_query('SELECT `smartphone_id`, `model`, `article`, `in_stock`, `price` FROM `smartphone`')

        table_widget_management = QTableWidget()
        table_widget_management.setColumnCount(7)
        table_widget_management.setHorizontalHeaderLabels([
            'pk', 'Название', 'Артикул', 'В наличии', 'Цена', ' ', ' '
        ])

        table_widget_management.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget_management.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget_management.setEditTriggers(QTableWidget.NoEditTriggers)


        table_widget_management.setColumnHidden(0, True)

        for i in managments:
            row_position = table_widget_management.rowCount()
            table_widget_management.insertRow(row_position)
            for col, value in enumerate(i):
                table_widget_management.setItem(row_position, col, QTableWidgetItem(str(value)))

            edit_button = QPushButton()
            edit_button.clicked.connect(lambda _, smartphone_id=i[0]: self.open_edit_smartphone_window(smartphone_id))
            edit_button.setIcon(QIcon('image/pen.png'))
            edit_button.setIconSize(QSize(20, 20))
            table_widget_management.setCellWidget(row_position, 5, edit_button)
            
            delete_button = QPushButton()
            delete_button.clicked.connect(lambda _, smartphone_id=i[0], row=row_position: self.delete_smartphone(smartphone_id, row, table_widget_management))
            delete_button.setIcon(QIcon('image/clear.png'))
            delete_button.setIconSize(QSize(20, 20))
            table_widget_management.setCellWidget(row_position, 6, delete_button)

        
        bottom_layout.addWidget(table_widget_management)
        bottom_container.setLayout(bottom_layout)

        # Компоновка раздела "Управление"
        management_layout.addWidget(top_container)
        management_layout.addWidget(bottom_container)

        # Создание нового виджета для замены контента
        new_content_widget = QWidget()
        new_content_layout = QVBoxLayout()
        new_content_widget.setLayout(new_content_layout)
        new_content_layout.addLayout(management_layout)

        self.replace_content_widget(new_content_widget)

    def open_add_smartphone_window(self):
        self.add_window = AddSmartphoneWindow()
        self.add_window.exec_()

    def delete_smartphone(self, smartphone_id, row, table_widget):
        """Удаляет выбранный смартфон из базы данных и из таблицы с подтверждением"""
        # Диалог подтверждения удаления
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить этот смартфон?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Запрос на удаление смартфона из базы данных
                db.execute_query('DELETE FROM `smartphone` WHERE `smartphone_id` = %s', (smartphone_id,))
                db.commit()

                # Удаляем строку из таблицы
                table_widget.removeRow(row)

                # Сообщение об успешном удалении
                QMessageBox.information(self, "Удалено", "Смартфон успешно удален.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить смартфон: {str(e)}")
        


    def open_edit_smartphone_window(self, smartphone_id):
        smartphone_data = db.fetch_query(
            '''
            SELECT `model`, `article`, `price`, `in_stock`, `characteristic`, `brand_id`
            FROM `smartphone`
            WHERE `smartphone_id` = %s
            ''',
            (smartphone_id,)
        )
        if smartphone_data:
            data = smartphone_data[0]
            self.add_window = AddSmartphoneWindow()
            self.add_window.article_input.setText(data[1])
            self.add_window.model_input.setText(data[0])
            self.add_window.price_input.setText(str(data[2]))
            self.add_window.stock_input.setText(str(data[3]))
            self.add_window.description_input.setPlainText(data[4])
            brand_name = db.fetch_query('SELECT `name` FROM `brand` WHERE `brand_id` = %s', (data[5],))[0][0]
            self.add_window.brand_input.setCurrentText(brand_name)

            # Передача ID смартфона в обработчик кнопки сохранения
            self.add_window.save_button.clicked.disconnect()  # Убираем предыдущие подключения
            self.add_window.save_button.clicked.connect(lambda: self.add_window.save_smartphone(smartphone_id))
            self.add_window.exec_()


    def show_sales(self):
        """Отображение данных из таблицы продаж"""
        sales_layout = QVBoxLayout()

        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        sales_top_button = QLabel('Продажи')
        top_layout.addWidget(sales_top_button)
        top_container.setLayout(top_layout)

        bottom_container = QWidget()
        bottom_layout = QVBoxLayout()

        table_widget_sales = QTableWidget()
        table_widget_sales.setColumnCount(5)
        table_widget_sales.setHorizontalHeaderLabels([
            'Модель', 'Артикул', 'ФИО', 'Сумма', 'Дата'
        ])

        try:
            # Выполняем запрос для получения данных о продажах
            sales = db.fetch_query('''
            SELECT 
                s.model,
                s.article,
                CONCAT(cl.lastname, ' ', cl.firstname, ' ', COALESCE(cl.patronymic, '')) AS full_name,
                (ss.quantity * ss.price) as item_total_price,
                sel.date_sell
            FROM sell sel
            INNER JOIN client cl ON sel.client_id = cl.client_id
            INNER JOIN sell_smartphone ss ON sel.sell_id = ss.sell_id
            INNER JOIN smartphone s ON ss.smartphone_id = s.smartphone_id
            ORDER BY sel.date_sell DESC
            ''')

            # Заполняем таблицу данными
            for row_data in sales:
                row_position = table_widget_sales.rowCount()
                table_widget_sales.insertRow(row_position)
                for col, value in enumerate(row_data):
                    table_widget_sales.setItem(row_position, col, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

        table_widget_sales.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget_sales.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget_sales.setEditTriggers(QTableWidget.NoEditTriggers)


        bottom_layout.addWidget(table_widget_sales)
        bottom_container.setLayout(bottom_layout)

        sales_layout.addWidget(top_container)
        sales_layout.addWidget(bottom_container)

        new_content_widget = QWidget()
        new_content_widget.setLayout(sales_layout)
        self.replace_content_widget(new_content_widget)


    def replace_content_widget(self, new_widget):
        self.main_splitter.widget(1).deleteLater()
        self.main_splitter.insertWidget(1, new_widget)

    def generate_receipt_preview(self, cart_id):
        try:
            # Получение данных корзины
            cart_items = db.fetch_query("SELECT s.model, cs.quantity, s.price FROM cart_smartphone cs JOIN smartphone s ON cs.smartphone_id = s.smartphone_id WHERE cs.cart_id = %s", (cart_id,)
            )
            
            if not cart_items:
                QMessageBox.warning(self, "Ошибка", "Корзина пуста, нечего показывать.")
                return
            # Подготовка данных для чека
            receipt_data = {
                "receipt_number": "ПРЕДПРОСМОТР",
                "date_time": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "location": "г. Киров, ул. Свободы, д. 172",
                "inn": "1234567890",
                "tax_system": "УСН",
                "seller_name": "ООО 'ZsellsmartZ'",
                "buyer_name": "—",
                "buyer_phone": "—",
                "items": [{"name": item[0], "quantity": item[1], "price": item[2]} for item in cart_items],
                "total_without_discount": sum(item[1] * item[2] for item in cart_items),
                "discount": 0,  # Укажите скидку, если требуется
                "total_with_discount": sum(item[1] * item[2] for item in cart_items),  # Учитываем скидку
                "payment_method": "—"
            }
            generate_receipt(receipt_data, is_preview=True)
            QMessageBox.information(self, "Чек", "Чек открыт для предпросмотра.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать макет чека: {str(e)}")



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
