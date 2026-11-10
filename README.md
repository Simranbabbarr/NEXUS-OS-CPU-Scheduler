# NEXUS OS – Interactive CPU Scheduling Simulator

## Overview

NEXUS OS is an interactive CPU Scheduling Simulator developed using Python and Streamlit. The application demonstrates the working of fundamental CPU scheduling algorithms and provides a visual representation of process execution, scheduling performance, and evaluation metrics.

The project aims to simplify the understanding of CPU scheduling concepts through an interactive dashboard and graphical analysis.

## Features

- **Multiple Scheduling Algorithms:** Implements First Come First Serve (FCFS), Shortest Job First (SJF – Non-Preemptive), and Round Robin (RR).
- **Process Management:** Allows users to configure process IDs, arrival times, and burst times.
- **Gantt Chart Visualization:** Displays the execution sequence of processes.
- **Performance Metrics:** Calculates Completion Time, Turnaround Time, Waiting Time, and Response Time.
- **Algorithm Comparison:** Enables users to compare scheduling algorithms based on their performance.
- **Interactive Dashboard:** Provides a centralized interface for simulation, analytics, and learning.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing and tabular representation |
| Plotly | Data visualization and Gantt charts |

## Scheduling Algorithms Implemented

### 1. First Come First Serve (FCFS)
A non-preemptive scheduling algorithm in which processes are executed in the order of their arrival.

### 2. Shortest Job First (SJF)
A non-preemptive scheduling algorithm that selects the available process with the shortest burst time.

### 3. Round Robin (RR)
A preemptive scheduling algorithm that allocates CPU time to each process for a fixed time quantum.

## Performance Metrics

The simulator calculates the following parameters:

- **Completion Time (CT):** Time at which a process finishes execution.
- **Turnaround Time (TAT):** Total time taken from arrival to completion.
- **Waiting Time (WT):** Total time a process spends waiting in the ready queue.
- **Response Time (RT):** Time between process arrival and its first CPU execution.

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/NEXUS-OS-CPU-Scheduler.git
```

### Navigate to the Project Directory

```bash
cd NEXUS-OS-CPU-Scheduler
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## Project Structure

```text
NEXUS-OS-CPU-Scheduler/
│
├── app.py
├── requirements.txt
└── README.md
```

## Learning Outcomes

- Understanding CPU scheduling concepts and algorithms.
- Implementing scheduling techniques using Python.
- Analyzing process execution and scheduling performance.
- Working with interactive dashboards and data visualization.
- Comparing scheduling algorithms using quantitative metrics.

## Future Enhancements

- Implementation of Priority Scheduling.
- Implementation of Shortest Remaining Time First (SRTF).
- Support for Multilevel Queue Scheduling.
- Advanced scheduling performance analytics.
- Exportable simulation reports.

## Author

Simran Babbar

B.Tech – Computer Science and Engineering (Artificial Intelligence and Machine Learning)

## License

This project is developed for academic and educational purposes.
