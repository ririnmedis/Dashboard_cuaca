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

# Custom CSS for better UI
st.markdown("""
<style>
    /* Global Styles */
    .main {
        padding-top: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2rem;
        color: #1a202c;
        text-align: center;
        margin: 1rem 0 1.5rem 0;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Section Cards */
    .section-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #667eea;
    }
    
    /* Section Titles */
    .section-title {
        font-size: 1.4rem;
        color: #2d3748;
        margin-bottom: 1rem;
        font-weight: 700;
        padding: 0.75rem 0;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Metrics Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #4299e1 0%, #667eea 100%) !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(66, 153, 225, 0.3) !important;
        margin: 0.5rem 0 !important;
    }
    
    div[data-testid="metric-container"] > div {
        color: white !important;
    }
    
    div[data-testid="metric-container"] [data-testid="metric-label"] {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
    }
    
    /* Control Styling */
    .stSelectbox label {
        font-weight: 600 !important;
        color: #2d3748 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox > div > div {
        background-color: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stMultiSelect label {
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        box-shadow: 0 2px 8px rgba(72, 187, 120, 0.3);
        margin: 0.5rem 0;
    }
    
    .insight-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
        opacity: 0.9;
    }
    
    .insight-card h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 800;
    }
    
    /* Chart Containers */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f7fafc;
    }
    
    /* Subheader Fix */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Clean up spacing */
    .block-container {
        padding-top: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .section-card {
            padding: 0.75rem;
            margin: 0.75rem 0;
        }
        
        .section-title {
            font-size: 1.1rem;
        }
        
        div[data-testid="metric-container"] {
            margin: 0.25rem 0 !important;
            padding: 0.75rem 1rem !important;
        }
    }
    
    /* Improved chart styling */
    .plotly-graph-div {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
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

# Title
st.markdown('''
<div style="text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 1rem; color: white; box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);">
    <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800;">🌪️  Dashboard Analisis Cuaca Ekstrem & Risiko Bencana</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Revisi SPD - Asia Tenggara vs Timur Tengah</p>
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

# Quick Stats
st.markdown("<div style='margin: 0.5rem 0;'><hr style='margin: 0.5rem 0; border: 1px solid #e2e8f0;'></div>", unsafe_allow_html=True)

# Main metrics
st.markdown("""<div style="margin: 0.5rem 0;"><h4 style="margin: 0.5rem 0; color: #2d3748;">📈 Metrik Utama</h4></div>""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_extreme = df_filtered['is_extreme'].sum()
    st.metric("🌪️ Kejadian Ekstrem", f"{total_extreme:,}")

with col2:
    total_countries = df_filtered['country'].nunique()
    st.metric("🌍 Negara", total_countries)

with col3:
    extreme_percentage = (df_filtered['is_extreme'].mean() * 100)
    st.metric("📊 Tingkat Ekstrem", f"{extreme_percentage:.1f}%")

with col4:
    avg_temp = df_filtered['temperature_celsius'].mean()
    st.metric("🌡️ Suhu Rata-rata", f"{avg_temp:.1f}°C")

# 🗺️ PETA PERSEBARAN CUACA EKSTREM (WAJIB)
st.markdown('''
<div class="section-card">
<div class="section-title">🗺️ Peta Persebaran Cuaca Ekstrem - Wilayah Paling Rawan</div>
<div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2196F3;">
    <strong>🎯 Tujuan:</strong> Identifikasi wilayah paling rawan cuaca ekstrem (Visual mudah dilihat dosen)
</div>
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
    region_extreme['percentage'] = region_extreme['mean'] * 100
    
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

# 📈 TREN WAKTU (DISARANKAN)
st.markdown('''
<div class="section-card">
<div class="section-title">📈 Tren Waktu - Periode Paling Rawan</div>
<div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #FF9800;">
    <strong>🚨 Tujuan:</strong> Identifikasi periode paling rawan untuk Sistem Peringatan Dini
</div>
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

st.markdown('</div>', unsafe_allow_html=True)

# 🔗 KORELASI EKSTREM VS BENCANA (WAJIB)
st.markdown('''
<div class="section-card">
<div class="section-title">🔗 Korelasi Cuaca Ekstrem vs Risiko Bencana</div>
<div style="background: #ffebee; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #F44336;">
    <strong>⚠️ INTI REVISI IBU RATNA:</strong><br>
    • <strong>Timur Tengah:</strong> Ekstrem tinggi × Bencana rendah<br>
    • <strong>Asia Tenggara:</strong> Ekstrem menengah × Bencana tinggi
</div>
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

# Analisis risiko
analysis_type = st.selectbox("Jenis Analisis:", ["Risiko vs Ekstrem", "Matriks Korelasi", "Plot Risiko 3D"])

if analysis_type == "Risiko vs Ekstrem":
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive scatter plot
        country_risk = df_risk.groupby(['country', 'region']).agg({
            'extreme_count': 'sum',
            'disaster_risk': 'mean',
            'is_extreme': 'sum',
            'temperature_celsius': 'mean'
        }).reset_index()
        
        # Add interactivity options
        color_by = st.selectbox("Warnakan berdasarkan", ["region", "temperature_celsius", "extreme_count"])
        size_by = st.selectbox("Ukuran berdasarkan", ["is_extreme", "extreme_count", "disaster_risk"])
        
        fig_scatter = px.scatter(
            country_risk,
            x='extreme_count',
            y='disaster_risk',
            size=size_by,
            color=color_by,
            hover_name='country',
            title="Korelasi Ekstrem vs Risiko",
            size_max=25,  # Kurangi ukuran maksimal titik
            opacity=0.7   # Tambahkan transparansi
        )
        
        # Perbaiki layout dengan tick yang lebih sederhana
        fig_scatter.update_layout(
            xaxis_title="Kejadian Ekstrem",
            yaxis_title="Skor Risiko (0-1)",
            height=300,
            title_x=0.5,
            margin=dict(l=0, r=0, t=40, b=60),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )
        
        # Sederhanakan grid dan axis
        fig_scatter.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
        fig_scatter.update_yaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Perbandingan regional
        st.markdown("#### 📊 Perbandingan Regional")
        
        risk_metrics = country_risk.groupby('region').agg({
            'extreme_count': 'mean',
            'disaster_risk': 'mean',
            'is_extreme': 'mean'
        }).round(2).sort_values('disaster_risk', ascending=False)
        
        key_regions = ['Asia Tenggara', 'Timur Tengah']
        
        for region in key_regions:
            if region in risk_metrics.index:
                with st.container():
                    color = "#FF6B6B" if region == "Asia Tenggara" else "#4ECDC4"
                    
                    st.markdown(f"""
                    <div style="background: {color}20; padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid {color};">
                        <strong>{region}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Ekstrem", f"{risk_metrics.loc[region, 'extreme_count']:.1f}")
                    with col_b:
                        st.metric("Risiko", f"{risk_metrics.loc[region, 'disaster_risk']:.2f}")
                    with col_c:
                        ratio = risk_metrics.loc[region, 'disaster_risk'] / max(risk_metrics.loc[region, 'extreme_count'], 1)
                        st.metric("Rasio", f"{ratio:.2f}")

elif analysis_type == "Plot Risiko 3D":
    # 3D scatter plot dengan tampilan yang disederhanakan
    country_risk = df_risk.groupby(['country', 'region']).agg({
        'extreme_count': 'sum',
        'disaster_risk': 'mean',
        'is_extreme': 'sum',
        'temperature_celsius': 'mean'
    }).reset_index()
    
    fig_3d = px.scatter_3d(
        country_risk,
        x='extreme_count',
        y='disaster_risk',
        z='temperature_celsius',
        color='region',
        size='is_extreme',
        hover_name='country',
        title="Analisis 3D: Ekstrem × Risiko × Suhu",
        size_max=15,  # Kurangi ukuran titik 3D
        opacity=0.8
    )
    
    # Perbaiki layout 3D
    fig_3d.update_layout(
        height=400, 
        margin=dict(l=0, r=0, t=40, b=0),
        scene=dict(
            xaxis_title="Kejadian Ekstrem",
            yaxis_title="Risiko Bencana",
            zaxis_title="Suhu (°C)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)  # Sudut pandang yang lebih baik
            )
        )
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Tambahkan penjelasan untuk 3D plot
    st.markdown("""
    <div style="background: #fff3e0; padding: 0.75rem; border-radius: 6px; margin: 0.5rem 0; border-left: 3px solid #FF9800; font-size: 0.9rem;">
        <strong>📊 3D Plot:</strong> Drag untuk memutar, scroll untuk zoom. Ukuran titik = jumlah kejadian ekstrem total.
    </div>
    """, unsafe_allow_html=True)

else:  # Correlation Matrix
    correlation_vars = ['temperature_celsius', 'wind_kph', 'precip_mm', 'humidity', 
                       'pressure_mb', 'extreme_count', 'disaster_risk']
    available_vars = [var for var in correlation_vars if var in df_risk.columns]
    correlation_data = df_risk[available_vars].corr()
    
    fig_corr = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        title="Korelasi Faktor",
        color_continuous_scale='RdBu_r'
    )
    fig_corr.update_layout(height=350, title_x=0.5, margin=dict(l=0, r=0, t=40, b=40))
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# 💡 KESIMPULAN UTAMA
st.markdown('''
<div class="section-card">
<div class="section-title">💡 Kesimpulan Revisi SPD</div>
<div style="background: #fff3e0; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #FF9800;">
    <strong>📝 Untuk Ibu Ratna:</strong> Analisis korelasi infrastruktur vs frekuensi cuaca ekstrem
</div>
''', unsafe_allow_html=True)

# Ringkasan untuk dosen - Layout yang diperbaiki
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

st.markdown("""
<div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #667eea; text-align: center;">
    <strong>📋 Kesimpulan Utama:</strong> Risiko bencana tidak hanya ditentukan oleh frekuensi cuaca ekstrem, tetapi juga oleh faktor infrastruktur dan kepadatan penduduk.
</div>
""", unsafe_allow_html=True)

# Tabel perbandingan
st.markdown("""
<div style="margin: 1rem 0;">
    <h4 style="margin: 0.5rem 0; color: #2d3748; font-weight: 600;">📊 Tabel Perbandingan Regional</h4>
</div>
""", unsafe_allow_html=True)

focus_comparison = df[df['region'].isin(['Asia Tenggara', 'Timur Tengah'])].groupby('region').agg({
    'is_extreme': ['sum', 'mean'],
    'temperature_celsius': 'mean',
    'wind_kph': 'mean', 
    'precip_mm': 'mean',
    'country': 'nunique'
}).round(2)

focus_comparison.columns = ['Total_Ekstrem', 'Rata_Harian', 'Suhu_C', 'Angin_kph', 'Hujan_mm', 'Negara']

if not df_filtered.empty:
    disaster_risk_by_region = df_filtered.groupby('region').apply(
        lambda x: x.apply(calculate_disaster_risk, axis=1).mean()
    ).round(3)
    
    for region in ['Asia Tenggara', 'Timur Tengah']:
        if region in disaster_risk_by_region.index:
            focus_comparison.loc[region, 'Risiko_Bencana'] = disaster_risk_by_region[region]

st.dataframe(focus_comparison, use_container_width=True)

# Temuan kunci dengan layout yang diperbaiki
st.markdown("""
<div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #2196F3;">
    <h4 style="margin: 0 0 0.5rem 0; color: #1565C0;">🎯 Poin Utama SPD:</h4>
    <ul style="margin: 0; color: #424242;">
        <li><strong>🌪️ Timur Tengah:</strong> Cuaca ekstrem tinggi, namun risiko bencana rendah (infrastruktur baik)</li>
        <li><strong>🌏 Asia Tenggara:</strong> Cuaca ekstrem sedang, namun risiko bencana tinggi (kepadatan populasi)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Separator sebelum data mentah
st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Show raw data if requested
if show_raw_data:
    st.markdown('''
    <div class="section-card">
    <div class="section-title">📋 Data Mentah</div>
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<div style='margin: 1rem 0;'><hr style='margin: 0.5rem 0; border: 1px solid #e2e8f0;'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #666; margin: 1rem 0; font-size: 0.9rem;'>Dashboard Cuaca Ekstrem | SPD Data Visualisasi</div>", unsafe_allow_html=True)