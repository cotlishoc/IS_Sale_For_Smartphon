from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QDateEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from model import db
import os


class ReportWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Основной макет раздела
        report_layout = QHBoxLayout()

        # Левый контейнер
        left_container = QWidget()
        left_layout = QVBoxLayout()

        # Заголовок
        top_container = QWidget()
        top_container.setFixedHeight(100)
        top_layout = QHBoxLayout()

        self.report_title_label = QLabel("Отчет:")
        self.report_title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(self.report_title_label)
        top_container.setLayout(top_layout)

        # Основной контент в левом контейнере
        content_container = QWidget()
        content_layout = QVBoxLayout()

        # Создание вертикального макета для вариантов отчетов
        report_options_layout = QVBoxLayout()

        # Первый вариант отчета: Отчетность по продажам
        self.sales_report_checkbox = QCheckBox()
        sales_report_label = QLabel("Отчетность по продажам")
        sales_report_label.setStyleSheet("font-size: 20px; font-family: Arial;")
        sales_period_label = QLabel("Выберите период:")
        sales_period_label.setStyleSheet("font-size: 18px; font-family: Arial;")

        self.sales_period_start = QDateEdit()
        self.sales_period_start.setCalendarPopup(True)
        self.sales_period_start.setDate(QDate.currentDate())
        self.sales_period_start.setFixedWidth(150)

        self.sales_period_end = QDateEdit()
        self.sales_period_end.setCalendarPopup(True)
        self.sales_period_end.setDate(QDate.currentDate())
        self.sales_period_end.setFixedWidth(150)

        sales_period_layout = QHBoxLayout()
        sales_period_layout.addWidget(self.sales_period_start)
        sales_period_layout.addWidget(self.sales_period_end)
        sales_period_layout.setSpacing(20)

        sales_report_layout = QVBoxLayout()
        sales_report_layout.addWidget(self.sales_report_checkbox)
        sales_report_layout.addWidget(sales_report_label)
        sales_report_layout.addWidget(sales_period_label)
        sales_report_layout.addLayout(sales_period_layout)
        sales_report_layout.setSpacing(10)

        report_options_layout.addLayout(sales_report_layout)

        # Разделительная полоса
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ccc;")
        separator.setContentsMargins(0, 50, 0, 50)

        report_options_layout.addWidget(separator)

        # Второй вариант отчета: Популярные модели смартфонов
        self.popular_models_checkbox = QCheckBox()
        popular_models_label = QLabel("Популярные модели смартфонов")
        popular_models_label.setStyleSheet("font-size: 20px; font-family: Arial;")
        popular_period_label = QLabel("Выберите период:")
        popular_period_label.setStyleSheet("font-size: 18px; font-family: Arial;")

        self.popular_period_start = QDateEdit()
        self.popular_period_start.setCalendarPopup(True)
        self.popular_period_start.setDate(QDate.currentDate())
        self.popular_period_start.setFixedWidth(150)

        self.popular_period_end = QDateEdit()
        self.popular_period_end.setCalendarPopup(True)
        self.popular_period_end.setDate(QDate.currentDate())
        self.popular_period_end.setFixedWidth(150)

        popular_period_layout = QHBoxLayout()
        popular_period_layout.addWidget(self.popular_period_start)
        popular_period_layout.addWidget(self.popular_period_end)
        popular_period_layout.setSpacing(20)

        popular_models_layout = QVBoxLayout()
        popular_models_layout.addWidget(self.popular_models_checkbox)
        popular_models_layout.addWidget(popular_models_label)
        popular_models_layout.addWidget(popular_period_label)
        popular_models_layout.addLayout(popular_period_layout)
        popular_models_layout.setSpacing(10)

        report_options_layout.addLayout(popular_models_layout)

        # Добавляем растяжение, чтобы прижать элементы к верху
        report_options_layout.addStretch()

        # Добавляем макет вариантов отчетов в контентный макет
        content_layout.addLayout(report_options_layout)
        content_layout.setContentsMargins(10, 10, 10, 10)  # Внешние отступы
        content_container.setLayout(content_layout)

        left_layout.addWidget(top_container)
        left_layout.addWidget(content_container)
        left_container.setLayout(left_layout)

        # Правый контейнер
        right_container = QWidget()
        right_layout = QVBoxLayout()

        self.report_output = QTextEdit()
        self.report_output.setPlaceholderText("Здесь появится выбранный отчет...")
        self.report_output.setReadOnly(True)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Очистить")
        export_button = QPushButton("Экспорт")
        button_layout.addWidget(clear_button)
        clear_button.clicked.connect(self.clear_report)
        button_layout.addWidget(export_button)
        export_button.clicked.connect(self.export_report_to_pdf)


        right_layout.addWidget(self.report_output)
        right_layout.addLayout(button_layout)
        right_container.setLayout(right_layout)

        # Устанавливаем минимальную ширину для правого контейнера
        right_container.setFixedWidth(400)

        # Добавляем контейнеры в основной макет
        report_layout.addWidget(left_container)
        report_layout.addWidget(right_container)

        # Устанавливаем основной макет для виджета
        self.setLayout(report_layout)

        # Подключение сигналов
        self.sales_report_checkbox.stateChanged.connect(self.update_report_title)
        self.popular_models_checkbox.stateChanged.connect(self.update_report_title)

    def update_report_title(self):
        """Обновляет заголовок отчета и генерирует содержимое"""
        if self.sales_report_checkbox.isChecked():
            self.popular_models_checkbox.setChecked(False)
            self.report_title_label.setText("Отчет: по продажам")
            self.generate_sales_report()
        elif self.popular_models_checkbox.isChecked():
            self.sales_report_checkbox.setChecked(False)
            self.report_title_label.setText("Отчет: по популярности")
            self.generate_popular_models_report()
        else:
            self.report_title_label.setText("Отчет:")
            self.report_output.clear()

    def clear_report(self):
        """Очищает все флажки, поля выбора периода и текстовое поле для отчета."""
        # Сбрасываем состояния флажков
        self.sales_report_checkbox.setChecked(False)
        self.popular_models_checkbox.setChecked(False)
        
        # Сбрасываем текстовое поле для отчета
        self.report_output.clear()

        # Сбрасываем периоды на текущую дату
        current_date = QDate.currentDate()
        self.sales_period_start.setDate(current_date)
        self.sales_period_end.setDate(current_date)
        self.popular_period_start.setDate(current_date)
        self.popular_period_end.setDate(current_date)

        # Сбрасываем заголовок отчета
        self.report_title_label.setText("Отчет:")



    def generate_sales_report(self):
        """Генерация отчета по продажам"""
        start_date = self.sales_period_start.date().toString("yyyy-MM-dd")
        end_date = self.sales_period_end.date().toString("yyyy-MM-dd")

        query = """
        SELECT 
            s.Model AS Модель,
            b.Name AS Бренд,
            SUM(ss.Quantity) AS Количество_продаж,
            SUM(ss.Quantity * ss.Price) AS Общая_сумма
        FROM Sell_Smartphone ss
        JOIN Smartphone s ON ss.Smartphone_ID = s.Smartphone_ID
        JOIN Brand b ON s.Brand_ID = b.Brand_ID
        JOIN Sell se ON ss.Sell_ID = se.Sell_ID
        WHERE se.Date_Sell BETWEEN %s AND %s
        GROUP BY s.Model, b.Name
        ORDER BY Общая_сумма DESC
        """
        data = db.fetch_query(query, (start_date, end_date))

        # Заголовок отчета
        report_header = f"Отчет по продажам за период: {start_date} - {end_date}\n\n"
        
        # Формируем таблицу
        table_data = [["Модель", "Бренд", "Количество продаж", "Общая сумма (руб.)"]]
        total_quantity = 0
        total_amount = 0
        
        for row in data:
            table_data.append([
                row[0],  # Модель
                row[1],  # Бренд
                str(row[2]),  # Количество
                f"{row[3]:.2f}"  # Сумма
            ])
            total_quantity += row[2]
            total_amount += row[3]
        
        # Добавляем итоговую строку
        table_data.append([
            "ИТОГО:",
            "",
            str(total_quantity),
            f"{total_amount:.2f}"
        ])
        
        # Формируем текст отчета
        text = report_header + "\n".join(["\t".join(map(str, row)) for row in table_data])
        self.report_output.setText(text)

    def generate_popular_models_report(self):
        """Генерация отчета по популярным моделям"""
        start_date = self.popular_period_start.date().toString("yyyy-MM-dd")
        end_date = self.popular_period_end.date().toString("yyyy-MM-dd")

        query = """
        SELECT 
            b.Name AS Бренд,
            s.Model AS Модель,
            s.Price AS Цена_за_единицу,
            SUM(ss.Quantity) AS Количество_продаж,
            SUM(ss.Quantity * ss.Price) AS Общая_сумма,
            ROUND(
                (SUM(ss.Quantity) * 100.0) / (
                    SELECT SUM(Quantity) 
                    FROM Sell_Smartphone ss2
                    JOIN Sell se2 ON ss2.Sell_ID = se2.Sell_ID
                    WHERE se2.Date_Sell BETWEEN %s AND %s
                ),
                2
            ) AS Доля_продаж
        FROM Sell_Smartphone ss
        JOIN Smartphone s ON ss.Smartphone_ID = s.Smartphone_ID
        JOIN Brand b ON s.Brand_ID = b.Brand_ID
        JOIN Sell se ON ss.Sell_ID = se.Sell_ID
        WHERE se.Date_Sell BETWEEN %s AND %s
        GROUP BY b.Name, s.Model, s.Price
        ORDER BY Количество_продаж DESC
        """
        data = db.fetch_query(query, (start_date, end_date, start_date, end_date))

        # Заголовок отчета
        report_header = f"Отчет по популярности моделей за период: {start_date} - {end_date}\n\n"
        
        # Формируем таблицу
        table_data = [["Бренд", "Модель", "Цена", "Продано шт.", "Общая сумма (руб.)", "Доля продаж %"]]
        
        for row in data:
            table_data.append([
                row[0],  # Бренд
                row[1],  # Модель
                f"{row[2]:.2f}",  # Цена за единицу
                str(row[3]),  # Количество
                f"{row[4]:.2f}",  # Общая сумма
                f"{row[5]}%"  # Доля продаж
            ])
        
        # Формируем текст отчета
        text = report_header + "\n".join(["\t".join(map(str, row)) for row in table_data])
        self.report_output.setText(text)

    # Регистрация шрифта DejaVu для поддержки кириллицы
    pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))

    def export_report_to_pdf(self):
        """Экспортирует текущий отчет в PDF с поддержкой кириллицы и правильным масштабированием."""
        report_text = self.report_output.toPlainText()
        if not report_text.strip():
            QMessageBox.warning(self, "Ошибка", "Отчет пустой. Нечего экспортировать.")
            return

        # Создаем папку для отчетов, если её нет
        reports_dir = "отчеты"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        # Формируем имя файла
        report_title = self.report_title_label.text().replace("Отчет: ", "").strip()
        if not report_title:
            report_title = "Отчет"

        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        report_number = len([f for f in os.listdir(reports_dir) if os.path.isfile(os.path.join(reports_dir, f))]) + 1
        file_name = f"{reports_dir}/{report_title}_{report_number}_{current_date}.pdf"

        # Генерация PDF
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))
            pdf = SimpleDocTemplate(file_name, pagesize=landscape(letter))
            lines = report_text.split("\n")
            table_data = [line.split("\t") for line in lines if line.strip()]

            # Создаем таблицу с правильными отступами и стилями
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ]))

            pdf.build([table])
            QMessageBox.information(self, "Успех", f"Отчет успешно сохранен: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить отчет: {e}")

