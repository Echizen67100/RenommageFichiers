import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import os

class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()

        # UI Setup
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # Top UI Elements
        hbox = QHBoxLayout()

        self.base_name_label = QLabel('Base nom fichier :', self)
        hbox.addWidget(self.base_name_label)

        self.base_name_entry = QLineEdit(self)
        hbox.addWidget(self.base_name_entry)

        self.start_number_label = QLabel('Numéro de départ :', self)
        hbox.addWidget(self.start_number_label)

        self.start_number_entry = QLineEdit(self)
        hbox.addWidget(self.start_number_entry)

        self.select_button = QPushButton('Sélectionner les fichiers', self)
        self.select_button.clicked.connect(self.showDialog)
        hbox.addWidget(self.select_button)

        self.preview_button = QPushButton('Prévisualiser', self)
        self.preview_button.clicked.connect(self.preview_rename)
        hbox.addWidget(self.preview_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_table)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        # Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Ancien nom', 'Nouveau nom', 'Actions'])
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 200)
        self.table.verticalHeader().setDefaultSectionSize(40)
        vbox.addWidget(self.table)

        # Rename Button
        self.rename_button = QPushButton('Renommer', self)
        self.rename_button.clicked.connect(self.rename_files)
        vbox.addWidget(self.rename_button)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 900, 400)
        self.setWindowTitle('Renommeur de fichiers')
        self.show()

    def showDialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Sélectionner les fichiers à renommer')
        
        if files:
            self.folder_path = os.path.dirname(files[0])
            for file_path in files:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(os.path.basename(file_path)))

                up_button = QPushButton('Monter')
                up_button.clicked.connect(lambda: self.move_item(-1))
                down_button = QPushButton('Descendre')
                down_button.clicked.connect(lambda: self.move_item(1))

                action_layout = QHBoxLayout()
                action_layout.addWidget(up_button)
                action_layout.addWidget(down_button)
                action_widget = QWidget()
                action_widget.setLayout(action_layout)

                self.table.setCellWidget(row_position, 2, action_widget)

    def preview_rename(self):
        start_number = int(self.start_number_entry.text())
        base_name = self.base_name_entry.text()
        for index in range(self.table.rowCount()):
            old_name = self.table.item(index, 0).text()
            _, file_extension = os.path.splitext(old_name)
            new_name = f"{base_name}{str(start_number + index).zfill(2)}{file_extension}"
            if self.table.item(index, 1):
                self.table.item(index, 1).setText(new_name)
            else:
                self.table.setItem(index, 1, QTableWidgetItem(new_name))

    def rename_files(self):
        for index in range(self.table.rowCount()):
            old_name = self.table.item(index, 0).text()
            new_name = self.table.item(index, 1).text()
            os.rename(os.path.join(self.folder_path, old_name), os.path.join(self.folder_path, new_name))
        self.table.setRowCount(0)
        QMessageBox.information(self, "Succès", "Les fichiers ont été renommés avec succès!")

    def move_item(self, direction):
        current_row = self.table.currentRow()
        next_row = current_row + direction
        if 0 <= next_row < self.table.rowCount():
            for col in range(self.table.columnCount()):
                current_item = self.table.takeItem(current_row, col)
                next_item = self.table.takeItem(next_row, col)
                self.table.setItem(next_row, col, current_item)
                self.table.setItem(current_row, col, next_item)
            self.table.setCurrentCell(next_row, self.table.currentColumn())

    def reset_table(self):
        self.table.setRowCount(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileRenamer()
    sys.exit(app.exec_())