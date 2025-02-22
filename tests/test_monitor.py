import unittest
from unittest.mock import mock_open, patch

from log_monitor.monitor import LogMonitor


class TestLogMonitor(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""11:00:00, Task 100, START, 100
11:30:00, Task 101, START, 101
11:32:00, Task 101, END, 101
11:35:00, Task 102, START, 102
11:50:00, Task 103, START, 103
11:55:00, Task 103, END, 103
11:45:00, Task 102, END, 102
12:00:00, Task 104, END, 104""",
    )
    def test_parse_log(self, mock_file):
        monitor = LogMonitor()
        monitor.parse_log()

        # Assert completed tasks
        self.assertEqual(len(monitor.completed_tasks), 4)
        self.assertEqual(monitor.completed_tasks[0].pid, 101)
        self.assertEqual(monitor.completed_tasks[1].pid, 103)
        self.assertEqual(monitor.completed_tasks[2].pid, 102)
        self.assertEqual(monitor.completed_tasks[3].pid, 104)

        # Assert unfinished tasks (task 100 start but no end)
        self.assertEqual(len(monitor.tasks), 1)
        self.assertEqual(list(monitor.tasks.keys()), [100])


if __name__ == "__main__":
    unittest.main()
