import unittest
from datetime import datetime, timedelta
from log_monitor.models import Task


class TestTaskModel(unittest.TestCase):

    def setUp(self):
        self.pid = 12345
        self.description = "Task Description"
        self.start_time = datetime.strptime("10:00:00", "%H:%M:%S")
        self.end_time = self.start_time + timedelta(minutes=2)
        self.task = Task(
            pid=self.pid,
            description=self.description,
            start_time=self.start_time,
        )

    def test_create_task(self):
        task = self.task
        self.assertEqual(task.pid, self.pid)
        self.assertEqual(task.description, self.description)
        self.assertEqual(task.start_time, self.start_time)
        self.assertIsNone(task.end_time)
        self.assertIsNone(task.duration)

    def test_create_task_given_only_end_time(self):
        task = Task(
            pid=self.pid,
            description=self.description,
            end_time=self.end_time,
        )
        self.assertEqual(task.pid, self.pid)
        self.assertEqual(task.description, self.description)
        self.assertIsNone(task.start_time)
        self.assertEqual(task.end_time, self.end_time)
        self.assertIsNone(task.duration)

    def test_end_task(self):
        task = self.task
        task.end(self.end_time)

        self.assertEqual(task.end_time, self.end_time)
        self.assertEqual(task.duration, self.end_time - self.start_time)

    def test_get_status_processing(self):
        task = self.task
        self.assertEqual(task.get_status(), "Processing")

    def test_get_status_completed(self):
        task = self.task
        task.end(self.start_time + timedelta(minutes=2))
        self.assertEqual(task.get_status(), "Completed")

    def test_get_remark_given_complete_task_should_return_empty(self):
        task = Task(
            pid=self.pid,
            description=self.description,
            start_time=self.start_time,
        )
        task.end(self.end_time)
        self.assertEqual(task.get_remark(), "")

    def test_get_remark_given_5_minutes_task_should_return_empty(self):
        task = Task(
            pid=self.pid,
            description=self.description,
            start_time=self.start_time,
        )
        task.end(self.start_time + timedelta(minutes=5))
        self.assertEqual(task.get_remark(), "")

    def test_get_remark_no_start_time(self):
        task = Task(
            pid=self.pid,
            description=self.description,
            start_time=None,
            end_time=self.end_time,
        )
        self.assertEqual(
            task.get_remark(),
            "WARNING: Task start time not found.",
        )

    def test_get_remark_task_in_progress(self):
        task = self.task
        self.assertEqual(
            task.get_remark(),
            "WARNING: Task is still in progress.",
        )

    def test_get_remark_task_longer_than_5_minutes(self):
        task = self.task
        task.end(self.start_time + timedelta(minutes=5, microseconds=1))
        self.assertEqual(
            task.get_remark(),
            "WARNING: This task took longer than 5 minutes.",
        )

    def test_get_remark_task_longer_than_10_minutes(self):
        task = self.task
        task.end(self.start_time + timedelta(minutes=10, microseconds=1))
        self.assertEqual(
            task.get_remark(),
            "ERROR: This task took longer than 10 minutes.",
        )

    def test_task_no_remark(self):
        task = self.task
        task.end(self.end_time)
        self.assertFalse(task.has_remark())

    def test_task_has_remark_given_warning_task(self):
        task = self.task
        task.end(self.start_time + timedelta(minutes=6))
        self.assertTrue(task.has_remark())

    def test_task_has_remark_given_error_task(self):
        task = self.task
        task.end(self.start_time + timedelta(minutes=10))
        self.assertTrue(task.has_remark())


if __name__ == "__main__":
    unittest.main()
