import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cyclistic Bike Analysis", layout="centered")

df = pd.read_parquet("..\\data\\processed\\df_processed.parquet")
df_station = pd.read_parquet("..\\data\\processed\\df_without_nulls.parquet")

df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at']   = pd.to_datetime(df['ended_at'])
df['duration']   = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

st.title("Cyclistic Bike Analysis Report")
st.markdown("**Habiba Ebrahim** | Analysis to convert more casual riders into annual members")
st.divider()

# -------------------------------------------------------
st.subheader("Distribution of Bike Types")

bike_counts = df['rideable_type'].value_counts().reset_index()
bike_counts.columns = ['rideable_type', 'count']

fig1 = px.pie(bike_counts, values='count', names='rideable_type',
              title='Distribution of Bike Types', width=800, height=400)
st.plotly_chart(fig1, use_container_width=True)

st.info("Electric bikes account for **66.1%** of all rides vs **33.9%** for classic bikes. Expanding electric bike availability — especially at high-traffic casual stations — could lower the barrier for casual users and make a membership feel more worthwhile.")

st.divider()

# -------------------------------------------------------
st.subheader("Distribution of User Types")

users_type = df['member_casual'].value_counts().reset_index()
users_type.columns = ['member_casual', 'count']

fig2 = px.pie(users_type, values='count', names='member_casual',
              title='Distribution of User Types', width=800, height=400)
st.plotly_chart(fig2, use_container_width=True)

st.info("Casual users represent **35.7%** of all rides — a significant base with clear conversion potential. Even a small shift in this segment toward annual membership would have a meaningful impact on revenue.")

st.divider()

# -------------------------------------------------------
st.subheader("Weekly Usage")

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
counts = df.groupby(['day_of_week', 'member_casual']).size().reset_index(name='ride_count')

fig3 = px.bar(counts, x='day_of_week', y='ride_count', color='member_casual',
              barmode='group', text='ride_count',
              category_orders={'day_of_week': day_order},
              title='Number of Rides by Day of Week', width=800, height=400)
fig3.update_traces(texttemplate='%{text:,}', textposition='outside')
st.plotly_chart(fig3, use_container_width=True)

st.info("Casual users ride most on **weekends** — this is the best window to reach them. Weekend-exclusive membership trials, discounts, or promotions placed at peak stations on Saturdays could drive conversions directly at the point of highest engagement.")

st.divider()

# -------------------------------------------------------
st.subheader("Hourly Usage")

hours = df.groupby(['hour', 'member_casual']).size().reset_index(name='ride_count')

fig4 = px.bar(hours, x='hour', y='ride_count', color='member_casual',
              barmode='group', text='ride_count',
              title='Number of Rides by Hour of Day', width=800, height=500)
fig4.update_traces(texttemplate='%{text:,}', textposition='outside')
st.plotly_chart(fig4, use_container_width=True)

st.info("Casual users peak around **4–6 PM**, while members also show strong activity at **7–9 AM** — a commuting pattern absent in casuals. Highlighting the cost savings and convenience of membership for daily commuting could appeal to casual users who already ride frequently in the afternoon.")

st.divider()

# -------------------------------------------------------
st.subheader("Monthly Riding Trends")

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
months = df.groupby(['month', 'member_casual']).size().reset_index(name='ride_count')

fig5 = px.bar(months, x='month', y='ride_count', color='member_casual',
              barmode='group', text='ride_count',
              category_orders={'month': month_order},
              title='Number of Rides by Month', width=800, height=400)
fig5.update_traces(texttemplate='%{text:,}', textposition='outside')
st.plotly_chart(fig5, use_container_width=True)

st.info("Casual usage spikes in **July and August** — the ideal time to launch conversion campaigns. Catching casual users at their peak engagement with a summer membership offer (e.g. discounted first year) maximizes the chance of long-term retention.")

st.divider()

# -------------------------------------------------------
st.subheader("Average Ride Duration by User Type")

Q1 = df['duration'].quantile(0.25)
Q3 = df['duration'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

duration_no_outliers = (
    df[(df['duration'] >= lower) & (df['duration'] <= upper)]
    .groupby('member_casual')['duration']
    .mean()
    .reset_index()
)

fig6 = px.bar(duration_no_outliers, x='member_casual', y='duration', text='duration',
              title='Average Ride Duration by User Type', width=800, height=400)
fig6.update_traces(texttemplate='%{text:.2f} min', textposition='outside')
st.plotly_chart(fig6, use_container_width=True)

st.info("Casual riders average **11.7 min** per ride vs **10.03 min** for members. Longer rides mean more spend per trip — messaging that frames membership as a cost-effective alternative for frequent recreational riders could resonate strongly with this group.")

st.divider()

# -------------------------------------------------------
st.subheader("Median Ride Duration by Day of Week")

avg_duration_by_day = df.groupby('day_of_week')['duration'].median().reset_index()

fig7 = px.bar(avg_duration_by_day, x='day_of_week', y='duration', text='duration',
              title='Median Ride Duration by Day of Week', width=800, height=400)
fig7.update_traces(texttemplate='%{text:.2f} min', textposition='outside')
st.plotly_chart(fig7, use_container_width=True)

st.info("Rides are longest on **Saturday (10.78 min)** and **Sunday (10.69 min)**. Since casual users take longer leisure rides on weekends, promoting membership benefits like unlimited ride time or no per-minute fees could directly address their usage pattern.")

st.divider()

# -------------------------------------------------------
st.subheader("Bike Type by User")

bike_type_by_user = (
    df.groupby(['member_casual'])['rideable_type']
    .value_counts()
    .reset_index(name='count')
)

fig8 = px.bar(bike_type_by_user, x='rideable_type', y='count', color='member_casual',
              barmode='group', text='count',
              title='Distribution of Bike Types by User Type', width=800, height=400)
fig8.update_traces(texttemplate='%{text:,}', textposition='outside')
st.plotly_chart(fig8, use_container_width=True)

st.info("Both groups strongly prefer **electric bikes**. Offering members priority access to electric bikes or guaranteed availability could be a compelling membership perk to attract casual users who already prefer them.")

st.divider()

# -------------------------------------------------------
st.subheader("Most Popular Start Stations for Casual Users")

top_casual_stations = (
    df_station[df_station['member_casual'] == 'casual']
    .groupby('start_station_name')
    .size()
    .reset_index(name='count')
    .sort_values('count', ascending=True)
    .tail(10)
)

fig9 = px.bar(top_casual_stations, x='count', y='start_station_name',
              orientation='h', hover_name='start_station_name', text='count',
              width=800, height=400)
fig9.update_yaxes(showticklabels=False)
st.plotly_chart(fig9, use_container_width=True)

st.info("Top stations like **Navy Pier**, **DuSable Lake Shore Dr**, and **Millennium Park** are all tourist and leisure hotspots. These are prime locations for on-site membership promotions, QR code campaigns, and digital ads targeting casual users at their highest-traffic touchpoints.")

st.divider()

# -------------------------------------------------------
st.subheader("Seasonal Usage Trends")

monthly_usage = df.groupby(['month', 'member_casual']).size().reset_index(name='count')

fig10 = px.line(monthly_usage, x='month', y='count', color='member_casual',
                markers=True, title='Monthly Usage Trend: Members vs Casual Riders',
                width=800, height=400)
fig10.update_layout(template='simple_white')
st.plotly_chart(fig10, use_container_width=True)

st.info("Casual usage drops sharply in winter while members stay consistent — showing that membership encourages year-round commitment. Promoting this stability angle ('ride anytime, not just in summer') could help convert seasonally-active casual users into committed annual members.")
