#!/usr/bin/env python3
"""
Hexa Index 주간 분석 스크립트
- 설 연휴(2026-02-16) 제외
- PARTNER_TOTAL 전체 분석
- 조직별 비교 분석
- 시계열 분석 (slope, p-value)
- 지표간 상관관계 분석
"""

import json
import os
import warnings
from io import StringIO

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr

warnings.filterwarnings("ignore")

# ── 설정 ──────────────────────────────────────────────────────────────────────
CSV_FILE = "weeklyWeekHexa_202603041516.csv"
JSON_FILE = "hexa-metrics.json"
OUTPUT_FILE = "collab_weekly.md"

# 설 연휴 제외 주차 (2026-02-16~20)
EXCLUDE_DATES = ["2026-02-16"]

# 유의수준
ALPHA = 0.05

# UNIT 점수 기준
# 악화(유의) -5, 악화(비유의) -3, 개선(비유의) +1, 개선(유의) +2
def get_trend_score(slope, p_value, sign):
    """
    slope: 시계열 회귀 기울기
    p_value: 유의확률
    sign: +1(클수록 좋음) / -1(작을수록 좋음)
    좋아지는 방향 = sign * slope > 0 이면 개선
    """
    improvement = (sign * slope) > 0
    significant = p_value < ALPHA
    if improvement and significant:
        return 2, "개선(유의)"
    elif improvement and not significant:
        return 1, "개선(비유의)"
    elif not improvement and not significant:
        return -3, "악화(비유의)"
    else:
        return -5, "악화(유의)"


# ── 데이터 로드 ────────────────────────────────────────────────────────────────
def load_data():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        metrics_raw = json.load(f)
    metrics = metrics_raw["hexaAdminMap"]  # {"1": {name, sign}, ...}

    df = pd.read_csv(CSV_FILE, quotechar='"', dtype=str)
    # snapdate를 datetime
    df["snapdate"] = pd.to_datetime(df["snapdate"])
    # 설 연휴 제외
    exclude_dt = [pd.to_datetime(d) for d in EXCLUDE_DATES]
    df = df[~df["snapdate"].isin(exclude_dt)].copy()

    # 수치형 변환 (null → NaN)
    metric_cols = [v["name"] for v in metrics.values() if v["name"] in df.columns]
    for col in metric_cols:
        df[col] = pd.to_numeric(df[col].replace("null", np.nan), errors="coerce")

    return df, metrics, metric_cols


# ── 분석 헬퍼 ──────────────────────────────────────────────────────────────────
def sign_label(sign):
    return "[+]" if sign == 1 else "[-]"


def fmt(v, decimals=3):
    if pd.isna(v):
        return "N/A"
    return f"{v:.{decimals}f}"


def trend_analysis(series: pd.Series):
    """시계열 OLS (x = 인덱스 순서). slope, p-value 반환"""
    valid = series.dropna()
    if len(valid) < 3:
        return np.nan, np.nan
    x = np.arange(len(valid))
    slope, intercept, r, p, se = stats.linregress(x, valid.values)
    return slope, p


def week_over_week(df_group: pd.DataFrame, col: str):
    """최근 2주 데이터 비교 (절대값 diff, % diff)"""
    sorted_df = df_group.sort_values("snapdate")
    vals = sorted_df[col].dropna()
    if len(vals) < 2:
        return np.nan, np.nan, np.nan, np.nan
    prev, curr = vals.iloc[-2], vals.iloc[-1]
    diff = curr - prev
    pct = (diff / abs(prev) * 100) if prev != 0 else np.nan
    return prev, curr, diff, pct


def mean_comparison(df_group: pd.DataFrame, df_total: pd.DataFrame, col: str):
    """해당 그룹 최근값 vs. PARTNER_TOTAL 전체 평균 비교"""
    g_last = df_group.sort_values("snapdate")[col].dropna()
    t_last = df_total.sort_values("snapdate")[col].dropna()
    if g_last.empty or t_last.empty:
        return np.nan, np.nan, np.nan
    g_val = g_last.iloc[-1]
    t_val = t_last.iloc[-1]
    return g_val, t_val, g_val - t_val


