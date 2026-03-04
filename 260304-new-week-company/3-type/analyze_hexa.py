"""
Hexa Index Weekly Analysis Script
- Excludes Lunar New Year holiday week (2026-02-16 ~ 2026-02-20)
- Only includes organizations with active head count >= 10
- Tests for significant changes using p-value threshold 0.1
- Hexa Index calculation: percentile-based composite score
"""

import pandas as pd
import numpy as np
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 1. Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv('weeklyWeekHexa_202603041516.csv', encoding='utf-8-sig')
df['snapdate'] = pd.to_datetime(df['snapdate'])

# Load metric definitions
with open('hexa-metrics.json') as f:
    hexa_json = json.load(f)

# Map metric name → sign  (+1 = higher is better, -1 = lower is better)
metric_sign = {v['name']: v['sign'] for v in hexa_json['hexaAdminMap'].values()}

# ── 2. Exclude Lunar New Year holiday week (snapdate 2026-02-16) ───────────────
holiday_dates = pd.to_datetime(['2026-02-16'])
df = df[~df['snapdate'].isin(holiday_dates)].copy()

# ── 3. Identify metric columns (present in both CSV and JSON) ─────────────────
non_metric_cols = {'GROUP', 'snapdate'}
csv_metric_cols = [c for c in df.columns if c not in non_metric_cols]
valid_metrics = [c for c in csv_metric_cols if c in metric_sign]

print(f"Valid metrics for Hexa Index: {len(valid_metrics)}")

# ── 4. Convert metric columns to numeric ──────────────────────────────────────
for col in valid_metrics:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ── 5. Hexa Index Calculation ─────────────────────────────────────────────────
#
# Formula (per metric, per row):
#   1. percentile_rank = rank(value, across all rows) / total_rows * 100
#   2. adjusted = percentile_rank if sign == +1  (higher value → higher score)
#                 100 - percentile_rank if sign == -1  (lower value → higher score)
#   3. hexa_index = mean(adjusted) across all valid metrics for that row
#
# Rationale: Percentile-based normalization is robust to outliers and ensures
# all metrics are on a comparable 0–100 scale before averaging.

def compute_hexa_index(data, metrics, sign_map):
    """Compute Hexa Index for each row as mean percentile score."""
    scores = pd.DataFrame(index=data.index)
    for col in metrics:
        sign = sign_map[col]
        # Percentile rank (0-100), NaN values excluded from ranking
        pct = data[col].rank(pct=True, na_option='keep') * 100
        if sign == -1:
            pct = 100 - pct  # Lower raw value → higher score
        scores[col] = pct
    return scores.mean(axis=1)  # Row-wise mean across all metrics

df['hexa_index'] = compute_hexa_index(df, valid_metrics, metric_sign)

# ── 6. Filter organizations by active head count >= 10 ────────────────────────
#
# "활성개발자수" column represents active developer head count.
# We include only organizations where the MOST RECENT week's active count >= 10.
# This ensures we analyze only sufficiently active teams.

headcount_col = '활성개발자수'
# Get latest available snapdate per group (excluding current analysis week)
latest_headcount = (
    df.groupby('GROUP')
    .apply(lambda g: g.sort_values('snapdate').iloc[-1][headcount_col])
    .reset_index()
)
latest_headcount.columns = ['GROUP', 'latest_headcount']
active_groups = latest_headcount[latest_headcount['latest_headcount'] >= 10]['GROUP'].tolist()

print(f"\nGroups with active head count >= 10: {active_groups}")

# ── 7. Statistical significance testing ───────────────────────────────────────
#
# For each group and each metric:
#   - "Baseline": all weeks except the most recent week
#   - "Latest": the most recent week's value
#   - Test: One-sample t-test comparing the most recent value against the 
#     distribution of baseline values
#   - p-value < 0.1 → significant change
#   - Direction: compare latest value vs baseline mean, adjusted by sign

