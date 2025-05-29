import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("📞 Call Centre Operations Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean up percentage columns
    df['Connect Rate Combined'] = df['Connect Rate Combined'].str.replace('%', '').astype(float)
    df['DMC Rate'] = df['DMC Rate'].str.replace('%', '').astype(float)
    df['Conversion'] = df['Conversion'].str.replace('%', '').astype(float)

    # Sidebar filters
    teams = st.sidebar.multiselect("Filter by Team", df["Team"].unique(), default=df["Team"].unique())
    campaigns = st.sidebar.multiselect("Filter by Campaign", df["Campaign"].unique(), default=df["Campaign"].unique())

    filtered_df = df[df["Team"].isin(teams) & df["Campaign"].isin(campaigns)]

    st.subheader("📋 Raw Data")
    st.dataframe(filtered_df)

    st.subheader("📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Outbound", int(filtered_df["Outbound"].sum()))
    col2.metric("Total Inbound", int(filtered_df["Inbound"].sum()))
    col3.metric("Sales", int(filtered_df["Sales"].sum()))

    col4, col5, col6 = st.columns(3)
    col4.metric("Avg Connect Rate", f"{filtered_df['Connect Rate Combined'].mean():.2f}%")
    col5.metric("Avg DMC Rate", f"{filtered_df['DMC Rate'].mean():.2f}%")
    col6.metric("Conversion", f"{filtered_df['Conversion'].mean():.2f}%")

    st.subheader("📊 Outbound Calls per User")
    fig = px.bar(filtered_df, x="User", y="Outbound", color="Team", title="Outbound Calls by User")
    st.plotly_chart(fig)

    st.subheader("🎯 Conversion Rate by User")
    fig2 = px.bar(filtered_df, x="User", y="Conversion", color="Campaign", title="Conversion Rate (%) by User")
    st.plotly_chart(fig2)

    st.subheader("🕒 Average Talk Time")
    df["Avg Talk Seconds"] = pd.to_timedelta(df["Avg Talk"]).dt.total_seconds()
    fig3 = px.bar(filtered_df, x="User", y="Avg Talk Seconds", color="Campaign", title="Avg Talk Time (seconds)")
    st.plotly_chart(fig3)
else:
    st.info("👆 Upload a CSV or Excel file to get started.")
