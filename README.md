# Log Monitoring Application

## Overview

This application processes log files to track the execution times of tasks.
Application will calculate task durations and generate report file with logs warning or error of the task that have duration exceed defined thresholds.

## Features

- Task Monitoring: Identify tasks with PID.
- Task Duration Calculation: Calculates task durations from a pair of tasks (start and end).
- Show Warnings and Errors:
  - Flags tasks that exceed 5 minutes with a warning
  - Flags tasks that exceed 10 minutes with an error.
  - Flags tasks that never closed with a warning (this task may be in progress).
  - Flags tasks that found only closed event with a warning.
- Reports: Generate a report file that list tasks with warning or error.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/peeexpand/log-monitor.git
   ```

2. Run application (no need to install any library)

   ```bash
   python main.py
   ```

## Running Tests

```bash
python -m unittest discover tests
```

## Usage

1. Replace your log file to `logs.log`.
2. Run the LogMonitor class to parse the log file:

   ```python
   from log_monitor.monitor import LogMonitor

   monitor = LogMonitor()
   monitor.parse_log()
   monitor.generate_report()
   ```

   or you can run

   ```bash
   python main.py
   ```

3. The application will generate a report (`report.txt`) containing details of tasks that have warning or error.

   Example of data in file `report.txt`

   ```log
   [39547] Task Completed | Start: 11:37:53 | End: 11:49:22 | Duration: 0:11:29 ERROR: This task took longer than 10 minutes.
   [45135] Task Completed | Start: 11:37:14 | End: 11:49:37 | Duration: 0:12:23 ERROR: This task took longer than 10 minutes.
   [71766] Task Completed | Start: 11:45:04 | End: 11:50:51 | Duration: 0:05:47 WARNING: This task took longer than 5 minutes.
   [81258] Task Completed | Start: 11:36:58 | End: 11:51:44 | Duration: 0:14:46 ERROR: This task took longer than 10 minutes.
   ```
