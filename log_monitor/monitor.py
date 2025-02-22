import csv
from datetime import datetime

from .models import Task


class LogMonitor:
    """
    Process a log file to track task execution times
    """

    def __init__(self):
        # Logs file location
        self.log_file = "logs.log"

        # Dictionary to store processing tasks: { PID: Task Object }
        self.tasks: dict[int, Task] = {}

        # List to store completed tasks
        self.completed_tasks: list[Task] = []

    def parse_log(self) -> None:
        """
        Read log file and extract task details.

        Log Structure:
        - Timestamp (HH:MM:SS)
        - Task description
        - Task status (START, END)
        - Task PID
        """
        with open(self.log_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                # Strip whitespace from each field in the row
                # e.g. ` START` > `START`
                timestamp, description, status, pid = map(str.strip, row)

                # Convert PID to an integer and timestamp to datetime object
                pid = int(pid)
                timestamp = datetime.strptime(timestamp, "%H:%M:%S")

                # identify task status
                if status == "START":
                    # Create a new task entry when a task starts
                    self.tasks[pid] = Task(
                        pid=pid,
                        start_time=timestamp,
                        description=description,
                    )

                elif status == "END":
                    # Check if the task exists, mark it as completed
                    # Otherwise create a new dangling Task
                    if pid in self.tasks:
                        task = self.tasks.pop(pid)
                        task.end(timestamp)
                    else:
                        task = Task(
                            pid=pid,
                            end_time=timestamp,
                            description=description,
                        )
                    self.completed_tasks.append(task)

                    # Print the completed task
                    print(task)

            # Print any tasks that started but never finished
            for task in self.tasks.values():
                if task.duration is None:
                    print(task)

    def generate_report(self):
        """
        Generate task report and save to report file.
        Report will include only the task that contian remarks.
        """
        with open("report.txt", "w") as file:
            for task in [c for c in self.completed_tasks if c.has_remark()]:
                file.write(str(task) + "\n")