# ── 메인 분석 ──────────────────────────────────────────────────────────────────
def main():
    df, metrics, metric_cols = load_data()

    groups = [g for g in df["GROUP"].unique() if g != "PARTNER_TOTAL"]
    df_total = df[df["GROUP"] == "PARTNER_TOTAL"].copy()

    lines = []

    # ══════════════════════════════════════════════════════════════════════════
    # 0. 헤더 및 설명
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "# Hexa Index 주간 분석 보고서",
        "",
        f"> **분석 기준일**: {df['snapdate'].max().strftime('%Y-%m-%d')} (최신 주차 기준)",
        f"> **데이터 범위**: {df['snapdate'].min().strftime('%Y-%m-%d')} ~ {df['snapdate'].max().strftime('%Y-%m-%d')}",
        f"> **설 연휴 제외**: 2026-02-16 (2/16~2/20 설 연휴 주차)",
        f"> **분석 그룹**: PARTNER_TOTAL(전체), {', '.join(groups)}",
        "",
        "---",
        "",
        "## 📌 지표 표기 규칙 및 용어 설명",
        "",
        "| 표기 | 의미 |",
        "|------|------|",
        "| **[+] 지표명** | 값이 클수록 좋은 방향 (예: 이슈 처리율, 코드 변경량) |",
        "| **[-] 지표명** | 값이 작을수록 좋은 방향 (예: 이슈 처리일, 잔여이슈) |",
        "| 🟢 개선 | 좋아지는 방향으로 변화 |",
        "| 🔴 악화 | 나빠지는 방향으로 변화 |",
        "| ⚪ 유지 | 변화 없음 또는 미미 |",
        "",
        "---",
        "",
        "## 📐 분석 방법 설명",
        "",
        "### Slope (기울기)란?",
        "",
        "**Slope**는 시계열 데이터에 선형 회귀(OLS)를 적합했을 때 나오는 **기울기 값**입니다.",
        "",
        "- **양(+) slope**: 시간이 지날수록 값이 증가하는 추세",
        "- **음(-) slope**: 시간이 지날수록 값이 감소하는 추세",
        "- **slope의 판단 기준**: 지표 방향([+]/[-])과 함께 해석해야 합니다.",
        "  - `[+]` 지표 + 양(+) slope → **개선 추세** 🟢",
        "  - `[+]` 지표 + 음(-) slope → **악화 추세** 🔴",
        "  - `[-]` 지표 + 음(-) slope → **개선 추세** 🟢",
        "  - `[-]` 지표 + 양(+) slope → **악화 추세** 🔴",
        "- **slope 절댓값**: 변화 속도를 나타냅니다. 클수록 빠르게 변하고 있음.",
        "",
        "### p-value (유의확률)란?",
        "",
        "**p-value**는 해당 추세(slope)가 **우연에 의한 것인지 아닌지**를 판단하는 확률입니다.",
        "",
        f"- **유의 기준**: p < {ALPHA} (5%)",
        "- **p < 0.05** → 추세가 통계적으로 유의미함 → **(유의)** 표기",
        "- **p ≥ 0.05** → 추세가 우연일 가능성 있음 → **(비유의)** 표기",
        "",
        "### UNIT 건강도 점수 계산식",
        "",
        "각 지표의 시계열 추세(slope + p-value + 방향)를 점수화하여 합산합니다.",
        "",
        "| 상태 | 판정 조건 | 점수 |",
        "|------|-----------|------|",
        "| 개선(유의) | sign×slope > 0 AND p < 0.05 | **+2** |",
        "| 개선(비유의) | sign×slope > 0 AND p ≥ 0.05 | **+1** |",
        "| 악화(비유의) | sign×slope < 0 AND p ≥ 0.05 | **-3** |",
        "| 악화(유의) | sign×slope < 0 AND p < 0.05 | **-5** |",
        "",
        "```",
        "건강도 점수 = Σ(각 지표별 점수)",
        "  - sign = +1이면 [+]지표 (클수록 좋음)",
        "  - sign = -1이면 [-]지표 (작을수록 좋음)",
        "  - sign×slope > 0 → 좋아지는 방향의 slope",
        "```",
        "",
        "---",
        "",
    ]

    # ══════════════════════════════════════════════════════════════════════════
    # 1. 전체(PARTNER_TOTAL) 분석
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 1. 전체(PARTNER_TOTAL) 분석",
        "",
    ]

    # 최신 주차 현황
    latest_date = df_total["snapdate"].max()
    prev_date = df_total.sort_values("snapdate")["snapdate"].unique()
    if len(prev_date) >= 2:
        prev_date = sorted(prev_date)[-2]
    else:
        prev_date = None

    df_latest = df_total[df_total["snapdate"] == latest_date]
    df_prev = df_total[df_total["snapdate"] == prev_date] if prev_date else None

    lines += [
        f"### 1.1 최신 주차 현황 ({latest_date.strftime('%Y-%m-%d')})",
        "",
        "| 지표 | 전주 | 금주 | 변화량 | 변화율 | 추이 |",
        "|------|------|------|--------|--------|------|",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        prev_v, curr_v, diff, pct = week_over_week(df_total, col)
        if pd.isna(curr_v):
            continue
        direction = sign_label(sign)
        # 추이 판단
        if pd.isna(diff):
            trend_icon = "⚪"
        elif sign * diff > 0:
            trend_icon = "🟢 개선"
        elif sign * diff < 0:
            trend_icon = "🔴 악화"
        else:
            trend_icon = "⚪ 유지"
        lines.append(
            f"| {direction} {col} | {fmt(prev_v)} | {fmt(curr_v)} | {fmt(diff,3)} | {fmt(pct,1)}% | {trend_icon} |"
        )

    lines += ["", "---", ""]

    # ── 1.2 전체 시계열 분석
    lines += [
        "### 1.2 전체(PARTNER_TOTAL) 시계열 추세 분석",
        "",
        f"> **유의 기준**: p < {ALPHA}",
        f"> **slope**: 주(week) 단위 변화 기울기. 양수=증가 추세, 음수=감소 추세.",
        "",
        "| 지표 | slope | p-value | 판정 |",
        "|------|-------|---------|------|",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        slope, p = trend_analysis(df_total.sort_values("snapdate")[col])
        if pd.isna(slope):
            continue
        direction = sign_label(sign)
        score, label = get_trend_score(slope, p, sign)
        icon = "🟢" if score > 0 else "🔴"
        lines.append(
            f"| {direction} {col} | {fmt(slope,4)} | {fmt(p,4)} | {icon} {label} |"
        )

    lines += ["", "---", "", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 2. 조직별 비교 분석
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 2. 조직별 비교 분석",
        "",
    ]

    # 2.1 전주 대비 변화 비교
    lines += [
        "### 2.1 조직별 전주 대비 변화",
        "",
        "> 각 지표의 전주(WoW) 변화를 조직별로 비교합니다.",
        "",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        direction = sign_label(sign)
        lines += [
            f"#### {direction} {col}",
            "",
            "| 조직 | 전주 | 금주 | 변화량 | 추이 |",
            "|------|------|------|--------|------|",
        ]
        for grp in ["PARTNER_TOTAL"] + groups:
            df_g = df[df["GROUP"] == grp]
            prev_v, curr_v, diff, pct = week_over_week(df_g, col)
            if pd.isna(curr_v):
                continue
            if pd.isna(diff):
                trend_icon = "⚪"
            elif sign * diff > 0:
                trend_icon = "🟢 개선"
            elif sign * diff < 0:
                trend_icon = "🔴 악화"
            else:
                trend_icon = "⚪ 유지"
            lines.append(
                f"| {grp} | {fmt(prev_v)} | {fmt(curr_v)} | {fmt(diff,3)} | {trend_icon} |"
            )
        lines += [""]

    lines += ["---", ""]

    # 2.2 전체 평균 대비 비교
    lines += [
        "### 2.2 조직별 vs. PARTNER_TOTAL 전체 평균 비교 (최신 주차)",
        "",
        "> 각 조직의 최신 주차 값과 전체(PARTNER_TOTAL) 값의 차이를 비교합니다.",
        "",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        direction = sign_label(sign)
        lines += [
            f"#### {direction} {col}",
            "",
            "| 조직 | 조직 최신값 | 전체(PARTNER_TOTAL) | 차이 | 상대 평가 |",
            "|------|------------|---------------------|------|-----------|",
        ]
        _, total_val, _ = mean_comparison(df_total, df_total, col)
        for grp in groups:
            df_g = df[df["GROUP"] == grp]
            g_val, t_val, diff = mean_comparison(df_g, df_total, col)
            if pd.isna(g_val) or pd.isna(t_val):
                continue
            if pd.isna(diff):
                eval_str = "⚪"
            elif sign * diff > 0:
                eval_str = "🟢 전체보다 우수"
            elif sign * diff < 0:
                eval_str = "🔴 전체보다 열위"
            else:
                eval_str = "⚪ 동일"
            lines.append(
                f"| {grp} | {fmt(g_val)} | {fmt(t_val)} | {fmt(diff,3)} | {eval_str} |"
            )
        lines += [""]

    lines += ["---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 3. 전체/조직별 시계열 분석
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 3. 전체/조직별 시계열 추세 분석",
        "",
        f"> **slope**: 주(week) 단위 선형 회귀 기울기. [+]지표에서 양수=개선, [-]지표에서 음수=개선.",
        f"> **p-value**: 추세의 통계적 유의성. **p < {ALPHA}** 이면 유의한 추세로 판정.",
        "",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        direction = sign_label(sign)
        lines += [
            f"#### {direction} {col}",
            "",
            "| 조직 | slope | p-value | 판정 |",
            "|------|-------|---------|------|",
        ]
        for grp in ["PARTNER_TOTAL"] + groups:
            df_g = df[df["GROUP"] == grp]
            slope, p = trend_analysis(df_g.sort_values("snapdate")[col])
            if pd.isna(slope):
                continue
            score, label = get_trend_score(slope, p, sign)
            icon = "🟢" if score > 0 else "🔴"
            lines.append(
                f"| {grp} | {fmt(slope,4)} | {fmt(p,4)} | {icon} {label} |"
            )
        lines += [""]

    lines += ["---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 4. UNIT 종합 건강도 점수 (조직별)
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 4. UNIT 종합 건강도 점수 (조직별, 시계열 추세 기반)",
        "",
        "### 계산식",
        "",
        "```",
        "각 지표에 대해 시계열 회귀(OLS) → slope, p-value 산출",
        "  if (sign × slope > 0) and (p < 0.05)  → 개선(유의)   = +2",
        "  if (sign × slope > 0) and (p ≥ 0.05)  → 개선(비유의) = +1",
        "  if (sign × slope ≤ 0) and (p ≥ 0.05)  → 악화(비유의) = -3",
        "  if (sign × slope ≤ 0) and (p < 0.05)  → 악화(유의)   = -5",
        "",
        "건강도 점수 = 모든 유효 지표의 점수 합산",
        "```",
        "",
        "| 조직 | 개선(유의) | 개선(비유의) | 악화(비유의) | 악화(유의) | 건강도 점수 |",
        "|------|-----------|-------------|-------------|-----------|------------|",
    ]

    unit_scores = {}
    for grp in ["PARTNER_TOTAL"] + groups:
        df_g = df[df["GROUP"] == grp]
        cnt = {"개선(유의)": 0, "개선(비유의)": 0, "악화(비유의)": 0, "악화(유의)": 0}
        total_score = 0
        for mid, minfo in metrics.items():
            col = minfo["name"]
            sign = minfo["sign"]
            if col not in df_g.columns:
                continue
            slope, p = trend_analysis(df_g.sort_values("snapdate")[col])
            if pd.isna(slope):
                continue
            s, label = get_trend_score(slope, p, sign)
            cnt[label] += 1
            total_score += s
        unit_scores[grp] = (total_score, cnt)

    # 점수 낮은 순 정렬
    sorted_units = sorted(unit_scores.items(), key=lambda x: x[1][0])
    for grp, (score, cnt) in sorted_units:
        lines.append(
            f"| {grp} | {cnt['개선(유의)']} | {cnt['개선(비유의)']} | {cnt['악화(비유의)']} | {cnt['악화(유의)']} | **{score}** |"
        )

    lines += ["", "---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 5. UNIT별 지표 악화/개선 상세 (점수 낮은 순)
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 5. UNIT별 지표 추세 상세 (악화 우선 표시)",
        "",
        "> 건강도 점수 낮은 조직부터 표시. 각 조직 내 지표는 악화(유의) → 악화(비유의) → 개선(비유의) → 개선(유의) 순.",
        "",
    ]

    for grp, (score, _) in sorted_units:
        df_g = df[df["GROUP"] == grp]
        lines += [
            f"### {grp} (건강도 점수: {score})",
            "",
            "| 지표 | slope | p-value | 점수 | 판정 |",
            "|------|-------|---------|------|------|",
        ]
        metric_results = []
        for mid, minfo in metrics.items():
            col = minfo["name"]
            sign = minfo["sign"]
            if col not in df_g.columns:
                continue
            slope, p = trend_analysis(df_g.sort_values("snapdate")[col])
            if pd.isna(slope):
                continue
            s, label = get_trend_score(slope, p, sign)
            direction = sign_label(sign)
            metric_results.append((s, label, direction, col, slope, p))

        # 악화 우선 정렬
        metric_results.sort(key=lambda x: x[0])
        for s, label, direction, col, slope, p in metric_results:
            icon = "🟢" if s > 0 else "🔴"
            lines.append(
                f"| {direction} {col} | {fmt(slope,4)} | {fmt(p,4)} | {s} | {icon} {label} |"
            )
        lines += [""]

    lines += ["---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 6. Hexa Index 간 상관관계 분석
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 6. Hexa Index 간 상관관계 분석 (PARTNER_TOTAL)",
        "",
        "> Pearson 상관계수 기반. |r| ≥ 0.7 이면 강한 상관, 0.4 ≤ |r| < 0.7 이면 중간 상관.",
        f"> p < {ALPHA} 인 경우만 유의한 상관관계로 표시.",
        "",
        "| 지표 A | 지표 B | 상관계수(r) | p-value | 해석 |",
        "|--------|--------|------------|---------|------|",
    ]

    # 상관관계 계산 (유효 지표만)
    corr_cols = []
    for mid, minfo in metrics.items():
        col = minfo["name"]
        if col in df_total.columns:
            valid_count = df_total.sort_values("snapdate")[col].dropna().shape[0]
            if valid_count >= 5:
                corr_cols.append(col)

    corr_pairs = []
    for i in range(len(corr_cols)):
        for j in range(i + 1, len(corr_cols)):
            col_a = corr_cols[i]
            col_b = corr_cols[j]
            merged = df_total[[col_a, col_b]].dropna()
            if len(merged) < 5:
                continue
            try:
                r, p = pearsonr(merged[col_a], merged[col_b])
            except Exception:
                continue
            if abs(r) >= 0.4 and p < ALPHA:
                corr_pairs.append((abs(r), r, col_a, col_b, p))

    corr_pairs.sort(reverse=True)
    for abs_r, r, col_a, col_b, p in corr_pairs[:50]:  # 상위 50개
        if abs_r >= 0.7:
            level = "강한 상관"
        else:
            level = "중간 상관"
        direction = "양(+)" if r > 0 else "음(-)"
        lines.append(
            f"| {col_a} | {col_b} | {fmt(r,3)} | {fmt(p,4)} | {level} / {direction} |"
        )

    lines += ["", "---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 7. 추가 분석 - 주요 지표 이동평균 & 변동성
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 7. 추가 분석: 주요 지표 변동성 (CV, 표준편차)",
        "",
        "> **CV (변동계수)** = 표준편차 / 평균 × 100 (%)",
        "> CV가 클수록 데이터의 변동성이 크고 불안정한 상태를 의미합니다.",
        "",
        "| 지표 | 평균 | 표준편차 | CV(%) | 안정성 |",
        "|------|------|---------|-------|--------|",
    ]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_total.columns:
            continue
        s = df_total[col].dropna()
        if len(s) < 3:
            continue
        mean_v = s.mean()
        std_v = s.std()
        cv = abs(std_v / mean_v * 100) if mean_v != 0 else np.nan
        if pd.isna(cv):
            continue
        direction = sign_label(sign)
        stability = "🟢 안정" if cv < 20 else ("🟡 보통" if cv < 50 else "🔴 불안정")
        lines.append(
            f"| {direction} {col} | {fmt(mean_v,3)} | {fmt(std_v,3)} | {fmt(cv,1)} | {stability} |"
        )

    lines += ["", "---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 8. 전체 데이터 원본 요약 (최신 3주)
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 8. 최근 3주 데이터 요약 (PARTNER_TOTAL)",
        "",
    ]

    recent_dates = sorted(df_total["snapdate"].unique())[-3:]
    df_recent = df_total[df_total["snapdate"].isin(recent_dates)].sort_values("snapdate")

    col_names = [v["name"] for v in metrics.values() if v["name"] in df_total.columns]
    header = "| 지표 | " + " | ".join([d.strftime("%m/%d") for d in recent_dates]) + " |"
    separator = "|" + "---|" * (len(recent_dates) + 1)
    lines += [header, separator]

    for mid, minfo in metrics.items():
        col = minfo["name"]
        sign = minfo["sign"]
        if col not in df_recent.columns:
            continue
        direction = sign_label(sign)
        vals = []
        for d in recent_dates:
            row = df_recent[df_recent["snapdate"] == d]
            v = row[col].values[0] if not row.empty and not pd.isna(row[col].values[0]) else np.nan
            vals.append(fmt(v))
        lines.append(f"| {direction} {col} | " + " | ".join(vals) + " |")

    lines += ["", "---", ""]

    # ══════════════════════════════════════════════════════════════════════════
    # 9. 악화 지표 요약 (유의한 것 우선)
    # ══════════════════════════════════════════════════════════════════════════
    lines += [
        "## 9. ⚠️ 전체 악화 지표 요약 (유의한 것 우선)",
        "",
        "| 조직 | 지표 | slope | p-value | 판정 |",
        "|------|------|-------|---------|------|",
    ]

    all_bad = []
    for grp in ["PARTNER_TOTAL"] + groups:
        df_g = df[df["GROUP"] == grp]
        for mid, minfo in metrics.items():
            col = minfo["name"]
            sign = minfo["sign"]
            if col not in df_g.columns:
                continue
            slope, p = trend_analysis(df_g.sort_values("snapdate")[col])
            if pd.isna(slope):
                continue
            s, label = get_trend_score(slope, p, sign)
            if s < 0:
                all_bad.append((s, grp, col, slope, p, label, sign))

    all_bad.sort(key=lambda x: x[0])
    for s, grp, col, slope, p, label, sign in all_bad:
        direction = sign_label(sign)
        icon = "🔴"
        lines.append(
            f"| {grp} | {icon} {direction} {col} | {fmt(slope,4)} | {fmt(p,4)} | {label} |"
        )

    lines += ["", "---", ""]

    # footer
    lines += [
        "",
        "---",
        f"*생성일시: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} by analyze_hexa.py (uv/pandas/scipy/statsmodels)*",
    ]

    # ── 파일 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 분석 완료: {OUTPUT_FILE} ({len(lines)} lines)")
    print(f"   데이터 범위: {df['snapdate'].min().date()} ~ {df['snapdate'].max().date()}")
    print(f"   그룹: {df['GROUP'].unique().tolist()}")
    print(f"   제외된 주차: {EXCLUDE_DATES}")


if __name__ == "__main__":
    main()
