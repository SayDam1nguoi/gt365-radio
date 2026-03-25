"""CSS styling cho giao diện."""


def get_custom_css_string():
    """Trả về CSS string cho giao diện."""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,600;1,500&display=swap');

        :root {
            --bg:           #f7f8fa;
            --surface:      #ffffff;
            --surface-2:    #f2f4f8;
            --surface-3:    #e8ecf3;
            --line:         #e3e8f0;
            --line-strong:  #ccd4e3;
            --text:         #111827;
            --text-2:       #4b5563;
            --text-3:       #9ca3af;
            --accent:       #1d4ed8;
            --accent-light: #eff4ff;
            --accent-mid:   #dbeafe;
            --green:        #16a34a;
            --green-dim:    #f0fdf4;
            --green-border: #bbf7d0;
            --red:          #dc2626;
            --red-dim:      #fef2f2;
            --red-border:   #fecaca;
            --amber:        #d97706;
            --amber-dim:    #fffbeb;
            --amber-border: #fde68a;
            --shadow-sm:    0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
            --shadow:       0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.04);
            --shadow-lg:    0 12px 40px rgba(0,0,0,0.09);
            --r:            16px;
            --r-sm:         10px;
            --r-xs:         7px;
        }

        /* ─── Base ──────────────────────────────────────────── */
        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--bg) !important;
            color: var(--text) !important;
            font-family: 'Be Vietnam Pro', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background: rgba(247,248,250,0.9) !important;
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--line);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1060px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        #MainMenu,
        footer,
        .viewerBadge_container__1QSob,
        [data-testid="stToolbar"] {
            display: none !important;
        }

        a, [data-testid="stHeaderActionElements"],
        .stHeadingAnchor, button[title*="anchor"],
        [data-testid="StyledLinkIconContainer"] {
            display: none !important;
        }

        p, span, label,
        .stMarkdown,
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label {
            font-family: 'Be Vietnam Pro', sans-serif !important;
            font-size: 0.875rem !important;
            line-height: 1.6 !important;
            color: var(--text-2) !important;
        }

        /* ─── Hero ──────────────────────────────────────────── */
        .hero-shell {
            position: relative;
            overflow: hidden;
            padding: 2.8rem 2.8rem 2.4rem;
            border-radius: 20px;
            background: var(--surface);
            border: 1px solid var(--line);
            box-shadow: var(--shadow);
            margin-bottom: 0.5rem;
        }

        .hero-shell::after {
            content: "";
            position: absolute;
            top: -100px; right: -100px;
            width: 380px; height: 380px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(29,78,216,0.05) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-eyebrow {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.32rem 0.75rem;
            border-radius: 999px;
            border: 1px solid var(--accent-mid);
            background: var(--accent-light);
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent) !important;
            margin-bottom: 1.1rem;
        }

        .hero-eyebrow::before {
            content: "";
            width: 5px; height: 5px;
            border-radius: 999px;
            background: var(--accent);
            animation: pulse-dot 2s ease-in-out infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%       { opacity: 0.4; transform: scale(0.65); }
        }

        .hero-title {
            position: relative;
            z-index: 1;
            margin: 0 0 0.8rem;
            font-family: 'Lora', serif !important;
            font-size: 2.6rem;
            line-height: 1.12;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--text) !important;
        }

        .hero-title em {
            font-style: italic;
            font-weight: 500;
            color: var(--accent) !important;
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 640px;
            margin: 0 0 2rem;
            font-size: 0.95rem !important;
            color: var(--text-2) !important;
            line-height: 1.75 !important;
            font-weight: 400;
        }

        .hero-grid {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1px;
            border: 1px solid var(--line);
            border-radius: var(--r-sm);
            overflow: hidden;
        }

        .hero-stat {
            padding: 1rem 1.25rem;
            background: var(--surface-2);
            transition: background 0.15s;
        }
        .hero-stat:hover { background: var(--surface-3); }

        .hero-stat span {
            display: block;
            font-size: 0.72rem !important;
            font-weight: 600;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: var(--text-3) !important;
            margin-bottom: 0.3rem;
        }

        .hero-stat strong {
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text) !important;
        }

        /* ─── Section Header ────────────────────────────────── */
        .section-card {
            background: transparent;
            padding: 0.2rem 0 1rem;
            margin-bottom: 0.2rem;
        }

        .section-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding-bottom: 0.8rem;
            border-bottom: 1.5px solid var(--line);
        }

        .section-title-wrap {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-icon {
            width: 36px; height: 36px;
            border-radius: var(--r-xs);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-light);
            border: 1px solid var(--accent-mid);
            font-size: 0.95rem;
            flex-shrink: 0;
        }

        .section-kicker {
            font-size: 0.68rem !important;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent) !important;
            display: block;
            margin-bottom: 0.1rem;
        }

        .section-title {
            margin: 0;
            font-size: 1rem !important;
            font-weight: 700;
            color: var(--text) !important;
            line-height: 1.3 !important;
        }

        .section-subtitle {
            margin: 0.1rem 0 0;
            font-size: 0.82rem !important;
            color: var(--text-3) !important;
            line-height: 1.5 !important;
        }

        .pill-note {
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            background: var(--surface-2);
            border: 1px solid var(--line-strong);
            font-size: 0.72rem !important;
            font-weight: 700;
            color: var(--text-3) !important;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }

        /* ─── Inputs ────────────────────────────────────────── */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox [data-baseweb="select"] > div {
            background: var(--surface) !important;
            color: var(--text) !important;
            border: 1.5px solid var(--line-strong) !important;
            border-radius: var(--r-xs) !important;
            box-shadow: none !important;
            font-family: 'Be Vietnam Pro', sans-serif !important;
            font-size: 0.875rem !important;
            transition: border-color 0.15s, box-shadow 0.15s;
        }

        .stTextInput input,
        .stNumberInput input { min-height: 44px; }

        .stTextArea textarea {
            line-height: 1.75 !important;
            padding: 0.85rem 1rem !important;
            border-radius: var(--r-sm) !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
        }

        .stSelectbox [data-baseweb="select"] span {
            font-size: 0.875rem !important;
            color: var(--text) !important;
        }

        /* ─── Buttons ───────────────────────────────────────── */
        .stButton > button {
            min-height: 40px;
            border: 1.5px solid var(--line-strong) !important;
            border-radius: var(--r-xs) !important;
            background: var(--surface) !important;
            color: var(--text-2) !important;
            font-family: 'Be Vietnam Pro', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            box-shadow: var(--shadow-sm) !important;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            background: var(--surface-2) !important;
            color: var(--text) !important;
            box-shadow: var(--shadow) !important;
        }

        .stButton > button[kind="primary"] {
            background: var(--accent) !important;
            border-color: var(--accent) !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            min-height: 52px;
            border-radius: var(--r-sm) !important;
            box-shadow: 0 4px 16px rgba(29,78,216,0.25) !important;
            letter-spacing: 0.01em;
        }

        .stButton > button[kind="primary"]:hover {
            background: #1e40af !important;
            border-color: #1e40af !important;
            box-shadow: 0 6px 20px rgba(29,78,216,0.35) !important;
            transform: translateY(-1px);
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"] * { color: #ffffff !important; }

        .stDownloadButton > button {
            min-height: 44px;
            border-radius: var(--r-xs) !important;
            background: var(--green-dim) !important;
            border: 1.5px solid var(--green-border) !important;
            color: var(--green) !important;
            font-family: 'Be Vietnam Pro', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            transition: all 0.15s ease;
        }

        .stDownloadButton > button:hover {
            background: #dcfce7 !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm) !important;
        }

        .stDownloadButton > button * { color: var(--green) !important; }

        /* ─── Tabs ──────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.2rem;
            padding: 0.25rem;
            border-radius: var(--r-sm);
            background: var(--surface);
            border: 1px solid var(--line);
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
        }

        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: var(--r-xs);
            color: var(--text-3) !important;
            font-family: 'Be Vietnam Pro', sans-serif !important;
            font-size: 0.875rem !important;
            font-weight: 600;
            padding: 0 1.1rem;
            background: transparent !important;
            transition: all 0.15s;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-2) !important;
            background: var(--surface-2) !important;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-light) !important;
            color: var(--accent) !important;
            border: 1px solid var(--accent-mid) !important;
        }

        /* ─── Controlled tab nav ───────────────────────────── */
        .tab-nav-shell {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.1rem 0.7rem;
            border: 1px solid var(--line);
            border-bottom: 0;
            border-radius: var(--r) var(--r) 0 0;
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(239,244,255,0.92));
            box-shadow: var(--shadow-sm);
        }

        .tab-nav-copy span {
            display: block;
            font-size: 0.68rem !important;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent) !important;
            margin-bottom: 0.18rem;
        }

        .tab-nav-copy strong {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text);
        }

        .stRadio > div[role="radiogroup"] {
            gap: 0.6rem;
            padding: 0.7rem;
            margin-bottom: 1.25rem;
            border: 1px solid var(--line);
            border-top: 0;
            border-radius: 0 0 var(--r) var(--r);
            background: var(--surface);
            box-shadow: var(--shadow-sm);
        }

        .stRadio > div[role="radiogroup"] label {
            margin: 0 !important;
            padding: 0.68rem 1rem !important;
            border: 1px solid var(--line) !important;
            border-radius: 999px !important;
            background: var(--surface-2) !important;
            transition: all 0.18s ease;
        }

        .stRadio > div[role="radiogroup"] label:hover {
            border-color: var(--accent-mid) !important;
            background: var(--accent-light) !important;
        }

        .stRadio > div[role="radiogroup"] label[data-selected="true"] {
            border-color: var(--accent) !important;
            background: var(--accent-light) !important;
            box-shadow: inset 0 0 0 1px rgba(29,78,216,0.12);
        }

        .stRadio > div[role="radiogroup"] label p {
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            color: var(--text) !important;
        }

        .stRadio > div[role="radiogroup"] label[data-selected="true"] p {
            color: var(--accent) !important;
        }

        /* ─── Status boxes ──────────────────────────────────── */
        .status-box {
            border-radius: var(--r-xs);
            padding: 0.75rem 0.95rem;
            border: 1px solid;
            margin: 0.6rem 0 0.15rem;
            font-size: 0.86rem !important;
            line-height: 1.6 !important;
        }

        .success-box { background: var(--green-dim); border-color: var(--green-border); color: var(--green) !important; }
        .success-box strong { color: var(--green) !important; }

        .warning-box { background: var(--amber-dim); border-color: var(--amber-border); color: var(--amber) !important; }
        .warning-box strong { color: var(--amber) !important; }

        .error-box { background: var(--red-dim); border-color: var(--red-border); color: var(--red) !important; }
        .error-box strong { color: var(--red) !important; }

        .inline-valid {
            margin: -0.05rem 0 0.45rem;
            color: var(--green);
            font-size: 0.8rem !important;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        .inline-valid::before { content: "✓"; font-weight: 800; }

        .inline-error {
            margin: -0.05rem 0 0.45rem;
            color: var(--red);
            font-size: 0.8rem !important;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        .inline-error::before { content: "✕"; font-weight: 800; }

        /* ─── Sources ───────────────────────────────────────── */
        .source-chip {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--r-xs);
            padding: 0.65rem 0.85rem;
            margin-bottom: 0.6rem;
            transition: all 0.15s;
            box-shadow: var(--shadow-sm);
        }
        .source-chip:hover { border-color: var(--accent-mid); background: var(--accent-light); }

        .source-chip__name {
            font-size: 0.86rem !important;
            font-weight: 700;
            color: var(--text) !important;
            margin-bottom: 0.14rem;
        }

        .source-chip__domain {
            font-size: 0.76rem !important;
            color: var(--text-3) !important;
            font-weight: 500;
        }

        /* ─── Overview grid ─────────────────────────────────── */
        .soft-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1px;
            border: 1px solid var(--line);
            border-radius: var(--r-sm);
            overflow: hidden;
            margin: 0.3rem 0 1.5rem;
            box-shadow: var(--shadow-sm);
        }

        .soft-stat { background: var(--surface); padding: 1rem 1.15rem; }

        .soft-stat span {
            display: block;
            font-size: 0.7rem !important;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: var(--text-3) !important;
            margin-bottom: 0.28rem;
        }

        .soft-stat strong {
            font-size: 0.9rem !important;
            font-weight: 700;
            color: var(--text) !important;
        }

        /* ─── Result card ───────────────────────────────────── */
        .result-card { padding: 0; margin: 1.4rem 0 0.6rem; }

        .result-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 0 0.8rem;
            border-bottom: 1.5px solid var(--line);
        }

        .result-title-wrap { display: flex; align-items: center; gap: 0.75rem; }

        .result-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .result-index {
            width: 36px; height: 36px;
            border-radius: var(--r-xs);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-light);
            border: 1px solid var(--accent-mid);
            color: var(--accent) !important;
            font-size: 0.82rem;
            font-weight: 800;
            flex-shrink: 0;
        }

        .result-title {
            margin: 0;
            font-size: 1rem !important;
            font-weight: 700;
            color: var(--text) !important;
            line-height: 1.3;
        }

        .result-subtitle {
            margin: 0.12rem 0 0;
            font-size: 0.8rem !important;
            color: var(--text-3) !important;
            line-height: 1.5;
        }

        .result-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.3rem 0.75rem;
            background: var(--green-dim);
            color: var(--green) !important;
            border: 1px solid var(--green-border);
            font-size: 0.72rem !important;
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        /* ─── Metric card ───────────────────────────────────── */
        .metric-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--r-xs);
            padding: 0.85rem 0.95rem;
            text-align: center;
            box-shadow: var(--shadow-sm);
        }

        .metric-label {
            margin: 0 0 0.25rem;
            font-size: 0.68rem !important;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-3) !important;
        }

        .metric-value {
            margin: 0;
            font-family: 'Lora', serif;
            font-size: 1.7rem !important;
            font-weight: 600;
            color: var(--accent) !important;
            line-height: 1;
        }

        .metric-note {
            margin: 0.25rem 0 0;
            font-size: 0.76rem !important;
            color: var(--text-3) !important;
        }

        /* ─── Success banner ────────────────────────────────── */
        .success-banner {
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
            padding: 1.1rem 1.25rem;
            margin: 0.9rem 0;
            border-radius: var(--r-sm);
            border: 1px solid var(--green-border);
            background: var(--green-dim);
            box-shadow: var(--shadow-sm);
        }

        .success-banner__icon {
            width: 40px; height: 40px;
            border-radius: var(--r-xs);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #dcfce7;
            font-size: 1.2rem;
            flex-shrink: 0;
        }

        .success-banner h3 { margin: 0 0 0.2rem; font-size: 0.95rem !important; font-weight: 700; color: var(--green) !important; }
        .success-banner p  { margin: 0 0 0.15rem; font-size: 0.86rem !important; color: #15803d !important; }
        .success-banner span { font-size: 0.82rem !important; color: #16a34a !important; font-weight: 500; }

        /* ─── Progress panel ───────────────────────────────── */
        .progress-shell {
            margin: 1rem 0 0.6rem;
            padding: 1rem 1.1rem;
            border-radius: var(--r-sm);
            border: 1px solid var(--accent-mid);
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            box-shadow: var(--shadow-sm);
        }

        .progress-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
        }

        .progress-kicker {
            font-size: 0.68rem !important;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent) !important;
            margin-bottom: 0.2rem;
        }

        .progress-status {
            font-size: 0.96rem;
            line-height: 1.5;
            font-weight: 600;
            color: var(--text);
        }

        .progress-percent {
            min-width: 68px;
            padding: 0.34rem 0.7rem;
            border-radius: 999px;
            background: var(--accent-light);
            border: 1px solid var(--accent-mid);
            font-size: 0.92rem;
            font-weight: 700;
            text-align: center;
            color: var(--accent);
        }

        .progress-detail {
            margin-top: 0.55rem;
            font-size: 0.84rem !important;
            color: var(--text-2) !important;
        }

        .progress-caption {
            margin-top: 0.28rem;
            font-size: 0.8rem !important;
            color: var(--text-3) !important;
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #1d4ed8, #2563eb) !important;
        }

        /* ─── Empty state ───────────────────────────────────── */
        .empty-state {
            padding: 4rem 2rem;
            border-radius: var(--r);
            border: 1.5px dashed var(--line-strong);
            background: var(--surface);
            text-align: center;
            box-shadow: var(--shadow-sm);
        }

        .empty-state-icon { font-size: 2.2rem; margin-bottom: 0.9rem; opacity: 0.35; }
        .empty-state h3 { margin: 0 0 0.4rem; font-size: 1.05rem !important; font-weight: 700; color: var(--text-2) !important; }
        .empty-state p  { margin: 0; font-size: 0.875rem !important; color: var(--text-3) !important; }

        /* ─── Textarea result ───────────────────────────────── */
        .stTextArea textarea {
            background: var(--surface) !important;
            border-color: var(--line-strong) !important;
            color: var(--text) !important;
            font-size: 0.9rem !important;
            line-height: 1.8 !important;
        }

        /* ─── Scrollbar ─────────────────────────────────────── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--line-strong); border-radius: 3px; }

        /* ─── Animations ────────────────────────────────────── */
        .fade-in { animation: fadein 0.35s ease both; }
        @keyframes fadein {
            from { opacity: 0; transform: translateY(5px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* ─── Expander ──────────────────────────────────────── */
        .streamlit-expanderHeader {
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            color: var(--text-2) !important;
            background: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--r-xs) !important;
        }

        /* ─── Responsive ────────────────────────────────────── */
        @media (max-width: 900px) {
            .hero-grid, .soft-grid { grid-template-columns: 1fr 1fr; }
        }

        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] { padding-top: 1.2rem; }
            .hero-shell { padding: 1.6rem 1.3rem; }
            .hero-title { font-size: 1.9rem; }
            .hero-grid, .soft-grid { grid-template-columns: 1fr; }
            .result-head, .section-head { flex-direction: column; align-items: flex-start; }
        }
    """
