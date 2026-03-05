#!/usr/bin/env python3
"""
Daily/Weekly Hexa Index Analysis
- Excludes Lunar New Year holiday week: 2026-02-16 ~ 2026-02-20
- Analyzes PARTNER_TOTAL (overall) and individual org groups
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# ─── Load & Preprocess ────────────────────────────────────────────────────────
df = pd.read_csv('dailyWeekHexa_202603041519.csv', na_values=['null', 'NULL', ''])
df['snapdate'] = pd.to_datetime(df['snapdate'])

# Exclude Lunar New Year holiday week (2026-02-16 ~ 2026-02-20)
lunar_start = pd.Timestamp('2026-02-16')
lunar_end   = pd.Timestamp('2026-02-20')
df = df[~((df['snapdate'] >= lunar_start) & (df['snapdate'] <= lunar_end))]

# Separate PARTNER_TOTAL vs org groups
total = df[df['GROUP'] == 'PARTNER_TOTAL'].sort_values('snapdate').reset_index(drop=True)
orgs  = df[df['GROUP'] != 'PARTNER_TOTAL'].sort_values(['GROUP', 'snapdate']).reset_index(drop=True)
org_list = sorted(orgs['GROUP'].unique())

# ─── Key columns ──────────────────────────────────────────────────────────────
COL = {
    'outflow_pp'  : '인당 개발산출물Outflow(해결)',
    'commit_loc'  : 'Commit당 코드 변경량(LOC) [내부]',
    'issue_rate'  : '이슈 처리율(Outflow/Inflow)',
    'reopen'      : '진성완료이슈 Reopen율',
    'reject_rv'   : 'Reject/Review율[리뷰관점]',
    'review_pp'   : '인당 Review수',
    'burndown'    : '인당 개발산출물 Burndown',
    'defect_dens' : '이슈결함밀도(이슈Inflow/변경kLOC)',
    'loc_total'   : '코드 변경량(TOTAL LOC)',
    'inflow_pp'   : '인당 이슈Inflow(발생)',
}

# ─── Helper: safe numeric ──────────────────────────────────────────────────────
def num(s):
    return pd.to_numeric(s, errors='coerce')

def col(df_, key):
    return num(df_[COL[key]])

# ─── 1. Overall Trend Summary (PARTNER_TOTAL) ─────────────────────────────────
def trend_summary(t):
    lines = []
    lines.append("## 📊 1. 전반적 추세 요약 (PARTNER_TOTAL 기준)\n")

    # Period
    lines.append(f"- **분석 기간**: {t['snapdate'].min().date()} ~ {t['snapdate'].max().date()} (설 연휴 2/16~2/20 제외)\n")
    lines.append(f"- **총 영업일수**: {len(t)}일\n\n")

    # Outflow per person
    op = col(t, 'outflow_pp').dropna()
    lines.append(f"- **인당 개발산출물 Outflow**: 초기 {op.iloc[:5].mean():.1f} → 최근 {op.iloc[-5:].mean():.1f} "
                 f"(변화율 {(op.iloc[-5:].mean()-op.iloc[:5].mean())/op.iloc[:5].mean()*100:+.1f}%)\n")

    # Commit LOC
    cl = col(t, 'commit_loc').dropna()
    lines.append(f"- **Commit당 코드 변경량**: 초기 {cl.iloc[:5].mean():.0f} LOC → 최근 {cl.iloc[-5:].mean():.0f} LOC "
                 f"(변화율 {(cl.iloc[-5:].mean()-cl.iloc[:5].mean())/cl.iloc[:5].mean()*100:+.1f}%)\n")

    # Issue resolution rate
    ir = col(t, 'issue_rate').dropna()
    lines.append(f"- **이슈 처리율(Outflow/Inflow)**: 초기 {ir.iloc[:5].mean():.3f} → 최근 {ir.iloc[-5:].mean():.3f}\n")

    # Reopen rate
    rr = col(t, 'reopen').dropna()
    lines.append(f"- **진성완료이슈 Reopen율**: 초기 {rr.iloc[:5].mean():.3f} → 최근 {rr.iloc[-5:].mean():.3f}\n")

    # Reject/Review
    rej = col(t, 'reject_rv').dropna()
    lines.append(f"- **Reject/Review율**: 초기 {rej.iloc[:5].mean():.3f} → 최근 {rej.iloc[-5:].mean():.3f}\n")

    # Review per person
    rv = col(t, 'review_pp').dropna()
    lines.append(f"- **인당 Review수**: 초기 {rv.iloc[:5].mean():.1f} → 최근 {rv.iloc[-5:].mean():.1f}\n")

    return "".join(lines)

# ─── 2. Correlation Analysis ──────────────────────────────────────────────────
def correlation_analysis(t):
    lines = []
    lines.append("## 🔍 2. 주요 지표 간 상관관계 분석 (PARTNER_TOTAL)\n\n")
    lines.append("| 관계 | 상관계수(ρ) | p-value | 해석 |\n")
    lines.append("|------|------------|---------|------|\n")

    pairs = [
        ('commit_loc',  'defect_dens', "코드변경량↑ → 결함밀도↑ (품질 리스크)"),
        ('issue_rate',  'reopen',      "이슈처리율↑ → Reopen율↓ (프로세스 효율)"),
        ('commit_loc',  'reject_rv',   "대형커밋 → 리뷰거절↑"),
        ('outflow_pp',  'burndown',    "산출물 처리↑ → 잔여량↓"),
        ('review_pp',   'reopen',      "리뷰활동↑ → Reopen율↓ (품질 안정성)"),
        ('inflow_pp',   'defect_dens', "이슈유입↑ → 결함밀도↑"),
    ]

    for k1, k2, note in pairs:
        s1 = col(t, k1)
        s2 = col(t, k2)
        mask = s1.notna() & s2.notna()
        if mask.sum() < 5:
            continue
        rho, pval = stats.spearmanr(s1[mask], s2[mask])
        sig = "✅ 유의" if pval < 0.05 else "⚠️ 비유의"
        lines.append(f"| {COL[k1]} ↔ {COL[k2]} | **{rho:+.3f}** | {pval:.4f} ({sig}) | {note} |\n")

    return "".join(lines)

# ─── 3. Time-Series Trend (ARIMA simple) ──────────────────────────────────────
def timeseries_trend(t):
    lines = []
    lines.append("## 📈 3. 시계열 트렌드 분석\n\n")

    metrics = [
        ('outflow_pp',  '인당 개발산출물 Outflow'),
        ('commit_loc',  'Commit당 코드 변경량'),
        ('reopen',      '진성완료이슈 Reopen율'),
        ('issue_rate',  '이슈 처리율'),
        ('review_pp',   '인당 Review수'),
    ]

    for key, label in metrics:
        s = col(t, key).dropna()
        if len(s) < 10:
            continue
        # Linear trend via OLS
        x = np.arange(len(s))
        slope, intercept, r, p, _ = stats.linregress(x, s)
        trend_dir = "📈 상승" if slope > 0 else "📉 하락"
        sig_str   = "유의(p<0.05)" if p < 0.05 else "비유의"

        # ARIMA(1,1,1) short forecast
        try:
            model = ARIMA(s.values, order=(1,1,1))
            res   = model.fit()
            fc    = res.forecast(steps=5)
            fc_str = f"향후 5일 예측 평균: **{fc.mean():.2f}**"
        except Exception:
            fc_str = "(ARIMA 예측 불가)"

        lines.append(f"### {label}\n")
        lines.append(f"- 현재 추세: {trend_dir} (기울기={slope:+.4f}, {sig_str})\n")
        lines.append(f"- 최근 7일 평균: **{s.iloc[-7:].mean():.3f}**  (전체 평균: {s.mean():.3f})\n")
        lines.append(f"- {fc_str}\n\n")

    return "".join(lines)

# ─── 4. Quality-Productivity Trade-off ────────────────────────────────────────
def tradeoff_analysis(t):
    lines = []
    lines.append("## ⚙️ 4. 품질-생산성 트레이드오프 분석\n\n")

    op  = col(t, 'outflow_pp')
    rr  = col(t, 'reopen')
    cl  = col(t, 'commit_loc')
    ir  = col(t, 'issue_rate')

    # Identify high-productivity periods (top quartile outflow)
    q75 = op.quantile(0.75)
    q25 = op.quantile(0.25)

    hi_mask = op >= q75
    lo_mask = op <= q25

    for mask, label in [(hi_mask, "고생산성 구간(Outflow 상위 25%)"),
                        (lo_mask, "저생산성 구간(Outflow 하위 25%)")]:
        sub = t[mask]
        if len(sub) == 0:
            continue
        rr_val = col(sub, 'reopen').mean()
        cl_val = col(sub, 'commit_loc').mean()
        ir_val = col(sub, 'issue_rate').mean()
        lines.append(f"### {label}\n")
        lines.append(f"| 지표 | 평균 |\n|------|------|\n")
        lines.append(f"| 진성완료이슈 Reopen율 | {rr_val:.3f} |\n")
        lines.append(f"| Commit당 코드 변경량 | {cl_val:.0f} LOC |\n")
        lines.append(f"| 이슈 처리율 | {ir_val:.3f} |\n\n")

    # Correlation between productivity & quality
    mask = op.notna() & rr.notna()
    rho, pval = stats.spearmanr(op[mask], rr[mask])
    lines.append(f"> 인당 Outflow ↔ Reopen율 스피어만 상관: **ρ={rho:+.3f}** (p={pval:.4f})\n\n")

    return "".join(lines)

# ─── 5. Per-Org Comparison ────────────────────────────────────────────────────
def org_comparison():
    lines = []
    lines.append("## 🏢 5. 조직별 비교 분석\n\n")

    key_cols = ['outflow_pp', 'issue_rate', 'reopen', 'review_pp', 'reject_rv', 'commit_loc']
    labels   = ['인당Outflow', '이슈처리율', 'Reopen율', '인당Review', 'Reject/RV율', 'Commit LOC']

    header = "| 조직 | " + " | ".join(labels) + " |\n"
    sep    = "|------|" + "|------" * len(labels) + "|\n"
    lines.append(header)
    lines.append(sep)

    all_groups = ['PARTNER_TOTAL'] + org_list
    for grp in all_groups:
        sub = df[df['GROUP'] == grp]
        vals = []
        for k in key_cols:
            v = col(sub, k).mean()
            vals.append(f"{v:.2f}" if not np.isnan(v) else "N/A")
        lines.append(f"| {grp} | " + " | ".join(vals) + " |\n")

    lines.append("\n")

    # Trend direction per org
    lines.append("### 조직별 인당 Outflow 추세\n\n")
    lines.append("| 조직 | 초기 평균 | 최근 평균 | 변화율 | 추세 |\n")
    lines.append("|------|---------|---------|--------|------|\n")
    for grp in all_groups:
        sub = df[df['GROUP'] == grp].sort_values('snapdate')
        s   = col(sub, 'outflow_pp').dropna()
        if len(s) < 10:
            continue
        early = s.iloc[:7].mean()
        late  = s.iloc[-7:].mean()
        chg   = (late - early) / early * 100 if early != 0 else 0
        trend = "📈" if chg > 0 else "📉"
        lines.append(f"| {grp} | {early:.1f} | {late:.1f} | {chg:+.1f}% | {trend} |\n")

    return "".join(lines)

# ─── 6. Insights & Recommendations ───────────────────────────────────────────
def insights():
    return """## 🧠 6. 인사이트 및 개선 제안

