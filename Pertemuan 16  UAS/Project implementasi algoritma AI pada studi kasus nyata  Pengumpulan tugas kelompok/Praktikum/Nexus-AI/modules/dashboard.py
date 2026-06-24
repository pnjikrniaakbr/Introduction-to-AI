import streamlit as st
import pandas as pd
import plotly.express as px
import os
from modules.theme import ICON, COLOR, section_header

# Palet warna konsisten untuk grafik
PALETTE = [COLOR.get("primary", "#3b82f6"), COLOR.get("danger", "#ef4444")]

@st.cache_data
def load_data():
    try:
        return pd.read_csv("Survei_Perilaku_Konsumen.csv")
    except Exception:
        return None

def kpi_card(st, icon_key, label, value, color, bg_color="#ffffff"):
    """Fungsi pembantu untuk membuat kartu KPI dengan efek hover yang mewah."""
    icon_url = ICON.get(icon_key, "https://cdn-icons-png.flaticon.com/512/1074/1074146.png")
    st.markdown(f"""
        <div class="metric-card anim-slide-up" style="background: {bg_color}; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; border-left: 5px solid {color}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: all 0.3s ease; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                <img src="{icon_url}" width="32" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
                <p style="margin: 0; color: #64748b; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">{label}</p>
            </div>
            <p style="margin: 0; color: #0f172a; font-size: 2.2rem; font-weight: 900; line-height: 1.1;">
                {value}
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    # 1. HERO BANNER (Desain Banner Startup Mewah)
    st.markdown(f"""
        <div class="anim-slide-up" style="background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%); padding: 30px; border-radius: 20px; border: 1px solid #bfdbfe; margin-bottom: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="{ICON.get('nav_dashboard', 'https://cdn-icons-png.flaticon.com/512/1074/1074146.png')}" width="70" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
                <div>
                    <h1 style="margin: 0; color: #0f172a; font-size: 2.4rem; font-weight: 900; letter-spacing: -0.5px;">Executive Dashboard</h1>
                    <p style="margin: 0; color: #475569; font-size: 1.05rem; margin-top: 5px;">Laporan analitik perilaku konsumen berbasis model Logistic Regression — Studi Kasus Preferensi Belanja Online vs Offline.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Load Data
    df_raw = load_data()
    if df_raw is None:
        st.error("⚠️ Dataset 'Survei_Perilaku_Konsumen.csv' tidak ditemukan! Pastikan file berada di folder utama.")
        return

    # Pemetaan/Rename Kolom
    col_map = {
        'Jenis Kelamin  ': 'Gender',
        'Usia  ': 'Usia',
        'Pekerjaan Utama  ': 'Pekerjaan',
        'Rata-rata Pengeluaran Belanja per Bulan  ': 'Pengeluaran',
        'Secara keseluruhan, dalam kondisi normal, platform mana yang lebih Anda prioritaskan untuk belanja saat ini?  ': 'Target',
    }
    df = df_raw.rename(columns=col_map)

    # 2. METRIK UTAMA
    total = len(df)
    online = df[df['Target'].str.contains('Online', case=False, na=False)]
    pct_online = (len(online) / total) * 100 if total > 0 else 0
    pct_offline = 100 - pct_online

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card(st, "people", "TOTAL RESPONDEN", f"{total}", COLOR.get("ink", "#0f172a"))
    with c2:
        kpi_card(st, "online", "ONLINE SHOPPER", f"{pct_online:.1f}%", COLOR.get("primary", "#3b82f6"))
    with c3:
        kpi_card(st, "offline", "OFFLINE SHOPPER", f"{pct_offline:.1f}%", COLOR.get("danger", "#ef4444"))
    with c4:
        kpi_card(st, "accuracy", "AKURASI MODEL AI", "81.0%", COLOR.get("success", "#10b981"), bg_color="#f0fdf4")

    st.write("")
    st.divider()

    # 3. FILTER INTERAKTIF (Header Flexbox Sejajar Sempurna)
    st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px; margin-top: 10px;">
            <img src="{ICON.get('network', 'https://cdn-icons-png.flaticon.com/512/3126/3126405.png')}" width="42" style="margin-top: 2px;">
            <div>
                <h3 style="margin: 0; padding: 0; color: #0f172a; font-weight: 800; line-height: 1.2;">Filter Data Interaktif</h3>
                <p style="margin: 0; padding: 0; color: #64748b; font-size: 0.95rem; margin-top: 6px;">Jelajahi data berdasarkan segmen demografi & ekonomi responden.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            f_gender = st.selectbox("Gender", ["Semua"] + sorted(df['Gender'].dropna().unique().tolist()))
        with f2:
            f_usia = st.selectbox("Kelompok Usia", ["Semua"] + sorted(df['Usia'].dropna().unique().tolist()))
        with f3:
            f_pengeluaran = st.selectbox("Pengeluaran/Bulan", ["Semua"] + sorted(df['Pengeluaran'].dropna().unique().tolist()))

    # Logika Filter Pandas
    df_f = df.copy()
    if f_gender != "Semua":
        df_f = df_f[df_f['Gender'] == f_gender]
    if f_usia != "Semua":
        df_f = df_f[df_f['Usia'] == f_usia]
    if f_pengeluaran != "Semua":
        df_f = df_f[df_f['Pengeluaran'] == f_pengeluaran]

    # Visualisasi Plotly
    if df_f.empty:
        st.warning("⚠️ Data kosong untuk kombinasi filter ini. Coba ubah pilihan filter di atas.")
    else:
        st.caption(f"✅ Menampilkan **{len(df_f)}** dari **{total}** responden sesuai kriteria filter terpilih.")
        c_g1, c_g2 = st.columns([1, 1.2]) 
        
        with c_g1:
            with st.container(border=True):
                fig_pie = px.pie(
                    df_f, names='Target', title="Proporsi Platform Belanja", hole=0.55,
                    color='Target', color_discrete_map={'Online Shopper': PALETTE[0], 'Offline Shopper': PALETTE[1]}
                )
                fig_pie.update_traces(textinfo='percent+label', textfont_size=13, marker=dict(line=dict(color='#ffffff', width=2)))
                fig_pie.update_layout(
                    legend=dict(orientation="h", y=-0.2), 
                    margin=dict(t=50, b=20, l=10, r=10), 
                    height=360,
                    paper_bgcolor="rgba(0,0,0,0)", # Latar transparan
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
        with c_g2:
            with st.container(border=True):
                fig_hist = px.histogram(
                    df_f, x='Pengeluaran', color='Target', barmode='group',
                    title="Anggaran Belanja vs Platform Pilihan",
                    color_discrete_map={'Online Shopper': PALETTE[0], 'Offline Shopper': PALETTE[1]}
                )
                fig_hist.update_layout(
                    legend=dict(orientation="h", y=-0.25), 
                    margin=dict(t=50, b=20, l=10, r=10), 
                    xaxis_title="Pengeluaran per Bulan", 
                    yaxis_title="Jumlah Responden",
                    height=360,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_hist, use_container_width=True)

        st.download_button(
            label="Unduh Data Terfilter (.csv)",
            data=df_f.to_csv(index=False).encode("utf-8"),
            file_name="data_terfilter_nexus_ai.csv",
            mime="text/csv",
            use_container_width=True,
            type="secondary"
        )

    # 4. BAGIAN INSIGHT MODEL
    st.divider()
    
    # Header Flexbox Insight Sejajar Sempurna
    st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 15px; margin-bottom: 25px;">
            <img src="{ICON.get('accuracy', 'https://cdn-icons-png.flaticon.com/512/3556/3556352.png')}" width="42" style="margin-top: 2px;">
            <div>
                <h3 style="margin: 0; padding: 0; color: #0f172a; font-weight: 800; line-height: 1.2;">Ekstraksi Pengetahuan (Model Insights)</h3>
                <p style="margin: 0; padding: 0; color: #64748b; font-size: 0.95rem; margin-top: 6px;">Perbandingan performa algoritma & temuan kritis dari notebook eksperimen kelompok.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Deretan Matriks Evaluasi Model
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        ("CV Accuracy", "86.5%", COLOR.get("primary", "#3b82f6")),
        ("Test Accuracy", "81.0%", COLOR.get("ink", "#0f172a")),
        ("Precision", "93.8%", COLOR.get("accent", "#8b5cf6")),
        ("Recall", "83.3%", COLOR.get("success", "#10b981")),
        ("F1-Score", "88.2%", COLOR.get("danger", "#ef4444")),
    ]
    
    for col, (label, value, color) in zip([m1, m2, m3, m4, m5], metrics):
        with col:
            # Menggunakan background abu-abu sangat muda untuk card kecil ini
            kpi_card(st, "network", label.upper(), value, color, bg_color="#f8fafc")
            
    st.caption("*Logistic Regression terpilih sebagai model produksi karena mengungguli Naive Bayes (42.9%) & K-Nearest Neighbors (71.4%) pada Test Accuracy.*")

    st.write("")
    
    # Galeri Gambar Ekstraksi Pengetahuan Jupyter (Telah dihapus div kosongnya)
    t1, t2, t3, t4 = st.tabs([
        "Matriks Korelasi", "Paradoks Risiko Siber",
        "Ketidakseimbangan Kelas", "Pengeluaran vs Preferensi",
    ])
    
    asset_map = {
        t1: "Correlation Heatmap (Matriks Korelasi Fitur Psikologis).png",
        t2: "Analisis Kritis Paradoks Risiko Penipuan vs Daya Tarik Harga Murah.png",
        t3: "Distribusi Kelas Target (Ketidakseimbangan Data).png",
        t4: "Distribusi Preferensi Berdasarkan Kapasitas Pengeluaran.png",
    }
    
    for tab, filename in asset_map.items():
        with tab:
            path = os.path.join("assets", filename)
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.info(f"💡 Gambar `{filename}` belum tersedia di folder `assets/`.")