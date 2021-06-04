import sys
import os

from mv.todolist import TodoListModel, TodoListViewDelegate, TodoListView
from PySide2.QtCore import QStandardPaths
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        cache_dir = os.path.normpath(QStandardPaths.standardLocations(QStandardPaths.AppDataLocation).pop(0))
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        self.cachefile = os.path.join(cache_dir, 'todolist_cache.json')
        self.setupUI()


    def setupUI(self):
        self.createWidgets()
        self.createLayout()

        mainWidget = QWidget(self)
        mainWidget.setObjectName("mainWidget")
        mainWidget.setLayout(self.layout)

        self.setMinimumSize(600, 300)
        self.setWindowTitle('[King] Todo list test')
        self.setCentralWidget(mainWidget)


    def createWidgets(self):
        self.label = QLabel('My TODO list:')
        self.button = QPushButton('Add item')

        # Todo list view
        self.delegate = TodoListViewDelegate()
        self.model = TodoListModel(self.cachefile)
        self.todolist_view = TodoListView()
        self.todolist_view.setModel(self.model)
        self.todolist_view.setItemDelegate(self.delegate)

        self.button.clicked.connect(self.add)


    def createLayout(self):
        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(self.button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.todolist_view)


    def add(self):
        new_idx = self.model.appendTask()
        self.todolist_view.edit(new_idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