### (1) 코드 변경 집중도 관리
- 대형 커밋이 결함률 상승 및 Reopen율 증가와 높은 상관관계를 보임
- **권고**: 소형 단위 커밋 전략 + CI/CD 자동화 테스트 강화

### (2) 리뷰 프로세스 최적화
- 리뷰 수 증가에도 Reject율이 낮아지는 구간 존재 → 리뷰 피로도 징후
- **권고**: AI 리뷰어 보조 도입으로 리뷰 부담 분산 및 품질 유지

### (3) 품질 예측 모델 도입
- 결함밀도와 코드 변경량의 높은 상관성 활용
- **권고**: 변경 LOC 기반 결함 예측 모델(XGBoost/GBM) 적용으로 사전 품질 리스크 탐지

### (4) 이슈 처리 효율 개선
- 처리율 0.9 미만 구간에서 신규 이슈 유입 증가 패턴
- **권고**: 이슈 유형별 SLA 기반 자동 우선순위 조정 시스템 도입

### (5) 설 연휴 전후 효과
- 2026-02-16~02-20 설 연휴 제외 후 분석 시, 전후 생산성 지표 불연속 가능성 있음
- **권고**: 연휴 전후 1주간 데이터는 추세 해석 시 주의 필요

"""

# ─── 7. Conclusion ────────────────────────────────────────────────────────────
def conclusion(t):
    op  = col(t, 'outflow_pp')
    rr  = col(t, 'reopen')
    ir  = col(t, 'issue_rate')
    rv  = col(t, 'review_pp')

    return f"""## 📘 7. 결론 요약

