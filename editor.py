from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTableView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
import sys

class EditorWindow(QMainWindow):
    def __init__(self, db_file="data/waybills.db"):        
        super().__init__()
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_file)
        self.db.open()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Редактор даних")
        central = QWidget()
        layout = QVBoxLayout(central)
        self.table = QTableView()
        self.model = QSqlTableModel(db=self.db)
        self.model.setTable('Drivers')
        self.model.select()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
        self.save_btn = QPushButton("Зберегти зміни")
        self.save_btn.clicked.connect(self.model.submitAll)
        layout.addWidget(self.save_btn)
        self.setCentralWidget(central)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EditorWindow()
    win.show()
    sys.exit(app.exec_())
