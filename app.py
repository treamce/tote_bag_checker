## Milestone Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="J&S MilestoneTracker", page_icon="🧡", layout="wide")

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

######

## Step 1 : Upload files
col1, col2 = st.columns(2)

with col1: 
# Upload booking system csv file
    attendance_file = st.file_uploader("Upload Booking System CSV", type=["csv"])
with col2: 
# Upload email list 
    email_file = st.file_uploader("Upload Previous Recipients Email List CSV", type=["csv"])

## Only run if both files are uploaded
if attendance_file and email_file:

    # Fit into tables 
    df = pd.read_csv(attendance_file)
    emails_received_df = pd.read_csv(email_file)

    ## Step 2: Clean up the data columns
    # We strip extra spaces and make lowercase for easy matching
    df.columns = df.columns.str.strip()
    emails_received_df.columns = emails_received_df.columns.str.strip()

    ## Step 3: Milestone logic 
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

    # Using 'Total attendances' from your new file format
    df['Milestone'] = df['Total attendances'].apply(get_milestone)
    eligible = df[df['Milestone'] > 0].copy()

    ## Step 4: Cross reference with the Email List
    # Match by Email column in both files
    already_received_emails = set(emails_received_df['Email'].astype(str).str.strip().str.lower())
    eligible['Already received?'] = eligible['Email'].astype(str).str.strip().str.lower().isin(already_received_emails)

    ## Step 5: Filter and summary 
    # Only show people who reached a milestone and are NOT in the email list
    new_eligible = eligible[eligible['Already received?'] == False].copy()

    st.divider()

    if not new_eligible.empty:
        # Display a summary of totals 
        summary_col1, summary_col2, summary_col3 = st.columns(3) 
        summary_col1.metric("🧡 50 Total Attendances", int((new_eligible['Milestone'] == 50).sum()))
        summary_col2.metric("✨ 100 Total Attendances", int((new_eligible['Milestone'] == 100).sum()))
        summary_col3.metric("🎉 150+ Total Attendances", int((new_eligible['Milestone'] >= 150).sum()))       

        st.subheader(f"New Milestones ({len(new_eligible)})")
        
        # Display table with relevant columns from your new file
        display_df = new_eligible[['Full name', 'Total attendances', 'Milestone', 'Email']]
        display_df.columns = ['Name', 'Attendances', 'Milestone', 'Email']
        st.dataframe(display_df, use_container_width=True)

        ## Step 6: Download 
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Milestone List (CSV)",
            data=csv_data,
            file_name='updated_milestones.csv',
            mime='text/csv'
        )                  
    else: 
        st.balloons()
        st.success("Everyone is up to date with their milestones!")

else: 
    st.info("Please upload both the Booking System CSV and the Email List CSV please <3")