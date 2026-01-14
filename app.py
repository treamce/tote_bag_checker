## J&S Milestone Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="J&S Milestone Tracker", page_icon="🧡", layout="wide")

## --- Styling ---
st.markdown("""
    <style>
    /* Change Metric colors to Orange */
    [data-testid="stMetricValue"] {
        color: #f48c36 !important;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f48c36;
    }
    /* Change Button color to Orange */
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
    email_file = st.file_uploader("Upload Previous Recipients List CSV", type=["csv"])

## Only run if both files are uploaded
if attendance_file and email_file:

    # Fit into tables 
    df = pd.read_csv(attendance_file)
    emails_received_df = pd.read_csv(email_file)

    ## Step 2: Clean up the data columns
    df.columns = df.columns.str.strip()
    emails_received_df.columns = emails_received_df.columns.str.strip()

    ## Step 3: Milestone logic 
    def get_milestone(n): 
        try:
            n = int(float(n))
            if n >= 350: return 350
            if n >= 300: return 300
            if n >= 250: return 250
            if n >= 200: return 200
            if n >= 150: return 150
            if n >= 100: return 100
            if n >= 50: return 50
        except:
            return 0
        return 0

    # Using 'Total attendances' from your file format
    df['Milestone'] = df['Total attendances'].apply(get_milestone)
    eligible = df[df['Milestone'] > 0].copy()

    ## Step 4: Cross reference with the Email List
    # We now check Email + Milestone so they can show up for 100 even if they've had 50
    if 'Email' in emails_received_df.columns and 'Milestone' in emails_received_df.columns:
        emails_received_df['History_Key'] = (
            emails_received_df['Email'].astype(str).str.strip().str.lower() + 
            "-" + 
            emails_received_df['Milestone'].astype(str).str.replace('.0', '', regex=False)
        )
        
        eligible['Current_Key'] = (
            eligible['Email'].astype(str).str.strip().str.lower() + 
            "-" + 
            eligible['Milestone'].astype(str)
        )

        already_received_keys = set(emails_received_df['History_Key'])
        eligible['Already received?'] = eligible['Current_Key'].isin(already_received_keys)
        
        # Only show people who reached a milestone and are NOT in the list for THIS specific milestone
        new_eligible = eligible[eligible['Already received?'] == False].copy()
    else:
        st.error("Wait! The 'Previous Recipients' CSV needs an 'Email' and a 'Milestone' column for this to work. <3")
        new_eligible = pd.DataFrame()

    st.divider()

    if not new_eligible.empty:
        # Step 5: Summary with 4 Buckets
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4) 
        summary_col1.metric("🧡 50-99 Attendances", len(new_eligible[new_eligible['Milestone'] == 50]))
        summary_col2.metric("✨ 100-149 Attendances", len(new_eligible[new_eligible['Milestone'] == 100]))
        summary_col3.metric("🎉 150-199 Attendances", len(new_eligible[new_eligible['Milestone'] == 150]))
        summary_col4.metric("🔥 200-350 Attendances", len(new_eligible[new_eligible['Milestone'] >= 200]))

        # --- Shading Logic ---
        def color_milestones(val):
            colors = {
                50:  'background-color: #fff3e0', 
                100: 'background-color: #ffe0b2', 
                150: 'background-color: #ffcc80', 
                200: 'background-color: #ffb74d', 
                250: 'background-color: #ffa726', 
                300: 'background-color: #fb8c00', 
                350: 'background-color: #f4511e'  
            }
            return colors.get(val, '')

        st.subheader(f"New Milestones <3 ({len(new_eligible)})")
        
        # Display table with relevant columns
        display_df = new_eligible[['Full name', 'Total attendances', 'Milestone', 'Email']]
        display_df.columns = ['Name', 'Attendances', 'Milestone', 'Email']
        
        # Apply Shading
        styled_df = display_df.sort_values('Milestone').style.applymap(color_milestones, subset=['Milestone'])
        st.dataframe(styled_df, use_container_width=True)

        ## Step 6: Download Buttons
        action_csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Action List (CSV)",
            data=action_csv,
            file_name='new_milestones.csv',
            mime='text/csv'
        ) 

        st.divider()
        
        # Master Log Output for copy-pasting
        st.subheader("Master Log Update")
        st.info("Add these rows to your 'Previous Recipients' CSV to keep history updated.")
        log_update = new_eligible[['Email', 'Milestone']].copy()
        st.dataframe(log_update, use_container_width=True)
        
        csv_log = log_update.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Master Log Entries (CSV)",
            data=csv_log,
            file_name='add_to_history.csv',
            mime='text/csv'
        )
                      
    else: 
        st.balloons()
        st.success("Everyone is up to date with their milestones!")

else: 
    st.info("Please upload both the Booking System CSV and the Email List CSV please <3")