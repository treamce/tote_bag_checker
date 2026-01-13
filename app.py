## Tote Bag Tracker!! <3

## Import necessary libraries
import streamlit as st 
import pandas as pd 

## Set up the Streamlit app page 
st.set_page_config(page_title="Tote Bag Tracker", page_icon="🛍️", layout="wide")
st.title("Tote Bag Tracker")
st.write("Upload bookings to see who has earned a tote bag <3")

## Step 1: Upload files
col1, col2 = st.columns(2)

with col1: 
    # Upload booking system csv file (Customer level data)
    attendance_file = st.file_uploader("Upload Booking System CSV", type=["csv"])
with col2: 
    # Upload email list 
    email_file = st.file_uploader("Upload Email List CSV", type=["csv"])

## Only run if both files are uploaded
if attendance_file and email_file:

    # Fit into tables 
    df = pd.read_csv(attendance_file)
    emails_df = pd.read_csv(email_file)

    ## Step 2: Set up Table and detect columns 
    # We look for a column called 'name' or use the first column
    name_col = 'name' if 'name' in [c.lower() for c in df.columns] else df.columns[0]
    
    # Look for the column that has the total classes (e.g., 'Total Bookings' or 'Count')
    count_col = None
    for col in df.columns:
        if any(word in col.lower() for word in ['count', 'total', 'classes', 'booked']):
            count_col = col
            break
    if not count_col:
        count_col = df.columns[1] # Default to second column if not found

    ## Step 3: Format the data 
    # Since the teacher said data is at 'customer level', we just grab the totals
    counts = df[[name_col, count_col]].copy()
    counts.columns = ['Name', 'Total Classes']

    ## Step 4: Milestone logic 
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

    counts['Milestone'] = counts['Total Classes'].apply(get_milestone)
    eligible = counts[counts['Milestone'] > 0].copy()

    ## Step 5: Cross reference with email list
    # Get names from the first column of the email list CSV
    prev_recipients = set(emails_df.iloc[:, 0].astype(str).str.strip().str.lower())

    # Check if people already have a bag