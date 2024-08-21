import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Get the absolute path to the file based on the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
root_dir = os.path.abspath(os.path.join(current_dir, ".."))  # Go one level up to the root directory
file_path = os.path.join(root_dir, 'Data', 'port_dataset.json')

# File path to the JSON dataset
file_path = '../Data/port_dataset.json'

if not os.path.exists(file_path):
    st.error(f"File not found: {file_path}. Please check the file path and ensure the file is available.")
else:
    with open(file_path, 'r') as file:
        parsed_data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(parsed_data)

# Melt the DataFrame to get the desired format
df_melted = df.melt(id_vars=["port"], var_name="port_name", value_name="TEU_values")

# Ensure the 'port' column is in datetime format
df_melted['port'] = pd.to_datetime(df_melted['port'], errors='coerce')

# Convert TEU values to numeric (with error coercion to handle non-numeric values)
df_melted['TEU_values'] = pd.to_numeric(df_melted['TEU_values'], errors='coerce')

# Drop rows where TEU_values could not be converted to numeric
df_melted = df_melted.dropna(subset=['TEU_values'])

# Extract the month and year from the 'port' column
df_melted['month'] = df_melted['port'].dt.strftime('%b')
df_melted['year'] = df_melted['port'].dt.year

# Function to categorize each month by season
def get_season(month):
    if month in ['Dec', 'Jan', 'Feb']:
        return 'Winter'
    elif month in ['Mar', 'Apr', 'May']:
        return 'Spring'
    elif month in ['Jun', 'Jul', 'Aug']:
        return 'Summer'
    elif month in ['Sep', 'Oct', 'Nov']:
        return 'Fall'

# Apply the season categorization
df_melted['season'] = df_melted['month'].apply(get_season)

# Group the data by season and port to calculate the total container volume for each season
seasonal_cargo_volumes = df_melted.groupby(['season', 'port_name']).agg({'TEU_values': 'sum'}).reset_index()

# Streamlit app
st.title('US Ports Activity Dashboard')

# Sidebar - Year and Month filter
selected_years = st.sidebar.multiselect('Select Year(s)', df_melted['year'].unique(), default=df_melted['year'].unique())
selected_months = st.sidebar.multiselect('Select Month(s)', df_melted['month'].unique(), default=df_melted['month'].unique())

# Sidebar - Port comparison filter
ports = df_melted['port_name'].unique().tolist()
selected_ports = st.sidebar.multiselect('Select Ports to Compare', ports, default=ports[:2])

# Filter the dataframe based on the selected years and months
filtered_df = df_melted[(df_melted['year'].isin(selected_years)) & (df_melted['month'].isin(selected_months))]

# Initial line chart for all ports over the entire period
line_chart_all_ports = px.line(df_melted, x='port', y='TEU_values', color='port_name', 
                               title='Monthly Container Throughput for All Ports', 
                               labels={'port': 'Date', 'TEU_values': 'TEU'})
st.plotly_chart(line_chart_all_ports)

# Display charts and table only if ports and dates are selected
if selected_ports and not filtered_df.empty:
    # Ensure selected ports exist in the filtered DataFrame
    available_ports = filtered_df['port_name'].unique().tolist()
    missing_ports = set(selected_ports) - set(available_ports)
    
    if missing_ports:
        st.warning(f"The following ports have no data for the selected period: {', '.join(missing_ports)}")
    
    # Filter selected_ports to only those available in the filtered DataFrame
    valid_ports = list(set(selected_ports) & set(available_ports))
    
    if valid_ports:
        # Stacked bar chart for selected ports and dates
        stacked_bar_chart = filtered_df[filtered_df['port_name'].isin(valid_ports)]
        bar_chart = px.bar(stacked_bar_chart, 
                           x='port_name', y='TEU_values', color='port', 
                           title='Stacked Bar Chart of Monthly Throughput', 
                           labels={'port_name': 'Port', 'TEU_values': 'Throughput'})
        st.plotly_chart(bar_chart)

        # Use the same data for the pie chart
        total_throughput = stacked_bar_chart.groupby('port_name')['TEU_values'].sum()

        # Pie chart for the selected time period and ports
        pie_chart = px.pie(total_throughput, names=total_throughput.index, values=total_throughput.values, 
                           title=f'Throughput Share for Selected Period')
        st.plotly_chart(pie_chart)

        # Bubble chart based on the same total throughput values
        bubble_data = total_throughput.reset_index()
        bubble_data.columns = ['Port', 'Total Volume']

        # Ensure that 'Total Volume' is numeric
        bubble_data['Total Volume'] = pd.to_numeric(bubble_data['Total Volume'], errors='coerce')

        # Drop any rows with NaN values (if conversion fails for any row)
        bubble_data = bubble_data.dropna(subset=['Total Volume'])

        bubble_chart = px.scatter(bubble_data, x='Port', y='Total Volume', 
                                  size='Total Volume', color='Port',
                                  title='Bubble Chart of Total Container Volume by Port', 
                                  size_max=60)

        # Customize the bubble chart: remove axis lines, labels, and grid lines
        bubble_chart.update_layout(
            xaxis_showgrid=False, 
            yaxis_showgrid=False, 
            xaxis=dict(showline=False, showticklabels=False),
            yaxis=dict(showline=False, showticklabels=False),
            showlegend=False
        )
        
        st.plotly_chart(bubble_chart)

        # # Show filtered data as a table
        # st.write('Filtered Data Table', filtered_df)
    else:
        st.warning("No valid data available for the selected ports and period.")
else:
    st.write("Please select at least one port and one date range.")

# Section for Seasonal Variation Analysis
st.header('Seasonal Variation in Container Throughput')

# Filter the seasonal dataframe based on the selected ports
seasonal_filtered_df = seasonal_cargo_volumes[seasonal_cargo_volumes['port_name'].isin(selected_ports)]

# Stacked bar chart showing seasonal container throughput for each port
if not seasonal_filtered_df.empty:
    seasonal_bar_chart = px.bar(seasonal_filtered_df, 
                                x='port_name', y='TEU_values', color='season', 
                                title='Seasonal Container Throughput by Port',
                                labels={'port_name': 'Port', 'TEU_values': 'Total TEU'},
                                barmode='stack')
    st.plotly_chart(seasonal_bar_chart)

    # Pie chart showing the total seasonal container throughput
    total_seasonal_throughput = seasonal_filtered_df.groupby('season')['TEU_values'].sum().reset_index()
    seasonal_pie_chart = px.pie(total_seasonal_throughput, names='season', values='TEU_values', 
                                title=f'Total Seasonal Container Throughput')
    st.plotly_chart(seasonal_pie_chart)

    # # Show seasonal filtered data as a table
    # st.write('Filtered Seasonal Data Table', seasonal_filtered_df)
else:
    st.write("Please select at least one port for seasonal analysis.")





