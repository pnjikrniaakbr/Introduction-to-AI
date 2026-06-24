"""Tema visual & aset ikon bersama untuk seluruh halaman Nexus AI Analytics."""

ICON = {
    "favicon": "https://cdn-icons-png.flaticon.com/512/2083/2083213.png",
    "logo": "https://cdn-icons-png.flaticon.com/512/8943/8943377.png",
    "nav_dashboard": "https://cdn-icons-png.flaticon.com/512/2920/2920349.png",
    "nav_predictor": "https://cdn-icons-png.flaticon.com/512/4712/4712139.png",
    "online": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png",
    "offline": "https://cdn-icons-png.flaticon.com/512/9356/9356985.png",
    "people": "https://cdn-icons-png.flaticon.com/512/1632/1632899.png",
    "accuracy": "https://cdn-icons-png.flaticon.com/512/3556/3556352.png",
    "network": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
    "lock": "https://cdn-icons-png.flaticon.com/512/6195/6195700.png",
    "cart_check": "https://cdn-icons-png.flaticon.com/512/2620/2620655.png",
}

COLOR = {
    "primary": "#3b82f6",
    "primary_dark": "#2563eb",
    "accent": "#8b5cf6",
    "ink": "#0f172a",
    "muted": "#64748b",
    "success": "#10b981",
    "danger": "#ef4444",
    "bg_soft": "#f8fafc",
    "border": "#e2e8f0",
}

GLOBAL_CSS = """
<style>
/* ==============================================================
   PENGATURAN HEADER: PAKSA TOMBOL SIDEBAR MUNCUL & HAPUS DEPLOY+MENU
   ============================================================== */
/* 1. Paksa tombol membuka/menutup sidebar di kiri atas untuk tetap muncul */
button[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
}

/* 2. Lenyapkan tombol "Deploy" di kanan atas */
[data-testid="stDeployButton"], .stDeployButton {
    display: none !important;
    visibility: hidden !important;
}

/* 3. Lenyapkan menu titik tiga di kanan atas */
#MainMenu, [data-testid="stMainMenu"], [data-testid="stHeaderActionElements"] {
    display: none !important;
    visibility: hidden !important;
}

/* 4. Lenyapkan footer watermark bawaan di bawah */
footer {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stBottom"] {
    display: none !important;
}

/* 5. Buat background header menjadi transparan agar tombol sidebar terlihat rapi */
header[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
}
/* ============================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #3b82f6, #8b5cf6); border-radius: 10px; }

@keyframes slideUp {
    0% { opacity: 0; transform: translateY(22px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
@keyframes floaty { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }
@keyframes shimmer {
    0% { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}

.anim-slide-up { animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.anim-fade { animation: fadeIn 0.8s ease forwards; }
.anim-float { animation: floaty 3.5s ease-in-out infinite; }

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f4f7ff 100%);
    border-right: 1px solid #e2e8f0;
}
.brand-title {
    text-align: center; font-weight: 800; font-size: 1.5rem; margin: 6px 0 0 0;
    background: linear-gradient(90deg, #2563eb, #8b5cf6);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.brand-sub {
    text-align: center; color: #3b82f6; font-weight: 600; font-size: 0.82rem;
    letter-spacing: 0.5px; margin-top: -2px;
}
.sidebar-card {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    padding: 14px; border-radius: 14px; border: 1px solid #e2e8f0;
    text-align: center; margin-top: 8px;
}
.dev-line { color:#0f172a; font-size: 0.88rem; font-weight: 700; }
.dev-sub { color:#64748b; font-size: 0.76rem; }

/* ---- Nav buttons (segmented control feel) ---- */
div[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all 0.18s ease;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 14px rgba(59,130,246,0.18);
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
    border: none !important;
}

/* ---- Generic surfaces ---- */
.hero-banner {
    background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 55%, #4338ca 100%);
    border-radius: 20px; padding: 26px 30px; position: relative; overflow: hidden;
    box-shadow: 0 14px 30px rgba(15,23,42,0.18);
}
.hero-banner::after {
    content: ""; position: absolute; right: -60px; top: -60px; width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,102,241,0.45), transparent 70%);
}
.hero-title { color: #ffffff; font-weight: 800; font-size: 1.9rem; margin: 0; }
.hero-sub { color: #c7d2fe; font-size: 1rem; margin-top: 4px; }

.metric-card {
    border-radius: 16px; padding: 16px 18px; border: 1px solid #e2e8f0;
    background: #ffffff; transition: all 0.25s ease;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px rgba(15,23,42,0.10); }
.metric-label { color:#64748b; font-weight:700; font-size:0.78rem; letter-spacing:0.4px; text-transform:uppercase; }
.metric-value { font-weight:800; font-size:1.9rem; margin-top:2px; }

.insight-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f5f3ff 100%);
    padding: 22px; border-radius: 16px; border-left: 5px solid #8b5cf6;
}

.section-title {
    color:#0f172a; font-weight:800; display:flex; align-items:center; gap:10px;
}
</style>
"""

def inject_global_css(st):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def section_header(st, icon_key: str, title: str, subtitle: str = "", icon_size: int = 30):
    c1, c2 = st.columns([1, 14])
    with c1:
        st.image(ICON[icon_key], width=icon_size)
    with c2:
        st.markdown(f"<h3 class='section-title' style='margin:0;'>{title}</h3>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p style='color:#64748b; margin:0;'>{subtitle}</p>", unsafe_allow_html=True)