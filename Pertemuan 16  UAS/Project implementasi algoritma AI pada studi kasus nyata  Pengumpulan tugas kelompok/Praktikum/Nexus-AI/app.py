import streamlit as st

# Import modul dari struktur folder baru
from modules.dashboard import show_dashboard
from modules.predictor import show_predictor
from modules.theme import ICON, inject_global_css

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Nexus AI Analytics",
    page_icon=ICON.get("favicon", "🤖"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# Injeksi CSS Global dari theme.py
inject_global_css(st)

# ==========================================
# 2. MANAJEMEN STATUS NAVIGASI
# ==========================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "dashboard"

NAV_ITEMS = [
    ("dashboard", "Executive Dashboard", "nav_dashboard"),
    ("predictor", "AI Persona Predictor", "nav_predictor"),
]

# ==========================================
# 3. MEMBANGUN SIDEBAR PREMIUM
# ==========================================
with st.sidebar:
    st.markdown('<div class="anim-slide-up">', unsafe_allow_html=True)

    # --- Logo & Branding ---
    col_logo1, col_logo2, col_logo3 = st.columns([1, 1.8, 1])
    with col_logo2:
        st.markdown(f"""
            <div class="anim-float" style="display: flex; justify-content: center; margin-top: 10px;">
                <img src="{ICON.get('logo')}" width="100%" style="filter: drop-shadow(0px 8px 12px rgba(59, 130, 246, 0.3));">
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<p style='margin-top: 10px; margin-bottom: 0; font-size: 2.2rem; font-weight: 900; text-align: center; letter-spacing: -0.5px; background: linear-gradient(90deg, #3b82f6, #1e40af); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Nexus AI</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-sub' style='margin-bottom: 20px;'>Consumer Behavior Intelligence</p>", unsafe_allow_html=True)
    
    st.markdown("""<hr style="margin: 10px 0 20px 0; border: none; border-top: 1px solid #e2e8f0;">""", unsafe_allow_html=True)

    # --- Menu Navigasi Interaktif ---
    st.markdown("<p style='font-size:0.75rem; color:#94a3b8; font-weight:800; letter-spacing:1.2px; margin-bottom: 10px;'>SISTEM NAVIGASI</p>", unsafe_allow_html=True)
    
    for key, label, icon_key in NAV_ITEMS:
        is_active = st.session_state.active_page == key
        c1, c2 = st.columns([1.2, 5])
        
        with c1:
            # Penyelarasan Vertikal agar ikon lurus dengan tombol
            st.markdown(f'<div style="display: flex; height: 100%; align-items: center; padding-top: 5px;"><img src="{ICON.get(icon_key)}" width="28"></div>', unsafe_allow_html=True)
            
        with c2:
            if st.button(
                label,
                key=f"btn_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.active_page = key
                st.rerun()

    st.write("")
    st.markdown("""<hr style="margin: 15px 0 20px 0; border: none; border-top: 1px solid #e2e8f0;">""", unsafe_allow_html=True)
    
    # --- Profil Tim Pengembang (Premium Card) ---
    st.markdown("<p style='font-size: 0.75rem; color: #64748b; font-weight: 800; letter-spacing: 1.2px;'>DEVELOPED BY</p>", unsafe_allow_html=True)

    st.markdown("""
        <div style="background: linear-gradient(145deg, #ffffff, #f8fafc); border: 1px solid #e2e8f0; border-left: 4px solid #2563eb; border-radius: 12px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-top: 5px;">
            <div style="margin-bottom: 12px;">
                <p style="margin: 0; font-weight: 800; color: #0f172a; font-size: 0.95rem;">Syarifah Nesia</p>
                <p style="margin: 0; font-weight: 500; color: #64748b; font-size: 0.75rem;">2024091017 (Teknik Sipil)</p>
            </div>
            <div>
                <p style="margin: 0; font-weight: 800; color: #0f172a; font-size: 0.95rem;">Panji Kurnia Akbar</p>
                <p style="margin: 0; font-weight: 500; color: #64748b; font-size: 0.75rem;">2024081024 (Sistem Informasi)</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. SISTEM ROUTING (RENDERING HALAMAN)
# ==========================================
if st.session_state.active_page == "dashboard":
    show_dashboard()
else:
    show_predictor()