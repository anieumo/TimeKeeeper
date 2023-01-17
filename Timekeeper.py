import sys
import os
import csv

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")

        self.calendar = QCalendarWidget(self)
        # self.calendar.selectionChanged.connect(self.createDate)
        today = self.calendar.selectedDate()
        self.selecteddaypreviuos = today
        self.calendar.setMaximumDate(today)

        self.calendar.selectionChanged.connect(self.changeddate)

        self.date = self.calendar.selectedDate()
        date = self.date.toString("dd.MM.yyyy")
        date = date[1:11]
        self.date = "Timecard." + date + ".csv"
        print(self.date)
        self.savepath = "/Users/aniediumoren/Desktop/TimecardKeeper/"
        self.path = os.path.join(self.savepath, self.date)

        self.model = QStandardItemModel(self)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QPushButton(self)
        self.pushButtonLoad.setText("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.loadCSVData)

        self.pushButtonWrite = QPushButton(self)
        self.pushButtonWrite.setText("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.exportCSVData)

        self.label = QLabel(self)
        self.label.setText("Hours Total:")
        
        self.hourslabel = QLabel(self)

        self.hoursButton = QPushButton(self)
        self.hoursButton.setText("add Hours")
        self.hoursButton.clicked.connect(self.addHours)

        self.addRowButton = QPushButton(self)
        self.addRowButton.setText("Add Row")
        self.addRowButton.clicked.connect(self.addRow)

        self.removeRowButton = QPushButton(self)
        self.removeRowButton.setText("Remove Top Row")
        self.removeRowButton.setToolTip('Remove top row')
        self.removeRowButton.clicked.connect(self.removeRow)

        self.removeSelectRowButton = QPushButton(self)
        self.removeSelectRowButton.setText("Remove Selected Row")
        self.removeSelectRowButton.setToolTip('Remove selected row')
        self.removeSelectRowButton.clicked.connect(self.removeSelectedRow)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.tableView)
        self.layout.addWidget(self.pushButtonLoad)
        self.layout.addWidget(self.pushButtonWrite)

        self.horizontallayout = QHBoxLayout()
        self.layout.addLayout(self.horizontallayout)
        # self.horizontallayout.addWidget(self.removeRowButton)
        self.horizontallayout.addWidget(self.label)
        self.horizontallayout.addWidget(self.hourslabel)
        self.horizontallayout.addWidget(self.hoursButton)
        self.horizontallayout.addWidget(self.addRowButton)
        self.horizontallayout.addWidget(self.removeRowButton)
        self.horizontallayout.addWidget(self.removeSelectRowButton)

        self.container = QWidget()

        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)
        self.resize(800, 500)

    def changeddate(self):
        self.tableView.clearSpans()
        rowcount = self.model.rowCount()
        print(rowcount)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Project', 'Task', 'Hours', 'Completed?', 'Note'])
        self.loadCSVData()

    def loadCSVData(self):
        # self.tableView.clearSpans()
        if self.calendar.selectedDate():
            date = self.calendar.selectedDate()
            setDateFormat = date.toString("dd.MM.yyyy")
            filename = "Timecard." + setDateFormat + ".csv"
            print(filename)
            savePathHead = "/Users/aniediumoren/Desktop/TimecardKeeper/"
            savePath = os.path.join(savePathHead, filename)
            _SAVEPATH = savePath
            print(_SAVEPATH)
            self.selecteddaypreviuos = date
            print(self.selecteddaypreviuos)

        # imports any saved data       
        if not os.path.exists(_SAVEPATH):
            return

        with open(_SAVEPATH, "r") as fileInput:
            reader = csv.reader(fileInput)
            list_of_column_names = []
            for row in reader:
                list_of_column_names.append(row)
                break
            print(list_of_column_names)

            for row in csv.reader(fileInput):
                items = [
                    QStandardItem(field)
                    for field in row
                ]
                print(items)

                self.model.setHorizontalHeaderLabels(['Project', 'Task', 'Hours', 'Completed?', 'Note'])
                self.model.appendRow(items)

    def exportCSVData(self):
        currentDate = self.calendar.selectedDate()
        date = currentDate.toString("dd.MM.yyyy")
        self.date = "Timecard." + date + ".csv"
        self.savepath = "/Users/aniediumoren/Desktop/TimecardKeeper/"
        _SAVEPATH = os.path.join(self.savepath, self.date)

        path, ok = QFileDialog.getSaveFileName(
            self, 'Save CSV', _SAVEPATH, 'CSV(*.csv)')
        if ok:
            columns = range(self.model.columnCount())
            header = [self.model.horizontalHeaderItem(column).text()
                    for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(
                    csvfile, dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(self.model.rowCount()):
                    writer.writerow(
                        self.model.item(row, column).text()
                        for column in columns)
            print(_SAVEPATH + " saved")
        if not path:
            print(_SAVEPATH + " not saved")
            return

    def addHours(self):
        hourslist = []
        rowcount = self.model.rowCount()
        print(rowcount)
        i = 0
        for i in range(rowcount):
            try:
                print(self.model.item(i, 2).text())
            except:
                return   
            hours = self.model.item(i,2).text()
            print(hours)
            if hours.isdigit() == True:
                hoursint = float(hours)
                hourslist.append(hoursint)
            else:
                return
        sumtest = sum(hourslist)
        sumstr = str(sumtest)
        self.hourslabel.setText(sumstr)

    def addRow(self):
        rowcount = self.model.rowCount()
        self.model.insertRow(rowcount)
        if self.model.columnCount() != 5:
            columncount = self.model.columnCount()
            self.model.insertColumns(columncount, 5)
        self.model.setHorizontalHeaderLabels(['Project', 'Task', 'Hours', 'Completed?', 'Note'])

    def removeRow(self):
        self.model.removeRow(0)

    def removeSelectedRow(self):
        selection = self.tableView.selectionModel().selectedRows()
        for index in sorted(selection):
            self.model.removeRow(index.row())


if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = MainWindow()
    main.show()
    app.exec()
    sys.exit()
