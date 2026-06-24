import streamlit as st
import pandas as pd
import joblib
import time
import plotly.graph_objects as go
from datetime import datetime
from modules.theme import ICON, COLOR

# --- KONSTANTA PARAMETER ---
GENDER_OPTS = ["Perempuan", "Laki-laki"]
USIA_OPTS = ["<18 Tahun", "18-25 Tahun", "26-35 Tahun", "36-45 Tahun", ">45 Tahun"]
PEKERJAAN_OPTS = ["Pelajar/Mahasiswa", "Wiraswasta", "Pegawai Swasta/PNS", "Ibu Rumah Tangga", "Barista", "Lainnya"]
PENGELUARAN_OPTS = ["< Rp1 Juta", "Rp1 Juta - Rp3 Juta", "Rp3 Juta - Rp5 Juta", "> Rp5 Juta"]
KATEGORI_ONLINE_OPTS = ["Elektronik", "Fashion", "Kebutuhan Pokok/Makanan", "Skincare/Kosmetik"]
ALASAN_ONLINE_ATOMS = ["Diskon/Promo", "Kemudahan Akses", "Variasi Produk", "Malas Keluar Rumah"]
ALASAN_OFFLINE_OPTS = ["Bisa mencoba/melihat fisik barang", "Keamanan transaksi", "Langsung mendapatkan barang", "Rekreasi"]
WAKTU_TUNGGU_OPTS = ["<24 Jam", "2-3 Hari", "4-7 Hari", ">1 Minggu"]

GROUP_LABELS = {
    "Gender_": "Gender",
    "Usia_": "Usia",
    "Pekerjaan_": "Pekerjaan",
    "Pengeluaran_": "Pengeluaran",
    "Kategori_Online_": "Kategori Online",
    "Alasan_Online_": "Alasan Pilih Online",
    "Alasan_Offline_": "Alasan Pilih Offline",
    "Waktu_Tunggu_": "Toleransi Waktu Tunggu",
}
NUMERIC_LABELS = {
    "Freq_Online": "Frekuensi Belanja Online",
    "Pengaruh_Review": "Pengaruh Ulasan/Review",
    "Khawatir_Penipuan": "Ketakutan Penipuan Online",
    "Harga_Murah": "Persepsi Harga Online Lebih Murah",
    "Penting_SPG": "Kebutuhan Interaksi/SPG",
}

def prettify(feature_name: str) -> str:
    if feature_name in NUMERIC_LABELS:
        return NUMERIC_LABELS[feature_name]
    for prefix, label in GROUP_LABELS.items():
        if feature_name.startswith(prefix):
            return f"{label}: {feature_name[len(prefix):]}"
    return feature_name

