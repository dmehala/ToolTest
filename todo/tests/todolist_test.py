# Workdaround to import check_headers module
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
todo_dir = os.path.normpath(os.path.join(currentdir, ".."))
sys.path.insert(0, todo_dir)

import tempfile
import unittest as ut
from todolist import Task, TodoList

EMPTY_TASK = Task(title='', done=False)
TMPFILE_NTASKS = 7
CONTENT_TMPFILE = """[
{"title": "Remove items from the list", "status": "done"},
{"title": "Get focus on added item", "status": "done"},
{"title": "Press enter to edit an item", "status": "done"},
{"title": "More efficient state persistence", "status": "ongoing"},
{"title": "Write test", "status": "ongoing"},
{"title": "Organize code to be cleaner", "status": "done"},
{"title": "Esc on empty task -> delete", "status": "ongoing"}
]
"""

class TodoListTest(ut.TestCase):
    def test_default_init(self):
        todos = TodoList()
        self.assertEqual(0, todos.count())


    def test_count(self):
        todos = TodoList()
        todos.addTask(0)
        todos.addTask(0)
        todos.addTask(0)
        todos.addTask(0)
        todos.addTask(0)

        self.assertEqual(5, todos.count())


    def test_getTask(self):
        todos = TodoList()
        self.assertEqual(None, todos.getTask(0))


    def test_addTasks(self):
        t1 = Task(title="foo", done=False)
        t2 = Task(title="bar", done=True)

        todos = TodoList()
        todos.addTask(0, t1)
        todos.addTask(0, t2) #< prepend
        todos.addTask(2)

        self.assertTrue(3 == todos.count())
        self.assertEqual(t1, todos.getTask(1))
        self.assertEqual(t2, todos.getTask(0))
        self.assertEqual(EMPTY_TASK, todos.getTask(2))


    def test_load(self):
        todos = TodoList()

        with tempfile.TemporaryFile(mode='w+') as fp:
            fp.write(CONTENT_TMPFILE)
            fp.seek(0)

            todos.load(fp)

        self.assertEqual(TMPFILE_NTASKS, todos.count())
        self.assertEqual(Task(title="Remove items from the list", done=True), todos.getTask(0))
        self.assertEqual(Task(title="Get focus on added item", done=True), todos.getTask(1))
        self.assertEqual(Task(title="Press enter to edit an item", done=True), todos.getTask(2))
        self.assertEqual(Task(title="More efficient state persistence", done=False), todos.getTask(3))
        self.assertEqual(Task(title="Write test", done=False), todos.getTask(4))
        self.assertEqual(Task(title="Organize code to be cleaner", done=True), todos.getTask(5))
        self.assertEqual(Task(title="Esc on empty task -> delete", done=False), todos.getTask(6))


    def test_dump_then_load(self):
        dumped_todos = TodoList()
        dumped_todos.addTask(0, Task(title="bar", done=True))
        dumped_todos.addTask(1, Task(title="foo", done=False))

        loaded_todos = TodoList()

        with tempfile.TemporaryFile(mode='w+') as fp:
            dumped_todos.dump(fp)

            fp.seek(0)
            loaded_todos.load(fp)

        self.assertEqual(loaded_todos.count(), dumped_todos.count())
        i = loaded_todos.count()
        while i >= 0:
            self.assertEqual(loaded_todos.getTask(i), dumped_todos.getTask(i))
            i -= 1


    def test_removeTask(self):
        todos = TodoList()
        todos.addTask(0, Task(title="Prepare meeting notes", done=True))
        todos.addTask(1, Task(title="Merge feature branch of my tool", done=False))
        todos.addTask(2, Task(title="Interview meeting for the tech test", done=False))
        todos.addTask(3, Task(title="Foo", done=False))
        todos.addTask(4, Task(title="Bar", done=False))

        self.assertEqual(5, todos.count())
        self.assertFalse(todos.removeTasks(10,5))
        self.assertTrue(todos.removeTasks(3,5))
        self.assertEqual(3, todos.count())
        self.assertEqual(Task(title="Prepare meeting notes", done=True), todos.getTask(0))
        self.assertEqual(Task(title="Merge feature branch of my tool", done=False), todos.getTask(1))
        self.assertEqual(Task(title="Interview meeting for the tech test", done=False), todos.getTask(2))