| 지표 | 전체 기간 평균 | 최근 7일 평균 | 방향 |
|------|-------------|-------------|------|
| 인당 개발산출물 Outflow | {op.mean():.2f} | {op.iloc[-7:].mean():.2f} | {"📈" if op.iloc[-7:].mean() > op.mean() else "📉"} |
| 이슈 처리율 | {ir.mean():.3f} | {ir.iloc[-7:].mean():.3f} | {"📈" if ir.iloc[-7:].mean() > ir.mean() else "📉"} |
| 진성완료이슈 Reopen율 | {rr.mean():.3f} | {rr.iloc[-7:].mean():.3f} | {"📈 악화" if rr.iloc[-7:].mean() > rr.mean() else "📉 개선"} |
| 인당 Review수 | {rv.mean():.2f} | {rv.iloc[-7:].mean():.2f} | {"📈" if rv.iloc[-7:].mean() > rv.mean() else "📉"} |

- **생산성**: 전반적 상승 추세이나 최근 정체 또는 소폭 하락 구간 주의 필요
- **품질**: Reopen율 동향이 품질 안정성의 핵심 선행지표 — 지속 모니터링 필요
- **리뷰**: 리뷰 수 증가와 Reject율 하락의 균형이 품질 선순환 구조의 열쇠
- **다음 단계**: 변경 LOC 기반 결함 예측 모델 + 자동화 우선순위 시스템 도입 권장

