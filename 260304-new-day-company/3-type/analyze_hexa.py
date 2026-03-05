#!/usr/bin/env python3
"""
Hexa Index 분석 스크립트
- 설 연휴(2026-02-16 ~ 2026-02-20) 제외
- 활성개발자수 >= 10인 조직만 분석
- p-value < 0.1 기준으로 유의미한 변화 탐지
- 결과를 collab_daily.md에 출력
"""

import pandas as pd
import numpy as np
import json
from scipy import stats
from datetime import datetime


def load_metrics_config(path="hexa-metrics.json"):
    """hexa-metrics.json에서 지표 설정 로드 (제외예정 지표 제외)"""
    with open(path, encoding="utf-8") as f:
        config = json.load(f)["hexaAdminMap"]
    valid = {}
    for k, v in config.items():
        name = v["name"]
        if "[제외예정]" not in name:
            valid[name] = v["sign"]
    return valid


def load_and_preprocess(csv_path="dailyWeekHexa_202603041519.csv"):
    """CSV 로드 및 전처리 (설 연휴 제외)"""
    df = pd.read_csv(csv_path)
    df["snapdate"] = pd.to_datetime(df["snapdate"])

    # 설 연휴 제외: 2026-02-16 ~ 2026-02-20
    holiday_mask = (df["snapdate"] >= "2026-02-16") & (df["snapdate"] <= "2026-02-20")
    excluded_count = holiday_mask.sum()
    df = df[~holiday_mask].copy()
    print(f"설 연휴 제외 행수: {excluded_count}개")
    return df


def calc_hexa_index(gdf: pd.DataFrame, metrics: dict) -> tuple[pd.Series, dict]:
    """
    그룹별 Hexa Index 계산
    
    계산식:
    - sign=+1 지표: 정규화점수 = (value - min) / (max - min) × 100
    - sign=-1 지표: 정규화점수 = 100 - (value - min) / (max - min) × 100
    - Hexa Index = 유효 지표 정규화점수의 평균 (0~100점 척도)
    
    Returns: (hexa_index_series, metric_normalized_dict)
    """
    gdf = gdf.copy()
    all_scores = {}
    
    for metric, sign in metrics.items():
        if metric not in gdf.columns:
            continue
        values = pd.to_numeric(gdf[metric], errors="coerce")
        if values.isna().all():
            continue
        vmin, vmax = values.min(), values.max()
        if vmax == vmin:
            # 변화 없음 → 중간값 50
            all_scores[metric] = pd.Series([50.0] * len(gdf), index=gdf.index)
            continue
        normalized = (values - vmin) / (vmax - vmin) * 100
        if sign == -1:
            normalized = 100 - normalized
        all_scores[metric] = normalized
    
    if not all_scores:
        return pd.Series(np.nan, index=gdf.index), {}
    
    scores_df = pd.DataFrame(all_scores, index=gdf.index)
    hexa_index = scores_df.mean(axis=1)
    return hexa_index, all_scores


def analyze_trend(t: np.ndarray, values: np.ndarray, min_points: int = 10):
    """
    선형회귀 기반 트렌드 분석
    
    반환: (slope, p_value, r_squared) 또는 None
    """
    valid = ~np.isnan(values)
    if valid.sum() < min_points:
        return None
    t_valid = t[valid]
    v_valid = values[valid]
    slope, intercept, r, p, se = stats.linregress(t_valid, v_valid)
    return {"slope": slope, "p_value": p, "r_squared": r ** 2,
            "mean": np.mean(v_valid), "std": np.std(v_valid)}


def direction_label(slope: float, sign: int) -> str:
    """트렌드 방향 → 개선/악화 판정"""
    # sign=1: slope>0이면 개선 / sign=-1: slope<0이면 개선 (이미 정규화 반영됨)
    if slope > 0:
        return "📈 개선"
    else:
        return "📉 악화"


def format_pval(p: float) -> str:
    if p < 0.01:
        return f"{p:.4f}***"
    elif p < 0.05:
        return f"{p:.4f}**"
    elif p < 0.1:
        return f"{p:.4f}*"
    else:
        return f"{p:.4f}"


