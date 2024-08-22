####### Author: Megh KC ##########
##### Script made for Interactive Seasonal Freight Data Visualization #########
##### Created Date: 08/21/2024 #######
##### Dashboard Creation using streamlit ##########

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json

# Sidebar navigation to select the dashboard
st.sidebar.title("Dashboard Selection")
dashboard = st.sidebar.radio("Select Dashboard", ("Rail Dashboard", "Water Dashboard"))

# Rail Dashboard
if dashboard == "Rail Dashboard":
    # Load the Rail dataset
    df = pd.read_csv('Rail_Carloadings_originated.csv')

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Function to determine the season based on the month
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'

    # Apply the function to create a new 'Season' column
    df['Season'] = df['Month'].apply(get_season)

    # Sidebar filters for year and railroad
    st.sidebar.header('Filter Options')
    selected_years = st.sidebar.multiselect('Select Year(s)', options=df['Year'].unique(), default=df['Year'].unique())
    selected_railroads = st.sidebar.multiselect('Select Railroad(s)', options=df['Railroad'].unique(), default=df['Railroad'].unique())

    # Filter the data based on selections
    filtered_df = df[(df['Year'].isin(selected_years)) & (df['Railroad'].isin(selected_railroads))]

    # Overall trend line chart for carloads by railroad over time
    st.header('Trend of Carloads Over Time by Railroad')
    date_totals_rr = df.groupby(['Date', 'Railroad']).agg({'Carloads': 'sum'}).reset_index()
    pivot_df_date_rr = date_totals_rr.pivot(index='Date', columns='Railroad', values='Carloads').fillna(0)

    option = st.radio("View", ("Chart", "Data"), key="railroad")
    if option == "Chart":
        st.line_chart(pivot_df_date_rr)
    else:
        st.dataframe(pivot_df_date_rr)

    # Overall trend line chart for carloads by commodity type over time
    st.header('Trend of Carloads Over Time by Commodity Type')
    date_totals_commodity = df.groupby(['Date', 'Commodity']).agg({'Carloads': 'sum'}).reset_index()
    pivot_df_date_commodity = date_totals_commodity.pivot(index='Date', columns='Commodity', values='Carloads').fillna(0)

    option = st.radio("View", ("Chart", "Data"), key="commodity")
    if option == "Chart":
        st.line_chart(pivot_df_date_commodity)
    else:
        st.dataframe(pivot_df_date_commodity)

    # Display the filtered data charts
    st.header('Filtered Data Visualizations')

    # Group by Year and Month, then plot bar chart
    monthly_totals_year = filtered_df.groupby(['Year', 'Month']).agg({'Carloads': 'sum'}).reset_index()
    pivot_df_year = monthly_totals_year.pivot(index='Year', columns='Month', values='Carloads').fillna(0)
    st.subheader('Total Carloads by Year and Month')
    option = st.radio("View", ("Chart", "Data"), key="year_month")
    if option == "Chart":
        st.bar_chart(pivot_df_year)
    else:
        st.dataframe(pivot_df_year)

    # Group by Year and Season, then plot bar chart
    seasonal_totals_year = filtered_df.groupby(['Year', 'Season']).agg({'Carloads': 'sum'}).reset_index()
    pivot_df_year = seasonal_totals_year.pivot(index='Year', columns='Season', values='Carloads').fillna(0)

    st.subheader('Total Carloads by Year and Season')
    option = st.radio("View", ("Chart", "Data"), key="year_season")
    if option == "Chart":
        st.bar_chart(pivot_df_year)
    else:
        st.dataframe(pivot_df_year)

    # Calculate percentage of carloads by Year and Season and plot stacked bar chart
    pivot_df_year_percent = pivot_df_year.div(pivot_df_year.sum(axis=1), axis=0) * 100

    st.subheader('Percentage of Carloads by Year and Season')
    option = st.radio("View", ("Chart", "Data"), key="year_season_percent")
    if option == "Chart":
        st.bar_chart(pivot_df_year_percent)
    else:
        st.dataframe(pivot_df_year_percent)

    # Group by Railroad and Season, then plot bar chart
    seasonal_totals_rr = filtered_df.groupby(['Railroad', 'Season']).agg({'Carloads': 'sum'}).reset_index()
    pivot_df_rr = seasonal_totals_rr.pivot(index='Railroad', columns='Season', values='Carloads').fillna(0)

    st.subheader('Total Carloads by Railroad and Season')
    option = st.radio("View", ("Chart", "Data"), key="railroad_season")
    if option == "Chart":
        st.bar_chart(pivot_df_rr)
    else:
        st.dataframe(pivot_df_rr)

    # Plot pie chart for total carloads by season
    total_carloads_by_season = filtered_df.groupby('Season').agg({'Carloads': 'sum'})

    st.subheader('Total Carloads by Season')
    option = st.radio("View", ("Chart", "Data"), key="season_pie")
    if option == "Chart":
        fig, ax = plt.subplots()
        ax.pie(total_carloads_by_season['Carloads'], labels=total_carloads_by_season.index, autopct='%1.1f%%')
        ax.set_title('Total Carloads by Season')
        st.pyplot(fig)
    else:
        st.dataframe(total_carloads_by_season)
    
    # Plot pie chart for total carloads by month
    total_carloads_by_month = filtered_df.groupby('Month').agg({'Carloads': 'sum'})
    st.subheader('Total Carloads by Month')
    option = st.radio("View", ("Chart", "Data"), key="month_pie")
    if option == "Chart":
        fig, ax = plt.subplots()
        ax.pie(total_carloads_by_month['Carloads'], labels=total_carloads_by_month.index, autopct='%1.1f%%')
        ax.set_title('Total Carloads by Month')
        st.pyplot(fig)
    else:
        st.dataframe(total_carloads_by_month)

# Water Dashboard
elif dashboard == "Water Dashboard":
    # Load the Water dataset
    # File path to the JSON dataset
    file_path = 'port_dataset.json'

    # Load JSON data
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

            # Show filtered data as a table
            st.write('Filtered Data Table', filtered_df)
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

        # Show seasonal filtered data as a table
        st.write('Filtered Seasonal Data Table', seasonal_filtered_df)
    else:
        st.write("Please select at least one port for seasonal analysis.")
