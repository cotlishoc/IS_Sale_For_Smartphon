import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Регистрация шрифта DejaVu
pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))

def generate_receipt(receipt_data, is_preview=False):
    receipt_folder = os.path.join(os.getcwd(), "чеки")
    if not is_preview:
        os.makedirs(receipt_folder, exist_ok=True)
        receipt_filename = f"receipt_{receipt_data['receipt_number']}.pdf"
        receipt_path = os.path.join(receipt_folder, receipt_filename)
    else:
        receipt_path = None

    # Создаем PDF
    c = canvas.Canvas(receipt_path or "receipt_preview.pdf", pagesize=A4)
    c.setFont("DejaVu", 12)  # Используем зарегистрированный шрифт
    width, height = A4

    # Заголовок
    c.setFont("DejaVu", 16)
    c.drawString(50, height - 50, "КАССОВЫЙ ЧЕК")

    # Основная информация
    c.setFont("DejaVu", 12)
    c.drawString(50, height - 100, f"Номер чека: {receipt_data['receipt_number']}")
    c.drawString(50, height - 120, f"Дата и время: {receipt_data['date_time']}")
    c.drawString(50, height - 140, f"Место расчета: {receipt_data['location']}")
    c.drawString(50, height - 160, f"ИНН: {receipt_data['inn']}")
    c.drawString(50, height - 180, f"Система налогообложения: {receipt_data['tax_system']}")
    c.drawString(50, height - 200, f"Продавец: {receipt_data['seller_name']}")

    # Данные покупателя
    c.drawString(50, height - 240, "Покупатель:")
    c.drawString(60, height - 260, f"ФИО: {receipt_data['buyer_name']}")
    c.drawString(60, height - 280, f"Телефон: {receipt_data['buyer_phone']}")

    # Товары
    c.drawString(50, height - 320, "Товары:")
    y_position = height - 340
    for idx, item in enumerate(receipt_data['items'], start=1):
        c.drawString(60, y_position, f"{idx}. {item['name']} - {item['quantity']} x {item['price']} ₽")
        y_position -= 20

    # Итого
    y_position -= 20
    # Сумма без скидки
    y_position -= 20
    c.drawString(50, y_position, f"Сумма без скидки: {receipt_data['total_without_discount']} ₽")

    # Сумма со скидкой
    y_position -= 20
    c.drawString(50, y_position, f"ИТОГО (со скидкой): {receipt_data['total_with_discount']} ₽")
    c.drawString(50, y_position - 60, f"Оплата: {receipt_data['payment_method']}")

    # Подпись
    c.drawString(50, y_position - 100, "Спасибо за покупку!")

    # Сохраняем или отображаем PDF
    c.save()
    return receipt_path if not is_preview else None
