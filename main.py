import sys
from PyQt5.QtWidgets import * # (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtCore import * # (QDateTime, Qt)
import pandas as pd

class MyTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)

        # Definícia hlavičiek
        self.headers = ["Číslo auta", "Príchod", "Príchod k pumpe", "Začiatok tankovania", "Koniec tankovania",
                        "Príchod do rady na platenie", "Príchod na rad", "Dokončenie platby", "Príchod do auta",
                        "Čas odchodu", "Čas príchodu do radu na kávu", "Príchod ku kávovaru", "Čas sadnutia si",
                        "Čas odchodu zo sadnutia"]

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setRowCount(0)

        # Nastavenie šírky každého stĺpca podľa nadpisu
        for i in range(len(self.headers)):
            self.resizeColumnToContents(i)

        # Povoliť výber bunky
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setSelectionBehavior(QTableWidget.SelectItems)

        # Zobraziť mriežku
        self.setShowGrid(True)

        # Pripojenie signálu po kliknutí na bunku
        self.cellClicked.connect(self.cell_was_clicked)

    def total_table_width(self):
        # Vráti celkovú šírku všetkých stĺpcov
        total_width = 0
        for i in range(self.columnCount()):
            total_width += self.columnWidth(i)
        return total_width

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
                current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
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
            current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
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
        self.file_name = None  # Premenná na uchovanie vybraného súboru

        # Nastavenie rozloženia
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        table_width = self.table_widget.total_table_width()
        self.resize(table_width + 40, 600)

        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        # Ak ešte nebol vybraný súbor alebo je názov neplatný, otvoríme dialóg na jeho výber
        if not self.file_name:
            self.file_name, _ = QFileDialog.getSaveFileName(self, "Uložiť do Excel súboru", "", "Excel Files (*.xlsx)")
            if not self.file_name:  # Ak užívateľ nezvolil súbor, vrátime sa
                return

        try:
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
            df.to_excel(self.file_name, index=False)
            print(f'Dáta boli uložené do {self.file_name}')

        except Exception as e:
            print(f"Chyba pri ukladaní: {e}")
            # Ak sa vyskytla chyba, nastavíme `self.file_name` na `None`, aby sa dialóg opäť otvoril
            self.file_name = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())