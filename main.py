import sys
from PyQt5.QtWidgets import * # (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import * # (QDateTime, Qt)
import pandas as pd

class MyTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)

        # Definícia hlavičiek
        self.headers = ["Číslo auta", "Príchod", "Príchod k pumpe", "Začiatok takovania", "Koniec tankovania",
                        "Príchod do rady na platenie", "Príchod na rad", "Dokončenie platby", "Príchod do auta",
                        "Čas odchodu"]
        # Ľahko pridáte ďalšie stĺpce pridaním do self.headers

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setRowCount(0)

        # Povoliť výber bunky
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setSelectionBehavior(QTableWidget.SelectItems)

        # Zobraziť mriežku
        self.setShowGrid(True)

        # Pripojenie signálu po kliknutí na bunku
        self.cellClicked.connect(self.cell_was_clicked)

    def cell_was_clicked(self, row, column):
        # Po kliknutí na bunku sa označí
        self.setCurrentCell(row, column)

    def keyPressEvent(self, event):
        key = event.key()
        current_row = self.currentRow()
        current_column = self.currentColumn()
        if key == Qt.Key_Space:
            # Zapísať aktuálny čas do označenej bunky
            if current_row >= 0 and current_column >= 0:
                current_time = QDateTime.currentDateTime().toString("hh:mm:ss yyyy-MM-dd")
                self.setItem(current_row, current_column, QTableWidgetItem(current_time))
                # Posunúť označenú bunku o jednu doprava (ak je to možné)
                if current_column + 1 < self.columnCount():
                    self.setCurrentCell(current_row, current_column + 1)
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            # Pridať nový riadok (nové auto) a zapísať aktuálny čas do stĺpca príchodu
            new_row = self.rowCount()
            self.insertRow(new_row)
            car_number = f"Auto {new_row + 1}"
            self.setItem(new_row, 0, QTableWidgetItem(car_number))
            current_time = QDateTime.currentDateTime().toString("hh:mm:ss yyyy-MM-dd")
            # Stĺpec príchodu je druhý stĺpec (index 1)
            self.setItem(new_row, 1, QTableWidgetItem(current_time))
            # Označiť bunku príchodu v novom riadku
            self.setCurrentCell(new_row, 2)
        elif key == Qt.Key_Left:
            if current_row >= 0 and current_column > 0:
                self.setCurrentCell(current_row, current_column - 1)
        elif key == Qt.Key_Right:
            if current_row >= 0 and current_column + 1 < self.columnCount():
                self.setCurrentCell(current_row, current_column + 1)
        elif key == Qt.Key_Up:
            if current_row > 0 and current_column >= 0:
                self.setCurrentCell(current_row - 1, current_column)
        elif key == Qt.Key_Down:
            if current_row + 1 < self.rowCount() and current_column >= 0:
                self.setCurrentCell(current_row + 1, current_column)
        else:
            super(MyTableWidget, self).keyPressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.table_widget = MyTableWidget()
        self.save_button = QPushButton('Uložiť')

        # Nastavenie rozloženia
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        # Načítanie dát z tabuľky
        rowCount = self.table_widget.rowCount()
        colCount = self.table_widget.columnCount()

        data = []
        for row in range(rowCount):
            rowData = []
            for column in range(colCount):
                item = self.table_widget.item(row, column)
                if item is not None:
                    rowData.append(item.text())
                else:
                    rowData.append('')
            data.append(rowData)

        # Konverzia na pandas DataFrame
        df = pd.DataFrame(data, columns=self.table_widget.headers)

        # Uloženie do Excel súboru
        file_name = 'data.xlsx'
        df.to_excel(file_name, index=False)
        print(f'Dáta boli uložené do {file_name}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())