## Tote Bag Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="Tote Bag Tracker", page_icon="🛍️", layout="wide")
st.title("Tote Bag Tracker")
st.write("Upload bookings to see who has earned a tote bag <3")

## Step 1 : Upload files
col1, col2 = st.columns(2)

with col1: 
# Upload booking system csv file (The one with Name, Bookings, and Email)
    attendance_file = st.file_uploader("Upload Booking System CSV", type=["csv"])
with col2: 
# Upload email list (The one with just the Email column)
    email_file = st.file_uploader("Upload Email List CSV", type=["csv"])

## Only run if both files are uploaded
if attendance_file and email_file:

    # Fit into tables 
    df = pd.read_csv(attendance_file)
    emails_received_df = pd.read_csv(email_file)

    ## Step 2: Clean up the data columns
    # We strip any extra spaces from the column names so they match perfectly
    df.columns = df.columns.str.strip()
    emails_received_df.columns = emails_received_df.columns.str.strip()

    ## Step 3: Milestone logic 
    def get_milestone(n): 
        try:
            n = int(n)
            if n >= 300: return 300
            if n >= 250: return 250
            if n >= 200: return 200
            if n >= 150: return 150
            if n >= 100: return 100
            if n >= 50: return 50
        except:
            return 0
        return 0

    # Apply milestone logic to your 'Bookings' column
    df['Milestone'] = df['Bookings'].apply(get_milestone)
    eligible = df[df['Milestone'] > 0].copy()

    ## Step 4: Cross reference with the Email List
    # We match by Email because it's more accurate than names! <3
    # This creates a list of people who have already been sent a bag email
    already_received_emails = set(emails_received_df['Email'].astype(str).str.strip().str.lower())

    # Check if the student's email is already in the list of people who got a bag
    eligible['Already received?'] = eligible['Email'].astype(str).str.strip().str.lower().isin(already_received_emails)

    ## Step 5: Filter and summary 
    # Only show people who hit the milestone and HAVEN'T received a bag yet 
    new_eligible = eligible[eligible['Already received?'] == False].copy()

    st.divider()

    if not new_eligible.empty:
        # Display a summary of totals 
        summary_col1, summary_col2, summary_col3 = st.columns(3) 
        summary_col1.metric("50 Class Bags", int((new_eligible['Milestone'] == 50).sum()))
        summary_col2.metric("100 Class Bags", int((new_eligible['Milestone'] == 100).sum()))
        summary_col3.metric("150+ Class Bags", int((new_eligible['Milestone'] >= 150).sum()))       

        st.subheader(f"New bags to gift ({len(new_eligible)})")
        
        # Display table with your columns
        st.dataframe(new_eligible[['Name', 'Bookings', 'Milestone', 'Email']], use_container_width=True)

        ## Step 6: Download 
        csv_data = new_eligible.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Tote Bag List as CSV",
            data=csv_data,
            file_name='tote_bag_eligibility.csv',
            mime='text/csv'
        )                  
    else: 
        st.success("Everyone is up to date with their tote bags! <3")

else: 
    st.info("Please upload both the Booking System CSV and the Email List CSV please <3")