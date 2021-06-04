import os

from todolist import TodoList
from PySide2.QtWidgets import QListView, QStyledItemDelegate
from PySide2.QtCore import QAbstractListModel, Qt, QModelIndex

class TodoListModel(QAbstractListModel):
    def __init__(self, cachefile):
        super(TodoListModel, self).__init__()

        if not os.path.exists(cachefile):
            with open(cachefile, 'w+') as fp: pass

        self.todoList = TodoList()
        self.fp = open(cachefile, 'r+')
        self.todoList.load(self.fp)


    def rowCount(self, index=QModelIndex()):
        return self.todoList.count()


    def data(self, index, role):
        task = self.todoList.getTask(index.row())
        if task is None:
            return

        if role in (Qt.DisplayRole, Qt.EditRole):
            return task.title
        elif role == Qt.CheckStateRole:
            return Qt.Checked if task.done else Qt.Unchecked


    def setData(self, index, value, role):
        task = self.todoList.getTask(index.row())
        if task is None:
            return False

        if role == Qt.CheckStateRole:
            task.done = True if value == Qt.Checked else False
            self.dataChanged.emit(index, index)
            self.save()
            return True
        elif role == Qt.EditRole:
            if not value:
                self.removeRows(index.row(), 1)
                return False
            else:
                task.title = value
                self.dataChanged.emit(index, index)
                self.save()
                return True

        return False


    def flags(self, index):
        return super(TodoListModel, self).flags(index) | Qt.ItemIsEditable | Qt.ItemIsUserCheckable


    def insertRows(self, position, n, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+n-1)
        while n > 0:
            self.todoList.addTask(position)
            n -= 1
        self.endInsertRows()

        return True


    def removeRows(self, position, n, parent=QModelIndex()):
        end_idx = position + n - 1
        self.beginRemoveRows(parent, position, end_idx)
        status = self.todoList.removeTasks(position, end_idx + 1)
        self.save()
        self.endRemoveRows()

        return status


    def appendTask(self):
        idx = self.rowCount()
        self.insertRows(idx, 1)
        return self.index(idx, 0, QModelIndex())


    def save(self):
        self.fp.seek(0)
        self.todoList.dump(self.fp)
        self.fp.truncate()


class TodoListViewDelegate(QStyledItemDelegate):
    def __init__(self):
        super(TodoListViewDelegate, self).__init__()


    def paint(self, painter, option, index):
        if index.data(Qt.CheckStateRole) == Qt.Checked:
            option.font.setItalic(True)
            option.font.setStrikeOut(True)
        super(TodoListViewDelegate, self).paint(painter, option, index)

    
class TodoListView(QListView):
    def __init__(self, *args, **kwargs):
        super(TodoListView, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            self.model().removeRows(self.currentIndex().row(), 1)
        else:
            super(TodoListView, self).keyPressEvent(event)
