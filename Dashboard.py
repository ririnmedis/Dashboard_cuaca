import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🌪️ Dashboard Cuaca Ekstrem",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for card-based dashboard
st.markdown("""
<style>
    /* Global Styles */
    .main {
        padding-top: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .block-container {
        padding: 1rem 1.5rem;
        max-width: none;
        background: transparent;
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .dashboard-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .dashboard-grid-full {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Chart Cards */
    .chart-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .chart-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chart-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    /* Metrics Cards */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    
    .metric-card-1::before { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .metric-card-2::before { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); }
    .metric-card-3::before { background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%); }
    .metric-card-4::before { background: linear-gradient(135deg, #00b894 0%, #00a085 100%); }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        opacity: 0.8;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #2d3748;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        backdrop-filter: blur(20px);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    .dashboard-description {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0.5rem 0 0 0;
    }
    
    /* Control Cards */
    .control-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
    }
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Responsive */
    @media (max-width: 768px) {
        .dashboard-grid, .dashboard-grid-2 {
            grid-template-columns: 1fr;
        }
        .metrics-row {
            grid-template-columns: repeat(2, 1fr);
        }
        .chart-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_weather_data():
    try:
        # Load the CSV file
        df = pd.read_csv('GlobalWeatherRepository.csv')
        
        # Data cleaning and preprocessing
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df['date'] = df['last_updated'].dt.date
        df['month'] = df['last_updated'].dt.month
        df['year'] = df['last_updated'].dt.year
        df['hour'] = df['last_updated'].dt.hour
        
        # Define extreme weather conditions
        def classify_extreme_weather(row):
            extremes = []
            
            # Temperature extremes (below 0°C or above 40°C)
            if row['temperature_celsius'] <= 0 or row['temperature_celsius'] >= 40:
                extremes.append('Suhu Ekstrem')
            
            # High wind speed (above 30 kph)
            if row['wind_kph'] >= 30:
                extremes.append('Angin Kencang')
            
            # Heavy precipitation (above 10mm)
            if row['precip_mm'] >= 10:
                extremes.append('Hujan Ekstrem')
            
            # Extreme conditions from text
            extreme_conditions = [
                'thunder', 'storm', 'heavy rain', 'snow', 'blizzard', 
                'tornado', 'cyclone', 'hurricane', 'extreme', 'severe'
            ]
            condition_lower = str(row['condition_text']).lower()
            if any(cond in condition_lower for cond in extreme_conditions):
                extremes.append('Cuaca Berbahaya')
            
            # High UV index (above 8)
            if row['uv_index'] >= 8:
                extremes.append('UV Ekstrem')
            
            return extremes if extremes else ['Normal']
        
        # Apply extreme weather classification
        df['extreme_weather'] = df.apply(classify_extreme_weather, axis=1)
        
        # Create binary extreme indicator
        df['is_extreme'] = df['extreme_weather'].apply(lambda x: 1 if x != ['Normal'] else 0)
        
        # Count total extreme events per country
        df['extreme_count'] = df['extreme_weather'].apply(lambda x: len([e for e in x if e != 'Normal']))
        
        # Regional classification
        def classify_region(country):
            asia_tenggara = ['Indonesia', 'Thailand', 'Malaysia', 'Singapore', 'Philippines', 
                           'Vietnam', 'Myanmar', 'Cambodia', 'Laos', 'Brunei']
            timur_tengah = ['Saudi Arabia', 'UAE', 'Iran', 'Iraq', 'Kuwait', 'Qatar', 
                          'Bahrain', 'Oman', 'Yemen', 'Jordan', 'Lebanon', 'Syria', 'Israel']
            
            if country in asia_tenggara:
                return 'Asia Tenggara'
            elif country in timur_tengah:
                return 'Timur Tengah'
            elif country in ['United States', 'Canada', 'Mexico']:
                return 'Amerika Utara'
            elif country in ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia']:
                return 'Amerika Selatan'
            elif country in ['Germany', 'France', 'Italy', 'Spain', 'UK', 'Poland']:
                return 'Eropa'
            elif country in ['Nigeria', 'Egypt', 'South Africa', 'Kenya', 'Morocco']:
                return 'Afrika'
            elif country in ['China', 'Japan', 'South Korea', 'India', 'Mongolia']:
                return 'Asia Timur & Selatan'
            else:
                return 'Lainnya'
        
        df['region'] = df['country'].apply(classify_region)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Header
st.markdown('''
<div class="dashboard-header">
    <h1 class="dashboard-title">🌪️  Dashboard Analisis Cuaca Ekstrem & Risiko Bencana</h1>
    
</div>
''', unsafe_allow_html=True)

# Load data
with st.spinner('🔄 Memuat data cuaca...'):
    df = load_weather_data()

if df is None:
    st.error("❌ Gagal memuat data. Pastikan file 'GlobalWeatherRepository.csv' tersedia.")
    st.stop()

# Interactive Controls
st.sidebar.markdown("""
<div style="
    background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
">
    <h2 style="margin: 0; color: white; font-size: 1.3rem; font-weight: 700;">🎛️ Pengaturan Dashboard</h2>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Sesuaikan tampilan data sesuai kebutuhan</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 **Opsi Tampilan**")
show_raw_data = st.sidebar.checkbox("📋 Tampilkan Data Mentah")

# Region filter with better UX
st.sidebar.markdown("### 🌍 **Filter Wilayah**")
all_regions = list(df['region'].unique())
selected_regions = st.sidebar.multiselect(
    "Pilih wilayah untuk dianalisis:",
    options=all_regions,
    default=['Asia Tenggara', 'Timur Tengah'],
    help="Pilih satu atau beberapa wilayah untuk fokus analisis"
)

# Date range filter
st.sidebar.markdown("### 📅 **Filter Waktu**")
st.sidebar.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
if 'last_updated' in df.columns:
    date_range = st.sidebar.date_input(
        "Rentang tanggal data:",
        value=[df['last_updated'].min().date(), df['last_updated'].max().date()],
        min_value=df['last_updated'].min().date(),
        max_value=df['last_updated'].max().date(),
        help="Pilih periode waktu untuk analisis data"
    )
    if len(date_range) == 2:
        df = df[(df['last_updated'].dt.date >= date_range[0]) & (df['last_updated'].dt.date <= date_range[1])]

# Filter data based on selection
if selected_regions:
    df_filtered = df[df['region'].isin(selected_regions)]
else:
    df_filtered = df

# Metrics Cards
st.markdown('<div class="metrics-row">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_extreme = df_filtered['is_extreme'].sum()
total_countries = df_filtered['country'].nunique()
extreme_percentage = (df_filtered['is_extreme'].mean() * 100)
avg_temp = df_filtered['temperature_celsius'].mean()

with col1:
    st.markdown(f'''
    <div class="metric-card metric-card-1">
        <div class="metric-icon">🌪️</div>
        <div class="metric-value">{total_extreme:,}</div>
        <div class="metric-label">Kejadian Ekstrem</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card metric-card-2">
        <div class="metric-icon">🌍</div>
        <div class="metric-value">{total_countries}</div>
        <div class="metric-label">Negara</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card metric-card-3">
        <div class="metric-icon">📊</div>
        <div class="metric-value">{extreme_percentage:.1f}%</div>
        <div class="metric-label">Tingkat Ekstrem</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="metric-card metric-card-4">
        <div class="metric-icon">🌡️</div>
        <div class="metric-value">{avg_temp:.1f}°C</div>
        <div class="metric-label">Suhu Rata-rata</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 🗺️ PETA PERSEBARAN CUACA EKSTREM (WAJIB)
st.markdown('''
<div class="chart-card">
    <div class="chart-title">🗺️ Peta Persebaran Cuaca Ekstrem - Wilayah Paling Rawan</div>
    <div class="info-card info-card-blue">
        <strong>🎯 Tujuan:</strong> Identifikasi wilayah paling rawan cuaca ekstrem 
    </div>
    <div class="chart-content">
''', unsafe_allow_html=True)

# Map controls
col1, col2 = st.columns(2)
with col1:
    map_metric = st.selectbox("Metrik:", ["Jumlah Ekstrem", "Suhu", "Kecepatan Angin", "Curah Hujan"])
with col2:
    map_type = st.selectbox("Tipe:", ["Scatter", "Choropleth"])

# Country-level extreme weather summary
country_summary = df.groupby(['country', 'latitude', 'longitude']).agg({
    'is_extreme': 'sum',
    'extreme_count': 'sum',
    'temperature_celsius': 'mean',
    'wind_kph': 'max',
    'precip_mm': 'max',
    'region': 'first'
}).reset_index()

# Map metric mapping
metric_mapping = {
    "Jumlah Ekstrem": 'extreme_count',
    "Suhu": 'temperature_celsius',
    "Kecepatan Angin": 'wind_kph',
    "Curah Hujan": 'precip_mm'
}

# Create interactive world map
if map_type == "Scatter":
    fig_map = px.scatter_geo(
        country_summary,
        lat='latitude',
        lon='longitude',
        size='is_extreme',
        color=metric_mapping[map_metric],
        hover_name='country',
        hover_data={
            'region': True,
            'temperature_celsius': ':.1f',
            'wind_kph': ':.1f',
            'precip_mm': ':.1f'
        },
        color_continuous_scale='Viridis',
        title=f"Distribusi {map_metric} Global",
        size_max=40
    )
else:
    fig_map = px.choropleth(
        country_summary,
        locations='country',
        locationmode='country names',
        color=metric_mapping[map_metric],
        hover_name='country',
        color_continuous_scale='Viridis',
        title=f"Distribusi {map_metric} Global"
    )

fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    ),
    height=400,
    title_x=0.5,
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)

# Regional comparison charts
col1, col2 = st.columns(2)

with col1:
    region_extreme = df.groupby('region')['is_extreme'].agg(['sum', 'count', 'mean']).reset_index()
    region_extreme['percentage'] = (region_extreme['mean'] * 100).round(1)
    
    # Interactive bar chart
    fig_region = px.bar(
        region_extreme.sort_values('sum', ascending=False).head(8),
        x='region',
        y='sum',
        color='percentage',
        title="Kejadian per Wilayah",
        color_continuous_scale='Plasma',
        text='sum'
    )
    fig_region.update_traces(textposition='outside')
    fig_region.update_layout(
        xaxis_tickangle=-45,
        height=300,
        title_x=0.5,
        margin=dict(l=0, r=0, t=40, b=60)
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    # Focus comparison
    focus_regions = df[df['region'].isin(['Asia Tenggara', 'Timur Tengah'])]
    if not focus_regions.empty:
        focus_data = focus_regions.groupby('region')['is_extreme'].sum().reset_index()
        
        fig_donut = px.pie(
            focus_data,
            values='is_extreme',
            names='region',
            title="Asia Tenggara vs Timur Tengah",
            hole=0.4,
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig_donut.update_traces(textinfo='label+percent')
        fig_donut.update_layout(height=300, title_x=0.5, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_donut, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# 📊 ANALISIS TAMBAHAN - JENIS EKSTREM & RISIKO
st.markdown('<div class="dashboard-grid-2">', unsafe_allow_html=True)

# 1. Grafik Batang Jenis Ekstrem
st.markdown('''
<div class="chart-card">
    <div class="chart-title">📊 Grafik Batang Jenis Ekstrem</div>
    <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #4CAF50;">
        <strong>🎯 Tujuan:</strong> Bukti bahwa jenis ekstrem di Asia Tenggara (Hujan) lebih relevan untuk SPD
    </div>
    <div class="chart-content">
''', unsafe_allow_html=True)

# Create more balanced extreme weather analysis
focus_regions_data = df_filtered[df_filtered['region'].isin(['Asia Tenggara', 'Timur Tengah'])]

if not focus_regions_data.empty:
    # Calculate average values per region for comparison
    region_weather_stats = focus_regions_data.groupby('region').agg({
        'temperature_celsius': ['mean', 'max', 'min'],
        'wind_kph': ['mean', 'max'],
        'precip_mm': ['mean', 'sum'],
        'humidity': 'mean'
    }).round(1)
    
    # Create comparative data for visualization
    comparison_data = []
    
    for region in ['Asia Tenggara', 'Timur Tengah']:
        region_data = focus_regions_data[focus_regions_data['region'] == region]
        
        # Count extreme events with moderate thresholds for better balance
        temp_extreme = len(region_data[(region_data['temperature_celsius'] <= 5) | (region_data['temperature_celsius'] >= 35)])
        wind_extreme = len(region_data[region_data['wind_kph'] >= 25])
        rain_extreme = len(region_data[region_data['precip_mm'] >= 5])
        humidity_extreme = len(region_data[(region_data['humidity'] <= 30) | (region_data['humidity'] >= 85)])
        
        # Add to comparison data
        comparison_data.extend([
            {'region': region, 'weather_type': 'Suhu Ekstrem', 'count': temp_extreme},
            {'region': region, 'weather_type': 'Angin Kencang', 'count': wind_extreme},
            {'region': region, 'weather_type': 'Hujan Intensif', 'count': rain_extreme},
            {'region': region, 'weather_type': 'Kelembaban Ekstrem', 'count': humidity_extreme}
        ])
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Create percentage for better comparison
    total_by_region = comparison_df.groupby('region')['count'].sum()
    comparison_df['percentage'] = comparison_df.apply(
        lambda row: (row['count'] / total_by_region[row['region']]) * 100 if total_by_region[row['region']] > 0 else 0, axis=1
    ).round(1)
    
    # Create side-by-side comparison chart
    fig_comparison = px.bar(
        comparison_df,
        x='weather_type',
        y='percentage',
        color='region',
        title="Perbandingan Pola Cuaca Ekstrem (%)",
        color_discrete_map={'Asia Tenggara': '#4ECDC4', 'Timur Tengah': '#FF6B6B'},
        text='percentage',
        barmode='group'
    )
    
    # Make text labels much more visible
    fig_comparison.update_traces(
        texttemplate='<b>%{text:.1f}%</b>',
        textposition='outside',
        textfont=dict(size=14, color='black', family="Arial Black")
    )
    
    fig_comparison.update_layout(
        height=400,
        xaxis_title="Jenis Cuaca Ekstrem",
        yaxis_title="Persentase dari Total Kejadian (%)",
        title_x=0.5,
        title_font_size=16,
        margin=dict(l=20, r=20, t=60, b=80),
        legend=dict(
            orientation="h",
            yanchor="bottom", 
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        yaxis=dict(
            range=[0, max(comparison_df['percentage']) * 1.3],
            title_font_size=12
        ),
        xaxis=dict(
            title_font_size=12,
            tickfont=dict(size=11)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Enhanced insights with clear SPD relevance
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown("### 🌏 **Asia Tenggara**")
        at_data = comparison_df[comparison_df['region'] == 'Asia Tenggara']
        if not at_data.empty:
            top_weather = at_data.loc[at_data['percentage'].idxmax()]
            st.markdown(f"🔸 **Pola Dominan:** {top_weather['weather_type']}")
            st.markdown(f"🔸 **Persentase:** {top_weather['percentage']:.1f}%")
            
            # SPD relevance
            rain_pct = at_data[at_data['weather_type'] == 'Hujan Intensif']['percentage'].iloc[0] if len(at_data[at_data['weather_type'] == 'Hujan Intensif']) > 0 else 0
            st.markdown(f"🌧️ **Hujan Intensif:** {rain_pct:.1f}% (Relevan untuk SPD)")
    
    with col_insight2:
        st.markdown("### 🏜️ **Timur Tengah**")
        tt_data = comparison_df[comparison_df['region'] == 'Timur Tengah']
        if not tt_data.empty:
            top_weather = tt_data.loc[tt_data['percentage'].idxmax()]
            st.markdown(f"🔸 **Pola Dominan:** {top_weather['weather_type']}")
            st.markdown(f"🔸 **Persentase:** {top_weather['percentage']:.1f}%")
            
            # Infrastructure note
            temp_pct = tt_data[tt_data['weather_type'] == 'Suhu Ekstrem']['percentage'].iloc[0] if len(tt_data[tt_data['weather_type'] == 'Suhu Ekstrem']) > 0 else 0
            st.markdown(f"🌡️ **Suhu Ekstrem:** {temp_pct:.1f}% (Infrastruktur Adaptif)")
    
    # Key finding for SPD
    st.markdown("""
    <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #4CAF50;">
        <strong>💡 Temuan Kunci SPD:</strong> Asia Tenggara menunjukkan pola hujan intensif yang lebih tinggi, 
        mendukung fokus Sistem Peringatan Dini pada bencana terkait presipitasi (banjir, longsor).
    </div>
    """, unsafe_allow_html=True)
    
else:
    st.info("Tidak ada data untuk wilayah yang dipilih")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close dashboard-grid-2

# 📈 TREN WAKTU (DISARANKAN)
st.markdown('''
<div class="chart-card">
    <div class="chart-title">📈 Tren Kejadian Cuaca Ekstrem Berdasarkan Bulan/Tahun</div>
    <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #FF9800;">
        <strong>🚨 Tujuan:</strong> Identifikasi periode paling rawan untuk Sistem Peringatan Dini
    </div>
    <div class="chart-content">
''', unsafe_allow_html=True)

# Time controls
col1, col2 = st.columns(2)
with col1:
    time_grouping = st.selectbox("Periode:", ["Bulanan", "Per Jam", "Harian"])
with col2:
    chart_type = st.selectbox("Grafik:", ["Garis", "Batang", "Area"])

if time_grouping == "Bulanan":
    time_data = df_filtered.groupby('month')['is_extreme'].sum().reset_index()
    time_data['month_name'] = time_data['month'].map({
        1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun',
        7:'Jul', 8:'Agt', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'
    })
    x_col, title = 'month_name', "Pola Bulanan"
elif time_grouping == "Per Jam":
    time_data = df_filtered.groupby('hour')['is_extreme'].sum().reset_index()
    x_col, title = 'hour', "Pola Per Jam"
else:
    time_data = df_filtered.groupby('date')['is_extreme'].sum().reset_index()
    x_col, title = 'date', "Pola Harian"

# Create dynamic chart based on selection
if chart_type == "Garis":
    fig_time = px.line(time_data, x=x_col, y='is_extreme', title=title, markers=True)
    fig_time.update_traces(line=dict(width=3))
elif chart_type == "Batang":
    fig_time = px.bar(time_data, x=x_col, y='is_extreme', title=title,
                     color='is_extreme', color_continuous_scale='Viridis')
else:
    fig_time = px.area(time_data, x=x_col, y='is_extreme', title=title)

fig_time.update_layout(
    height=300,
    title_x=0.5,
    xaxis_title="Periode Waktu",
    yaxis_title="Jumlah Kejadian Ekstrem",
    margin=dict(l=0, r=0, t=40, b=60)
)

st.plotly_chart(fig_time, use_container_width=True)

# Heatmap
if len(df_filtered) > 0:
    st.markdown("#### 🔥 Peta Panas Jam vs Bulan")
    heatmap_data = df_filtered.groupby(['month', 'hour'])['is_extreme'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='hour', columns='month', values='is_extreme').fillna(0)
    
    fig_heatmap = px.imshow(
        heatmap_pivot,
        title="Intensitas Jam vs Bulan",
        color_continuous_scale='Reds',
        aspect='auto'
    )
    fig_heatmap.update_layout(height=300, title_x=0.5, margin=dict(l=0, r=0, t=40, b=40))
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# 🔗 KORELASI EKSTREM VS BENCANA (WAJIB)
st.markdown('''
<div class="chart-card">
    <div class="chart-title">🔗 Perbandingan Kejadian Cuaca Ekstrem vs Bencana di Berbagai Wilayah</div>
    <div class="chart-content">
''', unsafe_allow_html=True)

# Create disaster risk score
def calculate_disaster_risk(row):
    risk_score = 0
    
    # Population density proxy (using latitude - closer to equator = higher pop density assumption)
    pop_factor = max(0, 1 - abs(row['latitude']) / 90)
    
    # Infrastructure vulnerability (based on region)
    infra_vulnerability = {
        'Asia Tenggara': 0.8,
        'Timur Tengah': 0.4,
        'Afrika': 0.9,
        'Amerika Selatan': 0.7,
        'Asia Timur & Selatan': 0.6,
        'Eropa': 0.3,
        'Amerika Utara': 0.3,
        'Lainnya': 0.5
    }
    
    # Climate adaptability
    climate_factor = infra_vulnerability.get(row['region'], 0.5)
    
    # Extreme weather intensity
    extreme_intensity = min(row['extreme_count'] / 3, 1)  # Normalize to 0-1
    
    # Combined risk score
    risk_score = (pop_factor * 0.3 + climate_factor * 0.4 + extreme_intensity * 0.3)
    
    return risk_score

df_risk = df_filtered.copy()
df_risk['disaster_risk'] = df_risk.apply(calculate_disaster_risk, axis=1)

# Country risk scatter plot
country_risk = df_risk.groupby(['country', 'region']).agg({
    'extreme_count': 'sum',
    'disaster_risk': 'mean',
    'is_extreme': 'sum',
    'temperature_celsius': 'mean'
}).reset_index()

fig_scatter = px.scatter(
    country_risk,
    x='extreme_count',
    y='disaster_risk',
    size='is_extreme',
    color='region',
    hover_name='country',
    title="Korelasi Ekstrem vs Risiko",
    size_max=25,
    opacity=0.7,
    color_discrete_map={'Asia Tenggara': '#4ECDC4', 'Timur Tengah': '#FF6B6B'}
)

fig_scatter.update_layout(
    xaxis_title="Frekuensi Cuaca Ekstrem",
    yaxis_title="Skor Risiko Bencana (0-1)",
    height=400,
    title_x=0.5,
    margin=dict(l=0, r=0, t=40, b=60)
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Regional comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); color: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; text-align: center;">
        <h4 style="margin: 0 0 0.5rem 0;">🌪️ Timur Tengah</h4>
        <p style="margin: 0; font-size: 0.9rem;">✅ Cuaca Ekstrem: <strong>TINGGI</strong></p>
        <p style="margin: 0; font-size: 0.9rem;">✅ Risiko Bencana: <strong>RENDAH</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.9;"><em>Infrastruktur baik, adaptasi tinggi</em></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%); color: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; text-align: center;">
        <h4 style="margin: 0 0 0.5rem 0;">🌏 Asia Tenggara</h4>
        <p style="margin: 0; font-size: 0.9rem;">⚠️ Cuaca Ekstrem: <strong>SEDANG</strong></p>
        <p style="margin: 0; font-size: 0.9rem;">⚠️ Risiko Bencana: <strong>TINGGI</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.9;"><em>Kepadatan tinggi, infrastruktur terbatas</em></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Show raw data if requested
if show_raw_data:
    st.markdown('''
    <div class="chart-card">
        <div class="chart-title">📋 Data Mentah</div>
        <div class="chart-content">
    ''', unsafe_allow_html=True)
    
    # Add search functionality
    search_country = st.text_input("🔍 Cari negara:")
    if search_country:
        filtered_display = df_filtered[df_filtered['country'].str.contains(search_country, case=False, na=False)]
    else:
        filtered_display = df_filtered
    
    # Tampilkan info jumlah data
    st.info(f"📊 Menampilkan {min(len(filtered_display), 500)} dari {len(filtered_display)} total data")
    
    st.dataframe(
        filtered_display.head(500),  # Limit for performance
        use_container_width=True,
        height=300
    )
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Footer
st.markdown("<div style='margin: 1rem 0;'><hr style='margin: 0.5rem 0; border: 1px solid #e2e8f0;'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; margin: 1rem 0; font-size: 0.9rem;'>Dashboard Cuaca Ekstrem | PowerOfQueen 2025</div>", unsafe_allow_html=True)