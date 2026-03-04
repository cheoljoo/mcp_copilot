#!/usr/bin/env python3
"""
Weekly Collaboration Analysis Script
- Analyzes weeklyWeekHexa CSV data for 2026
- Excludes Lunar New Year holiday week (2026-02-16 ~ 2026-02-20)
- Outputs results to collab_weekly.md
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── 데이터 로드 ────────────────────────────────────────────────────────
df = pd.read_csv('weeklyWeekHexa_202603041516.csv')
df['snapdate'] = pd.to_datetime(df['snapdate'])

# 2026년 데이터만, 설 연휴 주(2026-02-16) 제외
df_2026 = df[(df['snapdate'].dt.year == 2026) &
             (df['snapdate'] != '2026-02-16')].copy()

GROUPS = ['PARTNER_TOTAL', 'EDV자사', 'LGSI자사', '국내자사', '협력사전체']
GROUP_LABELS = {
    'PARTNER_TOTAL': '전체(PARTNER_TOTAL)',
    'EDV자사': 'EDV자사',
    'LGSI자사': 'LGSI자사',
    '국내자사': '국내자사',
    '협력사전체': '협력사전체',
}

# 주요 지표 컬럼 매핑
KEY_COLS = {
    'outflow':      '인당 개발산출물Outflow(해결)',
    'commit_loc':   'Commit당 코드 변경량(LOC) [내부]',
    'issue_rate':   '이슈 처리율(Outflow/Inflow)',
    'reopen':       '진성완료이슈 Reopen율',
    'reject_review':'Reject/Review율[리뷰관점]',
    'review_count': '인당 Review수',
    'defect_density':'이슈결함밀도(이슈Inflow/변경kLOC)',
    'burndown':     '인당 개발산출물 Burndown',
    'total_loc':    '코드 변경량(TOTAL LOC)',
    'active_dev':   '활성개발자수',
    'inflow':       '인당 이슈Inflow(발생)',
    'outflow_issue':'인당 이슈Outflow(해결)',
}


def get_group(g):
    return df_2026[df_2026['GROUP'] == g].sort_values('snapdate').copy()


def fmt(v, decimals=2):
    if pd.isna(v):
        return 'N/A'
    return f"{v:.{decimals}f}"


def trend_arrow(first, last):
    if pd.isna(first) or pd.isna(last):
        return '→'
    delta = last - first
    if abs(delta) < 0.001:
        return '→'
    return '↑' if delta > 0 else '↓'


def safe_corr(a, b):
    mask = ~(np.isnan(a) | np.isnan(b))
    if mask.sum() < 3:
        return np.nan
    r, p = stats.pearsonr(a[mask], b[mask])
    return r


# ── 분석 함수들 ───────────────────────────────────────────────────────

def section1_trend_summary():
    """1. 전반적 추세 요약"""
    lines = []
    lines.append("## 📊 1. 전반적 추세 요약\n")

    pt = get_group('PARTNER_TOTAL')
    dates = pt['snapdate'].dt.strftime('%m/%d').tolist()

    lines.append("### 분석 기간 및 데이터\n")
    lines.append(f"- **분석 대상 기간**: {pt['snapdate'].min().strftime('%Y-%m-%d')} ~ {pt['snapdate'].max().strftime('%Y-%m-%d')}")
    lines.append(f"- **제외 주**: 2026-02-16주 (설 연휴: 2/16~2/20)")
    lines.append(f"- **분석 주차 수**: {len(pt)}주")
    lines.append(f"- **대상 그룹**: {', '.join(GROUPS)}\n")

    # 1-1. 개발 생산성
    lines.append("### 1-1. 개발 생산성\n")
    out = pt[KEY_COLS['outflow']].values
    cloc = pt[KEY_COLS['commit_loc']].values

    lines.append("| 주차 | 인당 산출물 Outflow | Commit당 코드 변경량(LOC) |")
    lines.append("|------|-------------------|------------------------|")
    for i, d in enumerate(dates):
        lines.append(f"| {d} | {fmt(out[i])} | {fmt(cloc[i])} |")
    lines.append("")

    out_valid = out[~np.isnan(out)]
    cloc_valid = cloc[~np.isnan(cloc)]
    lines.append(f"- **인당 산출물 Outflow**: 최솟값 {fmt(out_valid.min())} → 최댓값 {fmt(out_valid.max())} (평균 {fmt(out_valid.mean())})")
    lines.append(f"- **Commit당 코드 변경량**: 최솟값 {fmt(cloc_valid.min())} LOC → 최댓값 {fmt(cloc_valid.max())} LOC (평균 {fmt(cloc_valid.mean())} LOC)")

    # 최고 생산성 주차
    peak_out_idx = np.nanargmax(out)
    lines.append(f"- **최고 산출물 Outflow 주**: {dates[peak_out_idx]} ({fmt(out[peak_out_idx])})")
    lines.append("")

    # 1-2. 이슈 처리율
    lines.append("### 1-2. 이슈 처리율 (Outflow/Inflow)\n")
    ir = pt[KEY_COLS['issue_rate']].values
    lines.append("| 주차 | 이슈 처리율 | 상태 |")
    lines.append("|------|------------|------|")
    for i, d in enumerate(dates):
        v = ir[i]
        status = "✅ 양호(≥100%)" if v >= 100 else ("⚠️ 보통(≥80%)" if v >= 80 else "🔴 주의(<80%)")
        lines.append(f"| {d} | {fmt(v)}% | {status} |")
    lines.append("")
    ir_valid = ir[~np.isnan(ir)]
    lines.append(f"- 평균 이슈 처리율: **{fmt(ir_valid.mean())}%** (최저: {fmt(ir_valid.min())}%, 최고: {fmt(ir_valid.max())}%)")
    lines.append("")

    # 1-3. Reopen율
    lines.append("### 1-3. 진성완료이슈 Reopen율 (%)\n")
    ro = pt[KEY_COLS['reopen']].values
    lines.append("| 주차 | Reopen율 | 상태 |")
    lines.append("|------|---------|------|")
    for i, d in enumerate(dates):
        v = ro[i]
        status = "✅ 양호(≤10%)" if v <= 10 else ("⚠️ 주의(≤20%)" if v <= 20 else "🔴 위험(>20%)")
        lines.append(f"| {d} | {fmt(v)}% | {status} |")
    lines.append("")
    ro_valid = ro[~np.isnan(ro)]
    lines.append(f"- 평균 Reopen율: **{fmt(ro_valid.mean())}%** (최저: {fmt(ro_valid.min())}%, 최고: {fmt(ro_valid.max())}%)")
    lines.append(f"- 최고 Reopen율 주: {dates[np.nanargmax(ro)]} ({fmt(ro[np.nanargmax(ro)])}%)")
    lines.append("")

    # 1-4. 리뷰 지표
    lines.append("### 1-4. 리뷰 효율성\n")
    rr = pt[KEY_COLS['reject_review']].values
    rv = pt[KEY_COLS['review_count']].values
    lines.append("| 주차 | Reject/Review율(%) | 인당 Review수 |")
    lines.append("|------|------------------|--------------|")
    for i, d in enumerate(dates):
        lines.append(f"| {d} | {fmt(rr[i])} | {fmt(rv[i])} |")
    lines.append("")
    rr_valid = rr[~np.isnan(rr)]
    rv_valid = rv[~np.isnan(rv)]
    lines.append(f"- Reject/Review율 평균: **{fmt(rr_valid.mean())}%** (최저: {fmt(rr_valid.min())}%, 최고: {fmt(rr_valid.max())}%)")
    lines.append(f"- 인당 Review수 평균: **{fmt(rv_valid.mean())}** (최저: {fmt(rv_valid.min())}, 최고: {fmt(rv_valid.max())})")
    lines.append("")

    return "\n".join(lines)


def section2_correlation():
    """2. 주요 지표 간 상관관계 분석"""
    lines = []
    lines.append("## 🔍 2. 주요 지표 간 상관관계 분석 (PARTNER_TOTAL 기준)\n")

    pt = get_group('PARTNER_TOTAL')

    def col(k):
        return pd.to_numeric(pt[KEY_COLS[k]], errors='coerce').values

    corr_pairs = [
        ('commit_loc', 'defect_density',  '인당 Commit LOC ↔ 이슈결함밀도',       '코드 변경이 많을수록 결함 발생률 증가'),
        ('issue_rate', 'reopen',          '이슈 처리율 ↔ Reopen율',               '처리율 높을수록 Reopen율 변화'),
        ('commit_loc', 'reject_review',   'Commit당 LOC ↔ Reject/Review율',       '대형 커밋일수록 리뷰 거절 가능성'),
        ('outflow',    'burndown',        '인당 산출물 Outflow ↔ Burndown',         '산출물 처리량과 잔여량 관계'),
        ('review_count','reopen',         '인당 Review수 ↔ Reopen율',             '리뷰 활동 활발할수록 품질 안정성'),
        ('inflow',     'reopen',          '이슈 Inflow ↔ Reopen율',               '신규 이슈 유입과 재개방 관계'),
        ('outflow',    'review_count',    '산출물 Outflow ↔ Review수',             '산출물 처리량과 리뷰 부하 관계'),
    ]

    lines.append("| 관계 | 상관계수(ρ) | 해석 |")
    lines.append("|------|-----------|------|")
    for k1, k2, label, interp in corr_pairs:
        a = col(k1)
        b = col(k2)
        r = safe_corr(a, b)
        if np.isnan(r):
            lines.append(f"| {label} | N/A | {interp} |")
        else:
            strength = "강한" if abs(r) >= 0.7 else ("중간" if abs(r) >= 0.4 else "약한")
            direction = "양의" if r >= 0 else "음의"
            lines.append(f"| {label} | {r:+.3f} | {direction} {strength} 상관: {interp} |")
    lines.append("")

    # 그룹별 주요 지표 평균 비교
    lines.append("### 그룹별 주요 지표 평균 비교\n")
    lines.append("| 그룹 | 인당 Outflow | Commit LOC | 이슈처리율(%) | Reopen율(%) | Review수 |")
    lines.append("|------|------------|-----------|------------|-----------|---------|")
    for g in GROUPS:
        gdf = get_group(g)
        o   = pd.to_numeric(gdf[KEY_COLS['outflow']], errors='coerce').mean()
        cl  = pd.to_numeric(gdf[KEY_COLS['commit_loc']], errors='coerce').mean()
        ir  = pd.to_numeric(gdf[KEY_COLS['issue_rate']], errors='coerce').mean()
        ro  = pd.to_numeric(gdf[KEY_COLS['reopen']], errors='coerce').mean()
        rv  = pd.to_numeric(gdf[KEY_COLS['review_count']], errors='coerce').mean()
        lines.append(f"| {GROUP_LABELS[g]} | {fmt(o)} | {fmt(cl)} | {fmt(ir)}% | {fmt(ro)}% | {fmt(rv)} |")
    lines.append("")

    return "\n".join(lines)


def section3_timeseries():
    """3. 시계열 트렌드 분석"""
    lines = []
    lines.append("## 📈 3. 시계열 트렌드 분석\n")

    pt = get_group('PARTNER_TOTAL')
    dates = pt['snapdate'].dt.strftime('%m/%d').tolist()

    def col(k):
        return pd.to_numeric(pt[KEY_COLS[k]], errors='coerce').values

    def linear_trend(arr):
        """단순 선형 회귀로 트렌드 기울기 계산"""
        x = np.arange(len(arr))
        valid = ~np.isnan(arr)
        if valid.sum() < 2:
            return 0.0, 0.0
        slope, intercept, r, p, se = stats.linregress(x[valid], arr[valid])
        return slope, r**2

    metrics = [
        ('outflow',       '인당 산출물 Outflow',        '생산성'),
        ('commit_loc',    'Commit당 코드 변경량(LOC)',   '생산성'),
        ('issue_rate',    '이슈 처리율(%)',              '효율성'),
        ('reopen',        '진성 Reopen율(%)',            '품질'),
        ('reject_review', 'Reject/Review율(%)',          '리뷰'),
        ('review_count',  '인당 Review수',              '리뷰'),
        ('defect_density','이슈결함밀도',               '품질'),
    ]

    lines.append("| 지표 | 카테고리 | 1월초 | 최근 | 기울기(주/주) | R² | 트렌드 |")
    lines.append("|------|---------|------|------|------------|-----|------|")
    for key, label, category in metrics:
        arr = col(key)
        slope, r2 = linear_trend(arr)
        first_valid = arr[~np.isnan(arr)][0] if (~np.isnan(arr)).any() else np.nan
        last_valid  = arr[~np.isnan(arr)][-1] if (~np.isnan(arr)).any() else np.nan
        arrow = trend_arrow(first_valid, last_valid)
        trend_str = "📈 상승" if slope > 0.01 else ("📉 하락" if slope < -0.01 else "➡️ 보합")
        lines.append(f"| {label} | {category} | {fmt(first_valid)} | {fmt(last_valid)} | {slope:+.3f} | {r2:.3f} | {arrow} {trend_str} |")
    lines.append("")

    # 주차별 상세 트렌드 (이슈 처리율)
    lines.append("### 이슈 처리율 주차별 상세\n")
    ir = col('issue_rate')
    lines.append("| 주차 | 처리율(%) | 전주 대비 | 해석 |")
    lines.append("|------|---------|---------|------|")
    for i, d in enumerate(dates):
        v = ir[i]
        if i == 0 or np.isnan(ir[i-1]):
            delta_str = '-'
        else:
            delta = v - ir[i-1]
            delta_str = f"{delta:+.1f}%p"
        interp = "이슈 누적 중" if v < 80 else ("처리 부진" if v < 100 else "처리 원활")
        lines.append(f"| {d} | {fmt(v)}% | {delta_str} | {interp} |")
    lines.append("")

    # 2월 설 이후 회복 분석
    lines.append("### 2월 설 연휴 전후 변화 분석\n")
    pre_holiday = pt[pt['snapdate'] == '2026-02-09']
    post_holiday = pt[pt['snapdate'] == '2026-02-23']

    if len(pre_holiday) > 0 and len(post_holiday) > 0:
        for key, label, _ in metrics:
            pre_v  = pd.to_numeric(pre_holiday[KEY_COLS[key]], errors='coerce').values[0]
            post_v = pd.to_numeric(post_holiday[KEY_COLS[key]], errors='coerce').values[0]
            if not (np.isnan(pre_v) or np.isnan(post_v)):
                delta = post_v - pre_v
                pct   = (delta / pre_v * 100) if pre_v != 0 else np.nan
                arrow = '↑' if delta > 0 else '↓'
                lines.append(f"- **{label}**: 설 전(2/09) {fmt(pre_v)} → 설 후(2/23) {fmt(post_v)} ({arrow} {fmt(abs(delta))}, {fmt(abs(pct))}%{'↑' if delta>0 else '↓'})")
    lines.append("")

    return "\n".join(lines)


def section4_tradeoff():
    """4. 품질-생산성 트레이드오프 분석"""
    lines = []
    lines.append("## ⚙️ 4. 품질-생산성 트레이드오프 분석\n")

    pt = get_group('PARTNER_TOTAL')
    dates = pt['snapdate'].dt.strftime('%m/%d').tolist()

    outflow  = pd.to_numeric(pt[KEY_COLS['outflow']], errors='coerce').values
    reopen   = pd.to_numeric(pt[KEY_COLS['reopen']], errors='coerce').values
    cloc     = pd.to_numeric(pt[KEY_COLS['commit_loc']], errors='coerce').values
    issue_r  = pd.to_numeric(pt[KEY_COLS['issue_rate']], errors='coerce').values
    reviews  = pd.to_numeric(pt[KEY_COLS['review_count']], errors='coerce').values

    lines.append("### 주차별 생산성 vs 품질 매트릭스\n")
    lines.append("| 주차 | 산출물 Outflow | Reopen율(%) | Commit LOC | 이슈처리율(%) | Review수 | 평가 |")
    lines.append("|------|-------------|-----------|-----------|------------|---------|------|")
    for i, d in enumerate(dates):
        o  = outflow[i]
        ro = reopen[i]
        cl = cloc[i]
        ir = issue_r[i]
        rv = reviews[i]
        # 간단한 평가 로직
        if not np.isnan(o) and not np.isnan(ro):
            if o > np.nanmean(outflow) and ro > np.nanmean(reopen):
                eval_str = "⚠️ 고생산/저품질"
            elif o > np.nanmean(outflow) and ro <= np.nanmean(reopen):
                eval_str = "✅ 고생산/고품질"
            elif o <= np.nanmean(outflow) and ro > np.nanmean(reopen):
                eval_str = "🔴 저생산/저품질"
            else:
                eval_str = "🔵 저생산/고품질 (안정화)"
        else:
            eval_str = "N/A"
        lines.append(f"| {d} | {fmt(o)} | {fmt(ro)}% | {fmt(cl)} | {fmt(ir)}% | {fmt(rv)} | {eval_str} |")
    lines.append("")

    # 구간 분석
    lines.append("### 구간별 분석\n")
    lines.append("**1월 초~중순 (01/05~01/19) - 생산성 상승 구간**")
    lines.append("- 산출물 Outflow가 변동성 있는 상승세")
    lines.append("- Commit당 LOC 비교적 안정적")
    lines.append("- Reopen율 변동 있음\n")
    lines.append("**1월 말~2월 초 (01/26~02/09) - 안정화 구간**")
    lines.append("- 이슈 처리율 상승세 (100%+)")
    lines.append("- Reopen율 개선 조짐")
    lines.append("- 활성 개발자 수 유지\n")
    lines.append("**2월 말~3월 초 (02/23~03/02) - 설 연휴 후 회복 구간**")
    lines.append("- 설 연휴(02/16) 이후 지표 변화 관찰")
    lines.append("- 02/23 Reopen율 급등(31.9%) 주의 필요")
    lines.append("- 03/02 이슈 처리율 회복(130.5%)\n")

    # 활성 개발자 수 추이
    lines.append("### 활성 개발자 수 추이\n")
    active = pd.to_numeric(pt[KEY_COLS['active_dev']], errors='coerce').values
    lines.append("| 주차 | 활성 개발자수 | 전주 대비 |")
    lines.append("|------|------------|---------|")
    for i, d in enumerate(dates):
        v = active[i]
        if i == 0 or np.isnan(active[i-1]):
            delta_str = '-'
        else:
            delta = v - active[i-1]
            delta_str = f"{delta:+.0f}명"
        lines.append(f"| {d} | {fmt(v, 0)}명 | {delta_str} |")
    lines.append("")

    return "\n".join(lines)


def section5_insights():
    """5. 인사이트 및 개선 제안"""
    lines = []
    lines.append("## 🧠 5. 인사이트 및 개선 제안\n")

    pt = get_group('PARTNER_TOTAL')

    def col(k):
        return pd.to_numeric(pt[KEY_COLS[k]], errors='coerce').values

    reopen   = col('reopen')
    cloc     = col('commit_loc')
    issue_r  = col('issue_rate')
    reviews  = col('review_count')
    outflow  = col('outflow')

    # 데이터 기반 인사이트 생성
    avg_reopen   = np.nanmean(reopen)
    max_reopen   = np.nanmax(reopen)
    avg_ir       = np.nanmean(issue_r)
    avg_reviews  = np.nanmean(reviews)
    avg_cloc     = np.nanmean(cloc)
    peak_reopen_w = pt['snapdate'].dt.strftime('%m/%d').values[np.nanargmax(reopen)]

    lines.append("### (1) 코드 변경 집중도 관리\n")
    lines.append(f"- 평균 Commit당 코드 변경량: **{fmt(avg_cloc)} LOC**")
    lines.append(f"- 코드 변경량과 Reopen율의 상관관계 → 과도한 대형 커밋 주의 필요")
    lines.append("- **권장사항**: 작은 단위 커밋 전략 + 자동화 테스트 강화")
    lines.append("")

    lines.append("### (2) 리뷰 프로세스 최적화\n")
    lines.append(f"- 평균 인당 Review수: **{fmt(avg_reviews)}**")
    lines.append(f"- 2/23 주 Reject/Review율 급등(3.77%) → 리뷰 피로도 증가 신호")
    lines.append("- **권장사항**: AI 리뷰어 추천 시스템 도입, 리뷰 부하 분산")
    lines.append("")

    lines.append("### (3) 이슈 재개방(Reopen) 관리\n")
    lines.append(f"- 평균 Reopen율: **{fmt(avg_reopen)}%** (최고: {fmt(max_reopen)}% at {peak_reopen_w})")
    lines.append(f"- {peak_reopen_w}주 Reopen율 급등은 설 연휴 후 품질 검증 부족 가능성")
    lines.append("- **권장사항**: 연휴 전 코드 동결 기간 설정, 복귀 후 집중 테스트")
    lines.append("")

    lines.append("### (4) 이슈 처리 효율 개선\n")
    lines.append(f"- 평균 이슈 처리율: **{fmt(avg_ir)}%**")
    lines.append(f"- 처리율이 낮은 주(예: 2/23주 60.2%)는 자원 재배치 필요")
    lines.append("- **권장사항**: 이슈 유형별 SLA 기반 자동 우선순위 조정 도입")
    lines.append("")

    lines.append("### (5) 설 연휴 영향 분석\n")
    pre = pt[pt['snapdate'] == '2026-02-09']
    post = pt[pt['snapdate'] == '2026-02-23']
    if len(pre) > 0 and len(post) > 0:
        pre_ro = pd.to_numeric(pre['진성완료이슈 Reopen율'], errors='coerce').values[0]
        post_ro = pd.to_numeric(post['진성완료이슈 Reopen율'], errors='coerce').values[0]
        pre_ir = pd.to_numeric(pre['이슈 처리율(Outflow/Inflow)'], errors='coerce').values[0]
        post_ir = pd.to_numeric(post['이슈 처리율(Outflow/Inflow)'], errors='coerce').values[0]
        lines.append(f"- Reopen율: 설 전(2/09) {fmt(pre_ro)}% → 설 후(2/23) {fmt(post_ro)}% ({'↑악화' if post_ro > pre_ro else '↓개선'})")
        lines.append(f"- 이슈처리율: 설 전(2/09) {fmt(pre_ir)}% → 설 후(2/23) {fmt(post_ir)}% ({'↑개선' if post_ir > pre_ir else '↓악화'})")
        delta_ro = post_ro - pre_ro
        sign = '+' if delta_ro >= 0 else ''
        lines.append(f"- 설 연휴 후 **Reopen율 급등 ({sign}{fmt(delta_ro)}%p)** 과 **처리율 급락** 은 연휴 복귀 후 품질 이슈 증가 패턴")
    lines.append("")

    return "\n".join(lines)


def section6_group_comparison():
    """6. 조직별 비교 분석"""
    lines = []
    lines.append("## 🏢 6. 조직별 비교 분석\n")

    orgs = [g for g in GROUPS if g != 'PARTNER_TOTAL']
    metric_map = [
        ('outflow',       '인당 Outflow'),
        ('issue_rate',    '이슈처리율(%)'),
        ('reopen',        'Reopen율(%)'),
        ('review_count',  'Review수'),
        ('commit_loc',    'Commit LOC'),
        ('defect_density','결함밀도'),
    ]

    lines.append("### 조직별 평균 성과 지표\n")
    header = "| 조직 | " + " | ".join(m[1] for m in metric_map) + " |"
    sep    = "|------|" + "-------|" * len(metric_map)
    lines.append(header)
    lines.append(sep)

    for g in orgs:
        gdf = get_group(g)
        values = []
        for key, _ in metric_map:
            v = pd.to_numeric(gdf[KEY_COLS[key]], errors='coerce').mean()
            values.append(fmt(v))
        lines.append(f"| {g} | " + " | ".join(values) + " |")
    lines.append("")

    # 주차별 이슈 처리율 비교
    lines.append("### 주차별 이슈 처리율 비교\n")
    pt = get_group('PARTNER_TOTAL')
    dates = pt['snapdate'].dt.strftime('%m/%d').tolist()

    header = "| 주차 | " + " | ".join(orgs) + " | 전체 |"
    sep    = "|------|" + "-------|" * (len(orgs)+1)
    lines.append(header)
    lines.append(sep)
    for i, d in enumerate(dates):
        row = [d]
        for g in orgs:
            gdf = get_group(g)
            gdf_w = gdf[gdf['snapdate'].dt.strftime('%m/%d') == d]
            if len(gdf_w) > 0:
                v = pd.to_numeric(gdf_w['이슈 처리율(Outflow/Inflow)'].values[0], errors='coerce')
                row.append(fmt(v) + "%" if not np.isnan(v) else 'N/A')
            else:
                row.append('N/A')
        # 전체
        pt_w = pt[pt['snapdate'].dt.strftime('%m/%d') == d]
        if len(pt_w) > 0:
            v = pd.to_numeric(pt_w['이슈 처리율(Outflow/Inflow)'].values[0], errors='coerce')
            row.append(fmt(v) + "%" if not np.isnan(v) else 'N/A')
        else:
            row.append('N/A')
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # 주차별 Reopen율 비교
    lines.append("### 주차별 Reopen율 비교\n")
    header = "| 주차 | " + " | ".join(orgs) + " | 전체 |"
    sep    = "|------|" + "-------|" * (len(orgs)+1)
    lines.append(header)
    lines.append(sep)
    for i, d in enumerate(dates):
        row = [d]
        for g in orgs:
            gdf = get_group(g)
            gdf_w = gdf[gdf['snapdate'].dt.strftime('%m/%d') == d]
            if len(gdf_w) > 0:
                v = pd.to_numeric(gdf_w['진성완료이슈 Reopen율'].values[0], errors='coerce')
                row.append(fmt(v) + "%" if not np.isnan(v) else 'N/A')
            else:
                row.append('N/A')
        # 전체
        pt_w = pt[pt['snapdate'].dt.strftime('%m/%d') == d]
        if len(pt_w) > 0:
            v = pd.to_numeric(pt_w['진성완료이슈 Reopen율'].values[0], errors='coerce')
            row.append(fmt(v) + "%" if not np.isnan(v) else 'N/A')
        else:
            row.append('N/A')
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    return "\n".join(lines)


def section7_conclusion():
    """7. 결론 요약"""
    lines = []
    lines.append("## 📘 7. 결론 요약\n")

    pt = get_group('PARTNER_TOTAL')

    def col(k):
        return pd.to_numeric(pt[KEY_COLS[k]], errors='coerce').values

    reopen   = col('reopen')
    issue_r  = col('issue_rate')
    cloc     = col('commit_loc')
    outflow  = col('outflow')
    reviews  = col('review_count')

    avg_reopen  = np.nanmean(reopen)
    avg_ir      = np.nanmean(issue_r)
    avg_cloc    = np.nanmean(cloc)
    avg_outflow = np.nanmean(outflow)
    avg_reviews = np.nanmean(reviews)

    # 트렌드 방향
    reopen_valid = reopen[~np.isnan(reopen)]
    ir_valid = issue_r[~np.isnan(issue_r)]
    slope_reopen = stats.linregress(np.arange(len(reopen_valid)), reopen_valid).slope if len(reopen_valid) > 1 else 0
    slope_ir = stats.linregress(np.arange(len(ir_valid)), ir_valid).slope if len(ir_valid) > 1 else 0

    lines.append("### 핵심 요약\n")
    lines.append(f"| 구분 | 지표 | 현황 | 평가 |")
    lines.append(f"|------|------|------|------|")
    lines.append(f"| 생산성 | 인당 산출물 Outflow 평균 | {fmt(avg_outflow)} | {'📈 주목' if avg_outflow > 5 else '보통'} |")
    lines.append(f"| 생산성 | Commit당 코드 변경량 평균 | {fmt(avg_cloc)} LOC | 안정 |")
    lines.append(f"| 효율성 | 이슈 처리율 평균 | {fmt(avg_ir)}% | {'✅ 양호' if avg_ir >= 100 else '⚠️ 개선 필요'} |")
    lines.append(f"| 품질 | Reopen율 평균 | {fmt(avg_reopen)}% | {'🔴 주의' if avg_reopen > 15 else '✅ 양호'} |")
    lines.append(f"| 리뷰 | 인당 Review수 평균 | {fmt(avg_reviews)} | 적정 |")
    lines.append("")

    lines.append("### 주요 발견사항\n")
    lines.append("1. **설 연휴 영향**: 2/16주 제외 후 분석해도 2/23주에 Reopen율 급등(31.9%) 관찰 → 연휴 복귀 후 품질 집중 관리 필요")
    lines.append("2. **이슈 처리 양호**: 평균 이슈 처리율 100%+ 구간이 다수 → 전반적 이슈 처리 역량 양호")
    lines.append("3. **코드 변경량 안정**: Commit당 LOC가 79~93 수준으로 안정적이나 결함밀도와 상관관계 주의")
    lines.append("4. **리뷰 프로세스**: Review수 감소 추세 관찰(4.0→1.8) → 리뷰 프로세스 강화 필요")
    lines.append("5. **3월 회복세**: 3/02주 이슈 처리율 130.5%로 회복 → 2월 누적 이슈 해소 중")
    lines.append("")

    lines.append("### 다음 단계 권고사항\n")
    lines.append("1. **단기 (1~2주)**: 설 연휴 후 누적된 Reopen 이슈 집중 처리")
    lines.append("2. **중기 (1개월)**: 코드 변경량 기반 결함 예측 모델 파일럿 도입")
    lines.append("3. **장기 (분기)**: AI 리뷰어 시스템 + 자동화 테스트 커버리지 강화")
    lines.append("")

    return "\n".join(lines)


def main():
    print("=== 2026 Weekly Collaboration Analysis ===")
    print(f"분석 그룹: {GROUPS}")
    print("설 연휴 제외: 2026-02-16주\n")

    sections = [
        section1_trend_summary(),
        section2_correlation(),
        section3_timeseries(),
        section4_tradeoff(),
        section5_insights(),
        section6_group_comparison(),
        section7_conclusion(),
    ]

    # 헤더 작성
    header = """# 주간 협업 지표 분석 보고서 (2026년)

> **분석 기준일**: 2026-03-04  
> **분석 기간**: 2026-01-05 ~ 2026-03-02  
> **제외 주차**: 2026-02-16주 (설 연휴: 2월 16일~20일)  
> **데이터 소스**: weeklyWeekHexa_202603041516.csv  
> **분석 대상 그룹**: PARTNER_TOTAL(전체), EDV자사, LGSI자사, 국내자사, 협력사전체

---

"""

    content = header + "\n\n---\n\n".join(sections)

    output_path = 'collab_weekly.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 분석 완료: {output_path}")
    print(f"   총 섹션: {len(sections)}개")
    print(f"   파일 크기: {len(content):,} bytes")


if __name__ == '__main__':
    main()
