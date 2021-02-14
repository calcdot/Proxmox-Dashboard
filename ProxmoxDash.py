#!/usr/bin/python3

#==============================================
# Description:
#  Raspi proxmox controll panel
#
# Author:
#  Slaven Vukcevic
#==============================================

import sys
import time
import requests
from PyQt5 import QtWidgets

# Request URL/Parameters
proxURL = 'https://proxmox.example.local:8006/api2/json/nodes/<server>/qemu/'
params = {'Authorization': 'PVEAPIToken=<user>@<realm>!<type>=<token>'}

# Main Function
def main():
    data1, data2, data3, datasorted = [], [], [], []
    rest = requests.get(proxURL, headers=params, verify=False).json()
    alist = rest['data']

    for i in alist:
        res = [i['name'], i['vmid'], i['status']]
        for ii in range(1):
            datasorted.append(res)

    datasortedOP = sorted(datasorted, key=lambda x: x[1])
    for machine in datasortedOP:
        data1.append(machine[0])
        data2.append(machine[1])
        data3.append(machine[2])

# Drawing Table
    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, parent=None):
            QtWidgets.QMainWindow.__init__(self, parent)
            self.setStyleSheet('font-size: 16px')
            self.table = QtWidgets.QTableWidget()
            self.table.setColumnCount(6)
            self.setCentralWidget(self.table)
            self.table.setRowCount(len(data1))

            for index in range(len(data1)):
                item1 = QtWidgets.QTableWidgetItem(data1[index])
                self.table.setItem(index, 0, item1)
                item2 = QtWidgets.QTableWidgetItem(data2[index])
                self.table.setItem(index, 1, item2)
                item3 = QtWidgets.QTableWidgetItem(data3[index])
                self.table.setItem(index, 2, item3)

                self.btn_sell = QtWidgets.QPushButton('Reboot')
                self.btn_sell.clicked.connect(self.handleButtonClicked)
                self.table.setCellWidget(index, 3, self.btn_sell)

                self.btn_sell = QtWidgets.QPushButton('Stop')
                self.btn_sell.clicked.connect(self.handleButtonClicked)
                self.table.setCellWidget(index, 4, self.btn_sell)

                self.btn_sell = QtWidgets.QPushButton('Start')
                self.btn_sell.clicked.connect(self.handleButtonClicked)
                self.table.setCellWidget(index, 5, self.btn_sell)

# Tracking buttton click
        def handleButtonClicked(self):
            button = QtWidgets.qApp.focusWidget()
            index = self.table.indexAt(button.pos())
            if index.isValid():
                choice = (index.row(), index.column())
                if choice[1] == 5:
                    decid = 'start'
                elif choice[1] == 4:
                    decid = 'stop'
                else:
                    decid = 'reboot'
                self.UpdateTable(choice, decid)

# Updating table
        def UpdateTable(self, choice, decid):
            vmid = data2[choice[0]]
            requests.post(proxURL + vmid + '/status/' + decid, headers=params, verify=False).json()
            time.sleep(5)
            current = requests.get(proxURL + vmid + '/status/current', headers=params, verify=False).json()
            crt = current['data']['status']
            cellupdate = QtWidgets.QTableWidgetItem(crt)
            self.table.setItem(choice[0], 2, cellupdate)

# After main rest call is made, following functions are called
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()

main()
