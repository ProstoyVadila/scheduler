import datetime


# TODO: remove after refactoring

TASKS = [
    {
        "id": 1,
        "name": "Task 1",
        "description": "This is task 1",
        "cron": "0 * * * *",
        "command": "echo 'Task 1 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=1),
    },
    {
        "id": 2,
        "name": "Task 2",
        "description": "This is task 2",
        "cron": "0 * * * *",
        "command": "echo 'Task 2 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=2),
    },
    {
        "id": 3,
        "name": "Task 3",
        "description": "This is task 3",
        "cron": "0 * * * *",
        "command": "echo 'Task 3 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=3),
    },
    {
        "id": 4,
        "name": "Task 4",
        "description": "This is task 4",
        "cron": "0 * * * *",
        "command": "echo 'Task 4 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=5),
    },
    {
        "id": 5,
        "name": "Task 5",
        "description": "This is task 5",
        "cron": "0 * * * *",
        "command": "echo 'Task 5 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=25),
    },
    {
        "id": 6,
        "name": "Task 6",
        "description": "This is task 6",
        "cron": "0 * * * *",
        "command": "echo 'Task 6 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=30),
    },
    {
        "id": 7,
        "name": "Task 7",
        "description": "This is task 7",
        "cron": "0 * * * *",
        "command": "echo 'Task 7 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=35),
    },
    {
        "id": 8,
        "name": "Task 8",
        "description": "This is task 8",
        "cron": "0 * * * *",
        "command": "echo 'Task 8 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=40),
    },
    {
        "id": 9,
        "name": "Task 9",
        "description": "This is task 9",
        "cron": "0 * * * *",
        "command": "echo 'Task 9 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=45),
    },
    {
        "id": 10,
        "name": "Task 10",
        "description": "This is task 10",
        "cron": "0 * * * *",
        "command": "echo 'Task 10 executed'",
        "next_run": datetime.datetime.now() + datetime.timedelta(minutes=50),
    },
]