def test_metric_change(group_df, metric, sign):
    """
    Test if latest week's metric value is significantly different from baseline.
    
    Returns: (latest_val, baseline_mean, z_score, p_value, direction)
    direction: 'improved' | 'worsened' | 'no_change'
    """
    group_df = group_df.sort_values('snapdate')
    latest = group_df.iloc[-1]
    baseline = group_df.iloc[:-1]
    
    latest_val = latest[metric]
    baseline_vals = baseline[metric].dropna()
    
    if len(baseline_vals) < 3 or pd.isna(latest_val):
        return None
    
    baseline_mean = baseline_vals.mean()
    baseline_std = baseline_vals.std()
    
    if baseline_std == 0:
        return None
    
    # One-sample t-test: is latest_val an outlier compared to baseline?
    t_stat, p_value = stats.ttest_1samp(baseline_vals, latest_val)
    
    # z-score of latest value relative to baseline
    z_score = (latest_val - baseline_mean) / baseline_std
    
    # Determine direction of change (good vs bad)
    # sign=+1: higher is better; sign=-1: lower is better
    if p_value < 0.1:
        raw_improvement = (latest_val - baseline_mean) * sign
        direction = 'improved' if raw_improvement > 0 else 'worsened'
    else:
        direction = 'no_change'
    
    return {
        'latest_val': latest_val,
        'baseline_mean': baseline_mean,
        'baseline_std': baseline_std,
        'z_score': z_score,
        'p_value': p_value,
        'direction': direction,
        'pct_change': (latest_val - baseline_mean) / abs(baseline_mean) * 100 if baseline_mean != 0 else 0,
    }

# ── 8. Hexa Index trend analysis ──────────────────────────────────────────────
results = {}
for group in active_groups:
    gdf = df[df['GROUP'] == group].copy().sort_values('snapdate')
    
    if len(gdf) < 4:
        continue
    
    # Hexa index trend test
    hexa_vals = gdf['hexa_index'].dropna()
    latest_hexa = gdf.iloc[-1]['hexa_index']
    baseline_hexa = gdf.iloc[:-1]['hexa_index'].dropna()
    
    hexa_test = None
    if len(baseline_hexa) >= 3:
        t_stat, p_value = stats.ttest_1samp(baseline_hexa, latest_hexa)
        z_score = (latest_hexa - baseline_hexa.mean()) / baseline_hexa.std() if baseline_hexa.std() > 0 else 0
        hexa_test = {
            'latest': latest_hexa,
            'baseline_mean': baseline_hexa.mean(),
            'baseline_std': baseline_hexa.std(),
            'z_score': z_score,
            'p_value': p_value,
            'direction': ('improved' if latest_hexa > baseline_hexa.mean() else 'worsened') if p_value < 0.1 else 'no_change',
        }
    
    # Per-metric analysis
    metric_results = {}
    for metric in valid_metrics:
        sign = metric_sign[metric]
        res = test_metric_change(gdf, metric, sign)
        if res:
            metric_results[metric] = res
    
    results[group] = {
        'hexa': hexa_test,
        'metrics': metric_results,
        'latest_date': gdf.iloc[-1]['snapdate'],
        'latest_headcount': gdf.iloc[-1][headcount_col],
        'hexa_history': gdf[['snapdate', 'hexa_index', headcount_col]].to_dict('records'),
    }

# ── 9. Generate Markdown Report ───────────────────────────────────────────────
def fmt_val(v, digits=2):
    if pd.isna(v):
        return 'N/A'
    return f"{v:.{digits}f}"

lines = []
lines.append("# Weekly Hexa Index 분석 보고서")
lines.append("")
lines.append(f"**분석 기준일:** {df['snapdate'].max().strftime('%Y-%m-%d')} (최근 주)")
lines.append(f"**분석 데이터 범위:** {df['snapdate'].min().strftime('%Y-%m-%d')} ~ {df['snapdate'].max().strftime('%Y-%m-%d')}")
lines.append("")
lines.append("## 분석 방법론")
lines.append("")
lines.append("### Hexa Index 계산 방법")
lines.append("")
lines.append("```")
lines.append("1. 각 지표별 퍼센타일 순위 계산:")
lines.append("   percentile_rank = rank(value) / total_rows × 100  (0~100)")
lines.append("")
lines.append("2. 방향성 보정 (sign 적용):")
lines.append("   adjusted = percentile_rank         (sign = +1, 높을수록 좋음)")
lines.append("   adjusted = 100 - percentile_rank   (sign = -1, 낮을수록 좋음)")
lines.append("")
lines.append("3. Hexa Index = mean(adjusted) across all valid metrics")
lines.append("   → 값이 높을수록 전반적으로 더 좋은 상태를 의미함")
lines.append("```")
lines.append("")
lines.append("### 유의미성 검정 방법")
lines.append("")
lines.append("```")
lines.append("- 기준선: 최근 주를 제외한 모든 주의 값")
lines.append("- 검정 방법: One-sample t-test (최근 주 값 vs 기준선 분포)")
lines.append("- 유의수준: p-value < 0.1 → 유의미한 변화")
lines.append("- z-score = (최근값 - 기준선 평균) / 기준선 표준편차")
lines.append("- 개선/악화 판단: (최근값 - 기준선 평균) × sign > 0 → 개선, < 0 → 악화")
lines.append("```")
lines.append("")
lines.append("### 분석 제외 조건")
lines.append("")
lines.append("- **설 연휴 주 제외**: 2026-02-16 주 (2/16~2/20 연휴)")
lines.append("- **조직 포함 기준**: 최근 주 활성개발자수 ≥ 10명")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 분석 대상 조직")
lines.append("")

