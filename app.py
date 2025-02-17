import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Heart Disease Analysis",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Update the Custom CSS to improve UI, metrics visibility, and title colors
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    /* Metric card styling */
    div[data-testid="metric-container"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 1rem;
        border-radius: 10px;
        color: #f3f4f6;
        margin: 0.5rem 0;
    }
    
    div[data-testid="metric-container"] label {
        color: #9ca3af;
    }
    
    div[data-testid="metric-container"] .st-emotion-cache-1gx6t7g {
        color: #f3f4f6 !important;
    }
    
    div[data-testid="metric-container"] .st-emotion-cache-10y5sf6 {
        color: #9ca3af !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937;
        border-radius: 4px;
        color: #f3f4f6;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #374151;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f3f4f6;
    }
    
    /* Chart background */
    .st-emotion-cache-1r6slb0 {
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    
    /* Title and Headers styling */
    h1 {
        color: #f3f4f6 !important;
        text-align: center;
        padding: 1.5rem;
    }
    
    h2, h3, .stMarkdown {
        color: #f3f4f6 !important;
    }
    
    /* Override any Streamlit default text colors */
    .stMarkdown p, .stMarkdown span {
        color: #f3f4f6 !important;
    }
    
    /* Make sure sidebar text is visible */
    .sidebar .stMarkdown {
        color: #f3f4f6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Update the title styling - remove the inline style since we're handling it in CSS
st.markdown("""
    <h1>
        ❤️ Heart Disease Analysis Dashboard
    </h1>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('heart.csv')
    # Add descriptive labels for categorical variables
    df['sex'] = df['sex'].map({1: 'Male', 0: 'Female'})
    df['cp'] = df['cp'].map({0: 'Typical Angina', 1: 'Atypical Angina', 
                            2: 'Non-anginal Pain', 3: 'Asymptomatic'})
    df['target'] = df['target'].map({0: 'No Disease', 1: 'Has Disease'})
    return df

df = load_data()

# Sidebar with better organization
with st.sidebar:
    st.markdown("### 📊 Analysis Controls")
    st.markdown("---")
    
    # Add tabs in sidebar for different filter categories
    filter_tabs = st.tabs(["📋 Basic Filters", "🔍 Advanced Filters"])
    
    with filter_tabs[0]:
        age_range = st.slider(
            "Select Age Range",
            min_value=int(df['age'].min()),
            max_value=int(df['age'].max()),
            value=(int(df['age'].min()), int(df['age'].max()))
        )
        
        sex_filter = st.multiselect(
            "Select Gender",
            options=df['sex'].unique(),
            default=df['sex'].unique()
        )

    with filter_tabs[1]:
        cp_filter = st.multiselect(
            "Chest Pain Type",
            options=df['cp'].unique(),
            default=df['cp'].unique()
        )
        
        thal_filter = st.multiselect(
            "Thalassemia Type",
            options=df['thal'].unique(),
            default=df['thal'].unique()
        )

# Filter the data
filtered_df = df[
    (df['age'].between(age_range[0], age_range[1])) &
    (df['sex'].isin(sex_filter)) &
    (df['cp'].isin(cp_filter))
]

# Main content area with tabs
main_tabs = st.tabs(["📈 Overview", "🔍 Detailed Analysis", "📋 Data Explorer"])

with main_tabs[0]:
    st.markdown("<h3 style='color: #f3f4f6;'>📊 Key Metrics</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Patients",
            f"{len(filtered_df):,}",
            delta=None
        )
    with col2:
        heart_disease_pct = (
            (filtered_df['target'] == 'Has Disease').mean() * 100
        ).round(2)
        st.metric(
            "Heart Disease %",
            f"{heart_disease_pct}%",
            delta=None
        )
    with col3:
        avg_age = filtered_df['age'].mean().round(2)
        st.metric(
            "Average Age",
            f"{avg_age} years",
            delta=None
        )
    with col4:
        gender_ratio = (
            (filtered_df['sex'] == 'Male').mean() * 100
        ).round(2)
        st.metric(
            "Male %",
            f"{gender_ratio}%",
            delta=None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing

    # Create improved visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #f3f4f6;'>Age Distribution by Disease Status</h3>", unsafe_allow_html=True)
        fig_age = px.histogram(
            filtered_df, 
            x='age', 
            color='target',
            barmode='group',
            color_discrete_sequence=['#ff9999', '#66b3ff'],
            labels={'target': 'Heart Disease Status'},
            title=None  # Remove the plotly title since we're using markdown
        )
        fig_age.update_layout(
            plot_bgcolor='#1f2937',  # Match the dark theme
            paper_bgcolor='#1f2937',
            font_color='#f3f4f6',    # Light text for dark background
            margin=dict(t=20, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #f3f4f6;'>Chest Pain Types Distribution</h3>", unsafe_allow_html=True)
        fig_cp = px.pie(
            filtered_df, 
            names='cp',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_cp.update_layout(
            plot_bgcolor='#1f2937',
            paper_bgcolor='#1f2937',
            font_color='#f3f4f6',
            margin=dict(t=20, l=10, r=10, b=10)
        )
        fig_cp.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_cp, use_container_width=True)

with main_tabs[1]:
    st.markdown("### Correlation Analysis")
    
    # Correlation heatmap
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1, zmax=1
    ))
    fig_corr.update_layout(
        title='Correlation Matrix of Numerical Features',
        height=600
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with main_tabs[2]:
    st.markdown("### Interactive Data Explorer")
    
    # Add column selector
    cols_to_show = st.multiselect(
        "Select columns to display",
        options=filtered_df.columns,
        default=filtered_df.columns[:6]
    )
    
    # Add search functionality
    search = st.text_input("Search in the dataset")
    
    # Filter and display the data
    if search:
        filtered_view = filtered_df[
            filtered_df.astype(str).apply(
                lambda x: x.str.contains(search, case=False)
            ).any(axis=1)
        ]
    else:
        filtered_view = filtered_df
        
    st.dataframe(
        filtered_view[cols_to_show],
        use_container_width=True,
        height=400
    )
    
    # Add download button
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_view.to_csv(index=False).encode('utf-8'),
        file_name="heart_disease_filtered_data.csv",
        mime="text/csv"
    ) 