## Tote Bag Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="Tote Bag Tracker", page_icon="🛍️", layout="wide")

## --- Styling ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛍️ Tote Bag Tracker")
st.write("Upload bookings to see who has earned a tote bag <3")

## Step 1 : Upload files
col1, col2 = st.columns(2)

with col1: 
# Upload booking system csv file
    attendance_file = st.file_uploader("Upload Booking System CSV", type=["csv"])
with col2: 
# Upload email list 
    email_file = st.file_uploader("Upload Email List CSV", type=["csv"])

## Only run if both files are uploaded
if attendance_file and email_file:

    # Fit into tables 
    df = pd.read_csv(attendance_file)
    emails_received_df = pd.read_csv(email_file)

    ## Step 2: Clean up the data columns
    df.columns = df.columns.str.strip().str.lower()
    emails_received_df.columns = emails_received_df.columns.str.strip().str.lower()

    # Define our targets based on your file structure
    name_col = 'name' if 'name' in df.columns else df.columns[0]
    book_col = 'bookings' if 'bookings' in df.columns else 'bookings'
    mail_col = 'email' if 'email' in df.columns else 'email'

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

    df['milestone'] = df[book_col].apply(get_milestone)
    eligible = df[df['milestone'] > 0].copy()

    ## Step 4: Cross reference with the Email List
    already_received_emails = set(emails_received_df['email'].astype(str).str.strip().str.lower())
    eligible['already received?'] = eligible[mail_col].astype(str).str.strip().str.lower().isin(already_received_emails)

    ## Step 5: Filter and summary 
    new_eligible = eligible[eligible['already received?'] == False].copy()

    st.divider()

    if not new_eligible.empty:
        # Display a summary of totals 
        summary_col1, summary_col2, summary_col3 = st.columns(3) 
        summary_col1.metric("🎒 50 Class Bags", int((new_eligible['milestone'] == 50).sum()))
        summary_col2.metric("🎁 100 Class Bags", int((new_eligible['milestone'] == 100).sum()))
        summary_col3.metric("✨ 150+ Class Bags", int((new_eligible['milestone'] >= 150).sum()))       

        st.subheader(f"New bags to gift ({len(new_eligible)})")
        
        # Display table
        display_df = new_eligible[[name_col, book_col, 'milestone', mail_col]]
        display_df.columns = ['Name', 'Total Bookings', 'Milestone', 'Email']
        st.dataframe(display_df, use_container_width=True)

        ## Step 6: Download 
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Tote Bag List as CSV",
            data=csv_data,
            file_name='tote_bag_eligibility.csv',
            mime='text/csv'
        )                  
    else: 
        st.balloons()
        st.success("Everyone is up to date with their tote bags! <3")

else: 
    st.info("Please upload both the Booking System CSV and the Email List CSV please <3")