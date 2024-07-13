import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'rag_output.json')
    with open(file_path) as f:
        return json.load(f)

data = load_data()

def provider_demo():
    st.title("Provider Demo")
    
    st.subheader("Welcome to the Provider Portal")
    st.write("This portal provides an overview of your patients, upcoming appointments, care gaps, and performance metrics. Navigate through the sections to manage and improve patient care.")

    nav_options = ["Member Overview", "Appointments and Live Events", "Care Gaps and Insights", "Communication and Coordination", "Performance Metrics"]
    choice = st.sidebar.radio("Select a section", nav_options, key="provider_nav")

    if choice == "Member Overview":
        member_overview()
    elif choice == "Appointments and Live Events":
        appointments_live_events()
    elif choice == "Care Gaps and Insights":
        care_gaps_insights()
    elif choice == "Communication and Coordination":
        communication_coordination()
    elif choice == "Performance Metrics":
        performance_metrics()

def member_overview():
    st.title("Member Overview")
    
    st.subheader("List of Members")
    member_data = []
    for entry in data:
        patient_info = json.loads(entry["measures"][0]["json_excerpt"])
        member_data.append({
            "Member ID": patient_info.get("patient_id", "Unknown ID"),
            "Name": patient_info.get("patient_name", "Unknown Name"),
            "Age": patient_info.get("patient_birthDate", "Unknown Birth Date"),
            "Gender": patient_info.get("patient_gender", "Unknown Gender"),
            "Health Status": "Unknown"
        })
    member_df = pd.DataFrame(member_data)
    
    for index, row in member_df.iterrows():
        with st.expander(f"{row['Name']} - {row['Health Status']}"):
            st.write(f"**Age:** {row['Age']}")
            st.write(f"**Gender:** {row['Gender']}")
            member_measures = next((entry["measures"] for entry in data if json.loads(entry["measures"][0]["json_excerpt"]).get("patient_id") == row["Member ID"]), [])
            for measure in member_measures:
                status_color = "green" if measure["status"] == "Met" else "red"
                st.markdown(f"""
                    <div style="color: {status_color};">
                        <p><strong>{measure['name']}</strong> - {measure['status']}</p>
                        {"<p><strong>Date:</strong> " + measure['date'] + "</p>" if measure['date'] else ""}
                        <strong>Factors:</strong>
                        <ul>
                """, unsafe_allow_html=True)
                if measure['sub_measures']:
                    for sub_measure in measure['sub_measures']:
                        sub_status_color = "green" if sub_measure["status"] == "Met" else "red"
                        st.markdown(f"""
                            <li>{sub_measure['name']}: <span style='color: {sub_status_color};'>{sub_measure['status']}</span>
                            {"<br><strong>Value:</strong> " + sub_measure['value'] if sub_measure['value'] else ""}
                            {"<br><strong>Date:</strong> " + sub_measure['date'] if sub_measure['date'] else ""}</li>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<li>No additional factors.</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

def appointments_live_events():
    st.title("Appointments and Live Events")

    st.subheader("Upcoming Appointments")
    appointments = [
        {"Date": "2023-07-14", "Time": "10:00 AM", "Patient": "John Doe"},
        {"Date": "2023-07-15", "Time": "02:00 PM", "Patient": "Jane Smith"},
    ]
    for appointment in appointments:
        st.write(f"{appointment['Date']} - {appointment['Time']} with {appointment['Patient']}")
    
    st.subheader("Next Appointment Countdown")
    st.write("Time until next appointment: 1 hour 30 minutes")

    st.subheader("Live Events and Notifications")
    live_events = [
        {"Event": "Check-up", "Patient": "John Doe", "Time": "10:00 AM"},
        {"Event": "Follow-up", "Patient": "Jane Smith", "Time": "02:00 PM"},
    ]
    for event in live_events:
        st.write(f"{event['Event']} for {event['Patient']} at {event['Time']}")

def care_gaps_insights():
    st.title("Care Gaps and Insights")

    st.subheader("Highlighted Care Gaps")
    care_gaps = []
    for entry in data:
        patient_info = json.loads(entry["measures"][0]["json_excerpt"])
        for measure in entry["measures"]:
            if measure["status"] != "Met":
                care_gaps.append({
                    "Patient": patient_info.get("patient_name", "Unknown Name"),
                    "Gap": measure["name"],
                    "Status": measure["status"],
                    "Date": measure.get("date", ""),
                    "Factors": measure.get("sub_measures", [])
                })
    
    for gap in care_gaps:
        with st.expander(f"{gap['Patient']} - {gap['Gap']} ({gap['Status']})"):
            st.write(f"**Gap:** {gap['Gap']}")
            st.write(f"**Status:** {gap['Status']}")
            if gap["Date"]:
                st.write(f"**Date:** {gap['Date']}")
            st.write("**Factors:**")
            if gap["Factors"]:
                for factor in gap["Factors"]:
                    sub_status_color = "green" if factor["status"] == "Met" else "red"
                    st.markdown(f"""
                        <li>{factor['name']}: <span style='color: {sub_status_color};'>{factor['status']}</span>
                        {"<br><strong>Value:</strong> " + factor['value'] if factor['value'] else ""}
                        {"<br><strong>Date:</strong> " + factor['date'] if factor['date'] else ""}</li>
                    """, unsafe_allow_html=True)
            else:
                st.write("No additional factors.")

    st.subheader("Care Gap Visualizations")
    measures = ["Blood Pressure Check", "Diabetes Screening"]
    patients = ["John Doe", "Jane Smith"]
    values = [[75, 85], [65, 90]]
    
    for i, measure in enumerate(measures):
        df = pd.DataFrame({
            "Patient": patients,
            "Value": values[i]
        })
        fig = px.bar(df, x="Patient", y="Value", title=f"{measure} Completion Rate")
        st.plotly_chart(fig)

def communication_coordination():
    st.title("Communication and Coordination")

    st.subheader("Communication Tools")
    st.write("Enable communication with other healthcare professionals.")
    st.text_area("Message")
    if st.button("Send Message"):
        st.write("Message sent successfully.")

    st.subheader("Collaboration Section")
    st.write("Notes and collaboration tools for patient care plans.")
    st.text_area("Notes")
    if st.button("Save Notes"):
        st.write("Notes saved successfully.")

def performance_metrics():
    st.title("Performance Metrics")

    st.subheader("Performance Metrics")
    metrics = [
        {"Metric": "HEDIS Measure Compliance", "Value": "80%"},
        {"Metric": "Patient Satisfaction", "Value": "90%"},
    ]
    for metric in metrics:
        st.write(f"**{metric['Metric']}:** {metric['Value']}")
    
    st.subheader("Visualizations")
    measures = ["HEDIS Measure Compliance", "Patient Satisfaction"]
    values = [80, 90]
    
    df = pd.DataFrame({
        "Measure": measures,
        "Value": values
    })
    fig = px.bar(df, x="Measure", y="Value", title="Performance Metrics")
    st.plotly_chart(fig)

# For testing purposes if running this script directly
if __name__ == "__main__":
    provider_demo()
