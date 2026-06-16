import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

#Page Configuration

st.set_page_config(
    page_title="Automobiles Price Analysis in Nigerian Dashboard",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data #Decorator to speed up the app
def load_data():
    try:
        df = pd.read_csv("data/cleaned_jiji_autos.csv")
        return df
    except FileExistsError as e:
        st.warning(f'Error!: {e}')


def sidebar_filter(df):
    st.sidebar.header('Cars Filters')

    car_brand = st.sidebar.multiselect(
        'Choose Brand',
        options=df['Make'].unique(),
        default=df['Make'].unique()
    )

    car_condition = st.sidebar.multiselect(
        'Choose Condition',
        options=df['Condition'].unique(),
        default=df['Condition'].unique()
    )

    car_transmission = st.sidebar.multiselect(
        'Auto or Manual',
        options=df['Transmission'].unique(),
        default=df['Transmission'].unique()
    )
    return car_brand, car_condition, car_transmission

    #To connect the filters
def filter_data(df, car_brand, car_condition, car_transmission):
    filtered_df = df[df['Make'].isin(car_brand) & df['Condition'].isin(car_condition) & df['Transmission'].isin(car_transmission)]
    return filtered_df

#KPI Metrics
def display_kpi(filtered_df):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('🚓 Total Cars', len(filtered_df))

    with col2:
        average_cars = filtered_df['Price'].mean() if len(filtered_df) > 0 else 0
        st.metric('🚌 Average Car Price', f'${average_cars:,.2f}')

    with col3:
        common_cars = filtered_df['Make'].mode()[0] if len(filtered_df) > 0 else 0
        st.metric('🚙 Top Brand', common_cars)

    with col4:
        foreign_pct = (filtered_df['Condition'] == 'Foreign Used').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric('🚢Foreign Used Cars', f'{foreign_pct:.2f}%')

def charts(filtered_df):
    if len(filtered_df) == 0:
        st.warning("Please Select Filters")
        return
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Count of Cars by Brands")
        brand_count = filtered_df['Make'].value_counts()
        fig1 = px.bar(
        x=brand_count.index,
        y=brand_count.values,
        )
        fig1.update_layout(
            xaxis_title="Car Brands",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig1, width='stretch')

    with col2:
        st.subheader('Average Price By Brand')
        brand = filtered_df.groupby('Make')['Price'].mean().sort_values(ascending=False)
        fig2 = px.bar(
            x=brand.values,
            y=brand.index,
        )
        fig2.update_layout(
            xaxis_title="Average Price",
            yaxis_title="Car Brands"
        )
        st.plotly_chart(fig2, width='stretch')

    col3, col4 = st.columns(2)

    with col3:
           st.subheader("Price Distribution by Condition")
           fig3 = px.box(
           filtered_df,
           x='Condition',
           y='Price'
           )
           st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader('Distribution of Year')
        fig4 = px.histogram(
            filtered_df, x='Year', nbins=20
        )
        fig4.update_traces(
            marker_line_color='white',
            marker_line_width=1
        )
        fig4.update_layout(
            xaxis_title='Year',
            yaxis_title='Frequency'
        )
        st.plotly_chart(fig4, width='stretch')

    col5, col6 = st.columns(2)
    with col5:
        fig5 = px.scatter(
            filtered_df,
            x="Year",
            y="Price",
            color='Condition',
            title="Price vs. Year by Condition",
            labels={'year': 'Year', 'price': 'Price', 'condition': 'Condition'},
            hover_data=['Condition']
        )
        fig5.update_traces(
            marker=dict(size=12, opacity=0.8)
        )
        fig5.update_layout(
            xaxis_title="Year", 
            yaxis_title="Price"
        )
        st.plotly_chart(fig5, use_container_width=True)


    with col6:
        st.subheader("Correlation Heatmap")
        num_data = filtered_df.select_dtypes(include=['number'])
        corr = num_data.corr()
        fig6, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
        corr,
        annot=True,
        cmap="vlag",
        fmt=".2f",
        linewidths=0.5,
        ax=ax
        )
        st.pyplot(fig6)

def table_data(filtered_df):
    if len (filtered_df) > 0:
        st.dataframe(filtered_df, width='stretch', height=300)
    else:
        st.warning("No Cars Data To Display")


#Control Function
def main():
    #load data
    df = load_data()

    #sidebar call
    car_brand, car_condition, car_transmission = sidebar_filter(df)

    #filter connection
    filtered_df = filter_data(df, car_brand, car_condition, car_transmission)

    st.title('Automobile Price Analysis in the Nigerian Dashboard')
    st.markdown('---')

    #call filter
    display_kpi(filtered_df)

    #Display Chart
    st.markdown("---")
    charts(filtered_df)

    #Display dataframe
    st.markdown("---")
    table_data(filtered_df)

main()