# Table of analyzed groups
lines.append("| 조직 | 최근 주 활성개발자수 | Hexa Index (최근) | Hexa Index (기준선 평균) | 변화 방향 | p-value |")
lines.append("|------|-------------------|-----------------|-----------------------|---------|---------|")

for group in active_groups:
    if group not in results:
        continue
    r = results[group]
    h = r['hexa']
    if h:
        direction_ko = {'improved': '📈 개선', 'worsened': '📉 악화', 'no_change': '➡️ 유의미하지 않음'}[h['direction']]
        sig_mark = '**' if h['p_value'] < 0.1 else ''
        lines.append(f"| {group} | {int(r['latest_headcount'])} | {fmt_val(h['latest'])} | {fmt_val(h['baseline_mean'])} | {sig_mark}{direction_ko}{sig_mark} | {fmt_val(h['p_value'], 3)} |")

lines.append("")
lines.append("---")
lines.append("")

# Detailed per-group analysis
for group in active_groups:
    if group not in results:
        continue
    r = results[group]
    h = r['hexa']
    latest_date = r['latest_date'].strftime('%Y-%m-%d')
    
    lines.append(f"## {group}")
    lines.append("")
    lines.append(f"- **분석 기준 주**: {latest_date}")
    lines.append(f"- **활성개발자수**: {int(r['latest_headcount'])}명")
    
    if h:
        lines.append(f"- **Hexa Index (최근)**: {fmt_val(h['latest'])}")
        lines.append(f"- **Hexa Index (기준선 평균 ± 표준편차)**: {fmt_val(h['baseline_mean'])} ± {fmt_val(h['baseline_std'])}")
        lines.append(f"- **z-score**: {fmt_val(h['z_score'])}")
        lines.append(f"- **p-value**: {fmt_val(h['p_value'], 3)}")
        dir_ko = {'improved': '📈 **유의미하게 개선됨** (p < 0.1)', 
                  'worsened': '📉 **유의미하게 악화됨** (p < 0.1)',
                  'no_change': '➡️ 유의미한 변화 없음 (p ≥ 0.1)'}[h['direction']]
        lines.append(f"- **Hexa Index 변화**: {dir_ko}")
    
    lines.append("")
    
    # Hexa Index time series (recent 10 weeks)
    lines.append("### Hexa Index 추이 (최근 10주)")
    lines.append("")
    lines.append("| 주차 | Hexa Index | 활성개발자수 |")
    lines.append("|------|-----------|------------|")
    for row in r['hexa_history'][-10:]:
        date_str = pd.to_datetime(row['snapdate']).strftime('%Y-%m-%d')
        hexa_str = fmt_val(row['hexa_index'])
        hc_str = str(int(row[headcount_col])) if not pd.isna(row[headcount_col]) else 'N/A'
        lines.append(f"| {date_str} | {hexa_str} | {hc_str} |")
    
    lines.append("")
    
    # Significant metric changes
    sig_improved = [(m, v) for m, v in r['metrics'].items() if v['direction'] == 'improved']
    sig_worsened = [(m, v) for m, v in r['metrics'].items() if v['direction'] == 'worsened']
    
    # Sort by p-value (most significant first)
    sig_improved.sort(key=lambda x: x[1]['p_value'])
    sig_worsened.sort(key=lambda x: x[1]['p_value'])
    
    if sig_improved:
        lines.append("### 📈 유의미하게 개선된 지표 (p < 0.1)")
        lines.append("")
        lines.append("| 지표 | 최근값 | 기준선 평균 | 변화율(%) | z-score | p-value | sign |")
        lines.append("|------|-------|-----------|---------|--------|---------|------|")
        for metric, v in sig_improved[:15]:  # top 15
            sign_str = '↑ 좋음' if metric_sign[metric] == 1 else '↓ 좋음'
            lines.append(f"| {metric} | {fmt_val(v['latest_val'])} | {fmt_val(v['baseline_mean'])} | {fmt_val(v['pct_change'])}% | {fmt_val(v['z_score'])} | {fmt_val(v['p_value'], 3)} | {sign_str} |")
        lines.append("")
    
    if sig_worsened:
        lines.append("### 📉 유의미하게 악화된 지표 (p < 0.1)")
        lines.append("")
        lines.append("| 지표 | 최근값 | 기준선 평균 | 변화율(%) | z-score | p-value | sign |")
        lines.append("|------|-------|-----------|---------|--------|---------|------|")
        for metric, v in sig_worsened[:15]:  # top 15
            sign_str = '↑ 좋음' if metric_sign[metric] == 1 else '↓ 좋음'
            lines.append(f"| {metric} | {fmt_val(v['latest_val'])} | {fmt_val(v['baseline_mean'])} | {fmt_val(v['pct_change'])}% | {fmt_val(v['z_score'])} | {fmt_val(v['p_value'], 3)} | {sign_str} |")
        lines.append("")
    
    if not sig_improved and not sig_worsened:
        lines.append("### 유의미한 지표 변화 없음")
        lines.append("")
        lines.append("> 모든 지표가 p ≥ 0.1 수준으로 유의미한 변화를 보이지 않았습니다.")
        lines.append("")
    
    lines.append("---")
    lines.append("")

