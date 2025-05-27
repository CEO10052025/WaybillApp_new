import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox
from database import init_db
from importer import import_excel
from editor import EditorWindow
from generator import generate_pdf

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.setWindowTitle("WaybillApp")
        menubar = self.menuBar()
        imp = menubar.addMenu("Файл")
        imp_drv = QAction("Імпорт водіїв", self)
        imp_drv.triggered.connect(lambda: self.load('Drivers'))
        imp.addAction(imp_drv)
        imp_car = QAction("Імпорт авто", self)
        imp_car.triggered.connect(lambda: self.load('Vehicles'))
        imp.addAction(imp_car)
        imp_rt = QAction("Імпорт маршрутів", self)
        imp_rt.triggered.connect(lambda: self.load('Routes'))
        imp.addAction(imp_rt)
        edit = QAction("Редагувати данные", self)
        edit.triggered.connect(self.open_editor)
        menubar.addAction(edit)
        gen = QAction("Генерувати шляховий лист", self)
        gen.triggered.connect(self.create_waybill)
        menubar.addAction(gen)

    def load(self, table):
        path, _ = QFileDialog.getOpenFileName(self, f"Виберіть файл для {table}", filter="Excel Files (*.xlsx)")
        if path:
            try:
                df = import_excel(path, table)
                QMessageBox.information(self, "Успіх", f"Імпортовано {len(df)} записів у {table}")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", str(e))

    def open_editor(self):
        self.editor = EditorWindow()
        self.editor.show()

    def create_waybill(self):
        # для демонстрації: обираємо останній запис
        import sqlite3
        conn = sqlite3.connect("data/waybills.db")
        c = conn.cursor()
        c.execute("SELECT id FROM Waybills ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        if not row:
            QMessageBox.warning(self, "Увага", "Немає даних для генерації")
            return
        waybill_id = row[0]
        output = QFileDialog.getSaveFileName(self, "Зберегти PDF", filter="PDF files (*.pdf)")[0]
        if output:
            try:
                generate_pdf(waybill_id, output)
                QMessageBox.information(self, "Успіх", "PDF згенеровано")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
