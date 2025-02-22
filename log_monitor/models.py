from datetime import datetime, timedelta


class Task:
    """
    Task model represents a task with start and end, and computes duration.
    """

    def __init__(
        self,
        pid: int,
        description: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ):
        """
        Args:
            pid (int): Task Process ID.
            description (str): Task description.
            start_time (datetime | None, optional): Start time of the task.
            end_time (datetime | None, optional): End time of the task.
        """
        self.pid = pid
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.duration = None

    def end(self, end_time: datetime) -> None:
        """
        Mark task as completed and calculates duration.

        Args:
            end_time (datetime): Time when task ended.
        """
        self.end_time = end_time
        self.duration = self.end_time - self.start_time

    def get_status(self) -> str:
        """
        Return status of the task.
        """
        if self.duration is not None:
            return "Completed"
        else:
            return "Processing"

    def get_remark(self) -> str:
        """
        Return task remark (Warning and Error)
        """
        if self.start_time is None:
            return "WARNING: Task start time not found."
        elif self.end_time is None:
            return "WARNING: Task is still in progress."
        elif self.duration > timedelta(minutes=10):
            return "ERROR: This task took longer than 10 minutes."
        elif self.duration > timedelta(minutes=5):
            return "WARNING: This task took longer than 5 minutes."
        else:
            return ""

    def has_remark(self) -> str:
        return self.get_remark() != ""

    def __str__(self) -> str:
        return (
            f"[{self.pid}] Task {self.get_status()} | "
            f"Start: {self.start_time.time() if self.start_time else None} | "
            f"End: {self.end_time.time() if self.end_time else None} | "
            f"Duration: {self.duration} "
            f"{self.get_remark()}"
        )