# ── 10. Overall summary ───────────────────────────────────────────────────────
lines.append("## 전체 요약")
lines.append("")
lines.append("### Hexa Index 기준 조직별 상태")
lines.append("")

improved_groups = [g for g in active_groups if g in results and results[g]['hexa'] and results[g]['hexa']['direction'] == 'improved']
worsened_groups = [g for g in active_groups if g in results and results[g]['hexa'] and results[g]['hexa']['direction'] == 'worsened']
stable_groups = [g for g in active_groups if g in results and results[g]['hexa'] and results[g]['hexa']['direction'] == 'no_change']

if improved_groups:
    lines.append(f"- **📈 유의미하게 개선**: {', '.join(improved_groups)}")
if worsened_groups:
    lines.append(f"- **📉 유의미하게 악화**: {', '.join(worsened_groups)}")
if stable_groups:
    lines.append(f"- **➡️ 유의미한 변화 없음**: {', '.join(stable_groups)}")

lines.append("")
lines.append("### 가장 많이 변화한 지표 TOP 10 (전체 조직 기준)")
lines.append("")

# Aggregate across all groups
all_metric_changes = {}
for group in active_groups:
    if group not in results:
        continue
    for metric, v in results[group]['metrics'].items():
        if v['direction'] in ('improved', 'worsened'):
            if metric not in all_metric_changes:
                all_metric_changes[metric] = {'improved': 0, 'worsened': 0, 'min_p': 1.0}
            all_metric_changes[metric][v['direction']] += 1
            all_metric_changes[metric]['min_p'] = min(all_metric_changes[metric]['min_p'], v['p_value'])

# Sort by total significant counts
sorted_metrics = sorted(all_metric_changes.items(), 
                        key=lambda x: x[1]['improved'] + x[1]['worsened'], reverse=True)

lines.append("| 지표 | 개선 조직 수 | 악화 조직 수 | 최소 p-value |")
lines.append("|------|-----------|-----------|------------|")
for metric, counts in sorted_metrics[:10]:
    lines.append(f"| {metric} | {counts['improved']} | {counts['worsened']} | {fmt_val(counts['min_p'], 3)} |")

lines.append("")

report = '\n'.join(lines)
with open('collab_weekly.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("\n=== Analysis Complete ===")
print(f"Report written to collab_weekly.md")
print(f"\nSummary:")
print(f"  Improved groups: {improved_groups}")
print(f"  Worsened groups: {worsened_groups}")
print(f"  Stable groups: {stable_groups}")
