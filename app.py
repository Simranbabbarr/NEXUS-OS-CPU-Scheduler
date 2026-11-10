
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NEXUS OS | CPU Scheduler",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# THEME AND CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1120;
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background: #111b2e;
    border-right: 1px solid #26344d;
}

[data-testid="stSidebar"] * {
    color: #dbeafe;
}

h1, h2, h3 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

p, label {
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17243a, #111c30);
    border: 1px solid #293b58;
    padding: 20px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #60a5fa !important;
}

.stButton button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    min-height: 43px;
}

.stButton button:hover {
    background: #3b82f6;
    border: none;
}

[data-testid="stDataFrame"] {
    border: 1px solid #293b58;
    border-radius: 10px;
}

div[data-testid="stForm"] {
    background: #111c30;
    padding: 15px;
    border-radius: 12px;
}

hr {
    border-color: #293b58;
}

div[data-testid="stExpander"] {
    background: #142137;
    border: 1px solid #293b58;
    border-radius: 12px;
}

.small-text {
    color: #94a3b8;
    font-size: 13px;
}

.hero {
    background: linear-gradient(120deg, #172d50, #24235a);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #344c79;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 32px;
    margin-bottom: 5px;
}

.hero p {
    color: #bacce8;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "processes" not in st.session_state:
    st.session_state.processes = [
        {"PID": "P1", "Arrival Time": 0, "Burst Time": 5},
        {"PID": "P2", "Arrival Time": 1, "Burst Time": 3},
        {"PID": "P3", "Arrival Time": 2, "Burst Time": 8},
        {"PID": "P4", "Arrival Time": 3, "Burst Time": 6}
    ]

# ==========================================
# SCHEDULING ALGORITHMS
# ==========================================

def fcfs(processes):

    jobs = sorted(
        processes,
        key=lambda p: (p["Arrival Time"], p["PID"])
    )

    time = 0
    results = []
    chart = []

    for p in jobs:

        if time < p["Arrival Time"]:
            chart.append({
                "Process": "IDLE",
                "Start": time,
                "Finish": p["Arrival Time"]
            })
            time = p["Arrival Time"]

        start = time
        time += p["Burst Time"]

        chart.append({
            "Process": p["PID"],
            "Start": start,
            "Finish": time
        })

        tat = time - p["Arrival Time"]

        results.append({
            "PID": p["PID"],
            "Arrival Time": p["Arrival Time"],
            "Burst Time": p["Burst Time"],
            "Completion Time": time,
            "Turnaround Time": tat,
            "Waiting Time": tat - p["Burst Time"],
            "Response Time": start - p["Arrival Time"]
        })

    return results, chart


def sjf(processes):

    remaining = processes.copy()
    time = 0
    results = []
    chart = []

    while remaining:

        available = [
            p for p in remaining
            if p["Arrival Time"] <= time
        ]

        if not available:

            next_arrival = min(
                p["Arrival Time"] for p in remaining
            )

            chart.append({
                "Process": "IDLE",
                "Start": time,
                "Finish": next_arrival
            })

            time = next_arrival
            continue

        p = min(
            available,
            key=lambda x: (
                x["Burst Time"],
                x["Arrival Time"],
                x["PID"]
            )
        )

        start = time
        time += p["Burst Time"]

        chart.append({
            "Process": p["PID"],
            "Start": start,
            "Finish": time
        })

        tat = time - p["Arrival Time"]

        results.append({
            "PID": p["PID"],
            "Arrival Time": p["Arrival Time"],
            "Burst Time": p["Burst Time"],
            "Completion Time": time,
            "Turnaround Time": tat,
            "Waiting Time": tat - p["Burst Time"],
            "Response Time": start - p["Arrival Time"]
        })

        remaining.remove(p)

    return results, chart


def round_robin(processes, quantum):

    jobs = sorted(
        processes,
        key=lambda p: (p["Arrival Time"], p["PID"])
    )

    remaining = {
        p["PID"]: p["Burst Time"] for p in jobs
    }

    first_start = {}
    completion = {}
    queue = []
    chart = []

    time = 0
    next_job = 0

    while len(completion) < len(jobs):

        while (
            next_job < len(jobs)
            and jobs[next_job]["Arrival Time"] <= time
        ):
            queue.append(jobs[next_job])
            next_job += 1

        if not queue:

            next_arrival = jobs[next_job]["Arrival Time"]

            chart.append({
                "Process": "IDLE",
                "Start": time,
                "Finish": next_arrival
            })

            time = next_arrival
            continue

        p = queue.pop(0)
        pid = p["PID"]

        if pid not in first_start:
            first_start[pid] = time

        start = time
        execution = min(quantum, remaining[pid])

        time += execution
        remaining[pid] -= execution

        chart.append({
            "Process": pid,
            "Start": start,
            "Finish": time
        })

        while (
            next_job < len(jobs)
            and jobs[next_job]["Arrival Time"] <= time
        ):
            queue.append(jobs[next_job])
            next_job += 1

        if remaining[pid] > 0:
            queue.append(p)
        else:
            completion[pid] = time

    results = []

    for p in jobs:

        pid = p["PID"]
        ct = completion[pid]
        tat = ct - p["Arrival Time"]

        results.append({
            "PID": pid,
            "Arrival Time": p["Arrival Time"],
            "Burst Time": p["Burst Time"],
            "Completion Time": ct,
            "Turnaround Time": tat,
            "Waiting Time": tat - p["Burst Time"],
            "Response Time": first_start[pid] - p["Arrival Time"]
        })

    return results, chart


# ==========================================
# GANTT CHART
# ==========================================

def gantt_chart(chart, title):

    df = pd.DataFrame(chart)

    colors = {
        "P1": "#3B82F6",
        "P2": "#8B5CF6",
        "P3": "#06B6D4",
        "P4": "#10B981",
        "IDLE": "#64748B"
    }

    fig = go.Figure()

    for _, row in df.iterrows():

        duration = row["Finish"] - row["Start"]

        fig.add_trace(
            go.Bar(
                x=[duration],
                y=["CPU"],
                base=[row["Start"]],
                orientation="h",
                name=row["Process"],
                marker_color=colors.get(
                    row["Process"], "#F59E0B"
                ),
                text=[
                    f'{row["Process"]}<br>'
                    f'{row["Start"]}–{row["Finish"]}'
                ],
                textposition="inside",
                hovertemplate=(
                    f'<b>{row["Process"]}</b><br>'
                    f'Start: {row["Start"]}<br>'
                    f'Finish: {row["Finish"]}<br>'
                    f'Duration: {duration}<extra></extra>'
                )
            )
        )

    fig.update_layout(
        title=title,
        barmode="overlay",
        template="plotly_dark",
        paper_bgcolor="#111c30",
        plot_bgcolor="#111c30",
        font=dict(color="#e2e8f0"),
        xaxis=dict(
            title="CPU Timeline",
            rangemode="tozero",
            showgrid=True,
            gridcolor="#293b58"
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        height=220,
        showlegend=False,
        margin=dict(l=20, r=20, t=55, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# RESULT GENERATOR
# ==========================================

def generate_results(processes, quantum):

    output = {}

    for name, function in [
        ("FCFS", lambda: fcfs(processes)),
        ("SJF", lambda: sjf(processes)),
        ("Round Robin", lambda: round_robin(processes, quantum))
    ]:

        results, chart = function()
        df = pd.DataFrame(results)

        output[name] = {
            "results": df,
            "chart": chart,
            "waiting": df["Waiting Time"].mean(),
            "turnaround": df["Turnaround Time"].mean(),
            "response": df["Response Time"].mean()
        }

    return output


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="color:#60a5fa!important;">
        ⚡ NEXUS OS
        </h2>
        <p style="color:#94a3b8;font-size:12px;">
        CPU SCHEDULING MANAGEMENT SYSTEM
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "🏠 Dashboard",
            "🖥️ Process Manager",
            "⚙️ Simulator",
            "📊 Analytics",
            "📚 Learn OS"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### SYSTEM STATUS")

    st.success("Scheduling engine ready")

    st.caption("NEXUS OS | Version 1.0")
    st.caption("Operating Systems Capstone")


# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to NEXUS OS ⚡</h1>
            <p>
            Intelligent CPU scheduling, process management
            and performance visualization.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("System Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Processes",
        len(st.session_state.processes)
    )

    c2.metric("Algorithms", "03")

    c3.metric(
        "Simulations",
        len(st.session_state.results)
    )

    c4.metric("Engine Status", "Online")

    st.divider()

    left, right = st.columns([1.5, 1])

    with left:

        st.subheader("Scheduling Algorithms")

        algorithm_info = pd.DataFrame({
            "Algorithm": [
                "FCFS",
                "SJF",
                "Round Robin"
            ],
            "Type": [
                "Non-Preemptive",
                "Non-Preemptive",
                "Preemptive"
            ],
            "Selection": [
                "Arrival Order",
                "Shortest Burst",
                "Time Quantum"
            ]
        })

        st.dataframe(
            algorithm_info,
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.subheader("Process Distribution")

        proc_df = pd.DataFrame(
            st.session_state.processes
        )

        fig = px.pie(
            proc_df,
            names="PID",
            values="Burst Time",
            hole=0.65,
            title="CPU Burst Distribution",
            color_discrete_sequence=[
                "#3B82F6",
                "#8B5CF6",
                "#06B6D4",
                "#10B981",
                "#F59E0B"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            font_color="#e2e8f0",
            height=300
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Recent Simulation Results")

    if st.session_state.results:

        recent = []

        for name, data in st.session_state.results.items():

            recent.append({
                "Algorithm": name,
                "Avg Waiting Time": round(data["waiting"], 2),
                "Avg Turnaround Time": round(data["turnaround"], 2),
                "Avg Response Time": round(data["response"], 2)
            })

        st.dataframe(
            pd.DataFrame(recent),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No simulation results yet. Visit the Simulator "
            "page to run your first experiment."
        )


# ==========================================
# PROCESS MANAGER
# ==========================================

elif page == "🖥️ Process Manager":

    st.title("🖥️ Process Manager")

    st.write(
        "Create, edit and manage processes before CPU scheduling."
    )

    st.subheader("Process Configuration")

    edited = st.data_editor(
        pd.DataFrame(st.session_state.processes),
        num_rows="dynamic",
        use_container_width=True,
        key="manager_editor"
    )

    if st.button("💾 Save Process Configuration"):

        try:

            if edited.empty:
                raise ValueError("Add at least one process.")

            if edited.isnull().values.any():
                raise ValueError("Fill in all fields.")

            edited["PID"] = (
                edited["PID"].astype(str).str.strip()
            )

            if edited["PID"].eq("").any():
                raise ValueError("Process IDs cannot be empty.")

            if edited["PID"].duplicated().any():
                raise ValueError("Process IDs must be unique.")

            processes = []

            for _, row in edited.iterrows():

                arrival = int(row["Arrival Time"])
                burst = int(row["Burst Time"])

                if arrival < 0 or burst <= 0:
                    raise ValueError(
                        "Arrival time must be >= 0 "
                        "and burst time must be > 0."
                    )

                processes.append({
                    "PID": row["PID"],
                    "Arrival Time": arrival,
                    "Burst Time": burst
                })

            st.session_state.processes = processes
            st.session_state.results = {}

            st.success("Process configuration saved!")

        except (ValueError, TypeError, KeyError) as e:

            st.error(str(e))

    st.divider()

    process_df = pd.DataFrame(
        st.session_state.processes
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Processes", len(process_df))
    c2.metric("Total Burst Time", process_df["Burst Time"].sum())
    c3.metric("Average Burst Time", round(process_df["Burst Time"].mean(), 2))


# ==========================================
# SIMULATOR PAGE
# ==========================================

elif page == "⚙️ Simulator":

    st.title("⚙️ CPU Scheduling Simulator")

    st.write(
        "Choose an algorithm and execute a CPU scheduling simulation."
    )

    st.subheader("Current Process Queue")

    st.dataframe(
        pd.DataFrame(st.session_state.processes),
        use_container_width=True,
        hide_index=True
    )

    algorithm = st.selectbox(
        "Select Scheduling Algorithm",
        [
            "FCFS",
            "SJF",
            "Round Robin",
            "Compare All"
        ]
    )

    quantum = 2

    if algorithm in ["Round Robin", "Compare All"]:

        quantum = st.number_input(
            "Time Quantum",
            min_value=1,
            max_value=100,
            value=2
        )

    if st.button("🚀 Execute Simulation"):

        try:

            if not st.session_state.processes:
                raise ValueError("No processes available.")

            results = generate_results(
                st.session_state.processes,
                quantum
            )

            if algorithm == "Compare All":
                st.session_state.results = results

            else:
                st.session_state.results = {
                    algorithm: results[algorithm]
                }

            st.success(
                f"{algorithm} simulation executed successfully!"
            )

        except (ValueError, TypeError, KeyError) as e:

            st.error(str(e))

    if st.session_state.results:

        st.divider()
        st.subheader("Execution Results")

        for name, data in st.session_state.results.items():

            st.markdown(f"### {name}")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Average Waiting",
                f'{data["waiting"]:.2f}'
            )

            c2.metric(
                "Average Turnaround",
                f'{data["turnaround"]:.2f}'
            )

            c3.metric(
                "Average Response",
                f'{data["response"]:.2f}'
            )

            st.dataframe(
                data["results"],
                use_container_width=True,
                hide_index=True
            )

            gantt_chart(
                data["chart"],
                f"{name} Execution Timeline"
            )

            st.divider()


# ==========================================
# ANALYTICS PAGE
# ==========================================

elif page == "📊 Analytics":

    st.title("📊 Performance Analytics")

    st.write(
        "Compare CPU scheduling algorithms using performance metrics."
    )

    if not st.session_state.results:

        st.warning(
            "Run a simulation first to view performance analytics."
        )

    else:

        rows = []

        for name, data in st.session_state.results.items():

            rows.append({
                "Algorithm": name,
                "Waiting Time": round(data["waiting"], 2),
                "Turnaround Time": round(data["turnaround"], 2),
                "Response Time": round(data["response"], 2)
            })

        df = pd.DataFrame(rows)

        c1, c2, c3 = st.columns(3)

        best_waiting = df.loc[
            df["Waiting Time"].idxmin()
        ]

        best_turnaround = df.loc[
            df["Turnaround Time"].idxmin()
        ]

        best_response = df.loc[
            df["Response Time"].idxmin()
        ]

        c1.metric(
            "Best Waiting Time",
            best_waiting["Algorithm"],
            f'{best_waiting["Waiting Time"]}'
        )

        c2.metric(
            "Best Turnaround",
            best_turnaround["Algorithm"],
            f'{best_turnaround["Turnaround Time"]}'
        )

        c3.metric(
            "Best Response",
            best_response["Algorithm"],
            f'{best_response["Response Time"]}'
        )

        st.divider()

        fig = px.bar(
            df,
            x="Algorithm",
            y=[
                "Waiting Time",
                "Turnaround Time",
                "Response Time"
            ],
            barmode="group",
            title="Algorithm Performance Comparison",
            color_discrete_sequence=[
                "#3B82F6",
                "#8B5CF6",
                "#10B981"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#111c30",
            font_color="#e2e8f0"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Detailed Comparison")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download Analytics CSV",
            df.to_csv(index=False),
            file_name="NEXUS_OS_Analytics.csv",
            mime="text/csv"
        )


# ==========================================
# LEARN OS PAGE
# ==========================================

elif page == "📚 Learn OS":

    st.title("📚 Operating Systems Learning Center")

    st.write(
        "Understand the concepts implemented in this project."
    )

    topics = {
        "CPU Scheduling": """
        CPU scheduling is the process of selecting a process
        from the ready queue and allocating the CPU to it.

        Its objective is to improve CPU utilization,
        throughput and response time.
        """,

        "FCFS Scheduling": """
        First Come First Serve executes processes according
        to their arrival time.

        It is non-preemptive and simple to implement.

        Disadvantage: Convoy effect.
        """,

        "SJF Scheduling": """
        Shortest Job First selects the available process
        having the smallest CPU burst time.

        It is optimal for average waiting time when
        all jobs are available together and burst times are known.

        Disadvantage: Long processes may suffer starvation.
        """,

        "Round Robin": """
        Round Robin assigns each process a fixed time quantum.

        If the process is not completed, it is moved
        to the end of the ready queue.

        It is suitable for time-sharing systems.
        """,

        "Scheduling Formulas": """
        Completion Time = Time at which process finishes.

        Turnaround Time = Completion Time - Arrival Time.

        Waiting Time = Turnaround Time - Burst Time.

        Response Time = First CPU Start Time - Arrival Time.
        """
    }

    for title, description in topics.items():

        with st.expander(title):
            st.write(description)

    st.divider()

    st.subheader("Project Technology Stack")

    tech = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Pandas",
            "Plotly"
        ],
        "Purpose": [
            "Scheduling algorithms",
            "Interactive dashboard",
            "Process data management",
            "Gantt charts and analytics"
        ]
    })

    st.dataframe(
        tech,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:15px;">
        <h4 style="color:#60a5fa!important;">
        ⚡ NEXUS OS
        </h4>
        <p style="color:#94a3b8;font-size:12px;">
        Interactive CPU Scheduling Management System
        <br>
        Operating Systems Capstone Project | Version 1.0
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
