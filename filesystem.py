import sys
from os import listdir
from os.path import isdir, join
from pathlib import Path

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

class FileSystem(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("FileSystem")
        self.setFixedWidth(800)
        self.setFixedHeight(500)
        self.tree = QTreeWidget()
        self.list = []
        self.completion_tree()
        self.home()


    def completion_tree(self):
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 400)
        self.tree.setHeaderLabels(['FileSystem', 'Path'])
        home = str(Path.home())
        root = QTreeWidgetItem(self.tree)
        root.setText(0, home)
        self.traversing_directories(home, root)


    def traversing_directories(self, path, parent):
        for name in listdir(path):
            child = QTreeWidgetItem()
            child.setText(0, name)
            child.setText(1, path)
            parent.addChild(child)
            if isdir(join(path, name)):
                self.traversing_directories(join(path, name), child)


    def search(self):
        self.tree.collapseAll()
        brush = QtGui.QBrush(Qt.white)
        if self.list:
            for i in self.list:
                i.setBackground(0, brush)
        text = self.lineedit.text()
        if text:
            self.list = self.tree.findItems(text, Qt.MatchRecursive | Qt.MatchContains, 0)
            brush = QtGui.QBrush(Qt.blue)
            if not self.list:
                self.error_label.setText("Nothing was found for this query")
            for i in self.list:
                i.setBackground(0, brush)
                while i.parent():
                    self.tree.expandItem(i.parent())
                    i = i.parent()
        else:
             self.error_label.setText("Empty query")


    def home(self):
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.tree)
        self.lineedit = QtWidgets.QLineEdit()
        button = QtWidgets.QPushButton("Search")
        button.setFixedSize(100, 40)
        button.clicked.connect(self.search)
        label = QtWidgets.QLabel("Search:")
        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("color: red;")
        vbox.addWidget(label)
        vbox.addWidget(self.lineedit)
        vbox.addWidget(self.error_label)
        vbox.addWidget(button, alignment = Qt.AlignCenter)
        self.setLayout(vbox)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = FileSystem()
    window.show()
    sys.exit(app.exec_())