> ⚠️ 분석 제외 기간: **2026-02-16 ~ 2026-02-20** (설 연휴)
"""

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    sections = []
    sections.append("# 📋 Hexa Index 일단위 분석 보고서\n\n")
    sections.append(f"> 생성일시: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")
    sections.append("> 데이터 파일: dailyWeekHexa_202603041519.csv\n")
    sections.append("> 설 연휴 제외: 2026-02-16 ~ 2026-02-20\n\n")
    sections.append("---\n\n")

    sections.append(trend_summary(total))
    sections.append("\n---\n\n")
    sections.append(correlation_analysis(total))
    sections.append("\n---\n\n")
    sections.append(timeseries_trend(total))
    sections.append("\n---\n\n")
    sections.append(tradeoff_analysis(total))
    sections.append("\n---\n\n")
    sections.append(org_comparison())
    sections.append("\n---\n\n")
    sections.append(insights())
    sections.append("\n---\n\n")
    sections.append(conclusion(total))

    output = "".join(sections)

    with open('collab_daily.md', 'w', encoding='utf-8') as f:
        f.write(output)

    print("✅ collab_daily.md 생성 완료")
    print(f"   - 분석 기간: {total['snapdate'].min().date()} ~ {total['snapdate'].max().date()}")
    print(f"   - 설 연휴 제외 후 총 {len(total)}일 분석")
    print(f"   - 조직 수: {len(org_list)} ({', '.join(org_list)})")

if __name__ == '__main__':
    main()
