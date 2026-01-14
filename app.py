## J&S Milestone Tracker!! <3

import streamlit as st 
import pandas as pd 

st.set_page_config(page_title="J&S Milestone Tracker", page_icon="🧡", layout="wide")

## --- Styling ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { color: #f48c36 !important; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f48c36;
    }
    div.stButton > button:first-child {
        background-color: #f48c36;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #e67e22;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧡 J&S Milestone Tracker")
st.write("Upload bookings to see who has hit new milestones <3")

## Step 1 : Upload files
col1, col2 = st.columns(2)

with col1: 
    attendance_file = st.file_uploader("Upload Booking System CSV", type=["csv"])
with col2: 
    email_file = st.file_uploader("Upload Previous Recipients List (CSV)", type=["csv"])

if attendance_file and email_file:
    df = pd.read_csv(attendance_file)
    history_df = pd.read_csv(email_file)

    ## Step 2: Clean up
    df.columns = df.columns.str.strip()
    history_df.columns = history_df.columns.str.strip()

    ## Step 3: Milestone logic (Up to 300)
    def get_milestone(n): 
        try:
            n = int(float(n))
            if n >= 300: return 300
            if n >= 250: return 250
            if n >= 200: return 200
            if n >= 150: return 150
            if n >= 100: return 100
            if n >= 50: return 50
        except:
            return 0
        return 0

    df['Milestone'] = df['Total attendances'].apply(get_milestone)
    eligible = df[df['Milestone'] > 0].copy()

    ## Step 4: Multi-Milestone Cross Reference
    if 'Email' in history_df.columns and 'Milestone' in history_df.columns:
        # Create keys to compare current status vs history
        history_df['History_Key'] = (
            history_df['Email'].astype(str).str.strip().str.lower() + 
            "-" + 
            history_df['Milestone'].astype(str).str.replace('.0', '', regex=False)
        )
        
        eligible['Current_Key'] = (
            eligible['Email'].astype(str).str.strip().str.lower() + 
            "-" + 
            eligible['Milestone'].astype(str)
        )

        already_rewarded_keys = set(history_df['History_Key'])
        new_eligible = eligible[~eligible['Current_Key'].isin(already_rewarded_keys)].copy()
    else:
        st.error("Error: The 'Previous Recipients' file must have 'Email' and 'Milestone' columns!")
        new_eligible = pd.DataFrame()

    st.divider()

    if not new_eligible.empty:
        # Summary Metrics
        m1, m2, m3, m4 = st.columns(4) 
        m1.metric("🧡 50-100", len(new_eligible[new_eligible['Milestone'].isin([50, 100])]))
        m2.metric("✨ 150-200", len(new_eligible[new_eligible['Milestone'].isin([150, 200])]))
        m3.metric("🎉 250-300", len(new_eligible[new_eligible['Milestone'].isin([250, 300])]))
        m4.metric("🔥 Total New", len(new_eligible))

        # Output 1: Friendly display for checking names
        st.subheader("📋 New Milestones to Action")
        display_df = new_eligible[['Full name', 'Total attendances', 'Milestone', 'Email']]
        display_df.columns = ['Name', 'Attendances', 'Milestone', 'Email']
        st.dataframe(display_df.sort_values('Milestone'), use_container_width=True)

        st.divider()

        # Output 2: System format for copy-pasting back into the history file
        st.subheader("💾 Master Log Update")
        st.write("Copy these rows or download this file to add to your 'Previous Recipients' CSV:")
        
        # This matches the history structure: Email, Milestone
        log_update = new_eligible[['Email', 'Milestone']].copy()
        st.dataframe(log_update, use_container_width=True)

        csv_log = log_update.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Log Update (CSV)",
            data=csv_log,
            file_name='add_to_history_log.csv',
            mime='text/csv'
        )                   
    else: 
        st.success("Everyone is up to date with their rewards!")

else: 
    st.info("Please upload both files. Note: Your 'Previous Recipients' list needs an 'Email' and a 'Milestone' column. <3")