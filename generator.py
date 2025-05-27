from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
from datetime import datetime

def generate_pdf(waybill_id: int, output_path: str, db_file: str = "data/waybills.db"):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""
        SELECT w.date, d.name, v.plate, r.start, r.end, w.mileage_start, w.mileage_end, w.fuel
        FROM Waybills w
        JOIN Drivers d ON w.driver_id=d.id
        JOIN Vehicles v ON w.vehicle_id=v.id
        JOIN Routes r ON w.route_id=r.id
        WHERE w.id=?
    """, (waybill_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise ValueError("Waybill not found")
    c = canvas.Canvas(output_path, pagesize=A4)
    c.drawString(50, 800, f"Шляховий лист — {row[0]}")
    labels = ["Водій:", "Авто:", "Маршрут:", "Пробіг до:", "Пробіг після:", "Пальне:"]
    values = [row[1], row[2], f"{row[3]} - {row[4]}", str(row[5]), str(row[6]), str(row[7])]
    y = 760
    for lbl, val in zip(labels, values):
        c.drawString(50, y, f"{lbl} {val}")
        y -= 20
    c.drawString(50, y-40, "Підпис: ________________")
    c.save()
