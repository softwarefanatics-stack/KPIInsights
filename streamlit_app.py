import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================================
# 1. Page Configuration
# ============================================================================
st.set_page_config(page_title="Innovation Unit Performance Portal", page_icon="📊", layout="wide")

# ============================================================================
# Mac-style design system (CSS)
# ============================================================================
MAC_CSS = """
<style>
:root {
    --mac-bg: #EEF1F6;
    --mac-border: rgba(0,0,0,0.07);
    --mac-text: #1D1D1F;
    --mac-subtext: #6E6E73;
    --mac-blue: #0A84FF;
    --mac-green: #30D158;
    --mac-orange: #FF9F0A;
    --mac-purple: #BF5AF2;
    --mac-red: #FF453A;
    --mac-teal: #64D2FF;
    --mac-yellow: #FFD60A;
    --mac-pink: #FF375F;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
                 "Helvetica Neue", Arial, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 0%, #F6F8FC 0%, var(--mac-bg) 55%);
}

header[data-testid="stHeader"] { background: transparent; }

/* ---- floating "window" shell ---- */
.mac-titlebar {
    display: flex;
    align-items: center;
    gap: 8px;
    max-width: 1200px;
    margin: 18px auto -1px auto;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--mac-border);
    border-radius: 14px 14px 0 0;
    padding: 12px 18px;
}
.mac-dot { width: 12px; height: 12px; border-radius: 50%; box-shadow: inset 0 0 0 1px rgba(0,0,0,0.08); }
.mac-dot.red { background: #FF5F57; }
.mac-dot.yellow { background: #FEBC2E; }
.mac-dot.green { background: #28C840; }
.mac-titlebar-title {
    margin-left: 10px;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--mac-subtext);
}

[data-testid="stAppViewContainer"] .main .block-container {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(30px) saturate(180%);
    border: 1px solid var(--mac-border);
    border-top: none;
    border-radius: 0 0 18px 18px;
    box-shadow: 0 24px 60px rgba(0,0,0,0.09);
    max-width: 1200px;
    padding: 36px 44px 56px 44px !important;
}

/* ---- header block ---- */
.mac-app-header { display:flex; align-items:center; gap:16px; margin-bottom: 4px; }
.mac-app-header h1 { margin:0; font-size: 26px; font-weight:800; color: var(--mac-text); letter-spacing:-0.02em; }
.mac-app-header p { margin: 2px 0 0 0; font-size: 14px; color: var(--mac-subtext); }

/* ---- app-icon badge, mac launchpad style ---- */
.app-icon {
    width: 50px; height: 50px;
    border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
    box-shadow: 0 6px 14px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.35);
}
.app-icon.small { width: 38px; height: 38px; font-size: 18px; border-radius: 10px; }
.app-icon.blue   { background: linear-gradient(160deg, #5AC8FF 0%, #0A84FF 100%); }
.app-icon.green  { background: linear-gradient(160deg, #79E89B 0%, #30D158 100%); }
.app-icon.orange { background: linear-gradient(160deg, #FFC972 0%, #FF9F0A 100%); }
.app-icon.purple { background: linear-gradient(160deg, #DE9CFF 0%, #BF5AF2 100%); }
.app-icon.red    { background: linear-gradient(160deg, #FF8A80 0%, #FF453A 100%); }
.app-icon.teal   { background: linear-gradient(160deg, #9CEEFF 0%, #64D2FF 100%); }
.app-icon.pink   { background: linear-gradient(160deg, #FF8FB3 0%, #FF375F 100%); }

/* ---- section headers ---- */
.section-header { display:flex; align-items:center; gap:14px; margin: 6px 0 20px 0; }
.section-header h2 { margin:0; font-size: 19px; font-weight:700; color: var(--mac-text); letter-spacing:-0.01em; }
.section-header p { margin:1px 0 0 0; font-size: 12.5px; color: var(--mac-subtext); }

/* ---- metric cards ---- */
.mac-metric-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid var(--mac-border);
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.07);
    display: flex; flex-direction: column; gap: 12px;
    height: 100%;
}
.mac-metric-card .icon-row { display:flex; align-items:center; justify-content:space-between; }
.mac-metric-card .value { font-size: 24px; font-weight: 800; color: var(--mac-text); letter-spacing: -0.02em; line-height:1.1; }
.mac-metric-card .label { font-size: 11.5px; color: var(--mac-subtext); font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }
.mac-metric-card .delta { font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 8px; display:inline-block; }
.mac-metric-card .delta.positive { color: #1f8b3d; background: rgba(48,209,88,0.14); }
.mac-metric-card .delta.negative { color: #c92a1e; background: rgba(255,69,58,0.14); }
.mac-metric-card .delta.neutral { color: var(--mac-subtext); background: rgba(110,110,115,0.1); }

/* ---- chart + dataframe cards ---- */
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.85);
    border: 1px solid var(--mac-border);
    border-radius: 16px;
    padding: 10px 6px 0 6px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.07);
}
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--mac-border);
    box-shadow: 0 8px 22px rgba(0,0,0,0.07);
}

/* ---- buttons ---- */
.stButton button, button[kind="primary"] {
    background: linear-gradient(180deg, #3AA2FF 0%, #0A84FF 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 980px !important;
    padding: 0.6rem 1.6rem !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(10,132,255,0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(10,132,255,0.45) !important;
}

/* ---- file uploader ---- */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.7) !important;
    border: 2px dashed rgba(10,132,255,0.35) !important;
    border-radius: 16px !important;
}

/* ---- alerts ---- */
[data-testid="stAlert"] { border-radius: 14px !important; border: 1px solid var(--mac-border) !important; }

/* ---- sidebar ---- */
[data-testid="stSidebar"] {
    background: rgba(246,247,250,0.85) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--mac-border);
}
.mac-sidebar-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid var(--mac-border);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}
.mac-sidebar-card ul { margin: 8px 0 0 0; padding-left: 18px; }
.mac-sidebar-card li { margin-bottom: 6px; font-size: 13px; color: var(--mac-text); }

hr { border-color: var(--mac-border) !important; }
</style>
"""

