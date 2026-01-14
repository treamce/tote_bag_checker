## J&S Milestone Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="J&S Milestone Tracker", page_icon="🧡", layout="wide")

## --- Styling ---
st.markdown("""
    <style>
    /* Metric Value (The Number) */
    [data-testid="stMetricValue"] {
        color: #f48c36 !important;
    }
    /* Metric Label (The Heading) - Now Bigger and Bolder */
    [data-testid="stMetricLabel"] p {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #333333 !important;
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

    df['Milestone'] = df['Total attendances'].apply(get_milestone)
    eligible = df[df['Milestone'] > 0].copy()

    ## Step 4: Multi-Milestone Cross Reference
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
        new_eligible = eligible[eligible['Already received?'] == False].copy()
    else:
        st.error("Wait! The 'Previous Recipients' CSV needs an 'Email' and a 'Milestone' column for this to work. <3")
        new_eligible = pd.DataFrame()

    st.divider()

    if not new_eligible.empty:
        # Step 5: Summary with 8 Specific Buckets and Emojis
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        row1_col1.metric("🧡 50-99", len(new_eligible[new_eligible['Milestone'] == 50]))
        row1_col2.metric("✨ 100-149", len(new_eligible[new_eligible['Milestone'] == 100]))
        row1_col3.metric("🎉 150-199", len(new_eligible[new_eligible['Milestone'] == 150]))
        row1_col4.metric("🔥 200-249", len(new_eligible[new_eligible['Milestone'] == 200]))

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        row2_col1.metric("🏅 250-299", len(new_eligible[new_eligible['Milestone'] == 250]))
        row2_col2.metric("⭐ 300-349", len(new_eligible[new_eligible['Milestone'] == 300]))
        row2_col3.metric("👑 350+", len(new_eligible[new_eligible['Milestone'] == 350]))
        row2_col4.metric("📊 Total New", len(new_eligible))

        # --- Enhanced Row Shading Logic ---
        def style_rows(row):
            m = row['Milestone']
            colors = {
                50:  'background-color: #fffaf0; color: #8a5a00;', 
                100: 'background-color: #fff3e0; color: #8a5a00;', 
                150: 'background-color: #ffe0b2; color: #5f3a00;', 
                200: 'background-color: #ffcc80; color: #4e2f00;', 
                250: 'background-color: #ffb74d; color: #000000;', 
                300: 'background-color: #ffa726; color: #000000;', 
                350: 'background-color: #fb8c00; color: #ffffff;'  
            }
            background = colors.get(m, '')
            return [background] * len(row)

        st.subheader(f"📋 New Milestones ({len(new_eligible)})")
        
        display_df = new_eligible[['Full name', 'Total attendances', 'Milestone', 'Email']]
        display_df.columns = ['Name', 'Attendances', 'Milestone', 'Email']
        
        # Display with row styling
        styled_df = display_df.sort_values('Milestone', ascending=False).style.apply(style_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True)

        action_csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download List (CSV)",
            data=action_csv,
            file_name='attendances_action.csv',
            mime='text/csv'
        ) 

        st.divider()
        
        # Master Log Update (Emoji removed)
        st.subheader("Master Log Update")
        st.info("Add these rows to your 'Previous Recipients' CSV history to keep the tracker accurate.")
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