def raw_early_recent(series: pd.Series, n: int = 7) -> tuple[float, float]:
    """원본 시계열에서 초기 n일 평균과 최근 n일 평균을 반환"""
    valid = series.dropna()
    if len(valid) < n:
        n = max(1, len(valid) // 2)
    return float(valid.iloc[:n].mean()), float(valid.iloc[-n:].mean())


def analyze_group(group_name: str, gdf: pd.DataFrame, metrics: dict) -> dict:
    """특정 그룹 분석"""
    gdf = gdf.sort_values("snapdate").copy()
    
    # 활성개발자수 평균
    mean_headcount = pd.to_numeric(gdf["활성개발자수"], errors="coerce").mean()
    
    # Hexa Index 계산
    hexa_index, metric_scores = calc_hexa_index(gdf, metrics)
    
    # 시간 숫자화 (일 단위)
    t = (gdf["snapdate"] - gdf["snapdate"].min()).dt.days.values.astype(float)
    
    # 전체 Hexa Index 트렌드
    hexa_trend = analyze_trend(t, hexa_index.values)
    
    # 개별 지표 트렌드 (정규화 점수 기준 trend + 원본값 비교)
    metric_trends = {}
    for metric, scores in metric_scores.items():
        trend = analyze_trend(t, scores.values)
        if trend and trend["p_value"] < 0.1:
            sign = metrics.get(metric, 1)
            # 원본 raw 값의 초기/최근 평균
            raw_series = pd.to_numeric(gdf[metric], errors="coerce")
            raw_e, raw_r = raw_early_recent(raw_series, n=7)
            metric_trends[metric] = {
                **trend,
                "sign": sign,
                "direction": direction_label(trend["slope"], sign),
                "raw_early": raw_e,
                "raw_recent": raw_r,
            }
    
    return {
        "group": group_name,
        "mean_headcount": mean_headcount,
        "data_points": len(gdf),
        "date_range": (gdf["snapdate"].min(), gdf["snapdate"].max()),
        "hexa_index_early": hexa_index.iloc[:7].mean() if len(hexa_index) >= 7 else hexa_index.mean(),
        "hexa_index_recent": hexa_index.iloc[-7:].mean() if len(hexa_index) >= 7 else hexa_index.mean(),
        "hexa_trend": hexa_trend,
        "significant_metrics": metric_trends,
        "hexa_series": hexa_index,
        "dates": gdf["snapdate"].values,
    }


def generate_markdown(results: list, metrics: dict) -> str:
    """분석 결과를 Markdown으로 변환"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append(f"# Hexa Index 분석 보고서")
    lines.append(f"\n> 생성일시: {now}")
    lines.append(f"\n## 분석 개요\n")
    lines.append("| 항목 | 내용 |")
    lines.append("|------|------|")
    lines.append("| 데이터 기간 | 2025-12-22 ~ 2026-03-02 |")
    lines.append("| 제외 기간 | 2026-02-16 ~ 2026-02-20 (설 연휴) |")
    lines.append("| 유의수준 | p < 0.1 (★★★: p<0.01, ★★: p<0.05, ★: p<0.1) |")
    lines.append("| 조직 필터 | 활성개발자수 평균 ≥ 10명 |")
    
    lines.append("\n---\n")
    lines.append("## 📐 계산식 설명\n")
    lines.append("### Hexa Index 계산")
    lines.append("```")
    lines.append("1. 각 지표별 정규화 점수 (0~100 척도):")
    lines.append("   - 높을수록 좋은 지표 (sign=+1):")
    lines.append("     정규화점수 = (value - 기간최솟값) / (기간최댓값 - 기간최솟값) × 100")
    lines.append("   - 낮을수록 좋은 지표 (sign=-1):")
    lines.append("     정규화점수 = 100 - (value - 기간최솟값) / (기간최댓값 - 기간최솟값) × 100")
    lines.append("")
    lines.append("2. Hexa Index = 유효 지표 정규화점수의 평균값")
    lines.append("   - 범위: 0 ~ 100점 (높을수록 좋음)")
    lines.append("   ⚠️  Hexa Index의 절댓값(예: 47.74점)은 분석 기간 내 min/max에 상대적인 값으로,")
    lines.append("      기간이 바뀌면 기준점이 달라지므로 절댓값 자체는 비교 의미가 없음.")
    lines.append("      의미 있는 것은 '추세(slope의 방향과 p-value)'이며,")
    lines.append("      Hexa Index가 전반적으로 오르는지 내리는지로 방향을 파악하는 용도임.")
    lines.append("")
    lines.append("3. 트렌드 분석 (선형회귀):")
    lines.append("   - scipy.stats.linregress(날짜_일수, 정규화점수) 으로 slope, p-value 산출")
    lines.append("   - slope > 0 → 개선 추세 / slope < 0 → 악화 추세")
    lines.append("   - p-value < 0.1 → 통계적으로 유의미한 추세")
    lines.append("")
    lines.append("4. 원본값 비교 (초기 7일 평균 → 최근 7일 평균):")
    lines.append("   - 정규화 이전 실제 지표값 기준으로 얼마나 변했는지 확인")
    lines.append("   - sign=+1: 값이 커지면 개선 / sign=-1: 값이 작아지면 개선")
    lines.append("```\n")
    
    lines.append("---\n")
    lines.append("## 🏢 조직별 분석 결과\n")
    
    for res in results:
        g = res["group"]
        hc = res["mean_headcount"]
        dp = res["data_points"]
        dr = res["date_range"]
        hi_early = res["hexa_index_early"]
        hi_recent = res["hexa_index_recent"]
        ht = res["hexa_trend"]
        sig_metrics = res["significant_metrics"]
        
        lines.append(f"### {'전체' if g == 'PARTNER_TOTAL' else g}")
        lines.append(f"\n| 항목 | 값 |")
        lines.append("|------|-----|")
        lines.append(f"| 그룹명 | {g} |")
        lines.append(f"| 평균 활성개발자수 | {hc:.1f}명 |")
        lines.append(f"| 분석 데이터수 | {dp}일 |")
        lines.append(f"| 분석 기간 | {dr[0].strftime('%Y-%m-%d')} ~ {dr[1].strftime('%Y-%m-%d')} |")
        lines.append(f"| Hexa Index 초기 7일 평균 | {hi_early:.2f}점 (정규화 기준, 절댓값 비교 무의미) |")
        lines.append(f"| Hexa Index 최근 7일 평균 | {hi_recent:.2f}점 (정규화 기준, 절댓값 비교 무의미) |")
        
        if ht:
            p = ht["p_value"]
            sig = "유의미" if p < 0.1 else "무의미"
            dir_arrow = "📈 전반적 개선" if ht["slope"] > 0 else "📉 전반적 악화"
            r2 = ht["r_squared"]
            lines.append(f"| Hexa Index 전체 추세 | {dir_arrow} (slope={ht['slope']:.4f}, p={format_pval(p)}, R²={r2:.3f}) → **{sig}** |")
        
        lines.append("")
        
        if sig_metrics:
            # 개선 지표
            improving = {k: v for k, v in sig_metrics.items() if v["slope"] > 0}
            deteriorating = {k: v for k, v in sig_metrics.items() if v["slope"] <= 0}
            
            if improving:
                lines.append(f"#### 📈 유의미하게 개선된 지표 ({len(improving)}개)\n")
                lines.append("| 지표명 | 방향 | 초기7일 평균 → 최근7일 평균 | slope | p-value | R² |")
                lines.append("|--------|------|--------------------------|-------|---------|-----|")
                for metric, info in sorted(improving.items(), key=lambda x: -x[1]["slope"]):
                    sign = info["sign"]
                    re = info["raw_early"]
                    rr = info["raw_recent"]
                    # 개선 방향 화살표: sign=+1이면 값이 커져야 개선
                    arrow = "↑" if rr > re else "↓"
                    lines.append(
                        f"| {metric} | {info['direction']} | "
                        f"{re:.3g} → {rr:.3g} {arrow} | "
                        f"{info['slope']:.4f} | {format_pval(info['p_value'])} | "
                        f"{info['r_squared']:.3f} |"
                    )
                lines.append("")
            
            if deteriorating:
                lines.append(f"#### 📉 유의미하게 악화된 지표 ({len(deteriorating)}개)\n")
                lines.append("| 지표명 | 방향 | 초기7일 평균 → 최근7일 평균 | slope | p-value | R² |")
                lines.append("|--------|------|--------------------------|-------|---------|-----|")
                for metric, info in sorted(deteriorating.items(), key=lambda x: x[1]["slope"]):
                    sign = info["sign"]
                    re = info["raw_early"]
                    rr = info["raw_recent"]
                    arrow = "↑" if rr > re else "↓"
                    lines.append(
                        f"| {metric} | {info['direction']} | "
                        f"{re:.3g} → {rr:.3g} {arrow} | "
                        f"{info['slope']:.4f} | {format_pval(info['p_value'])} | "
                        f"{info['r_squared']:.3f} |"
                    )
                lines.append("")
        else:
            lines.append("> ✅ 유의미한(p<0.1) 개별 지표 변화 없음\n")
        
        lines.append("---\n")
    
    # 요약 테이블 - 추세 중심으로 재구성
    lines.append("## 📊 전체 요약 (Hexa Index 추세)\n")
    lines.append("> ⚠️ **Hexa Index 절댓값(초기/최근 평균점수)은 분석 기간 내 상대 정규화값이므로 수치 자체보다 '추세 방향(slope)'과 '유의성(p-value)'을 중심으로 해석하세요.**")
    lines.append("")
    lines.append("| 조직 | 활성개발자수 | Hexa Index 추세 방향 | slope | p-value | 판정 | 유의미 개선지표 | 유의미 악화지표 |")
    lines.append("|------|------------|---------------------|-------|---------|------|----------------|----------------|")
    for res in results:
        g = res["group"]
        hc = res["mean_headcount"]
        ht = res["hexa_trend"]
        sig = res["significant_metrics"]
        n_imp = sum(1 for v in sig.values() if v["slope"] > 0)
        n_det = sum(1 for v in sig.values() if v["slope"] <= 0)
        if ht:
            slope = ht["slope"]
            p = ht["p_value"]
            trend_str = "📈 개선" if slope > 0 else "📉 악화"
            sig_str = "**유의미**" if p < 0.1 else "무의미"
        else:
            trend_str = "-"
            slope = float("nan")
            p = float("nan")
            sig_str = "-"
        lines.append(
            f"| {g} | {hc:.0f}명 | {trend_str} | "
            f"{slope:.4f} | {format_pval(p) if not np.isnan(p) else '-'} | "
            f"{sig_str} | {n_imp}개 | {n_det}개 |"
        )
    
    lines.append("")
    lines.append(f"\n> 분석도구: Python (uv), pandas, scipy, numpy  |  분석기준일: {now}")
    
    return "\n".join(lines)


def main():
    print("=== Hexa Index 분석 시작 ===")
    
    # 지표 설정 로드
    metrics = load_metrics_config()
    print(f"분석 지표 수: {len(metrics)}개 (제외예정 제외)")
    
    # 데이터 로드
    df = load_and_preprocess()
    print(f"전처리 후 데이터: {df.shape}")
    
    # 그룹별 분석
    results = []
    excluded_groups = []
    
    for group in df["GROUP"].unique():
        gdf = df[df["GROUP"] == group].copy()
        mean_hc = pd.to_numeric(gdf["활성개발자수"], errors="coerce").mean()
        
        if mean_hc < 10:
            excluded_groups.append((group, mean_hc))
            print(f"  [제외] {group}: 평균 활성개발자수 {mean_hc:.1f}명 < 10명")
            continue
        
        print(f"  [분석] {group}: 평균 활성개발자수 {mean_hc:.1f}명, {len(gdf)}일 데이터")
        result = analyze_group(group, gdf, metrics)
        results.append(result)
    
    # PARTNER_TOTAL을 맨 앞으로
    results.sort(key=lambda x: (0 if x["group"] == "PARTNER_TOTAL" else 1, x["group"]))
    
    print(f"\n분석 완료: {len(results)}개 조직")
    
    for res in results:
        ht = res["hexa_trend"]
        g = res["group"]
        hi_e = res["hexa_index_early"]
        hi_r = res["hexa_index_recent"]
        sig_count = len(res["significant_metrics"])
        if ht:
            trend = "개선" if ht["slope"] > 0 else "악화"
            p = ht["p_value"]
            sig_str = f"(p={p:.4f}, {'유의미' if p < 0.1 else '무의미'})"
        else:
            trend, sig_str = "-", ""
        print(f"  {g}: Hexa Index 초기→최근={hi_e:.2f}→{hi_r:.2f}, 추세={trend}{sig_str}, 유의미지표={sig_count}개")
    
    # Markdown 생성
    md_content = generate_markdown(results, metrics)
    output_path = "collab_daily.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n결과 저장: {output_path}")


if __name__ == "__main__":
    main()
