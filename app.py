
import streamlit as st
import pandas as pd
from datetime import date, time, datetime, timedelta

st.set_page_config(
    page_title="CarePing | Appointment Reminder",
    page_icon="🩺",
    layout="wide",
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f7fafc;
    }

    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #e8f5f2, #eef3ff);
        border: 1px solid #dbe8e8;
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        color: #173b4d !important;
    }

    .hero p {
        margin: .35rem 0 0 0;
        color: #48616d !important;
    }

    /* FIX: readable dashboard metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #d5e1e8;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(23, 59, 77, 0.06);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p {
        color: #48616d !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div {
        color: #173b4d !important;
        font-size: 30px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #173b4d !important;
    }

    h1, h2, h3, p, label {
        color: inherit;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🩺 CarePing</h1>
    <p>A simple appointment planner to organize visits
    and highlight upcoming reminders.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
COLUMNS = [
    "patient_name",
    "appointment_type",
    "appointment_date",
    "appointment_time",
    "contact",
    "notes",
    "created_at",
]

if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=COLUMNS)


def to_datetime(row):
    try:
        appointment_date = pd.to_datetime(
            row["appointment_date"]
        ).date()
        appointment_time = pd.to_datetime(
            str(row["appointment_time"])
        ).time()

        return datetime.combine(
            appointment_date, appointment_time
        )
    except (ValueError, TypeError, KeyError):
        return None


def friendly_datetime(value):
    try:
        return pd.to_datetime(value).strftime("%d %b %Y")
    except (ValueError, TypeError):
        return "Not set"


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("Quick actions")

    st.caption(
        "Demo only: this app does not send SMS, "
        "email, or real notifications."
    )

    if st.button(
        "Load sample appointments",
        use_container_width=True,
    ):
        today = date.today()
        now_text = datetime.now().isoformat(timespec="minutes")

        sample = [
            [
                "Aarav Kumar",
                "General check-up",
                (today + timedelta(days=1)).isoformat(),
                "10:00",
                "demo@example.com",
                "Bring previous reports",
                now_text,
            ],
            [
                "Meera Reddy",
                "Dental check-up",
                (today + timedelta(days=2)).isoformat(),
                "14:30",
                "demo@example.com",
                "Routine appointment",
                now_text,
            ],
            [
                "Rohan Das",
                "Follow-up",
                today.isoformat(),
                "16:00",
                "demo@example.com",
                "Demo record only",
                now_text,
            ],
        ]

        st.session_state.appointments = pd.DataFrame(
            sample, columns=COLUMNS
        )
        st.success("Sample appointments loaded.")
        st.rerun()

    if st.button(
        "Clear all appointments",
        use_container_width=True,
    ):
        st.session_state.appointments = pd.DataFrame(
            columns=COLUMNS
        )
        st.rerun()

    st.divider()
    st.markdown("**Privacy note**")
    st.caption(
        "Use fictional information for demonstrations. "
        "Records are held in session memory and may be lost "
        "when the session resets. Do not enter real patient data."
    )

# -------------------- DASHBOARD --------------------
today = date.today()
df = st.session_state.appointments.copy()

if not df.empty:
    df["_datetime"] = df.apply(to_datetime, axis=1)
    now = datetime.now()

    valid_datetimes = [
        value for value in df["_datetime"]
        if isinstance(value, datetime)
    ]

    today_count = sum(
        1 for value in valid_datetimes
        if value.date() == today
    )

    upcoming_count = sum(
        1 for value in valid_datetimes
        if now <= value <= now + timedelta(days=7)
    )
else:
    df["_datetime"] = pd.Series(dtype="object")
    today_count = 0
    upcoming_count = 0

m1, m2, m3 = st.columns(3)

m1.metric("Total appointments", len(df))
m2.metric("Today", today_count)
m3.metric("Next 7 days", upcoming_count)

# -------------------- TABS --------------------
tab_add, tab_view, tab_export = st.tabs([
    "➕ Add appointment",
    "📅 Appointment list",
    "⬇️ Export",
])

# -------------------- ADD APPOINTMENT --------------------
with tab_add:
    st.subheader("Create an appointment")
    st.write(
        "Add a visit below. The app will show it in "
        "the appointment list and upcoming section."
    )

    with st.form("appointment_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            patient_name = st.text_input(
                "Patient name *",
                placeholder="e.g. Demo Patient",
            )

            appointment_type = st.selectbox(
                "Appointment type *",
                [
                    "General check-up",
                    "Dental check-up",
                    "Follow-up",
                    "Eye check-up",
                    "Vaccination",
                    "Lab test",
                    "Other",
                ],
            )

            appointment_date = st.date_input(
                "Appointment date *",
                value=today,
                min_value=today,
            )

        with c2:
            appointment_time = st.time_input(
                "Appointment time *",
                value=time(10, 0),
                step=900,
            )

            contact = st.text_input(
                "Contact (optional)",
                placeholder="Email or phone",
            )

            notes = st.text_area(
                "Notes (optional)",
                placeholder="e.g. Bring documents",
            )

        submitted = st.form_submit_button(
            "Save appointment",
            type="primary",
        )

        if submitted:
            if not patient_name.strip():
                st.error("Please enter a patient name.")
            else:
                new_row = {
                    "patient_name": patient_name.strip(),
                    "appointment_type": appointment_type,
                    "appointment_date": appointment_date.isoformat(),
                    "appointment_time": appointment_time.strftime("%H:%M"),
                    "contact": contact.strip(),
                    "notes": notes.strip(),
                    "created_at": datetime.now().isoformat(
                        timespec="minutes"
                    ),
                }

                st.session_state.appointments = pd.concat(
                    [
                        st.session_state.appointments,
                        pd.DataFrame([new_row]),
                    ],
                    ignore_index=True,
                )

                st.success("Appointment saved.")
                st.rerun()

# -------------------- APPOINTMENT LIST --------------------
with tab_view:
    st.subheader("Appointments")

    current = st.session_state.appointments.copy()

    if current.empty:
        st.info(
            "No appointments yet. Add one, or use "
            "'Load sample appointments' in the sidebar."
        )
    else:
        current["_sort_dt"] = current.apply(to_datetime, axis=1)
        current = current.sort_values(
            "_sort_dt", na_position="last"
        )

        current["Date"] = current["appointment_date"].apply(
            friendly_datetime
        )
        current["Time"] = current["appointment_time"]

        display = current[
            [
                "patient_name",
                "appointment_type",
                "Date",
                "Time",
                "contact",
                "notes",
            ]
        ].rename(
            columns={
                "patient_name": "Patient",
                "appointment_type": "Appointment type",
                "contact": "Contact",
                "notes": "Notes",
            }
        )

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
        )

        now = datetime.now()

        upcoming = current[
            current["_sort_dt"].apply(
                lambda value: (
                    isinstance(value, datetime) and value >= now
                )
            )
        ]

        st.subheader("Upcoming reminders")

        if upcoming.empty:
            st.info("There are no future appointments in the list.")
        else:
            for _, row in upcoming.head(5).iterrows():
                dt = row["_sort_dt"]
                days = (dt.date() - today).days

                if days == 0:
                    when = "Today"
                elif days == 1:
                    when = "Tomorrow"
                else:
                    when = f"In {days} days"

                st.markdown(
                    f"**{when} · {dt.strftime('%d %b, %I:%M %p')}** — "
                    f"{row['patient_name']} · {row['appointment_type']}"
                )

        st.subheader("Remove an appointment")

        options = {
            (
                f"{row['patient_name']} — "
                f"{row['appointment_type']} — "
                f"{row['appointment_date']} "
                f"{row['appointment_time']} (row {index + 1})"
            ): index
            for index, row in current.iterrows()
        }

        selected = st.selectbox(
            "Choose a record to remove",
            [""] + list(options.keys()),
        )

        if selected and st.button(
            "Remove selected appointment",
            type="secondary",
        ):
            original_index = options[selected]

            st.session_state.appointments = (
                st.session_state.appointments
                .drop(index=original_index)
                .reset_index(drop=True)
            )

            st.success("Appointment removed.")
            st.rerun()

# -------------------- EXPORT --------------------
with tab_export:
    st.subheader("Export appointment data")

    export_df = st.session_state.appointments.copy()

    if export_df.empty:
        st.info("Add at least one appointment to enable export.")
    else:
        csv_bytes = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download appointments as CSV",
            data=csv_bytes,
            file_name="careping_appointments.csv",
            mime="text/csv",
            type="primary",
        )

        st.caption(
            "CSV export is useful for a demo or further analysis. "
            "Use fictional records only."
        )

# -------------------- FOOTER --------------------
st.divider()
st.caption(
    "CarePing is an educational scheduling prototype, not a "
    "clinical system. It does not provide medical advice or "
    "send real reminders."
)
