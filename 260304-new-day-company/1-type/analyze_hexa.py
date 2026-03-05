#!/usr/bin/env python3
"""
Hexa Index Daily/Weekly Analysis
Excludes Lunar New Year holiday week: 2026-02-16 ~ 2026-02-20
"""

import json
import math
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

# ── Font setup (Korean support) ─────────────────────────────────────────────
_korean_fonts = [f.name for f in fm.fontManager.ttflist if any(k in f.name for k in ["NanumGothic", "Malgun", "AppleGothic", "UnDotum", "NotoSansCJK", "DejaVu"])]
if _korean_fonts:
    plt.rcParams["font.family"] = _korean_fonts[0]
else:
    plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

# ── Constants ────────────────────────────────────────────────────────────────
HOLIDAY_START = pd.Timestamp("2026-02-16")
HOLIDAY_END   = pd.Timestamp("2026-02-20")
CSV_GLOB      = "dailyWeekHexa_*.csv"
METRICS_JSON  = "hexa-metrics.json"

# ── Load data ────────────────────────────────────────────────────────────────
base = Path(__file__).parent

with open(base / METRICS_JSON, encoding="utf-8") as f:
    metrics_meta = json.load(f)["hexaAdminMap"]

metric_names = {int(k): v["name"] for k, v in metrics_meta.items()}
metric_signs  = {int(k): v["sign"] for k, v in metrics_meta.items()}
# name → sign mapping
name_sign = {v["name"]: v["sign"] for k, v in metrics_meta.items()}

csv_file = sorted(base.glob(CSV_GLOB))[-1]
df_raw = pd.read_csv(csv_file, encoding="utf-8-sig")
df_raw["snapdate"] = pd.to_datetime(df_raw["snapdate"])

# Convert numeric columns
num_cols = [c for c in df_raw.columns if c not in ("GROUP", "snapdate")]
for c in num_cols:
    df_raw[c] = pd.to_numeric(df_raw[c].replace("null", np.nan), errors="coerce")

# Exclude holiday week
holiday_mask = (df_raw["snapdate"] >= HOLIDAY_START) & (df_raw["snapdate"] <= HOLIDAY_END)
df = df_raw[~holiday_mask].copy()

PARTNER = "PARTNER_TOTAL"
ORGS = [g for g in df["GROUP"].unique() if g != PARTNER]
ALL_GROUPS = [PARTNER] + ORGS


def sign_label(col_name: str) -> str:
    """Prefix [+] or [-] based on metric direction."""
    s = name_sign.get(col_name, 1)
    return "[+]" if s == 1 else "[-]"


def fmt(val, decimals=3):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "N/A"
    if isinstance(val, float):
        return f"{val:.{decimals}f}"
    return str(val)


def week_label(dt: pd.Timestamp) -> str:
    return f"W{dt.isocalendar().week:02d}"


# ── Assign ISO week to each row ──────────────────────────────────────────────
df["week"] = df["snapdate"].apply(week_label)
df["year_week"] = df["snapdate"].dt.strftime("%Y-W%V")

# ── Key metrics for summary (a representative subset) ───────────────────────
KEY_METRICS = [
    "인당 상시잔여이슈",
    "이슈 처리일",
    "인당 이슈Inflow(발생)",
    "인당 이슈Outflow(해결)",
    "이슈 처리율(Outflow/Inflow)",
    "인당 코드 변경량",
    "인당 개발산출물Outflow(해결)",
    "개발산출물 처리율 (Outflow/Inflow)",
    "인당 Review수",
    "인당 Reject수",
    "Reject/Review율[리뷰관점]",
    "활성개발자수",
    "이슈 쏠림[내부]",
]
KEY_METRICS = [m for m in KEY_METRICS if m in df.columns]

# ── Helper: latest full week data ─────────────────────────────────────────────
def latest_two_weeks(group: str):
    sub = df[df["GROUP"] == group].sort_values("snapdate")
    weeks = sub["year_week"].unique()
    if len(weeks) < 2:
        return sub, sub
    prev = sub[sub["year_week"] == weeks[-2]]
    curr = sub[sub["year_week"] == weeks[-1]]
    return prev, curr


