import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Task:
    __slots__ = ['title', 'done']
    title: str
    done: bool

def as_task(d: Dict[str, str]) -> Task:
    if 'status' in d and 'title' in d:
        return Task(title=d['title'], done=True if d['status'] == 'done' else False)
    return d


def task_to_dict(task: Task) -> Dict[str, str]:
    d = dict()
    d['title'] = task.title
    d['status'] = 'done' if task.done else 'ongoing'
    return d

class TodoList:
    def __init__(self, tasks: List[Task] = None) -> None:
        self.tasks = tasks if tasks is not None else list()


    def load(self, fp) -> None:
        try:
            self.tasks = [x for x in json.load(fp, object_hook=as_task) if isinstance(x, Task)]
        except json.JSONDecodeError:
            pass


    def dump(self, fp) -> None:
        l = [task_to_dict(x) for x in self.tasks]
        json.dump(l, fp)


    def count(self) -> int:
        return len(self.tasks)


    def getTask(self, index) -> Task:
        try:
            return self.tasks[index]
        except IndexError:
            return None

    
    def addTask(self, idx: int, task: Task=None) -> bool:
        task = Task(title='', done=False) if task is None else task
        self.tasks.insert(idx, task)
        return True


    def removeTasks(self, beg: int, end: int) -> bool:
        if beg >= len(self.tasks):
            return False

        del self.tasks[beg:end]
        return True