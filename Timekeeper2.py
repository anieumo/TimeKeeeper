import sys
import os
import csv

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# everyday needs its own csv file to write and update to
# and to call data from on open

_SAVEPATH = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")

        self.calendar = QCalendarWidget(self)
        self.calendar.selectionChanged.connect(self.createDate)
        today = self.calendar.selectedDate()
        self.selecteddaypreviuos = today
        self.calendar.setMaximumDate(today)

        self.date = self.calendar.selectedDate()
        # date = QDate.getDate(self.date)
        # date = str(date)
        date = self.date.toString("dd.MM.yyy")
        # date = date.replace(", ", ".")
        date = date[1:11]
        self.date = "Timecard." + date + ".csv"
        print(self.date)
        self.savepath = "/Users/aniediumoren/Desktop/TimecardKeeper/"
        self.path = os.path.join(self.savepath, self.date)

        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        i = 0
        for i in range(5):
            self.table.setItem(0,i, QTableWidgetItem("0"))

        self.table.cellChanged.connect(self.addHours)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(['Project', 'Task', 'Hours', 'Completed?', 'Note'])
        self.table.itemChanged.connect(self.addHours)

        self.table.show()
        
        self.loadCSV = QPushButton('Load CSV Data In')
        self.loadCSV.clicked.connect(self.loadcsvdata)
        self.exportbutton = QPushButton('Export to Excel')
        self.exportbutton.clicked.connect(self.exportAsCSV)
        self.addRowButton = QPushButton('+')
        self.addRowButton.setFixedWidth(40)
        self.addRowButton.clicked.connect(self.addRow)
        self.removeRowButton = QPushButton('-')
        self.removeRowButton.clicked.connect(self.removeSelectedRow)
        self.removeRowButton.setFixedWidth(40)
        self.label = QLabel()
        self.label.setText("User Daily Total:")
        self.hourslabel = QLabel()
        self.hourslabel.setText("0.0")
        self.menubar = QMenuBar()
        refreshAction = QAction("Refresh")
        refreshAction.triggered.connect(self.refreshQTable)
        refreshAction.setShortcut('Ctrl+O')
        fileMenu = self.menubar.addMenu('File')
        fileMenu.addAction(refreshAction)
        

        self.horizontallayout = QHBoxLayout()

        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.exportbutton)
        self.layout.addWidget(self.loadCSV)
        self.layout.addLayout(self.horizontallayout)
        self.horizontallayout.addWidget(self.addRowButton)
        self.horizontallayout.addWidget(self.removeRowButton)
        self.horizontallayout.addWidget(self.label)
        self.horizontallayout.addWidget(self.hourslabel)
        self.horizontallayout.addWidget(self.label)

        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)
        self.resize(800, 500)

    def loadcsvdata(self, test):
        test = _SAVEPATH
        with open(test, 'r') as csvfile:
            reader = csv.reader(csvfile, dialect='excel', lineterminator='\n')
            for row in reader:
                end = int(row)
                print(int(row))
                for item in row[1:end]:
                    print(item)
                    num = 0
                    while num < 5:
                        self.table.setItem(0,num, QTableWidgetItem(item))
                        num = num + 1

    def resavepath(self):
        date = self.calendar.selectedDate()
        # qdate = QDate.getDate(date)
        # stringQDate = str(qdate)
        date.toString("dd.MM.yyy")
        # setDateFormat = stringQDate.replace(", ", ".")
        # setDateString = setDateFormat[1:11]
        setDateString = date[1:11]
        filename = "Timecard." + setDateString + ".csv"
        savePathHead = "/Users/aniediumoren/Desktop/TimecardKeeper/"
        savePath = os.path.join(savePathHead, filename)
        _SAVEPATH = savePath

    def addHours(self):
        hourslist = []
        rowcount = self.table.rowCount()
        i = 0
        for i in range(rowcount):
            try:
                print(self.table.item(i, 2).text())
            except:
                return   
            hours = self.table.item(i,2).text()
            if hours.isdigit() == True:
                hoursint = float(hours)
                hourslist.append(hoursint)
            else:
                return
        sumtest = sum(hourslist)
        sumstr = str(sumtest)
        self.hourslabel.setText(sumstr)

    def updatelabel(self):
        self.hourslabel.setText(sumstr)

    def createDate(self):
        self.exportAsCSV()
     
        # grabs savepath
        if self.calendar.selectedDate():
            date = self.calendar.selectedDate()
            # qdate = QDate.getDate(date)
            # stringQDate = str(qdate)
            setDateFormat = date.toString("dd.MM.yyyy")
            # setDateFormat = stringQDate.replace(", ", ".")
            # setDateString = setDateFormat[1:11]
            # *** grab selected date name
            filename = "Timecard." + setDateFormat + ".csv"
            print(filename)
            savePathHead = "/Users/aniediumoren/Desktop/TimecardKeeper/"
            savePath = os.path.join(savePathHead, filename)
            _SAVEPATH = savePath
            print(_SAVEPATH)
            self.selecteddaypreviuos = date
            # reset this varable to use later
            print(self.selecteddaypreviuos)

        # imports any saved data
            test = _SAVEPATH
            if not os.path.exists(_SAVEPATH):
                i = 0
                rowcount = self.table.rowCount()
                for i in range(rowcount):
                    self.table.removeRow(i)
                i = 0
                for i in range(5):
                    self.table.setItem(0,i, QTableWidgetItem("0"))

                return
            else:
                with open(test, 'r') as csvfile:
                    reader = csv.reader(csvfile, dialect='excel', lineterminator='\n')
                    itemlist = []
                    for row in reader:
                        for item in row:
                            print(item)
                            itemlist.append(item)

                    # sansheader = int(len(itemlist)/2)
                    sansheader = itemlist[5:len(itemlist)]
                    # data = itemlist[sansheader::1]
                    itemsToList = []
                    itemsToList.append(sansheader)
                    print(itemsToList)

                    rowcount = int(len(sansheader)/5)
                    columncount = 5
                    i = 0
                    j = 0
                    for item in sansheader:
                        for i in range(rowcount):
                            for j in range(columncount):
                                self.table.setItem(i,j, QTableWidgetItem(item))

                    # i = 0
                    # for i in range(sansheader):
                    #     self.table.setItem(0,i, QTableWidgetItem(item))
            # set header
            self.table.setHorizontalHeaderLabels(['Project', 'Task', 'Hours', 'Completed?', 'Note'])

    def exportAsCSV(self):
        # print(self.selecteddaypreviuos)
        # date = QDate.getDate(self.selecteddaypreviuos)
        # date = str(date)
        date = self.selecteddaypreviuos.toString("dd.MM.yyyy")
        print(date)
        # date = date.replace(", ", ".")
        # date = date[1:11]
        self.date = "Timecard." + date + ".csv"
        self.savepath = "/Users/aniediumoren/Desktop/TimecardKeeper/"
        _SAVEPATH = os.path.join(self.savepath, self.date)

        path, ok = QFileDialog.getSaveFileName(
            self, 'Save CSV', _SAVEPATH, 'CSV(*.csv)')
        if ok:
            columns = range(self.table.columnCount())
            header = [self.table.horizontalHeaderItem(column).text()
                    for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(
                    csvfile, dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(self.table.rowCount()):
                    writer.writerow(
                        self.table.item(row, column).text()
                        for column in columns)
            print(_SAVEPATH + " saved")
        if not path:
            print(_SAVEPATH + " not saved")
            return
        # catch cancel case

    def addRow(self):
        rowcount = self.table.rowCount()
        self.table.insertRow(rowcount)

        i = 0
        for i in range(5):
            self.table.setItem(rowcount,i, QTableWidgetItem("0"))
            print(self.table.item(rowcount,i).text())

    def removeSelectedRow(self):
        self.table.removeRow(self.table.rowCount())

    def refreshQTable(self):
        rowcount = self.table.rowCount()
        for i in range(5):
            self.table.setItem(rowcount,i, QTableWidgetItem("0"))



def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__=='__main__':
    run()
