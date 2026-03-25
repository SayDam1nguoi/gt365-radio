"""CSS styling cho giao diện."""


def get_custom_css_string():
    """Trả về CSS string cho giao diện."""
    return """
        :root {
            --bg: #f4f7fb;
            --surface: #ffffff;
            --surface-soft: #f8fbff;
            --line: #d9e3f0;
            --line-strong: #c5d4e8;
            --text: #10203a;
            --muted: #5f6f86;
            --brand-1: #0f766e;
            --brand-2: #2563eb;
            --brand-3: #0ea5e9;
            --success-bg: #eefaf2;
            --success-border: #8fe0ae;
            --success-text: #166534;
            --warning-bg: #fff8e8;
            --warning-border: #f6d387;
            --warning-text: #b45309;
            --error-bg: #fff2f4;
            --error-border: #f5b3bd;
            --error-text: #be123c;
            --shadow-soft: 0 14px 36px rgba(15, 23, 42, 0.08);
            --shadow-strong: 0 20px 50px rgba(15, 23, 42, 0.10);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background:
                radial-gradient(circle at top left, rgba(14, 165, 233, 0.10), transparent 30%),
                radial-gradient(circle at top right, rgba(37, 99, 235, 0.10), transparent 28%),
                linear-gradient(180deg, #f6f9fd 0%, #f2f6fb 100%) !important;
            color: var(--text) !important;
            font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
        }

        [data-testid="stHeader"] {
            background: rgba(244, 247, 251, 0.82) !important;
            backdrop-filter: blur(12px);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        a,
        [data-testid="stHeaderActionElements"],
        .stHeadingAnchor,
        button[title*="anchor"],
        button[aria-label*="anchor"],
        [data-testid="StyledLinkIconContainer"] {
            display: none !important;
            visibility: hidden !important;
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            padding: 2.35rem 2.4rem;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.98) 0%, rgba(37, 99, 235, 0.98) 100%);
            color: #ffffff;
            box-shadow: var(--shadow-strong);
            margin-bottom: 1rem;
        }

        .hero-shell::before {
            content: "";
            position: absolute;
            right: -60px;
            bottom: -80px;
            width: 260px;
            height: 260px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
        }

        .hero-shell::after {
            content: "";
            position: absolute;
            left: -60px;
            top: -60px;
            width: 180px;
            height: 180px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.10);
        }

        .hero-eyebrow {
            position: relative;
            z-index: 1;
            display: inline-flex;
            padding: 0.5rem 0.9rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.22);
            background: rgba(255, 255, 255, 0.10);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            margin: 1rem 0 0.65rem;
            font-size: 2.35rem;
            line-height: 1.12;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #ffffff !important;
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 760px;
            margin: 0;
            color: rgba(255, 255, 255, 0.92) !important;
            line-height: 1.7;
            font-size: 1rem;
        }

        .hero-grid {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.95rem;
            margin-top: 1.4rem;
        }

        .hero-stat {
            padding: 1rem 1.05rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.11);
            border: 1px solid rgba(255, 255, 255, 0.14);
        }

        .hero-stat span {
            display: block;
            margin-bottom: 0.25rem;
            color: rgba(255, 255, 255, 0.72) !important;
            font-size: 0.82rem;
        }

        .hero-stat strong {
            color: #ffffff !important;
            font-size: 1rem;
            font-weight: 700;
        }

        .section-card {
            background: transparent;
            border: none;
            box-shadow: none;
            padding: 0.5rem 0 1rem;
            margin-bottom: 0.8rem;
        }

        .section-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding-bottom: 0.65rem;
            border-bottom: 2px solid var(--line);
        }

        .section-title-wrap {
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
        }

        .section-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.15rem;
        }

        .section-kicker {
            color: var(--brand-2) !important;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .section-icon {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(37, 99, 235, 0.12));
            font-size: 1.1rem;
        }

        .section-title {
            margin: 0;
            color: var(--text) !important;
            font-size: 1.22rem;
            font-weight: 800;
            line-height: 1.2;
        }

        .section-subtitle {
            margin: 0.12rem 0 0;
            color: var(--muted) !important;
            font-size: 0.93rem;
            line-height: 1.55;
        }

        .pill-note {
            padding: 0.5rem 0.85rem;
            border-radius: 999px;
            background: #edf4ff;
            border: 1px solid #cfe0ff;
            color: #2458d3 !important;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .status-box {
            border-radius: 18px;
            padding: 1rem 1.1rem;
            border: 1px solid;
            margin: 0.8rem 0 0.2rem;
            line-height: 1.6;
        }

        .success-box {
            background: var(--success-bg);
            border-color: var(--success-border);
            color: var(--success-text);
        }

        .warning-box {
            background: var(--warning-bg);
            border-color: var(--warning-border);
            color: var(--warning-text);
        }

        .error-box {
            background: var(--error-bg);
            border-color: var(--error-border);
            color: var(--error-text);
        }

        .inline-valid {
            margin: -0.2rem 0 0.6rem;
            color: #15803d;
            font-size: 0.84rem;
            font-weight: 700;
        }

        .inline-error {
            margin: -0.2rem 0 0.6rem;
            color: #be123c;
            font-size: 0.84rem;
            font-weight: 700;
        }

        .stButton > button,
        .stDownloadButton > button {
            min-height: 52px;
            border: none !important;
            border-radius: 16px !important;
            background: linear-gradient(135deg, var(--brand-1) 0%, var(--brand-2) 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 14px 28px rgba(37, 99, 235, 0.18);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 34px rgba(37, 99, 235, 0.22);
        }

        .stButton > button *,
        .stDownloadButton > button * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.95) !important;
            color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 18px !important;
            box-shadow: none !important;
        }

        .stTextInput input,
        .stNumberInput input {
            min-height: 52px;
        }

        .stTextArea textarea {
            min-height: 160px;
            line-height: 1.72;
            padding: 1rem 1.1rem !important;
            border-radius: 22px !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: #93c5fd !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.10) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.7rem;
            padding: 0.35rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid var(--line);
            margin-bottom: 1.4rem;
            box-shadow: var(--shadow-soft);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            border-radius: 14px;
            color: var(--muted) !important;
            font-weight: 800;
            padding: 0 1rem;
            background: transparent !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.10), rgba(37, 99, 235, 0.12)) !important;
            color: var(--text) !important;
        }

        .soft-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.95rem;
            margin: 0.2rem 0 1.4rem;
        }

        .soft-stat {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1.05rem;
            box-shadow: var(--shadow-soft);
        }

        .soft-stat span {
            display: block;
            color: var(--muted) !important;
            font-size: 0.82rem;
            margin-bottom: 0.28rem;
        }

        .soft-stat strong {
            color: var(--text) !important;
            font-size: 1rem;
            font-weight: 800;
        }

        .result-card {
            background: transparent;
            padding: 0;
            margin: 1.2rem 0 0.7rem;
        }

        .result-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.25rem 0 0.85rem;
            border-bottom: 2px solid var(--line);
        }

        .result-title-wrap {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }

        .result-index {
            width: 46px;
            height: 46px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #ffffff;
            border: 1px solid var(--line);
            color: var(--brand-2);
            font-weight: 800;
            box-shadow: var(--shadow-soft);
        }

        .result-head h3 {
            margin: 0;
            color: var(--text) !important;
            font-size: 1.16rem;
            font-weight: 800;
        }

        .result-head p {
            margin: 0.2rem 0 0;
            color: var(--muted) !important;
            font-size: 0.9rem;
        }

        .result-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.45rem 0.85rem;
            background: #ecfdf5;
            color: #047857 !important;
            border: 1px solid #a7f3d0;
            font-size: 0.82rem;
            font-weight: 800;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem;
            text-align: center;
            box-shadow: var(--shadow-soft);
        }

        .metric-card h4 {
            margin: 0 0 0.35rem;
            color: var(--muted) !important;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .metric-card h2 {
            margin: 0;
            color: var(--text) !important;
            font-size: 1.65rem;
            font-weight: 800;
        }

        .metric-card p {
            margin: 0.3rem 0 0;
            color: var(--muted) !important;
            font-size: 0.86rem;
        }

        .success-banner {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            padding: 1.35rem 1.45rem;
            margin: 1rem 0;
            border-radius: 22px;
            border: 1px solid var(--success-border);
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.10), rgba(34, 197, 94, 0.04));
            box-shadow: var(--shadow-soft);
        }

        .success-banner__icon {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #dcfce7;
            font-size: 1.45rem;
        }

        .success-banner h3 {
            margin: 0 0 0.3rem;
            color: #15803d !important;
            font-size: 1.08rem;
            font-weight: 800;
        }

        .success-banner p {
            margin: 0 0 0.25rem;
            color: #166534 !important;
        }

        .success-banner span {
            color: #166534 !important;
            font-weight: 700;
            font-size: 0.95rem;
        }

        .empty-state {
            padding: 2.2rem 1.4rem;
            border-radius: 24px;
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.84);
            text-align: center;
            box-shadow: var(--shadow-soft);
        }

        .empty-state h3 {
            margin: 0 0 0.5rem;
            color: var(--text) !important;
        }

        .empty-state p {
            margin: 0;
            color: var(--muted) !important;
        }

        .source-chip {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.9rem 0.95rem;
            box-shadow: var(--shadow-soft);
            margin-bottom: 0.8rem;
        }

        .source-chip__name {
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .source-chip__domain {
            color: var(--muted);
            font-size: 0.83rem;
        }

        .stMarkdown,
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label,
        p,
        span,
        label {
            color: var(--text) !important;
        }

        @media (max-width: 900px) {
            .hero-grid,
            .soft-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 1.2rem;
            }

            .hero-shell {
                padding: 1.5rem 1.2rem;
                border-radius: 22px;
            }

            .hero-title {
                font-size: 1.85rem;
            }

            .result-head,
            .section-head {
                align-items: flex-start;
                flex-direction: column;
            }
        }
    """
