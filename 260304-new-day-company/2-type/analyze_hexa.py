#!/usr/bin/env python3
"""
Hexa Metrics 종합 분석 스크립트
설 연휴(2/16~2/20) 해당 주 제외
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────
# 0. 데이터 로드
# ─────────────────────────────────────────────────
with open("hexa-metrics.json", encoding="utf-8") as f:
    metrics_meta = json.load(f)["hexaAdminMap"]

# sign 맵 {지표명: +1/-1}
sign_map = {v["name"]: v["sign"] for v in metrics_meta.values()}

df = pd.read_csv("dailyWeekHexa_202603041519.csv", encoding="utf-8-sig")
df["snapdate"] = pd.to_datetime(df["snapdate"])

# 주번호 (ISO week)
df["week"] = df["snapdate"].dt.isocalendar().week.astype(int)
df["year"] = df["snapdate"].dt.isocalendar().year.astype(int)
df["yearweek"] = df["year"].astype(str) + "-W" + df["week"].astype(str).str.zfill(2)

# 설 연휴 포함 주 제외: 2026년 W08 (2/16~2/20 포함)
EXCLUDED_YEARWEEKS = {"2026-W08"}
df_clean = df[~df["yearweek"].isin(EXCLUDED_YEARWEEKS)].copy()

# 주간 데이터: 각 주의 마지막 날짜 기준 (스냅샷)
# PARTNER_TOTAL vs 조직들
groups_org = ["EDV자사", "LGSI자사", "국내자사", "협력사전체"]
all_groups = ["PARTNER_TOTAL"] + groups_org

# 수치 컬럼 목록
metric_cols = [c for c in df.columns if c not in ["GROUP", "snapdate", "week", "year", "yearweek"]]

# null 처리
for c in metric_cols:
    df_clean[c] = pd.to_numeric(df_clean[c], errors="coerce")

# [+]/[-] 접두사 함수
def prefix(col):
    s = sign_map.get(col, 1)
    return "[+]" if s == 1 else "[-]"

def metric_label(col):
    return f"{prefix(col)} {col}"

# ─────────────────────────────────────────────────
# 1. 주간 집계: 각 주 마지막 스냅샷 기준
# ─────────────────────────────────────────────────
# 주별로 마지막 날짜 행 선택
weekly = (
    df_clean.sort_values("snapdate")
    .groupby(["GROUP", "yearweek"])
    .last()
    .reset_index()
)

weekly_sorted = weekly.sort_values(["GROUP", "snapdate"])

# 전체(PARTNER_TOTAL) 주간 데이터
wk_total = weekly_sorted[weekly_sorted["GROUP"] == "PARTNER_TOTAL"].copy().reset_index(drop=True)
weeks_all = wk_total["yearweek"].tolist()

# ─────────────────────────────────────────────────
# 헬퍼 함수들
# ─────────────────────────────────────────────────

def trend_analysis(series, label=""):
    """시계열 선형 회귀 → slope, p-value, 방향 판정"""
    s = series.dropna()
    if len(s) < 3:
        return None
    x = np.arange(len(s))
    slope, intercept, r, p, se = stats.linregress(x, s.values)
    return {"slope": slope, "p_value": p, "n": len(s)}

def week_over_week_change(df_grp, col):
    """전주 대비 변화"""
    vals = df_grp[col].values
    if len(vals) < 2:
        return np.nan, np.nan
    curr = vals[-1]
    prev = vals[-2]
    if pd.isna(curr) or pd.isna(prev) or prev == 0:
        return np.nan, np.nan
    chg = curr - prev
    pct = (chg / abs(prev)) * 100
    return chg, pct

def score_unit(direction_ok, p_value, ALPHA=0.05):
    """
    악화(유의) = -5, 악화(비유의) = -3
    개선(비유의) = +1, 개선(유의) = +2
    direction_ok: True=개선, False=악화
    """
    sig = p_value < ALPHA
    if direction_ok:
        return 2 if sig else 1
    else:
        return -5 if sig else -3

def improvement_flag(chg, sign, p=None, ALPHA=0.05):
    """방향 판정 문자열"""
    if pd.isna(chg):
        return "N/A"
    improved = (chg * sign) > 0
    if p is not None:
        sig = p < ALPHA
        if improved:
            return "✅ 개선(유의)" if sig else "🔵 개선(비유의)"
        else:
            return "🔴 악화(유의)" if sig else "⚠️ 악화(비유의)"
    else:
        return "✅ 개선" if improved else "⚠️ 악화"

# ─────────────────────────────────────────────────
# 2. 보고서 생성
# ─────────────────────────────────────────────────

lines = []
def h(s): lines.append(s)
def br(): lines.append("")

h("# Hexa Index 종합 분석 보고서")
h("")
h(f"**분석 기간**: {df_clean['snapdate'].min().date()} ~ {df_clean['snapdate'].max().date()}")
h(f"**설 연휴 제외**: 2026년 W08 (2/16~2/20 포함 주)")
h(f"**데이터 파일**: dailyWeekHexa_202603041519.csv")
h("")
h("---")
h("")

# ═══════════════════════════════════════════
# 범례
# ═══════════════════════════════════════════
h("## 📌 범례 및 분석 방법 설명")
br()
h("### 지표 방향 표시")
h("| 기호 | 의미 |")
h("|------|------|")
h("| **[+]** | 값이 클수록 좋은 지표 (예: 인당 Commit수, 처리율 등) |")
h("| **[-]** | 값이 작을수록 좋은 지표 (예: 이슈 처리일, 잔여이슈수 등) |")
br()
h("### 개선/악화 판정 기호")
h("| 기호 | 의미 |")
h("|------|------|")
h("| ✅ 개선(유의) | 방향 개선 + 통계적 유의 (p < 0.05) |")
h("| 🔵 개선(비유의) | 방향 개선 + 통계적 비유의 (p ≥ 0.05) |")
h("| ⚠️ 악화(비유의) | 방향 악화 + 통계적 비유의 (p ≥ 0.05) |")
h("| 🔴 악화(유의) | 방향 악화 + 통계적 유의 (p < 0.05) |")
br()
h("### p-value 설명")
h("> **p-value**는 귀무가설(추세가 없다)이 참일 때 현재 데이터가 나올 확률입니다.")
h("> - **유의 기준**: p < 0.05 (5% 수준) → 추세가 통계적으로 의미 있음")
h("> - **비유의**: p ≥ 0.05 → 추세가 우연에 의한 것일 가능성 높음")
br()
h("### slope(기울기) 설명")
h("> **slope**는 시계열 선형 회귀에서 **단위 주(week)당 지표값의 평균 변화량**을 의미합니다.")
h("> - slope > 0: 시간이 지남에 따라 지표값이 **증가** 추세")
h("> - slope < 0: 시간이 지남에 따라 지표값이 **감소** 추세")
h("> - [+] 지표에서 slope > 0이면 개선 추세, slope < 0이면 악화 추세")
h("> - [-] 지표에서 slope < 0이면 개선 추세, slope > 0이면 악화 추세")
h("> - |slope| 값이 클수록 변화 속도가 빠름")
br()
h("### UNIT 건강도 점수 계산 방식")
h("> **점수화 기준**: 전주 대비 변화 방향 + 선형 회귀 p-value (유의성)")
h("> ")
h("> | 상태 | 점수 |")
h("> |------|------|")
h("> | 악화(유의): 방향 악화 + p < 0.05 | **-5점** |")
h("> | 악화(비유의): 방향 악화 + p ≥ 0.05 | **-3점** |")
h("> | 개선(비유의): 방향 개선 + p ≥ 0.05 | **+1점** |")
h("> | 개선(유의): 방향 개선 + p < 0.05 | **+2점** |")
h("> ")
h("> **종합 건강도 점수 = Σ(각 지표별 점수) / 유효지표수 × 10** (표준화)")
h("> - 각 지표에 대해 시계열 기울기(slope)의 방향과 p-value를 계산하여 위 기준으로 점수 부여")
h("> - 점수가 높을수록 건강한 상태, 낮을수록 개선 필요")
br()
h("---")
br()

# ═══════════════════════════════════════════
# 섹션 1: 전체(PARTNER_TOTAL) 현황
# ═══════════════════════════════════════════
h("## 1. 전체(PARTNER_TOTAL) 최신 현황")
br()

latest_total = wk_total.iloc[-1]
prev_total = wk_total.iloc[-2] if len(wk_total) >= 2 else None
latest_week = latest_total["yearweek"]

h(f"**최신 분석 주차**: {latest_week} ({latest_total['snapdate'].date()})")
br()

# 핵심 지표 테이블
KEY_METRICS_IDS = [2, 3, 5, 7, 8, 16, 17, 19, 27, 35]
key_names = [metrics_meta[str(i)]["name"] for i in KEY_METRICS_IDS if str(i) in metrics_meta]
key_names = [n for n in key_names if n in metric_cols]

h("### 1.1 핵심 지표 전주 대비 변화")
br()
h("| 지표 | 전주값 | 이번주값 | 변화량 | 변화율 | 판정 |")
h("|------|--------|---------|--------|--------|------|")

for col in key_names:
    if col not in wk_total.columns:
        continue
    s = sign_map.get(col, 1)
    chg, pct = week_over_week_change(wk_total, col)
    curr_val = latest_total.get(col, np.nan)
    prev_val = prev_total.get(col, np.nan) if prev_total is not None else np.nan
    flag = improvement_flag(chg, s)
    lbl = metric_label(col)
    cv = f"{curr_val:.3f}" if not pd.isna(curr_val) else "N/A"
    pv = f"{prev_val:.3f}" if not pd.isna(prev_val) else "N/A"
    cg = f"{chg:+.3f}" if not pd.isna(chg) else "N/A"
    pg = f"{pct:+.1f}%" if not pd.isna(pct) else "N/A"
    h(f"| {lbl} | {pv} | {cv} | {cg} | {pg} | {flag} |")

br()

# ═══════════════════════════════════════════
# 섹션 2: 전체 시계열 분석 (주간)
# ═══════════════════════════════════════════
h("## 2. 전체(PARTNER_TOTAL) 시계열 분석")
br()
h("> **slope**: 주당 평균 변화량 | **p-value**: 0.05 미만이면 유의한 추세")
br()

# 주요 지표들 (너무 많으면 핵심만)
TREND_METRIC_IDS = list(range(1, 36))  # 1~35번
trend_names = [metrics_meta[str(i)]["name"] for i in TREND_METRIC_IDS
               if str(i) in metrics_meta and metrics_meta[str(i)]["name"] in metric_cols]

h("### 2.1 핵심 지표 시계열 추세 (선형 회귀)")
br()
h("| 지표 | slope | p-value | 유의성 | 추세 판정 |")
h("|------|-------|---------|--------|----------|")

trend_rows = []
for col in trend_names:
    if col not in wk_total.columns:
        continue
    s = sign_map.get(col, 1)
    res = trend_analysis(wk_total[col])
    if res is None:
        continue
    slope = res["slope"]
    p = res["p_value"]
    sig_str = "✅ 유의" if p < 0.05 else "비유의"
    # 방향 판정: slope*sign > 0 이면 좋은 방향
    direction_ok = (slope * s) > 0
    flag = improvement_flag(slope, s, p)
    trend_rows.append((col, slope, p, flag))
    h(f"| {metric_label(col)} | {slope:+.4f} | {p:.4f} | {sig_str} | {flag} |")

br()

# 악화 유의 지표 강조
bad_sig = [(c, sl, p, fl) for c, sl, p, fl in trend_rows if "악화(유의)" in fl]
if bad_sig:
    h("### ⚠️ 2.2 악화 추세 (유의) 지표 목록")
    br()
    h("| 지표 | slope | p-value |")
    h("|------|-------|---------|")
    for c, sl, p, fl in bad_sig:
        h(f"| {metric_label(c)} | {sl:+.4f} | {p:.4f} |")
    br()

good_sig = [(c, sl, p, fl) for c, sl, p, fl in trend_rows if "개선(유의)" in fl]
if good_sig:
    h("### ✅ 2.3 개선 추세 (유의) 지표 목록")
    br()
    h("| 지표 | slope | p-value |")
    h("|------|-------|---------|")
    for c, sl, p, fl in good_sig:
        h(f"| {metric_label(c)} | {sl:+.4f} | {p:.4f} |")
    br()

# ═══════════════════════════════════════════
# 섹션 3: 조직별 비교 분석
# ═══════════════════════════════════════════
h("## 3. 조직별 비교 분석")
br()

# 3.1 조직별 최신 주차 현황 vs PARTNER_TOTAL
h("### 3.1 조직별 vs 전체(PARTNER_TOTAL) 비교 (최신 주차)")
br()

org_data = {}
for grp in groups_org:
    wk_g = weekly_sorted[weekly_sorted["GROUP"] == grp].sort_values("snapdate").reset_index(drop=True)
    org_data[grp] = wk_g

# 최신 주차: 각 조직의 마지막 스냅
total_latest = wk_total.iloc[-1]

for col in key_names:
    if col not in metric_cols:
        continue
    s = sign_map.get(col, 1)
    h(f"#### {metric_label(col)}")
    h("| 조직 | 최신값 | 전체(기준) | 차이 | 전체대비 판정 |")
    h("|------|--------|-----------|------|--------------|")
    base_val = total_latest.get(col, np.nan)
    for grp in groups_org:
        wk_g = org_data[grp]
        if len(wk_g) == 0:
            continue
        gv = wk_g.iloc[-1].get(col, np.nan)
        diff = gv - base_val if not pd.isna(gv) and not pd.isna(base_val) else np.nan
        flag = improvement_flag(diff, s)
        gv_s = f"{gv:.3f}" if not pd.isna(gv) else "N/A"
        bv_s = f"{base_val:.3f}" if not pd.isna(base_val) else "N/A"
        diff_s = f"{diff:+.3f}" if not pd.isna(diff) else "N/A"
        h(f"| {grp} | {gv_s} | {bv_s} | {diff_s} | {flag} |")
    br()

# 3.2 조직별 전주 대비 비교
h("### 3.2 조직별 전주 대비 변화 비교")
br()

for grp in groups_org:
    wk_g = org_data[grp]
    if len(wk_g) < 2:
        continue
    h(f"#### 📊 {grp}")
    h("| 지표 | 전주값 | 이번주값 | 변화량 | 변화율 | 판정 |")
    h("|------|--------|---------|--------|--------|------|")
    for col in key_names:
        if col not in wk_g.columns:
            continue
        s = sign_map.get(col, 1)
        chg, pct = week_over_week_change(wk_g, col)
        curr_val = wk_g.iloc[-1].get(col, np.nan)
        prev_val = wk_g.iloc[-2].get(col, np.nan)
        flag = improvement_flag(chg, s)
        lbl = metric_label(col)
        cv = f"{curr_val:.3f}" if not pd.isna(curr_val) else "N/A"
        pv = f"{prev_val:.3f}" if not pd.isna(prev_val) else "N/A"
        cg = f"{chg:+.3f}" if not pd.isna(chg) else "N/A"
        pg = f"{pct:+.1f}%" if not pd.isna(pct) else "N/A"
        h(f"| {lbl} | {pv} | {cv} | {cg} | {pg} | {flag} |")
    br()

# ═══════════════════════════════════════════
# 섹션 4: 조직별 시계열 분석
# ═══════════════════════════════════════════
h("## 4. 조직별 시계열 분석")
br()
h("> slope: 주당 평균 변화량 / p-value 유의 기준: 0.05")
br()

for grp in groups_org:
    wk_g = org_data[grp]
    if len(wk_g) < 3:
        continue
    h(f"### 4.{groups_org.index(grp)+1} {grp} 시계열 추세")
    h("| 지표 | slope | p-value | 유의성 | 추세 판정 |")
    h("|------|-------|---------|--------|----------|")
    for col in trend_names:
        if col not in wk_g.columns:
            continue
        s = sign_map.get(col, 1)
        res = trend_analysis(wk_g[col])
        if res is None:
            continue
        slope = res["slope"]
        p = res["p_value"]
        sig_str = "✅ 유의" if p < 0.05 else "비유의"
        flag = improvement_flag(slope, s, p)
        h(f"| {metric_label(col)} | {slope:+.4f} | {p:.4f} | {sig_str} | {flag} |")
    br()

# ═══════════════════════════════════════════
# 섹션 5: UNIT별 건강도 점수 비교
# ═══════════════════════════════════════════
h("## 5. UNIT별 종합 건강도 점수")
br()
h("> **점수 계산식**: 각 지표별 시계열 slope 방향(지표 sign 고려) + p-value 유의성으로 점수 부여")
h("> - 악화(유의) = **-5점** (p < 0.05, 나쁜 방향)")
h("> - 악화(비유의) = **-3점** (p ≥ 0.05, 나쁜 방향)")
h("> - 개선(비유의) = **+1점** (p ≥ 0.05, 좋은 방향)")
h("> - 개선(유의) = **+2점** (p < 0.05, 좋은 방향)")
h("> ")
h("> **종합 점수 = Σ(지표별 점수)** (유효 지표 기준)")
br()

unit_scores = {}
unit_details = {}

for grp in all_groups:
    if grp == "PARTNER_TOTAL":
        wk_g = wk_total
    else:
        wk_g = org_data[grp]
    
    if len(wk_g) < 3:
        continue
    
    total_score = 0
    count = 0
    details = []
    for col in trend_names:
        if col not in wk_g.columns:
            continue
        s = sign_map.get(col, 1)
        res = trend_analysis(wk_g[col])
        if res is None:
            continue
        slope = res["slope"]
        p = res["p_value"]
        direction_ok = (slope * s) > 0
        sc = score_unit(direction_ok, p)
        total_score += sc
        count += 1
        details.append((col, slope, p, sc))
    
    unit_scores[grp] = (total_score, count)
    unit_details[grp] = details

# 점수 낮은 순 정렬
sorted_units = sorted(unit_scores.items(), key=lambda x: x[1][0])

h("### 5.1 UNIT별 종합 점수 순위 (낮은 순 → 개선 필요)")
br()
h("| 순위 | UNIT | 총점 | 유효지표수 | 평균점수 | 건강도 |")
h("|------|------|------|-----------|---------|--------|")
for rank, (grp, (sc, cnt)) in enumerate(sorted_units, 1):
    avg = sc / cnt if cnt > 0 else 0
    health = "🔴 위험" if avg < -2 else "⚠️ 주의" if avg < 0 else "🔵 보통" if avg < 1 else "✅ 양호"
    h(f"| {rank} | {grp} | {sc} | {cnt} | {avg:.2f} | {health} |")

br()

# 최하위 UNIT 상세
if sorted_units:
    worst_grp = sorted_units[0][0]
    h(f"### 5.2 최하위 UNIT 상세 분석: {worst_grp}")
    br()
    # 악화 유의 지표만
    bad_details = [(c, sl, p, sc) for c, sl, p, sc in unit_details[worst_grp] if sc == -5]
    bad_ns = [(c, sl, p, sc) for c, sl, p, sc in unit_details[worst_grp] if sc == -3]
    
    if bad_details:
        h("#### 🔴 악화(유의) 지표")
        h("| 지표 | slope | p-value |")
        h("|------|-------|---------|")
        for c, sl, p, sc in bad_details:
            h(f"| {metric_label(c)} | {sl:+.4f} | {p:.4f} |")
        br()
    
    if bad_ns:
        h("#### ⚠️ 악화(비유의) 지표")
        h("| 지표 | slope | p-value |")
        h("|------|-------|---------|")
        for c, sl, p, sc in bad_ns:
            h(f"| {metric_label(c)} | {sl:+.4f} | {p:.4f} |")
        br()

# ═══════════════════════════════════════════
# 섹션 6: UNIT별 지표 점수화 비교 (전주 대비)
# ═══════════════════════════════════════════
h("## 6. UNIT별 지표 점수화 비교 (전주 대비, 낮은 점수 순)")
br()
h("> **점수 계산식**: 전주 대비 변화 방향(지표 sign 고려) + 시계열 p-value(유의성)")
h("> - 악화(유의) = **-5점**, 악화(비유의) = **-3점**, 개선(비유의) = **+1점**, 개선(유의) = **+2점**")
br()

wow_scores = {}
wow_details = {}

for grp in all_groups:
    if grp == "PARTNER_TOTAL":
        wk_g = wk_total
    else:
        wk_g = org_data[grp]
    
    if len(wk_g) < 2:
        continue
    
    total_score = 0
    count = 0
    details = []
    
    for col in trend_names:
        if col not in wk_g.columns:
            continue
        s = sign_map.get(col, 1)
        chg, pct = week_over_week_change(wk_g, col)
        if pd.isna(chg):
            continue
        
        # 시계열 p-value (유의성 판단용)
        res = trend_analysis(wk_g[col])
        p = res["p_value"] if res else 0.99
        
        direction_ok = (chg * s) > 0
        sc = score_unit(direction_ok, p)
        total_score += sc
        count += 1
        details.append((col, chg, pct, p, sc))
    
    wow_scores[grp] = (total_score, count)
    wow_details[grp] = details

sorted_wow = sorted(wow_scores.items(), key=lambda x: x[1][0])

h("### 6.1 UNIT별 전주 대비 종합 점수 순위")
br()
h("| 순위 | UNIT | 총점 | 유효지표수 | 건강도 |")
h("|------|------|------|-----------|--------|")
for rank, (grp, (sc, cnt)) in enumerate(sorted_wow, 1):
    avg = sc / cnt if cnt > 0 else 0
    health = "🔴 위험" if avg < -2 else "⚠️ 주의" if avg < 0 else "🔵 보통" if avg < 1 else "✅ 양호"
    h(f"| {rank} | {grp} | {sc} | {cnt} | {health} |")

br()

# 각 UNIT 지표별 점수 (악화 중심)
for grp, (sc, cnt) in sorted_wow:
    wk_g = wk_total if grp == "PARTNER_TOTAL" else org_data[grp]
    details = wow_details[grp]
    # 낮은 점수 순 정렬
    details_sorted = sorted(details, key=lambda x: x[4])
    
    h(f"### 6.{list(dict(sorted_wow).keys()).index(grp)+1+1} {grp} 전주 대비 지표별 점수 (낮은 순)")
    h("| 지표 | 전주→이번주 변화량 | 변화율 | p-value | 점수 | 판정 |")
    h("|------|------------------|--------|---------|------|------|")
    for col, chg, pct, p, sco in details_sorted[:20]:  # 상위 20개
        s = sign_map.get(col, 1)
        lbl = metric_label(col)
        flag = improvement_flag(chg, s, p)
        cg = f"{chg:+.3f}" if not pd.isna(chg) else "N/A"
        pg = f"{pct:+.1f}%" if not pd.isna(pct) else "N/A"
        h(f"| {lbl} | {cg} | {pg} | {p:.4f} | {sco:+d} | {flag} |")
    br()

# ═══════════════════════════════════════════
# 섹션 7: Hexa Index 간 상관관계 분석
# ═══════════════════════════════════════════
h("## 7. Hexa Index 간 상관관계 분석")
br()
h("> **분석 방법**: Pearson 상관계수 + p-value (전체 PARTNER_TOTAL 주간 데이터 기준)")
h("> **유의 기준**: p < 0.05, |r| > 0.7 = 강한 상관")
br()

# 핵심 지표 간 상관관계 분석
CORR_METRIC_IDS = list(range(1, 20))
corr_names = [metrics_meta[str(i)]["name"] for i in CORR_METRIC_IDS
              if str(i) in metrics_meta and metrics_meta[str(i)]["name"] in wk_total.columns]

corr_data = wk_total[corr_names].dropna(axis=1, how='all')
valid_cols = corr_data.columns.tolist()

h("### 7.1 강한 상관관계 지표 쌍 (|r| > 0.7, p < 0.05)")
br()
h("| 지표 A | 지표 B | Pearson r | p-value | 관계 |")
h("|--------|--------|-----------|---------|------|")

corr_pairs = []
for i, c1 in enumerate(valid_cols):
    for c2 in valid_cols[i+1:]:
        s1 = corr_data[c1].dropna()
        s2 = corr_data[c2].dropna()
        common = s1.index.intersection(s2.index)
        if len(common) < 5:
            continue
        r, p = stats.pearsonr(s1[common], s2[common])
        if abs(r) > 0.7 and p < 0.05:
            corr_pairs.append((c1, c2, r, p))

corr_pairs_sorted = sorted(corr_pairs, key=lambda x: abs(x[2]), reverse=True)
for c1, c2, r, p in corr_pairs_sorted[:30]:
    rel = "🔴 강한 양의 상관" if r > 0.9 else "🔵 양의 상관" if r > 0 else "⚠️ 음의 상관"
    h(f"| {metric_label(c1)} | {metric_label(c2)} | {r:.3f} | {p:.4f} | {rel} |")

br()

h("### 7.2 주요 지표 상관계수 매트릭스")
br()
# 핵심 5개 지표만
MATRIX_COLS = [metrics_meta[str(i)]["name"] for i in [2, 3, 5, 7, 16]
               if str(i) in metrics_meta and metrics_meta[str(i)]["name"] in valid_cols]

if len(MATRIX_COLS) >= 2:
    header_str = "| 지표 | " + " | ".join([c[:12]+"..." if len(c)>12 else c for c in MATRIX_COLS]) + " |"
    sep_str = "|------|" + "-------|" * len(MATRIX_COLS)
    h(header_str)
    h(sep_str)
    for c1 in MATRIX_COLS:
        row_vals = []
        for c2 in MATRIX_COLS:
            if c1 == c2:
                row_vals.append("1.000")
            else:
                s1 = corr_data[c1].dropna() if c1 in corr_data else pd.Series()
                s2 = corr_data[c2].dropna() if c2 in corr_data else pd.Series()
                common = s1.index.intersection(s2.index)
                if len(common) < 3:
                    row_vals.append("N/A")
                else:
                    r, _ = stats.pearsonr(s1[common], s2[common])
                    row_vals.append(f"{r:.3f}")
        lbl = c1[:12]+"..." if len(c1)>12 else c1
        h(f"| {lbl} | " + " | ".join(row_vals) + " |")
    br()

# ═══════════════════════════════════════════
# 섹션 8: 주간 추이 테이블 (전체)
# ═══════════════════════════════════════════
h("## 8. 주간 추이 테이블 (PARTNER_TOTAL)")
br()
h("> 주요 지표의 주별 값 변화 (설 연휴 주 제외)")
br()

weeks_list = wk_total["yearweek"].tolist()
h("### 8.1 핵심 지표 주별 값")
h("| 지표 | " + " | ".join(weeks_list) + " |")
h("|------|" + "-------|" * len(weeks_list))

for col in key_names:
    if col not in wk_total.columns:
        continue
    vals = []
    for _, row in wk_total.iterrows():
        v = row.get(col, np.nan)
        vals.append(f"{v:.2f}" if not pd.isna(v) else "N/A")
    h(f"| {metric_label(col)} | " + " | ".join(vals) + " |")

br()

# ═══════════════════════════════════════════
# 섹션 9: 추가 분석 – 주차별 조직 비교
# ═══════════════════════════════════════════
h("## 9. 추가 분석: 조직별 상대적 위치 분석")
br()
h("> 각 지표에서 전체 평균 대비 각 조직이 어느 위치에 있는지 분석")
h("> Z-score 기반: (조직값 - 전체값) / 전체표준편차")
br()

# 최신 주차 기준 z-score 비교
for col in key_names:
    if col not in metric_cols:
        continue
    s = sign_map.get(col, 1)
    values = {}
    all_vals = []
    for grp in groups_org:
        wk_g = org_data[grp]
        if len(wk_g) == 0:
            continue
        v = wk_g.iloc[-1].get(col, np.nan)
        if not pd.isna(v):
            values[grp] = v
            all_vals.append(v)
    
    if len(all_vals) < 2:
        continue
    
    mean_v = np.mean(all_vals)
    std_v = np.std(all_vals)
    
    h(f"#### {metric_label(col)}")
    h("| 조직 | 값 | 조직간 평균 | Z-score | 상대위치 |")
    h("|------|-----|-----------|---------|---------|")
    for grp, v in values.items():
        z = (v - mean_v) / std_v if std_v > 0 else 0
        pos = "▲ 상위" if (z * s) > 0.5 else "▼ 하위" if (z * s) < -0.5 else "→ 평균"
        h(f"| {grp} | {v:.3f} | {mean_v:.3f} | {z:+.2f} | {pos} |")
    br()

# ═══════════════════════════════════════════
# 섹션 10: 이상치 탐지
# ═══════════════════════════════════════════
h("## 10. 추가 분석: 이상치(Anomaly) 탐지")
br()
h("> 각 지표의 주별 값에서 IQR 방법으로 이상치 탐지")
h("> 이상치: Q1 - 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과")
br()

h("### 10.1 PARTNER_TOTAL 이상치 발생 지표")
br()
h("| 지표 | 이상치 주차 | 이상값 | 정상범위 |")
h("|------|-----------|--------|---------|")

for col in key_names:
    if col not in wk_total.columns:
        continue
    s_data = wk_total[col].dropna()
    if len(s_data) < 4:
        continue
    q1, q3 = s_data.quantile(0.25), s_data.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    
    for idx, row in wk_total.iterrows():
        v = row.get(col, np.nan)
        if pd.isna(v):
            continue
        if v < lower or v > upper:
            wk_str = row["yearweek"]
            h(f"| {metric_label(col)} | {wk_str} | {v:.3f} | [{lower:.3f}, {upper:.3f}] |")

br()

# ═══════════════════════════════════════════
# 마무리
# ═══════════════════════════════════════════
h("---")
h("")
h(f"*분석 생성 일시: 2026-03-04*")
h(f"*데이터 기준: dailyWeekHexa_202603041519.csv*")
h(f"*설 연휴(2026 W08: 2/16~2/20) 해당 주 분석 제외*")

# 파일 저장
output = "\n".join(lines)
with open("collab_daily.md", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ collab_daily.md 생성 완료")
print(f"총 줄수: {len(lines)}")
