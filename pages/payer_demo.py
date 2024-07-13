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

def payer_demo():
    st.title("Payer Demo")
    
    st.subheader("Overview")
    st.write("""
        This section provides an overview of projected HEDIS care gap measure rates for the population.
    """)

    measures = ["Annual Wellness Visit (AWV)", "Controlling High Blood Pressure (CBP)", "Comprehensive Diabetes Care (CDC)"]
    measure_codes = ["AWV", "CBP", "CDC"]
    projected_rates = []
    target_rates = [85, 75, 90]  # Example target rates
    
    for code in measure_codes:
        total = 0
        met = 0
        for entry in data:
            for measure in entry["measures"]:
                if measure["code"] == code:
                    total += 1
                    if measure["status"] == "Met":
                        met += 1
        projected_rate = (met / total) * 100 if total > 0 else 0
        projected_rates.append(projected_rate)

    df = pd.DataFrame({
        "Measure": measures,
        "Projected Rate": projected_rates,
        "Target Rate": target_rates
    })
    
    st.markdown("### Key Performance Indicators")
    for i, measure in enumerate(measures):
        kpi_html = f"""
        <div style="padding: 10px; border-radius: 5px; background-color: #f0f0f5; margin-bottom: 10px; border-left: 6px solid #4CAF50;">
            <h3 style="color: #333;">{measure} Projected Rate</h3>
            <p style="font-size: 24px; font-weight: bold; color: #333;">{df['Projected Rate'][i]:.2f}%</p>
            <p style="font-size: 18px; color: {'green' if df['Projected Rate'][i] >= df['Target Rate'][i] else 'red'};">{df['Projected Rate'][i] - df['Target Rate'][i]:.2f}% from target</p>
        </div>
        """
        st.markdown(kpi_html, unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["Measure"],
        y=df["Projected Rate"],
        name='Projected Rate',
        marker_color='indianred'
    ))

    fig.add_trace(go.Scatter(
        x=df["Measure"],
        y=df["Target Rate"],
        name='Target Rate',
        mode='lines+markers',
        line=dict(color='royalblue', width=2)
    ))

    fig.update_layout(
        title="Projected HEDIS Care Gap Measure Rates",
        xaxis_title="Measure",
        yaxis_title="Rate (%)",
        legend_title="Rate Type",
        barmode='group'
    )

    st.plotly_chart(fig)
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    annual_data = {
        "Month": months * 3,
        "Rate": [60 + i % 12 for i in range(12)] + [70 + i % 12 for i in range(12)] + [50 + i % 12 for i in range(12)],
        "Target Rate": [85] * 12 + [75] * 12 + [90] * 12,
        "Measure": ["AWV"] * 12 + ["CBP"] * 12 + ["CDC"] * 12
    }
    annual_df = pd.DataFrame(annual_data)

    selected_measure = st.selectbox("Select Measure for Annual Projection", measures)
    measure_code = measure_codes[measures.index(selected_measure)]
    filtered_df = annual_df[annual_df["Measure"] == measure_code]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=filtered_df["Month"],
        y=filtered_df["Rate"],
        fill='tozeroy',
        name='Projected Rate',
        mode='lines+markers',
        line=dict(color='indianred')
    ))

    fig2.add_trace(go.Scatter(
        x=filtered_df["Month"],
        y=filtered_df["Target Rate"],
        name='Target Rate',
        mode='lines+markers',
        line=dict(color='royalblue', dash='dash')
    ))

    fig2.update_layout(
        title=f"Annual Projection of {selected_measure} Rate vs Target Rate",
        xaxis_title="Month",
        yaxis_title="Rate (%)",
        legend_title="Rate Type"
    )

    st.plotly_chart(fig2)

    st.subheader("Member-Level Drill Down")
    st.write("Select a member to view their specific gaps in care.")
    
    member_data = []
    for entry in data:
        patient_info = json.loads(entry["measures"][0]["json_excerpt"])
        member_data.append({
            "Member ID": patient_info.get("patient_id", "Unknown ID"),
            "Name": patient_info.get("patient_name", "Unknown Name")
        })
    member_df = pd.DataFrame(member_data)
    
    selected_member = st.selectbox("Select Member ID", member_df["Member ID"])
    member_info = next((entry for entry in data if json.loads(entry["measures"][0]["json_excerpt"]).get("patient_id") == selected_member), None)
    
    if member_info:
        patient_info = json.loads(member_info["measures"][0]["json_excerpt"])
        
        st.write(f"### Member Information for {patient_info.get('patient_name', 'Unknown Name')}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 5px; background-color: #f8f9fa; text-align: center;">
                    <h4>Age</h4>
                    <p>{patient_info.get('patient_birthDate', 'Unknown Birth Date')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="padding: 10px; border-radius: 5px; background-color: #f8f9fa; text-align: center;">
                    <h4>Gender</h4>
                    <p>{patient_info.get('patient_gender', 'Unknown Gender')}</p>
                </div>
                """, unsafe_allow_html=True)

        for measure in member_info["measures"]:
            status_color = "green" if measure["status"] == "Met" else "red"
            with st.expander(f"{measure['name']} ({measure['status']})", expanded=True):
                st.markdown(f"""
                    <div style="color: {status_color};">
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
        
        gap_data = {
            "Measure": [],
            "Status": [],
            "Value": [],
            "Date": []
        }
        for measure in member_info["measures"]:
            gap_data["Measure"].append(measure["name"])
            gap_data["Status"].append(measure["status"])
            gap_data["Value"].append(measure["value"] if measure["value"] else "N/A")
            gap_data["Date"].append(measure["date"] if measure["date"] else "N/A")
            for sub_measure in measure.get("sub_measures", []):
                gap_data["Measure"].append(sub_measure["name"])
                gap_data["Status"].append(sub_measure["status"])
                gap_data["Value"].append(sub_measure["value"] if sub_measure["value"] else "N/A")
                gap_data["Date"].append(sub_measure["date"] if sub_measure["date"] else "N/A")
        
        gap_df = pd.DataFrame(gap_data)
        fig = px.bar(gap_df, x="Measure", y="Value", color="Status", title="Member's Gaps in Care")
        st.plotly_chart(fig)

# For testing purposes if running this script directly
if __name__ == "__main__":
    payer_demo()