st.markdown(MAC_CSS, unsafe_allow_html=True)

# Fake macOS window title bar
st.markdown(
    """
    <div class="mac-titlebar">
        <span class="mac-dot red"></span>
        <span class="mac-dot yellow"></span>
        <span class="mac-dot green"></span>
        <span class="mac-titlebar-title">Innovation Unit Performance Portal</span>
    </div>
    """,
    unsafe_allow_html=True,
)


def app_icon(symbol: str, color: str, size: str = "") -> str:
    """Return HTML for a macOS launchpad-style icon badge."""
    cls = f"app-icon {color} {size}".strip()
    return f'<div class="{cls}">{symbol}</div>'


def section_header(symbol: str, color: str, title: str, subtitle: str = "") -> None:
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="section-header">
            {app_icon(symbol, color, "small")}
            <div><h2>{title}</h2>{sub_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mac_metric(col, symbol: str, color: str, label: str, value: str, delta: str = None, sentiment: str = "neutral") -> None:
    delta_html = f'<span class="delta {sentiment}">{delta}</span>' if delta else ""
    col.markdown(
        f"""
        <div class="mac-metric-card">
            <div class="icon-row">{app_icon(symbol, color, "small")}{delta_html}</div>
            <div class="value">{value}</div>
            <div class="label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig):
    """Apply a consistent, light, macOS-flavoured look to a plotly figure."""
    fig.update_layout(
        title_font=dict(size=15, color="#1D1D1F"),
        title_x=0.01,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="-apple-system, 'Helvetica Neue', Arial, sans-serif", color="#1D1D1F", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="left", x=0, title=None, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=70, b=10),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False)
    return fig


# Vivid macOS accent palette
MAC_BLUE, MAC_GREEN, MAC_ORANGE = "#0A84FF", "#30D158", "#FF9F0A"
MAC_PURPLE, MAC_RED, MAC_TEAL = "#BF5AF2", "#FF453A", "#64D2FF"
MAC_YELLOW, MAC_PINK, MAC_GRAY = "#FFD60A", "#FF375F", "#C7C9CE"
MAC_QUALITATIVE = [MAC_BLUE, MAC_GREEN, MAC_ORANGE, MAC_PURPLE, MAC_RED, MAC_TEAL, MAC_YELLOW, MAC_PINK]

# ============================================================================
# Header
# ============================================================================
st.markdown(
    f"""
    <div class="mac-app-header">
        {app_icon("📈", "blue")}
        <div>
            <h1>🇿🇦 Innovation Unit Performance Portal</h1>
            <p>Upload your unit's performance report to generate the operational KPI dashboard.</p>
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True,
)

# Strict validation schema matching Innovation_Unit_Performance.csv
REQUIRED_COLUMNS = [
    'Innovation', 'Budget_ZAR', 'Revenue_Generated_ZAR', 'Net_Benefit_ZAR',
    'ROI_Percent', 'Implementation_Months'
]

# ============================================================================
# 2. File Upload Component
# ============================================================================
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        # Support both CSV and Excel format based on user upload
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Clean whitespaces from uploaded column headers
        df.columns = [str(col).strip() for col in df.columns]

        # Schema verification
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

        if missing_cols:
            st.error("❌ **Upload Failed: Missing Required Columns**")
            st.warning(f"Your report layout is missing these column headers: {missing_cols}")
            st.info("Please align your file to match the standard Innovation Unit schema exactly.")
        else:
            st.success("✅ File format verified successfully!")

            # 3. Execution Trigger Button
            if st.button("🚀 Generate KPI Dashboard", type="primary"):
                with st.spinner("Processing innovation metrics..."):

                    # Core Derived Calculations
                    df['Benefit-Cost Ratio'] = df['Revenue_Generated_ZAR'] / df['Budget_ZAR']

                    st.write("")
                    section_header("🎯", "orange", "Operational Executive Summary")

                    # High-Level Metrics Row
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

                    total_budget = df['Budget_ZAR'].sum()
                    total_revenue = df['Revenue_Generated_ZAR'].sum()
                    total_net_benefit = df['Net_Benefit_ZAR'].sum()
                    avg_roi = df['ROI_Percent'].mean()

                    mac_metric(
                        m_col1, "💰", "blue", "Total Budget Allocated",
                        f"R {total_budget:,.2f}"
                    )
                    mac_metric(
                        m_col2, "📈", "orange", "Total Revenue Generated",
                        f"R {total_revenue:,.2f}",
                        delta=f"R {total_net_benefit:,.2f} net benefit",
                        sentiment="positive" if total_net_benefit >= 0 else "negative"
                    )
                    mac_metric(
                        m_col3, "💎", "green", "Total Net Benefit",
                        f"R {total_net_benefit:,.2f}"
                    )
                    mac_metric(
                        m_col4, "🎯", "purple", "Average ROI",
                        f"{avg_roi:,.1f}%"
                    )

                    st.write("")
                    st.write("")

                    # Charts Section - Row 1: KPI Performance and Budgeting
                    section_header("📊", "purple", "Performance & Budgetary Insights")
                    c_col1, c_col2 = st.columns(2)

                    with c_col1:
                        # Budget vs Revenue Generated by Innovation
                        df_melted_fin = df.melt(
                            id_vars=['Innovation'],
                            value_vars=['Budget_ZAR', 'Revenue_Generated_ZAR'],
                            var_name='Financial Type', value_name='Amount (R)'
                        )
                        fig_fin = px.bar(
                            df_melted_fin, x='Innovation', y='Amount (R)', color='Financial Type',
                            barmode='group', title='Budget vs Revenue Generated by Innovation',
                            color_discrete_map={'Budget_ZAR': MAC_GREEN, 'Revenue_Generated_ZAR': MAC_ORANGE}
                        )
                        st.plotly_chart(style_chart(fig_fin), use_container_width=True)

                    with c_col2:
                        # Return on Investment by Innovation
                        fig_roi = px.bar(
                            df.sort_values('ROI_Percent', ascending=False),
                            x='Innovation', y='ROI_Percent',
                            title='Return on Investment (ROI %) by Innovation',
                            color='ROI_Percent',
                            color_continuous_scale=[MAC_RED, MAC_YELLOW, MAC_GREEN]
                        )
                        st.plotly_chart(style_chart(fig_roi), use_container_width=True)

                    st.write("")

                    # Charts Section - Row 2: Department Impact & Categories
                    c_col3, c_col4 = st.columns(2)

                    with c_col3:
                        # Net Benefit distribution across the innovation portfolio
                        fig_benefit = px.pie(
                            df, values='Net_Benefit_ZAR', names='Innovation',
                            title='Net Benefit Distribution by Innovation',
                            hole=0.55, color_discrete_sequence=MAC_QUALITATIVE
                        )
                        fig_benefit.update_traces(textfont_size=12, marker=dict(line=dict(color="white", width=2)))
                        st.plotly_chart(style_chart(fig_benefit), use_container_width=True)

                    with c_col4:
                        # Implementation timeline vs ROI, bubble sized by budget
                        fig_scatter = px.scatter(
                            df, x='Implementation_Months', y='ROI_Percent',
                            size='Budget_ZAR', color='Innovation',
                            title='Implementation Timeline vs ROI (bubble size = Budget)',
                            color_discrete_sequence=MAC_QUALITATIVE,
                            size_max=42, hover_data=['Net_Benefit_ZAR']
                        )
                        st.plotly_chart(style_chart(fig_scatter), use_container_width=True)

                    # 4. Master Data Grid
                    st.write("")
                    section_header("🗂️", "teal", "Innovation Portfolio Directory")

                    st.dataframe(
                        df[[
                            'Innovation', 'Budget_ZAR', 'Revenue_Generated_ZAR',
                            'Net_Benefit_ZAR', 'ROI_Percent', 'Implementation_Months',
                            'Benefit-Cost Ratio'
                        ]].style.format({
                            'Budget_ZAR': 'R{:,.2f}',
                            'Revenue_Generated_ZAR': 'R{:,.2f}',
                            'Net_Benefit_ZAR': 'R{:,.2f}',
                            'ROI_Percent': '{:.1f}%',
                            'Implementation_Months': '{:.0f} mo',
                            'Benefit-Cost Ratio': '{:.2f}×'
                        }),
                        use_container_width=True
                    )

    except Exception as e:
        st.error(f"Error reading dataset. Please ensure the uploaded document is valid. Details: {e}")
else:
    # Initial landing screen sidebar hints
    with st.sidebar:
        st.markdown(
            f"""
            <div class="section-header" style="margin-bottom:14px;">
                {app_icon("📘", "teal", "small")}
                <div><h2 style="font-size:16px;">Schema Format Rules</h2></div>
            </div>
            <div class="mac-sidebar-card">
                Your document must include the following precise headers:
                <ul>
                    <li><b>Innovation</b></li>
                    <li><b>Budget_ZAR</b></li>
                    <li><b>Revenue_Generated_ZAR</b></li>
                    <li><b>Net_Benefit_ZAR</b></li>
                    <li><b>ROI_Percent</b></li>
                    <li><b>Implementation_Months</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
