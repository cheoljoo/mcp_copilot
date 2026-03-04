#!/usr/bin/env python3
"""
Hexa Metrics 주간 분석 스크립트
- 설 연휴(2026-02-16 ~ 2026-02-20) 주 제외
- 전체 분석, 조직별 비교, 시계열 분석, 상관관계 분석
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ─── 경로 설정 ───────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
CSV_FILE = BASE / "weeklyWeekHexa_202603041516.csv"
JSON_FILE = BASE / "hexa-metrics.json"
OUTPUT_MD = BASE / "collab_weekly.md"

# ─── 데이터 로드 ──────────────────────────────────────────────────────────────
with open(JSON_FILE) as f:
    hexa_meta = json.load(f)["hexaAdminMap"]

# 지표 이름 → sign 매핑
metric_sign = {v["name"]: v["sign"] for v in hexa_meta.values()}

df_raw = pd.read_csv(CSV_FILE)
df_raw["snapdate"] = pd.to_datetime(df_raw["snapdate"])

# 설 연휴 주 제외 (2026-02-16 시작 주)
LUNAR_WEEK = pd.Timestamp("2026-02-16")
df = df_raw[df_raw["snapdate"] != LUNAR_WEEK].copy()

# 숫자형 컬럼 (GROUP, snapdate 제외)
metric_cols = [c for c in df.columns if c not in ("GROUP", "snapdate")]

# null 문자열 → NaN
for c in metric_cols:
    df[c] = pd.to_numeric(df[c].astype(str).replace("null", float("nan")), errors="coerce")

# GROUP 분리
PARTNER_TOTAL = "PARTNER_TOTAL"
ORGS = ["EDV자사", "LGSI자사", "국내자사", "협력사전체"]
ALL_GROUPS = [PARTNER_TOTAL] + ORGS

df_total = df[df["GROUP"] == PARTNER_TOTAL].sort_values("snapdate").reset_index(drop=True)
df_org = {org: df[df["GROUP"] == org].sort_values("snapdate").reset_index(drop=True) for org in ORGS}

# 최신 주, 이전 주
latest_date = df_total["snapdate"].max()
prev_date = df_total[df_total["snapdate"] < latest_date]["snapdate"].max()

# ─── 헬퍼 함수 ───────────────────────────────────────────────────────────────
def sign_label(metric_name: str) -> str:
    s = metric_sign.get(metric_name, 1)
    return "[+]" if s == 1 else "[-]"


def fmt_val(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"{v:.3f}"


def trend_symbol(delta, sign):
    """delta > 0 이고 sign=1 → 개선(▲), delta < 0 이고 sign=-1 → 개선(▼)"""
    if delta is None or (isinstance(delta, float) and np.isnan(delta)):
        return "➖"
    if sign == 1:
        return "▲ 개선" if delta > 0 else ("▼ 악화" if delta < 0 else "➖")
    else:
        return "▼ 개선" if delta < 0 else ("▲ 악화" if delta > 0 else "➖")


def get_row(dframe, date, col):
    row = dframe[dframe["snapdate"] == date]
    if row.empty:
        return float("nan")
    return row[col].values[0]


# ─── 분석 결과를 리스트로 누적 ────────────────────────────────────────────────
lines = []

def h(level: int, text: str):
    lines.append("\n" + "#" * level + " " + text + "\n")

def p(text: str = ""):
    lines.append(text)

def table_row(*cols):
    lines.append("| " + " | ".join(str(c) for c in cols) + " |")

def table_sep(*aligns):
    lines.append("| " + " | ".join(aligns) + " |")


# ═══════════════════════════════════════════════════════════════════════════════
h(1, "📊 Hexa Index 주간 분석 보고서")
p(f"> **분석 기준일**: {latest_date.strftime('%Y-%m-%d')} (최신 주)")
p(f"> **분석 기간**: {df_total['snapdate'].min().strftime('%Y-%m-%d')} ~ {latest_date.strftime('%Y-%m-%d')} ({len(df_total)}주)")
p(f"> **설 연휴 제외**: 2026-02-16 ~ 2026-02-20 (해당 주 데이터 분석에서 제외)")
p(f"> **지표 표기**: [+] 값이 높을수록 좋음 / [-] 값이 낮을수록 좋음")
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "1. 전체(PARTNER_TOTAL) 분석")

h(2, "1.1 최신 주 핵심 지표 요약 (전주 대비)")
p("최신 주와 전주 데이터를 비교하여 주요 지표 변화를 분석합니다.\n")

KEY_METRICS = [
    "인당 프로젝트수", "인당 상시잔여이슈", "이슈 처리일",
    "인당 이슈Inflow(발생)", "인당 이슈Outflow(해결)",
    "인당 코드 변경량", "인당 개발산출물Outflow(해결)",
    "이슈 처리율(Outflow/Inflow)", "개발산출물 처리율 (Outflow/Inflow)",
    "활성개발자수", "이슈 최초대응일", "완료이슈 Reopen율",
    "Reject/Review율[리뷰관점]", "인당 Review수",
]

table_row("지표명", f"전주({prev_date.strftime('%m/%d')})", f"최신({latest_date.strftime('%m/%d')})", "변화량", "방향")
table_sep("---", "---:", "---:", "---:", "---")
for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    prev_v = get_row(df_total, prev_date, m)
    curr_v = get_row(df_total, latest_date, m)
    if np.isnan(prev_v) or np.isnan(curr_v):
        continue
    delta = curr_v - prev_v
    table_row(f"{sign_label(m)} {m}", fmt_val(prev_v), fmt_val(curr_v), f"{delta:+.3f}", trend_symbol(delta, s))
p()

h(2, "1.2 전체 기간 통계 요약")
p("분석 기간 동안의 기술통계량입니다.\n")

stats_cols = KEY_METRICS
table_row("지표명", "평균", "표준편차", "최솟값", "최댓값", "최근 추세")
table_sep("---", "---:", "---:", "---:", "---:", "---")
for m in stats_cols:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    series = df_total[m].dropna()
    if len(series) < 2:
        continue
    mean_v = series.mean()
    std_v = series.std()
    min_v = series.min()
    max_v = series.max()
    # 최근 4주 기울기
    recent = series.tail(4)
    if len(recent) >= 2:
        slope, _, _, _, _ = stats.linregress(range(len(recent)), recent)
        trend = "↗ 상승" if slope > 0 else "↘ 하락"
    else:
        trend = "-"
    table_row(f"{sign_label(m)} {m}", fmt_val(mean_v), fmt_val(std_v), fmt_val(min_v), fmt_val(max_v), trend)
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "2. 조직별 비교 분석")

h(2, "2.1 최신 주 조직별 현황 비교 (전체 평균 기준)")
p(f"최신 주({latest_date.strftime('%Y-%m-%d')}) 기준 각 조직의 지표 값을 전체(PARTNER_TOTAL)와 비교합니다.\n")

for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    total_v = get_row(df_total, latest_date, m)
    if np.isnan(total_v):
        continue
    p(f"#### {sign_label(m)} {m}")
    table_row("조직", "값", "전체 대비", "평가")
    table_sep("---", "---:", "---:", "---")
    table_row("PARTNER_TOTAL (기준)", fmt_val(total_v), "—", "—")
    for org in ORGS:
        dfo = df_org[org]
        org_v = get_row(dfo, latest_date, m)
        if np.isnan(org_v):
            table_row(org, "N/A", "N/A", "N/A")
            continue
        diff = org_v - total_v
        if s == 1:
            eval_str = "✅ 우수" if diff > 0 else ("⚠️ 미흡" if diff < 0 else "➖ 동일")
        else:
            eval_str = "✅ 우수" if diff < 0 else ("⚠️ 미흡" if diff > 0 else "➖ 동일")
        table_row(org, fmt_val(org_v), f"{diff:+.3f}", eval_str)
    p()

h(2, "2.2 조직별 전주 대비 변화")
p(f"각 조직의 최신 주({latest_date.strftime('%m/%d')})와 전주({prev_date.strftime('%m/%d')}) 대비 변화입니다.\n")

table_row("조직", "지표명", f"전주({prev_date.strftime('%m/%d')})", f"최신({latest_date.strftime('%m/%d')})", "변화", "방향")
table_sep("---", "---", "---:", "---:", "---:", "---")
for org in ORGS:
    dfo = df_org[org]
    for m in KEY_METRICS:
        if m not in dfo.columns:
            continue
        s = metric_sign.get(m, 1)
        prev_v = get_row(dfo, prev_date, m)
        curr_v = get_row(dfo, latest_date, m)
        if np.isnan(prev_v) or np.isnan(curr_v):
            continue
        delta = curr_v - prev_v
        table_row(org, f"{sign_label(m)} {m}", fmt_val(prev_v), fmt_val(curr_v), f"{delta:+.3f}", trend_symbol(delta, s))
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "3. 시계열 분석")

h(2, "3.1 전체(PARTNER_TOTAL) 시계열 추세")
p("분석 기간 전체에 걸친 핵심 지표의 주별 추세와 회귀 기울기입니다.\n")

table_row("지표명", "기울기(주당)", "추세", "추세 통계적 유의성(p<0.05)")
table_sep("---", "---:", "---:", "---")
for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    series = df_total[m].dropna()
    if len(series) < 3:
        continue
    x = np.arange(len(series))
    slope, intercept, r, p_val, se = stats.linregress(x, series)
    trend_dir = "↗ 상승" if slope > 0 else "↘ 하락"
    sig = "✅ 유의" if p_val < 0.05 else "—"
    # 좋은/나쁜 추세 표시
    if (s == 1 and slope > 0) or (s == -1 and slope < 0):
        trend_eval = f"🟢 {trend_dir}"
    else:
        trend_eval = f"🔴 {trend_dir}"
    table_row(f"{sign_label(m)} {m}", f"{slope:+.4f}", trend_eval, sig)
p()

h(2, "3.2 조직별 시계열 추세 (전체 기간)")
p("각 조직별 핵심 지표의 장기 추세입니다.\n")

for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    p(f"#### {sign_label(m)} {m}")
    table_row("조직", "기울기(주당)", "추세 평가", "p-value")
    table_sep("---", "---:", "---:", "---:")

    # 전체
    series = df_total[m].dropna()
    if len(series) >= 3:
        x = np.arange(len(series))
        slope, _, _, p_val, _ = stats.linregress(x, series)
        trend_dir = "↗ 상승" if slope > 0 else "↘ 하락"
        if (s == 1 and slope > 0) or (s == -1 and slope < 0):
            eval_str = f"🟢 {trend_dir}"
        else:
            eval_str = f"🔴 {trend_dir}"
        table_row("PARTNER_TOTAL", f"{slope:+.4f}", eval_str, f"{p_val:.4f}")

    for org in ORGS:
        dfo = df_org[org]
        if m not in dfo.columns:
            continue
        series = dfo[m].dropna()
        if len(series) < 3:
            continue
        x = np.arange(len(series))
        slope, _, _, p_val, _ = stats.linregress(x, series)
        trend_dir = "↗ 상승" if slope > 0 else "↘ 하락"
        if (s == 1 and slope > 0) or (s == -1 and slope < 0):
            eval_str = f"🟢 {trend_dir}"
        else:
            eval_str = f"🔴 {trend_dir}"
        table_row(org, f"{slope:+.4f}", eval_str, f"{p_val:.4f}")
    p()

h(2, "3.3 이동평균 기반 최근 변화율 분석 (4주 이동평균)")
p("최근 4주 이동평균과 이전 4주 이동평균을 비교하여 단기 추세를 파악합니다.\n")

table_row("지표명", "이전 4주 평균", "최근 4주 평균", "변화율(%)", "단기 추세")
table_sep("---", "---:", "---:", "---:", "---")
for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    s = metric_sign.get(m, 1)
    series = df_total[m].dropna()
    if len(series) < 8:
        continue
    recent4 = series.tail(4).mean()
    prev4 = series.iloc[-8:-4].mean()
    if prev4 == 0:
        continue
    chg_pct = (recent4 - prev4) / abs(prev4) * 100
    if (s == 1 and chg_pct > 0) or (s == -1 and chg_pct < 0):
        eval_str = f"🟢 개선 ({chg_pct:+.1f}%)"
    else:
        eval_str = f"🔴 악화 ({chg_pct:+.1f}%)"
    table_row(f"{sign_label(m)} {m}", fmt_val(prev4), fmt_val(recent4), f"{chg_pct:+.1f}", eval_str)
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "4. Hexa Index 간 상관관계 분석")
p("각 지표 간 Pearson 상관계수를 계산하여 강한 상관관계(|r| ≥ 0.7)를 가진 지표 쌍을 분석합니다.\n")

h(2, "4.1 강한 양의 상관관계 지표 쌍 (r ≥ 0.7)")
p("전체(PARTNER_TOTAL) 기준, 함께 증가하는 경향이 있는 지표 쌍입니다.\n")

# 상관분석용 컬럼 (결측치 적은 것만)
corr_cols = [c for c in metric_cols if df_total[c].notna().sum() >= int(len(df_total) * 0.5)]
corr_matrix = df_total[corr_cols].corr(method="pearson")

pos_pairs = []
neg_pairs = []
for i, c1 in enumerate(corr_cols):
    for j, c2 in enumerate(corr_cols):
        if j <= i:
            continue
        r = corr_matrix.loc[c1, c2]
        if np.isnan(r):
            continue
        if r >= 0.7:
            pos_pairs.append((c1, c2, r))
        elif r <= -0.7:
            neg_pairs.append((c1, c2, r))

pos_pairs.sort(key=lambda x: -x[2])
neg_pairs.sort(key=lambda x: x[2])

table_row("지표 A", "지표 B", "상관계수(r)", "해석")
table_sep("---", "---", "---:", "---")
for c1, c2, r in pos_pairs[:20]:
    table_row(f"{sign_label(c1)} {c1}", f"{sign_label(c2)} {c2}", f"{r:.3f}", "함께 증가하는 경향")
p()

h(2, "4.2 강한 음의 상관관계 지표 쌍 (r ≤ -0.7)")
p("전체(PARTNER_TOTAL) 기준, 반대 방향으로 움직이는 경향이 있는 지표 쌍입니다.\n")

table_row("지표 A", "지표 B", "상관계수(r)", "해석")
table_sep("---", "---", "---:", "---")
for c1, c2, r in neg_pairs[:20]:
    table_row(f"{sign_label(c1)} {c1}", f"{sign_label(c2)} {c2}", f"{r:.3f}", "반대 방향으로 움직이는 경향")
p()

h(2, "4.3 주요 지표 간 인과 관계 해석")
p("강한 상관관계를 바탕으로 도출된 주요 인사이트입니다.\n")

# 의미 있는 상관쌍 직접 분석
interesting_pairs = [
    ("인당 이슈Inflow(발생)", "인당 상시잔여이슈"),
    ("인당 이슈Outflow(해결)", "이슈 처리율(Outflow/Inflow)"),
    ("인당 코드 변경량", "인당 이슈Outflow(해결)"),
    ("활성개발자수", "이슈Outflow(해결)"),
    ("인당 Review수", "Reject/Review율[리뷰관점]"),
]
for c1, c2 in interesting_pairs:
    if c1 not in corr_cols or c2 not in corr_cols:
        continue
    r = corr_matrix.loc[c1, c2] if c1 in corr_matrix.index and c2 in corr_matrix.columns else float("nan")
    if np.isnan(r):
        continue
    p(f"- **{sign_label(c1)} {c1}** ↔ **{sign_label(c2)} {c2}**: r={r:.3f}")
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "5. 추가 분석 (Confluence 미포함 독자 분석)")

h(2, "5.1 지표 이상값(Outlier) 탐지 — Z-Score 기반")
p("전체(PARTNER_TOTAL) 최신 주 지표 중 Z-Score가 ±2 이상인 항목을 탐지합니다.\n")

table_row("지표명", "최신값", "Z-Score", "판정")
table_sep("---", "---:", "---:", "---")
for m in metric_cols:
    if m not in df_total.columns:
        continue
    series = df_total[m].dropna()
    if len(series) < 4:
        continue
    curr_v = get_row(df_total, latest_date, m)
    if np.isnan(curr_v):
        continue
    z = (curr_v - series.mean()) / (series.std() + 1e-9)
    if abs(z) >= 2.0:
        flag = "🔴 이상값 (낮음)" if z < -2 else "🟡 이상값 (높음)"
        table_row(f"{sign_label(m)} {m}", fmt_val(curr_v), f"{z:.2f}", flag)
p()

h(2, "5.2 조직별 성과 순위 (최신 주)")
p("핵심 지표를 기반으로 조직 성과를 점수화합니다.\n방향(sign)에 따라 정규화 후 합산합니다.\n")

score_metrics = [m for m in KEY_METRICS if m in df_total.columns]
org_scores = {}
for org in ORGS:
    dfo = df_org[org]
    score = 0
    cnt = 0
    for m in score_metrics:
        if m not in dfo.columns:
            continue
        val = get_row(dfo, latest_date, m)
        all_vals = df[df["GROUP"].isin(ORGS)][m].dropna()
        if np.isnan(val) or len(all_vals) < 2:
            continue
        s = metric_sign.get(m, 1)
        v_min, v_max = all_vals.min(), all_vals.max()
        if v_max == v_min:
            continue
        normalized = (val - v_min) / (v_max - v_min)
        score += normalized if s == 1 else (1 - normalized)
        cnt += 1
    org_scores[org] = score / cnt if cnt > 0 else float("nan")

sorted_orgs = sorted(org_scores.items(), key=lambda x: (x[1] if not np.isnan(x[1]) else -999), reverse=True)

table_row("순위", "조직", "종합 점수 (0~1)", "평가")
table_sep("---", "---", "---:", "---")
medals = ["🥇", "🥈", "🥉", "4️⃣"]
for rank, (org, score) in enumerate(sorted_orgs):
    eval_str = "우수" if score >= 0.6 else ("보통" if score >= 0.4 else "개선 필요")
    table_row(f"{medals[rank]} {rank+1}", org, fmt_val(score), eval_str)
p()

h(2, "5.3 변동성 분석 — 지표 안정성 평가 (CV)")
p("변동계수(CV = 표준편차/평균)로 각 조직의 지표 안정성을 평가합니다.\nCV가 낮을수록 안정적입니다.\n")

table_row("조직", "지표명", "평균", "표준편차", "CV(%)", "안정성")
table_sep("---", "---", "---:", "---:", "---:", "---")
for org in [PARTNER_TOTAL] + ORGS:
    dfo = df_total if org == PARTNER_TOTAL else df_org[org]
    for m in KEY_METRICS[:6]:
        if m not in dfo.columns:
            continue
        series = dfo[m].dropna()
        if len(series) < 3 or series.mean() == 0:
            continue
        mean_v = series.mean()
        std_v = series.std()
        cv = abs(std_v / mean_v) * 100
        stability = "🟢 안정" if cv < 15 else ("🟡 보통" if cv < 30 else "🔴 불안정")
        table_row(org, f"{sign_label(m)} {m}", fmt_val(mean_v), fmt_val(std_v), f"{cv:.1f}", stability)
p()

h(2, "5.4 계절성 분석 — 월별 평균 패턴")
p("월별 평균 값을 통해 특정 월에 반복되는 패턴을 분석합니다.\n")

df_total["month"] = df_total["snapdate"].dt.month
for m in ["인당 이슈Inflow(발생)", "인당 이슈Outflow(해결)", "인당 코드 변경량"]:
    if m not in df_total.columns:
        continue
    monthly = df_total.groupby("month")[m].mean()
    p(f"**{sign_label(m)} {m}** 월별 평균:")
    row_vals = [f"{mo}월: {fmt_val(v)}" for mo, v in monthly.items()]
    p("  " + " | ".join(row_vals))
p()

h(2, "5.5 조직 간 갭 분석 (최신 주)")
p("최신 주 기준 조직 간 최댓값과 최솟값의 차이(Gap)를 분석합니다.\n")

table_row("지표명", "최고 조직", "최저 조직", "Gap", "Gap비율(%)")
table_sep("---", "---", "---", "---:", "---:")
for m in KEY_METRICS:
    if m not in df_total.columns:
        continue
    org_vals = {}
    for org in ORGS:
        v = get_row(df_org[org], latest_date, m)
        if not np.isnan(v):
            org_vals[org] = v
    if len(org_vals) < 2:
        continue
    s = metric_sign.get(m, 1)
    if s == 1:
        best_org = max(org_vals, key=lambda k: org_vals[k])
        worst_org = min(org_vals, key=lambda k: org_vals[k])
    else:
        best_org = min(org_vals, key=lambda k: org_vals[k])
        worst_org = max(org_vals, key=lambda k: org_vals[k])
    gap = abs(org_vals[best_org] - org_vals[worst_org])
    total_v = get_row(df_total, latest_date, m)
    gap_pct = abs(gap / total_v * 100) if total_v and total_v != 0 else float("nan")
    table_row(
        f"{sign_label(m)} {m}",
        f"{best_org} ({fmt_val(org_vals[best_org])})",
        f"{worst_org} ({fmt_val(org_vals[worst_org])})",
        fmt_val(gap),
        f"{gap_pct:.1f}" if not np.isnan(gap_pct) else "N/A"
    )
p()

# ═══════════════════════════════════════════════════════════════════════════════
h(1, "6. 전체 주간 데이터 (PARTNER_TOTAL — 핵심 지표)")
p("분석에 사용된 원본 시계열 데이터입니다.\n")

display_metrics = KEY_METRICS[:8]
header = ["주(snapdate)"] + [f"{sign_label(m)} {m}" for m in display_metrics if m in df_total.columns]
table_row(*header)
table_sep(*["---:"] * len(header))
for _, row in df_total.iterrows():
    vals = [row["snapdate"].strftime("%Y-%m-%d")]
    for m in display_metrics:
        if m not in df_total.columns:
            continue
        vals.append(fmt_val(row[m]))
    table_row(*vals)
p()

# ─── 파일 쓰기 ────────────────────────────────────────────────────────────────
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ 분석 완료: {OUTPUT_MD}")
print(f"   총 {len(lines)}줄 생성")