@st.cache_resource
def load_model():
    model = joblib.load("models/model_lr.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler

def build_feature_row(feats, inputs):
    row = {f: 0 for f in feats}
    row["Freq_Online"] = inputs["freq_online"]
    row["Pengaruh_Review"] = inputs["pengaruh_review"]
    row["Khawatir_Penipuan"] = inputs["khawatir_penipuan"]
    row["Harga_Murah"] = inputs["harga_murah"]
    row["Penting_SPG"] = inputs["penting_spg"]

    if inputs["gender"] == "Perempuan":
        row["Gender_Perempuan"] = 1

    for prefix, value in [
        ("Usia_", inputs["usia"]),
        ("Pekerjaan_", inputs["pekerjaan"]),
        ("Pengeluaran_", inputs["pengeluaran"]),
        ("Kategori_Online_", inputs["kategori_online"]),
        ("Alasan_Online_", inputs["alasan_online"]),
        ("Alasan_Offline_", inputs["alasan_offline"]),
        ("Waktu_Tunggu_", inputs["waktu_tunggu"]),
    ]:
        col = f"{prefix}{value}"
        if col in row:
            row[col] = 1

    return pd.DataFrame([row], columns=feats)

def show_predictor():
    st.markdown('<div class="anim-slide-up">', unsafe_allow_html=True)

    # 1. HERO BANNER (Desain Banner AI Mewah)
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #f5f3ff 100%); padding: 30px; border-radius: 20px; border: 1px solid #ddd6fe; margin-bottom: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; gap: 20px;">
                <img src="{ICON.get('nav_predictor', 'https://cdn-icons-png.flaticon.com/512/4712/4712139.png')}" width="70" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
                <div>
                    <h1 style="margin: 0; color: #0f172a; font-size: 2.4rem; font-weight: 900; letter-spacing: -0.5px;">Predictive Intelligence</h1>
                    <p style="margin: 0; color: #475569; font-size: 1.05rem; margin-top: 5px;">Simulator Inferensi menggunakan model Logistic Regression terlatih (Log-Odds Calculus) dari hasil riset Data Science.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    try:
        model, scaler = load_model()
        feats = list(model.feature_names_in_)
    except Exception as e:
        st.error(f"Gagal memuat model Machine Learning: {e}")
        return

    # Layout Asimetris (Kiri untuk Input, Kanan untuk Output AI)
    col_input, col_output = st.columns([1, 1.6], gap="large")

    with col_input:
        # Header Flexbox
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 20px;">
                <img src="{ICON.get('people', 'https://cdn-icons-png.flaticon.com/512/1632/1632899.png')}" width="38" style="margin-top: 2px;">
                <div>
                    <h3 style="margin: 0; padding: 0; color: #0f172a; font-weight: 800; line-height: 1.2;">Parameter Input</h3>
                    <p style="margin: 0; padding: 0; color: #64748b; font-size: 0.9rem; margin-top: 4px;">Atur segmentasi responden.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<p style='color:#3b82f6; font-weight:800; letter-spacing: 0.5px; font-size:0.85rem;'>1. PROFIL DEMOGRAFI</p>", unsafe_allow_html=True)
            gender = st.selectbox("Identitas Gender", GENDER_OPTS)
            usia = st.selectbox("Kelompok Usia", USIA_OPTS, index=1)
            pekerjaan = st.selectbox("Pekerjaan Utama", PEKERJAAN_OPTS)
            pengeluaran = st.selectbox("Rata-rata Pengeluaran/Bulan", PENGELUARAN_OPTS, index=1)

            st.divider()
            st.markdown("<p style='color:#3b82f6; font-weight:800; letter-spacing: 0.5px; font-size:0.85rem;'>2. KEBIASAAN BELANJA</p>", unsafe_allow_html=True)
            kategori_online = st.selectbox("Kategori Produk Favorit", KATEGORI_ONLINE_OPTS)
            alasan_online_pilihan = st.multiselect(
                "Faktor Pendorong Belanja Online", ALASAN_ONLINE_ATOMS,
                default=["Diskon/Promo", "Kemudahan Akses"],
            )
            waktu_tunggu = st.selectbox("Toleransi Waktu Tunggu Pengiriman", WAKTU_TUNGGU_OPTS, index=1)
            alasan_offline = st.selectbox("Alasan Tetap Belanja Offline", ALASAN_OFFLINE_OPTS)

            st.divider()
            st.markdown("<p style='color:#3b82f6; font-weight:800; letter-spacing: 0.5px; font-size:0.85rem;'>3. ATRIBUT PSIKOLOGIS (1-5)</p>", unsafe_allow_html=True)
            freq_online = st.slider("Frekuensi Belanja Online", 1, 5, 4)
            review = st.slider("Ketergantungan Ulasan", 1, 5, 4)
            harga = st.slider("Sensitivitas Harga Diskon", 1, 5, 4)
            khawatir = st.slider("Ketakutan Penipuan Siber", 1, 5, 3)
            spg = st.slider("Kebutuhan Pelayanan Fisik/SPG", 1, 5, 2)

            st.write("")
            btn_predict = st.button("JALANKAN INFERENSI AI", use_container_width=True, type="primary")

    # Parsing fitur array
    ordered_atoms = [a for a in ALASAN_ONLINE_ATOMS if a in alasan_online_pilihan]
    alasan_online_combo = ", ".join(ordered_atoms) if ordered_atoms else "Diskon/Promo"
    alasan_online_col = f"Alasan_Online_{alasan_online_combo}"
    combo_dikenal = (alasan_online_col in feats) or (alasan_online_combo == "Diskon/Promo")

    with col_output:
        # Header Flexbox
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 20px;">
                <img src="https://cdn-icons-png.flaticon.com/512/2830/2830305.png" width="38" style="margin-top: 2px;">
                <div>
                    <h3 style="margin: 0; padding: 0; color: #0f172a; font-weight: 800; line-height: 1.2;">Ekstraksi Algoritma</h3>
                    <p style="margin: 0; padding: 0; color: #64748b; font-size: 0.9rem; margin-top: 4px;">Kalkulasi probabilitas Log-Odds secara Real-Time.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if not combo_dikenal:
            st.caption("*Kombinasi faktor pendorong ini tidak tercatat di data latih — sistem memperlakukannya setara kategori dasar Diskon/Promo.*")

        if not btn_predict:
            st.info("**Sistem dalam posisi siaga.** Silakan atur parameter kuesioner di panel sebelah kiri lalu tekan tombol eksekusi untuk melihat hasil probabilitas algoritma.")

        if btn_predict:
            inputs = {
                "gender": gender, "usia": usia, "pekerjaan": pekerjaan, "pengeluaran": pengeluaran,
                "kategori_online": kategori_online, "alasan_online": alasan_online_combo,
                "alasan_offline": alasan_offline, "waktu_tunggu": waktu_tunggu,
                "freq_online": freq_online, "pengaruh_review": review,
                "khawatir_penipuan": khawatir, "harga_murah": harga, "penting_spg": spg,
            }

            with st.status("Mengkalkulasi Arsitektur Logistic Regression...", expanded=True) as status:
                st.write("Menyusun 39 matriks fitur (One-Hot Encoding + Standard Scaling)...")
                time.sleep(0.4)
                st.write("Mengekstrak matriks bobot pendorong (*Driving Forces*) & penahan (*Restraining Forces*)...")
                time.sleep(0.4)
                st.write("Memetakan peluang akhir melewati fungsi aktivasi Sigmoid...")
                time.sleep(0.4)
                status.update(label="Kalkulasi AI Selesai!", state="complete", expanded=False)

            # --- PROSES MACHINE LEARNING ---
            row_df = build_feature_row(feats, inputs)
            X_scaled = pd.DataFrame(scaler.transform(row_df), columns=feats)
            prob_final = float(model.predict_proba(X_scaled)[0][1])
            label_final = "Online Shopper" if prob_final >= 0.5 else "Offline Shopper"

            contributions = (model.coef_[0] * X_scaled.iloc[0].values)
            contrib_series = pd.Series(contributions, index=feats).sort_values()
            top_restraining = contrib_series.head(4)
            top_driving = contrib_series.tail(4)
            tornado = pd.concat([top_restraining, top_driving]).sort_values()

            # --- SIMPAN RIWAYAT ---
            if "riwayat_prediksi" not in st.session_state:
                st.session_state.riwayat_prediksi = []
            st.session_state.riwayat_prediksi.insert(0, {
                "Waktu": datetime.now().strftime("%H:%M:%S"),
                "Gender": gender, "Usia": usia,
                "Probabilitas Online": f"{prob_final*100:.1f}%",
                "Vonis AI": label_final,
            })
            st.session_state.riwayat_prediksi = st.session_state.riwayat_prediksi[:8]

            if prob_final >= 0.50:
                st.balloons()

            # --- GRAFIK DASHBOARD OUTPUT ---
            c_rad, c_gau = st.columns(2)
            with c_rad:
                with st.container(border=True):
                    df_radar = pd.DataFrame(dict(
                        r=[freq_online, review, harga, khawatir, spg, freq_online],
                        theta=['Freq. Online', 'Review', 'Harga Murah', 'Risiko Siber', 'Layanan SPG', 'Freq. Online'],
                    ))
                    fig_radar = go.Figure(go.Scatterpolar(r=df_radar['r'], theta=df_radar['theta'], fill='toself', line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)'))
                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
                        title={'text': "Peta Jaring Persona", 'font': {'size': 14, 'color': '#0f172a'}}, 
                        margin=dict(t=40, b=20, l=30, r=30), 
                        height=260,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

            with c_gau:
                with st.container(border=True):
                    warna_bar = COLOR.get("success", "#10b981") if prob_final >= 0.5 else COLOR.get("danger", "#ef4444")
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number", value=prob_final * 100, number={'suffix': "%", 'font': {'size': 35, 'color': '#0f172a'}},
                        title={'text': "Confidence Ratio (P-Online)", 'font': {'size': 14, 'color': '#0f172a'}},
                        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': warna_bar}, 'threshold': {'line': {'color': "#0f172a", 'width': 3}, 'value': 50}}
                    ))
                    fig_gauge.update_layout(
                        margin=dict(t=40, b=20, l=30, r=30), 
                        height=260,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

            st.write("")
            with st.container(border=True):
                fig_tornado = go.Figure(go.Bar(
                    x=tornado.values, y=[prettify(f) for f in tornado.index], orientation='h',
                    marker_color=[COLOR.get("danger", "#ef4444") if v < 0 else COLOR.get("primary", "#3b82f6") for v in tornado.values],
                ))
                fig_tornado.update_layout(
                    title={'text': "Transparansi AI — Kontribusi Log-Odds per Fitur", 'font': {'size': 15, 'color': '#0f172a'}},
                    xaxis_title="Kontribusi terhadap kecenderungan Online (+) / Offline (-)",
                    margin=dict(t=50, b=20, l=10, r=10), 
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_tornado, use_container_width=True)

            st.write("")
            
            # --- KARTU VONIS CUSTOM ---
            if prob_final >= 0.50:
                st.markdown(f"""
                    <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 6px solid #10b981; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <h3 style="color: #065f46; margin-top: 0; margin-bottom: 8px;">🛒 VONIS AI: ONLINE SHOPPER ({prob_final*100:.1f}%)</h3>
                        <p style="color: #0f172a; font-size: 1rem; margin: 0; line-height: 1.5;">
                            <b>Transparansi AI:</b> Faktor pendorong terbesar adalah <b>{prettify(top_driving.index[-1])}</b>, yang menarik kecenderungan berbelanja ke arah platform digital. Faktor penahan (keraguan fisik/siber) terbesar yang berhasil dikalahkan oleh sentimen ini adalah <b>{prettify(top_restraining.index[0])}</b>.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-left: 6px solid #ef4444; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <h3 style="color: #991b1b; margin-top: 0; margin-bottom: 8px;">🏪 VONIS AI: OFFLINE SHOPPER ({(1-prob_final)*100:.1f}%)</h3>
                        <p style="color: #0f172a; font-size: 1rem; margin: 0; line-height: 1.5;">
                            <b>Transparansi AI:</b> Faktor penahan terbesar adalah <b>{prettify(top_restraining.index[0])}</b>, yang sangat kuat mengunci preferensi konsumen ini agar tetap loyal di dunia nyata. Daya tarik digital (pendorong) terbesar yang gagal mengubah keputusan ini adalah <b>{prettify(top_driving.index[-1])}</b>.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    # --- RIWAYAT EKSPANSI ---
    if st.session_state.get("riwayat_prediksi"):
        st.divider()
        with st.expander("Log Riwayat Prediksi (Sesi Saat Ini)", expanded=False):
            st.dataframe(pd.DataFrame(st.session_state.riwayat_prediksi), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)