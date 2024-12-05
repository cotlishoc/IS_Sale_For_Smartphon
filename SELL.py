from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSplitter,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SELL FOR SMARTPHONE')  # Установка заголовка окна приложения
        self.setGeometry(0, 0, 1920, 1080)  # Установка размеров и положения окна

        # Единый стиль для всех элементов
        self.setStyleSheet("""
            QPushButton { height: 50px; font-size: 16px; }
            QLabel { font-size: 52px; font-family: Arial; }
            QLineEdit { font-size: 16px; height: 50px; }
        """)

        # Создание кнопок
        self.catalog_button = QPushButton('Каталог')
        self.catalog_button.clicked.connect(self.show_catalog)
        
        self.client_button = QPushButton('Покупатели')
        self.client_button.clicked.connect(self.show_clients)
        
        self.cart_button = QPushButton('Корзина')
        self.cart_button.clicked.connect(self.show_cart)
        
        self.management_button = QPushButton('Управление')
        
        self.sell_button = QPushButton('Продажи')
        
        self.report_button = QPushButton('Отчет')

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
        self.section_button_widget.setFixedWidth(200)  # Фиксированная ширина контейнера

        # Основной сплиттер для разделения кнопок разделов и содержимого
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.section_button_widget)

        # Инициализация текущего виджета содержимого
        self.content_widget = QWidget()
        self.main_splitter.addWidget(self.content_widget)
        self.main_splitter.setSizes([200, 1720])

        # Установка центрального виджета
        self.setCentralWidget(self.main_splitter)

        # Показ раздела "Каталог" при открытии приложения
        self.show_catalog()

    def show_catalog(self):
        catalog_layout = QVBoxLayout()

        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        catalog_top_button = QLabel('Каталог')

        search_bar = QLineEdit()
        search_bar.setPlaceholderText('Поиск по каталогу...')

        top_layout.addWidget(catalog_top_button)
        top_layout.addWidget(search_bar)
        top_container.setLayout(top_layout)

        bottom_container = QWidget()
        bottom_layout = QVBoxLayout()

        table_widget_catalog = QTableWidget()
        table_widget_catalog.setColumnCount(5)
        table_widget_catalog.setHorizontalHeaderLabels([ 
            'Порядковый номер', 'Название', 'Артикул', 'В наличии', 'Цена'
        ])

        bottom_layout.addWidget(table_widget_catalog)
        bottom_container.setLayout(bottom_layout)

        catalog_layout.addWidget(top_container)
        catalog_layout.addWidget(bottom_container)

        new_content_widget = QWidget()
        new_content_layout = QVBoxLayout()
        new_content_widget.setLayout(new_content_layout)
        new_content_layout.addLayout(catalog_layout)

        self.replace_content_widget(new_content_widget)

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
        table_widget_clients.setColumnCount(3)
        table_widget_clients.setHorizontalHeaderLabels([
            'Порядковый номер', 'ФИО', 'Номер телефона'
        ])

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
        clear_button.setStyleSheet("border: 1px solid black;")
        # TODO: Добавить функцию для кнопки очистки

        top_layout.addWidget(cart_label)
        top_layout.addStretch()
        top_layout.addWidget(clear_button)
        top_container.setLayout(top_layout)

        table_widget_cart = QTableWidget()
        table_widget_cart.setColumnCount(4)
        table_widget_cart.setHorizontalHeaderLabels([
            'X', 'Название', 'Артикул', 'Цена'
        ])

        left_layout.addWidget(top_container)
        left_layout.addWidget(table_widget_cart)
        left_container.setLayout(left_layout)

        # Правый контейнер для управления
        right_container = QWidget()
        right_container.setFixedWidth(400)
        right_layout = QVBoxLayout()

        title_label = QLabel('Название')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 46px;")

        price_label = QLabel('Цена')
        price_label.setStyleSheet("font-size: 32px;")

        spacer = QWidget()
        spacer.setFixedHeight(60)  # Расстояние между Названием и Ценой

        total_price_field = QLabel('')
        total_price_field.setStyleSheet("font-size: 32px;")

        discount_label = QLabel('Скидка')
        discount_label.setStyleSheet("font-size: 28px;")

        discount_field = QLabel('')
        discount_field.setStyleSheet("font-size: 28px;")

        customer_data_label = QLabel('Данные покупателя')
        customer_data_label.setStyleSheet("font-size: 28px;")

        name_input = QLineEdit()
        name_input.setPlaceholderText('ФИО')

        phone_input = QLineEdit()
        phone_input.setPlaceholderText('Номер телефона')

        receipt_button = QPushButton('Чек')
        payment_button = QPushButton('Оплата')

        right_layout.addWidget(title_label)
        right_layout.addWidget(spacer)  # Добавлен отступ
        right_layout.addWidget(price_label)
        right_layout.addWidget(total_price_field)
        right_layout.addWidget(discount_label)
        right_layout.addWidget(discount_field)
        right_layout.addWidget(customer_data_label)
        right_layout.addWidget(name_input)
        right_layout.addWidget(phone_input)
        right_layout.addStretch()
        right_layout.addWidget(receipt_button)
        right_layout.addWidget(payment_button)

        right_container.setLayout(right_layout)

        cart_layout.addWidget(left_container)
        cart_layout.addWidget(right_container)

        new_content_widget = QWidget()
        new_content_widget.setLayout(cart_layout)

        self.replace_content_widget(new_content_widget)

    def replace_content_widget(self, new_widget):
        self.main_splitter.widget(1).deleteLater()
        self.main_splitter.insertWidget(1, new_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