def weekly_mean(group: str) -> pd.DataFrame:
    sub = df[df["GROUP"] == group][["year_week"] + num_cols]
    return sub.groupby("year_week")[num_cols].mean()


# ════════════════════════════════════════════════════════════════════════════
# Build Markdown report
# ════════════════════════════════════════════════════════════════════════════
lines = []

def h(level: int, text: str):
    lines.append("\n" + "#" * level + " " + text + "\n")

def para(*args):
    lines.append(" ".join(str(a) for a in args))

def nl():
    lines.append("")

def table_header(*cols):
    lines.append("| " + " | ".join(str(c) for c in cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")

def table_row(*cols):
    lines.append("| " + " | ".join(str(c) for c in cols) + " |")


# ── Title ────────────────────────────────────────────────────────────────────
lines.append("# Hexa Index 일단위 분석 보고서")
lines.append(f"\n> 데이터 파일: `{csv_file.name}`  ")
lines.append(f"> 분석 기준일: {df['snapdate'].max().strftime('%Y-%m-%d')}  ")
lines.append(f"> ⚠️ 설 연휴({HOLIDAY_START.strftime('%Y-%m-%d')} ~ {HOLIDAY_END.strftime('%Y-%m-%d')}) 제외  ")
lines.append(f"> 분석 대상 그룹: {', '.join(ALL_GROUPS)}\n")
lines.append("> **지표 방향 표시**: `[+]` 값이 클수록 좋음 / `[-]` 값이 작을수록 좋음\n")
lines.append("---\n")

# ════════════════════════════════════════════════════════════════════════════
# 1. 전체(PARTNER_TOTAL) 주간 요약
# ════════════════════════════════════════════════════════════════════════════
h(2, "1. 전체(PARTNER_TOTAL) 주간 평균 요약")

wm = weekly_mean(PARTNER)
wm_key = wm[KEY_METRICS] if all(m in wm.columns for m in KEY_METRICS) else wm

header_row = ["주차"] + [f"{sign_label(m)} {m}" for m in wm_key.columns]
table_header(*header_row)
for wk, row in wm_key.iterrows():
    table_row(wk, *[fmt(v) for v in row])

# ════════════════════════════════════════════════════════════════════════════
# 2. 최근 2주 전체 비교 (전주 vs 이번주)
# ════════════════════════════════════════════════════════════════════════════
h(2, "2. PARTNER_TOTAL 전주 대비 이번주 변화 (핵심 지표)")

prev_w, curr_w = latest_two_weeks(PARTNER)
prev_mean = prev_w[KEY_METRICS].mean()
curr_mean = curr_w[KEY_METRICS].mean()

table_header("지표", "전주 평균", "이번주 평균", "변화량", "변화율(%)", "방향")
for m in KEY_METRICS:
    pv = prev_mean.get(m, np.nan)
    cv = curr_mean.get(m, np.nan)
    sign = name_sign.get(m, 1)
    if not np.isnan(pv) and not np.isnan(cv) and pv != 0:
        delta = cv - pv
        pct   = delta / abs(pv) * 100
        if sign == 1:
            direction = "🔺 개선" if delta > 0 else ("🔻 악화" if delta < 0 else "→ 동일")
        else:
            direction = "🔺 개선" if delta < 0 else ("🔻 악화" if delta > 0 else "→ 동일")
        table_row(f"{sign_label(m)} {m}", fmt(pv), fmt(cv), fmt(delta), fmt(pct, 1), direction)
    else:
        table_row(f"{sign_label(m)} {m}", fmt(pv), fmt(cv), "N/A", "N/A", "-")

# ════════════════════════════════════════════════════════════════════════════
# 3. 조직별 최신주 비교
# ════════════════════════════════════════════════════════════════════════════
h(2, "3. 조직별 최신주 핵심 지표 비교")

para("각 조직의 최신 데이터 주차 기준 평균값 비교입니다.")
nl()

# Build per-org last week means
org_latest = {}
for g in ALL_GROUPS:
    _, cw = latest_two_weeks(g)
    org_latest[g] = cw[KEY_METRICS].mean() if len(cw) > 0 else pd.Series(dtype=float)

header_cols = ["지표"] + [f"{'★' if g == PARTNER else ''}{g}" for g in ALL_GROUPS]
table_header(*header_cols)
for m in KEY_METRICS:
    row_vals = [f"{sign_label(m)} {m}"]
    for g in ALL_GROUPS:
        row_vals.append(fmt(org_latest[g].get(m, np.nan)))
    table_row(*row_vals)

# ════════════════════════════════════════════════════════════════════════════
# 4. 조직별 전주 대비 변화
# ════════════════════════════════════════════════════════════════════════════
h(2, "4. 조직별 전주 대비 이번주 변화")

for org in ALL_GROUPS:
    h(3, f"4.{ALL_GROUPS.index(org)+1} {org}")
    prev_o, curr_o = latest_two_weeks(org)
    if len(prev_o) == 0 or len(curr_o) == 0:
        para("데이터 부족")
        continue
    pm = prev_o[KEY_METRICS].mean()
    cm = curr_o[KEY_METRICS].mean()
    table_header("지표", "전주", "이번주", "Δ", "방향")
    for m in KEY_METRICS:
        pv = pm.get(m, np.nan)
        cv = cm.get(m, np.nan)
        sign = name_sign.get(m, 1)
        if not np.isnan(pv) and not np.isnan(cv):
            delta = cv - pv
            if sign == 1:
                arrow = "↑ 개선" if delta > 0 else ("↓ 악화" if delta < 0 else "→")
            else:
                arrow = "↑ 개선" if delta < 0 else ("↓ 악화" if delta > 0 else "→")
            table_row(f"{sign_label(m)} {m}", fmt(pv), fmt(cv), fmt(delta), arrow)
        else:
            table_row(f"{sign_label(m)} {m}", fmt(pv), fmt(cv), "N/A", "-")

# ════════════════════════════════════════════════════════════════════════════
# 5. 시계열 분석 (전체 + 조직별)
# ════════════════════════════════════════════════════════════════════════════
h(2, "5. 시계열 분석 (전체 및 조직별)")

para("### 5.1 PARTNER_TOTAL 일별 시계열 추세")
nl()
para("아래는 전체(PARTNER_TOTAL) 핵심 지표의 일별 추이를 나타냅니다.")
nl()

pt_ts = df[df["GROUP"] == PARTNER].sort_values("snapdate")

# Trend stats per metric
h(3, "5.1 PARTNER_TOTAL 핵심 지표 일별 추세 분석")
table_header("지표", "최솟값 날짜", "최솟값", "최댓값 날짜", "최댓값", "전체 평균", "선형추세(기울기)", "해석")
for m in KEY_METRICS:
    s = pt_ts[["snapdate", m]].dropna()
    if len(s) < 3:
        continue
    mn_idx = s[m].idxmin()
    mx_idx = s[m].idxmax()
    mn_date = s.loc[mn_idx, "snapdate"].strftime("%m-%d")
    mx_date = s.loc[mx_idx, "snapdate"].strftime("%m-%d")
    mn_val  = s[m].min()
    mx_val  = s[m].max()
    avg_val = s[m].mean()
    x = np.arange(len(s))
    slope, _, _, p, _ = stats.linregress(x, s[m].values)
    sign = name_sign.get(m, 1)
    if abs(slope) < 1e-6:
        trend_txt = "수평"
    elif sign == 1:
        trend_txt = "📈 개선 추세" if slope > 0 else "📉 악화 추세"
    else:
        trend_txt = "📈 개선 추세" if slope < 0 else "📉 악화 추세"
    pmark = " *" if p < 0.05 else ""
    table_row(f"{sign_label(m)} {m}", mn_date, fmt(mn_val), mx_date, fmt(mx_val),
              fmt(avg_val), f"{slope:+.4f}{pmark}", trend_txt)

nl()
para("> `*` p<0.05 (통계적으로 유의한 선형 추세)")
nl()

# Per-org weekly trend
h(3, "5.2 조직별 주간 평균 추세")
for m in KEY_METRICS[:6]:  # limit to 6 for readability
    h(4, f"{sign_label(m)} {m}")
    # collect weekly means per org
    org_wm = {}
    for g in ALL_GROUPS:
        wm_g = weekly_mean(g)
        if m in wm_g.columns:
            org_wm[g] = wm_g[m]
    all_weeks = sorted(set(w for s in org_wm.values() for w in s.index))
    cols_h = ["주차"] + list(org_wm.keys())
    table_header(*cols_h)
    for wk in all_weeks:
        row = [wk]
        for g in org_wm:
            v = org_wm[g].get(wk, np.nan)
            row.append(fmt(v))
        table_row(*row)
    nl()

# ════════════════════════════════════════════════════════════════════════════
# 6. 상관관계 분석
# ════════════════════════════════════════════════════════════════════════════
h(2, "6. Hexa Index 간 상관관계 분석")

para("PARTNER_TOTAL 일별 데이터 기준으로 핵심 지표 간 Pearson 상관계수를 분석합니다.")
nl()

pt_corr_df = df[df["GROUP"] == PARTNER][KEY_METRICS].dropna(how="all")
corr_matrix = pt_corr_df.corr(method="pearson")

# Print correlation matrix
short_names = {m: m[:12] for m in KEY_METRICS}
h(3, "6.1 Pearson 상관계수 행렬")
header_cols = ["지표"] + [f"{sign_label(m)}{m[:10]}" for m in KEY_METRICS]
table_header(*header_cols)
for m in KEY_METRICS:
    row_vals = [f"{sign_label(m)} {m}"]
    for m2 in KEY_METRICS:
        v = corr_matrix.loc[m, m2] if (m in corr_matrix.index and m2 in corr_matrix.columns) else np.nan
        if np.isnan(v):
            row_vals.append("N/A")
        else:
            row_vals.append(f"{v:.3f}")
    table_row(*row_vals)

# Strong correlations
h(3, "6.2 강한 상관관계 쌍 (|r| ≥ 0.7)")
table_header("지표 A", "지표 B", "상관계수 r", "해석")
pairs_found = False
for i, m1 in enumerate(KEY_METRICS):
    for m2 in KEY_METRICS[i+1:]:
        if m1 not in corr_matrix.index or m2 not in corr_matrix.columns:
            continue
        r = corr_matrix.loc[m1, m2]
        if abs(r) >= 0.7:
            pairs_found = True
            direction = "양(+) 상관" if r > 0 else "음(-) 상관"
            strength = "매우 강함" if abs(r) >= 0.9 else "강함"
            sign_a = name_sign.get(m1, 1)
            sign_b = name_sign.get(m2, 1)
            if sign_a == sign_b:
                interpret = f"두 지표 방향 일치 → {direction} ({strength})"
            else:
                interpret = f"두 지표 방향 반대 → {direction} ({strength})"
            table_row(f"{sign_label(m1)} {m1}", f"{sign_label(m2)} {m2}", f"{r:.3f}", interpret)

if not pairs_found:
    para("강한 상관관계(|r|≥0.7)를 가진 지표 쌍 없음")
nl()

# ════════════════════════════════════════════════════════════════════════════
# 7. 이상값(Outlier) 탐지 분석
# ════════════════════════════════════════════════════════════════════════════
h(2, "7. 이상값(Outlier) 탐지 (IQR 방법)")

para("일별 데이터에서 IQR 1.5배 기준 이상값 발생 날짜를 탐지합니다.")
nl()

pt_ts_sorted = df[df["GROUP"] == PARTNER].sort_values("snapdate")
outlier_summary = {}
for m in KEY_METRICS:
    s = pt_ts_sorted[["snapdate", m]].dropna()
    if len(s) < 5:
        continue
    q1 = s[m].quantile(0.25)
    q3 = s[m].quantile(0.75)
    iqr = q3 - q1
    lo = q1 - 1.5 * iqr
    hi = q3 + 1.5 * iqr
    outliers = s[(s[m] < lo) | (s[m] > hi)]
    if len(outliers):
        outlier_summary[m] = outliers

if outlier_summary:
    table_header("지표", "이상값 날짜", "이상값", "Q1", "Q3", "IQR")
    for m, out_df in outlier_summary.items():
        s = pt_ts_sorted[["snapdate", m]].dropna()
        q1 = s[m].quantile(0.25)
        q3 = s[m].quantile(0.75)
        iqr = q3 - q1
        for _, row in out_df.iterrows():
            table_row(f"{sign_label(m)} {m}", row["snapdate"].strftime("%Y-%m-%d"),
                      fmt(row[m]), fmt(q1), fmt(q3), fmt(iqr))
else:
    para("탐지된 이상값 없음")
nl()

# ════════════════════════════════════════════════════════════════════════════
# 8. 이슈 생산성 지수 (복합 지표)
# ════════════════════════════════════════════════════════════════════════════
h(2, "8. 복합 생산성 지수 분석")

para("이슈 처리 효율성과 코드 생산성을 결합한 복합 지수를 계산합니다.")
nl()

prod_metrics = {
    "이슈처리효율": ["이슈 처리율(Outflow/Inflow)", "인당 이슈Outflow(해결)"],
    "코드생산성": ["인당 코드 변경량", "인당 개발산출물Outflow(해결)"],
    "리뷰활동": ["인당 Review수", "인당 Reject수"],
}

for group in ALL_GROUPS:
    h(3, f"8.{ALL_GROUPS.index(group)+1} {group} 복합 지수")
    sub_g = df[df["GROUP"] == group].sort_values("snapdate")
    for idx_name, mlist in prod_metrics.items():
        mlist_avail = [m for m in mlist if m in sub_g.columns]
        if not mlist_avail:
            continue
        # Normalize each metric 0-1 within its range, then average
        normed = []
        for m in mlist_avail:
            s = sub_g[m].dropna()
            if s.max() == s.min():
                normed.append(pd.Series(0.5, index=sub_g.index))
            else:
                n = (sub_g[m] - s.min()) / (s.max() - s.min())
                if name_sign.get(m, 1) == -1:
                    n = 1 - n  # invert: smaller is better
                normed.append(n)
        composite = pd.concat(normed, axis=1).mean(axis=1)
        sub_g = sub_g.copy()
        sub_g[f"__idx_{idx_name}"] = composite
    
    # Print weekly composite
    sub_g_w = sub_g.copy()
    sub_g_w["year_week"] = sub_g_w["snapdate"].dt.strftime("%Y-W%V")
    idx_cols = [c for c in sub_g_w.columns if c.startswith("__idx_")]
    if idx_cols:
        wg = sub_g_w.groupby("year_week")[idx_cols].mean()
        wg.columns = [c.replace("__idx_", "") for c in wg.columns]
        table_header("주차", *wg.columns)
        for wk, row in wg.iterrows():
            table_row(wk, *[fmt(v) for v in row])
        nl()

# ════════════════════════════════════════════════════════════════════════════
# 9. 주별 Z-Score 분석
# ════════════════════════════════════════════════════════════════════════════
h(2, "9. 주별 Z-Score 분석 (PARTNER_TOTAL)")

para("각 지표의 전체 기간 평균 대비 주별 편차를 Z-Score로 표현합니다.")
nl()

pt_zdf = df[df["GROUP"] == PARTNER].copy()
pt_zdf["year_week"] = pt_zdf["snapdate"].dt.strftime("%Y-W%V")
weekly_z = pt_zdf.groupby("year_week")[KEY_METRICS].mean()

z_scores = (weekly_z - weekly_z.mean()) / weekly_z.std()

header_cols = ["주차"] + [f"{sign_label(m)}{m[:10]}" for m in KEY_METRICS]
table_header(*header_cols)
for wk, row in z_scores.iterrows():
    cells = [wk]
    for m in KEY_METRICS:
        v = row.get(m, np.nan)
        if np.isnan(v):
            cells.append("N/A")
        else:
            # Highlight extreme values
            if abs(v) > 2:
                cells.append(f"**{v:.2f}**")
            else:
                cells.append(f"{v:.2f}")
    table_row(*cells)

nl()
para("> 굵은 값(**x.xx**)은 |Z|>2 로 평균에서 크게 벗어난 주를 의미합니다.")
nl()

# ════════════════════════════════════════════════════════════════════════════
# 10. 종합 인사이트
# ════════════════════════════════════════════════════════════════════════════
h(2, "10. 종합 인사이트 및 권고사항")

# Compute overall trends for insights
insights = []
for m in KEY_METRICS:
    s = pt_ts[["snapdate", m]].dropna()
    if len(s) < 3:
        continue
    x = np.arange(len(s))
    slope, intercept, r, p, _ = stats.linregress(x, s[m].values)
    sign = name_sign.get(m, 1)
    improving = (sign == 1 and slope > 0) or (sign == -1 and slope < 0)
    if p < 0.05:
        insights.append((m, slope, p, improving, "통계 유의"))
    else:
        insights.append((m, slope, p, improving, "추세 미유의"))

good_trends = [(m, sl, p, s) for m, sl, p, b, s in insights if b and p < 0.05]
bad_trends  = [(m, sl, p, s) for m, sl, p, b, s in insights if not b and p < 0.05]

h(3, "10.1 개선 중인 지표 (통계적 유의)")
if good_trends:
    table_header("지표", "기울기", "p-값")
    for m, sl, p, _ in good_trends:
        table_row(f"{sign_label(m)} {m}", f"{sl:+.5f}", f"{p:.4f}")
else:
    para("통계적으로 유의한 개선 추세 지표 없음")

nl()
h(3, "10.2 악화 중인 지표 (통계적 유의)")
if bad_trends:
    table_header("지표", "기울기", "p-값")
    for m, sl, p, _ in bad_trends:
        table_row(f"{sign_label(m)} {m}", f"{sl:+.5f}", f"{p:.4f}")
else:
    para("통계적으로 유의한 악화 추세 지표 없음")

nl()
h(3, "10.3 조직별 종합 평가")
para("최신 주차 기준 PARTNER_TOTAL 대비 각 조직 핵심 지표 상대적 평가입니다.")
nl()

pt_latest_mean = org_latest.get(PARTNER, pd.Series(dtype=float))
table_header("조직", "개선 지표수", "악화 지표수", "평가")
for org in ORGS:
    org_mean = org_latest.get(org, pd.Series(dtype=float))
    better = 0
    worse  = 0
    for m in KEY_METRICS:
        pt_v  = pt_latest_mean.get(m, np.nan)
        org_v = org_mean.get(m, np.nan)
        if np.isnan(pt_v) or np.isnan(org_v):
            continue
        sign = name_sign.get(m, 1)
        diff = org_v - pt_v
        if sign == 1:
            better += 1 if diff > 0 else 0
            worse  += 1 if diff < 0 else 0
        else:
            better += 1 if diff < 0 else 0
            worse  += 1 if diff > 0 else 0
    grade = "🟢 양호" if better > worse else ("🔴 주의" if worse > better * 2 else "🟡 보통")
    table_row(org, better, worse, grade)

nl()

# ── Footer ───────────────────────────────────────────────────────────────────
lines.append("\n---\n")
lines.append(f"*분석 스크립트: `analyze_hexa.py` | 데이터: `{csv_file.name}` | 분석일시: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n")

# ════════════════════════════════════════════════════════════════════════════
# Write output
# ════════════════════════════════════════════════════════════════════════════
out_file = base / "collab_daily.md"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ 분석 완료: {out_file}")
print(f"   - 데이터 범위: {df['snapdate'].min().date()} ~ {df['snapdate'].max().date()}")
print(f"   - 설 연휴 제외: {HOLIDAY_START.date()} ~ {HOLIDAY_END.date()}")
print(f"   - 분석 그룹: {ALL_GROUPS}")
print(f"   - 핵심 지표: {len(KEY_METRICS)}개")
