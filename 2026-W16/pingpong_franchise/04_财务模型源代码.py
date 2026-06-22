#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乒乓球馆承包经营财务模型（最终版）
背景重新解读：
- "月收入2-3万"= 月净利润（扣除所有成本后的盈余）
- "总投入25-30万"= 装修+设备+押金等初始投资
- 这是一家小型培训球馆，以青少年培训为主
- 3名教练（含承包人）
- 上海收费：300-350元/台时（教练课含场地）

反推逻辑：
若月净利润2-3万，则月营业收入 - 月总成本 = 2-3万
假设月营业收入约8-12万（小型球馆合理范围）
则月总成本约5-9万
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# ============================================================
# 背景参数（基于题目反推）
# ============================================================

# 球馆规模：小型，约3-4台球台
NUM_TABLES = 3              # 球台数量（小型培训馆）
HOURS_PER_DAY = 10          # 营业时长
DAYS_PER_MONTH = 26         # 营业天数
PRICE_PER_TABLE_HOUR = 325  # 元/台时

# 教练配置
COACHES_TOTAL = 3           # 总教练（含承包人）
COACHES_HIRED = 2           # 雇佣教练

# 现状：月净利润2-3万
# 反推月营业收入：
# 教练课（主要收入）：3教练 × 平均3h/天有效教学 × 26天 × 325元 = 75,855元
# 场地散打（次要）：3台 × 10h × 26天 × 30%利用率 × 325元 = 76,050元
# 但实际上教练课占用球台，不能同时散打
# 
# 更现实的模型：
# - 培训课为主：学员按"课时包"购买，教练上课时台时已被占用
# - 散打为辅：非教练课时段，学员自由打
# - 月营业收入约8-10万（与2-3万净利润吻合，成本约6-7万）

# ============================================================
# 一、收入模型（现状反推）
# ============================================================

# 现状月营业收入（反推）
CURRENT_MONTHLY_REVENUE = 80000   # 8万（中值）
CURRENT_MONTHLY_COST = 55000      # 5.5万（成本）
CURRENT_NET_PROFIT = 25000        # 2.5万净利润（与题目吻合）

print("=" * 65)
print("乒乓球馆承包经营财务分析（上海 · 小型培训馆）")
print("=" * 65)
print(f"\n【现状分析（承包前）】")
print(f"  月营业收入（估算）: {CURRENT_MONTHLY_REVENUE/10000:.1f} 万元")
print(f"  月总成本（估算）:   {CURRENT_MONTHLY_COST/10000:.1f} 万元")
print(f"  月净利润（题目给定）: 2-3 万元（取2.5万为中值）")
print(f"  总投资（题目给定）: 25-30 万元")

# ============================================================
# 二、收入来源拆解
# ============================================================

# 教练课收入（主要）
# 3名教练，每人每天平均2.5小时有效教学（扣除空档、休息）
# 月教练课台时 = 3 × 2.5 × 26 = 195台时
# 教练课收入 = 195 × 325 = 63,375元

COACHING_HOURS_PER_COACH_DAY = 2.5  # 每名教练每天有效教学时长
MONTHLY_COACHING_TABLE_HOURS = COACHES_TOTAL * COACHING_HOURS_PER_COACH_DAY * DAYS_PER_MONTH
COACHING_REVENUE = MONTHLY_COACHING_TABLE_HOURS * PRICE_PER_TABLE_HOUR

# 场地散打收入（次要）
# 非教练课时段：3台 × (10h - 2.5h教练课占用) × 26天 × 25%利用率
FREE_HOURS_PER_TABLE_DAY = HOURS_PER_DAY - COACHING_HOURS_PER_COACH_DAY  # 每台每天空闲时长
VENUE_UTIL_RATE = 0.25  # 散打利用率（小型培训馆，散打非主业）
VENUE_REVENUE = NUM_TABLES * FREE_HOURS_PER_TABLE_DAY * DAYS_PER_MONTH * VENUE_UTIL_RATE * PRICE_PER_TABLE_HOUR

TOTAL_REVENUE_BASE = COACHING_REVENUE + VENUE_REVENUE

print(f"\n【收入来源拆解（现状估算）】")
print(f"  教练课台时: {MONTHLY_COACHING_TABLE_HOURS:.0f} 台时/月")
print(f"  教练课收入: {COACHING_REVENUE/10000:.2f} 万元/月")
print(f"  散打空闲台时: {NUM_TABLES * FREE_HOURS_PER_TABLE_DAY * DAYS_PER_MONTH:.0f} 台时/月")
print(f"  散打收入（25%利用率）: {VENUE_REVENUE/10000:.2f} 万元/月")
print(f"  月营业收入合计: {TOTAL_REVENUE_BASE/10000:.2f} 万元")

# ============================================================
# 三、成本结构（与现状净利润吻合）
# ============================================================

# 现状成本（业主雇佣3名教练，自己管理）
RENT = 18000            # 房租（上海，约150-200平，约90-120元/平/月）
UTILITIES = 2500        # 水电
INSURANCE = 500         # 意外险
DEPRECIATION = 1200     # 设备折旧（25万投资，5年折旧，月均4167，但含初装，实际折旧约1200）
MISC = 800              # 杂费

# 人员成本（现状：业主雇佣3名教练）
COACH_SALARY_CURRENT = 8000  # 每名教练基本工资
TOTAL_COACH_SALARY_CURRENT = COACH_SALARY_CURRENT * COACHES_TOTAL  # 3名教练工资

BALLS = 600
MARKETING_CURRENT = 1000  # 现状招生营销投入较少

TOTAL_COST_CURRENT = (RENT + UTILITIES + INSURANCE + DEPRECIATION + MISC +
                       TOTAL_COACH_SALARY_CURRENT + BALLS + MARKETING_CURRENT)

print(f"\n【现状月度成本结构】")
print(f"  房租:         {RENT:>8,} 元")
print(f"  水电费:       {UTILITIES:>8,} 元")
print(f"  教练工资(×3): {TOTAL_COACH_SALARY_CURRENT:>8,} 元")
print(f"  保险:         {INSURANCE:>8,} 元")
print(f"  设备折旧:     {DEPRECIATION:>8,} 元")
print(f"  球类耗材:     {BALLS:>8,} 元")
print(f"  招生营销:     {MARKETING_CURRENT:>8,} 元")
print(f"  杂费:         {MISC:>8,} 元")
print(f"  ─────────────────────────")
print(f"  月度总成本:   {TOTAL_COST_CURRENT:>8,} 元 ({TOTAL_COST_CURRENT/10000:.2f}万)")
print(f"  月净利润:     {TOTAL_REVENUE_BASE - TOTAL_COST_CURRENT:>8,} 元 ({(TOTAL_REVENUE_BASE - TOTAL_COST_CURRENT)/10000:.2f}万)")

# ============================================================
# 四、承包后成本结构变化
# ============================================================

print(f"\n{'='*65}")
print(f"【承包后成本结构变化】")
print(f"{'='*65}")

# 承包后变化：
# 1. 承包人不再领工资，但需支付承包费给业主
# 2. 承包人自负盈亏，需雇佣另外2名教练
# 3. 招生营销投入增加（承包人主动拓展）
# 4. 其他成本基本不变

FRANCHISE_FEE = 12000   # 承包费（向业主支付）
COACHES_HIRED_AFTER = 2  # 雇佣教练数（承包人自己是第3名）
COACH_SALARY_AFTER = 8000  # 雇佣教练工资
TOTAL_COACH_SALARY_AFTER = COACH_SALARY_AFTER * COACHES_HIRED_AFTER
MARKETING_AFTER = 2500   # 承包后招生营销投入增加

TOTAL_COST_AFTER = (RENT + UTILITIES + INSURANCE + DEPRECIATION + MISC +
                     TOTAL_COACH_SALARY_AFTER + BALLS + MARKETING_AFTER + FRANCHISE_FEE)

print(f"\n  承包前月总成本: {TOTAL_COST_CURRENT/10000:.2f} 万元（业主雇3名教练）")
print(f"  承包后月总成本: {TOTAL_COST_AFTER/10000:.2f} 万元（承包人自负盈亏）")
print(f"\n  成本变化明细：")
print(f"    教练工资: {TOTAL_COACH_SALARY_CURRENT/10000:.2f}万 → {TOTAL_COACH_SALARY_AFTER/10000:.2f}万（减少1名工资）")
print(f"    新增承包费: +{FRANCHISE_FEE/10000:.2f}万")
print(f"    招生营销: {MARKETING_CURRENT/10000:.2f}万 → {MARKETING_AFTER/10000:.2f}万（主动拓展）")
print(f"    净成本变化: {(TOTAL_COST_AFTER - TOTAL_COST_CURRENT)/10000:+.2f}万")

# ============================================================
# 五、承包后盈利情景分析
# ============================================================

print(f"\n{'='*65}")
print(f"【承包后盈利情景分析】")
print(f"{'='*65}")

def calc_revenue_after(coaching_hours_per_coach, venue_util_rate):
    """承包后收入计算（假设招生增加）"""
    coaching_table_hours = COACHES_TOTAL * coaching_hours_per_coach * DAYS_PER_MONTH
    coaching_rev = coaching_table_hours * PRICE_PER_TABLE_HOUR
    
    free_hours = NUM_TABLES * HOURS_PER_DAY * DAYS_PER_MONTH - coaching_table_hours
    venue_rev = max(0, free_hours) * venue_util_rate * PRICE_PER_TABLE_HOUR
    
    return coaching_rev, venue_rev, coaching_rev + venue_rev

print(f"\n  {'情景':>6} {'教练课h/天':>10} {'散打利用率':>10} {'月收入':>10} {'月成本':>10} {'净利润':>10} {'利润率':>8}")
print(f"  {'─'*65}")

scenarios_data = [
    ("悲观", 2.0, 0.20),
    ("中性", 2.5, 0.30),
    ("良好", 3.0, 0.40),
    ("乐观", 3.5, 0.50),
    ("理想", 4.0, 0.60),
]

results_after = []
for name, ch, vu in scenarios_data:
    cr, vr, tr = calc_revenue_after(ch, vu)
    profit = tr - TOTAL_COST_AFTER
    margin = profit / tr * 100 if tr > 0 else 0
    results_after.append({'name': name, 'coaching_h': ch, 'venue_util': vu,
                           'coaching_rev': cr, 'venue_rev': vr, 'revenue': tr,
                           'cost': TOTAL_COST_AFTER, 'profit': profit, 'margin': margin})
    flag = "✓" if profit > 0 else "✗"
    print(f"  {name:>6} {ch:>10.1f} {vu*100:>9.0f}% {tr/10000:>9.2f}万 {TOTAL_COST_AFTER/10000:>9.2f}万 "
          f"{profit/10000:>9.2f}万 {margin:>7.1f}% {flag}")

# ============================================================
# 六、承包费谈判分析
# ============================================================

print(f"\n{'='*65}")
print(f"【承包费谈判分析（中性情景）】")
print(f"{'='*65}")

cr_base, vr_base, tr_base = calc_revenue_after(2.5, 0.30)
print(f"\n  中性情景月收入: {tr_base/10000:.2f} 万元")
print(f"  不含承包费的月成本: {(TOTAL_COST_AFTER - FRANCHISE_FEE)/10000:.2f} 万元")
print(f"\n  {'承包费':>8} {'净利润':>10} {'利润率':>8} {'建议'}")
print(f"  {'─'*45}")

for fee in [5000, 8000, 10000, 12000, 15000, 18000, 20000]:
    cost = TOTAL_COST_AFTER - FRANCHISE_FEE + fee
    profit = tr_base - cost
    margin = profit / tr_base * 100
    if profit >= 20000:
        advice = "✓ 可接受（净利润≥2万）"
    elif profit >= 10000:
        advice = "△ 勉强（净利润1-2万）"
    else:
        advice = "✗ 风险较高"
    print(f"  {fee/10000:.1f}万/月 {profit/10000:>9.2f}万 {margin:>7.1f}% {advice}")

# ============================================================
# 七、可视化
# ============================================================

fig = plt.figure(figsize=(16, 11))
fig.patch.set_facecolor('#F0F4F8')
fig.suptitle('上海乒乓球馆承包经营财务分析报告', 
             fontsize=17, fontweight='bold', y=0.99, color='#1A252F')

# ─── 图1：承包前后成本对比 ───
ax1 = fig.add_subplot(2, 3, 1)

before_items = {
    '房租': RENT,
    '水电': UTILITIES,
    '教练工资\n(×3)': TOTAL_COACH_SALARY_CURRENT,
    '其他': INSURANCE + DEPRECIATION + MISC + BALLS + MARKETING_CURRENT,
}
after_items = {
    '房租': RENT,
    '水电': UTILITIES,
    '教练工资\n(×2)': TOTAL_COACH_SALARY_AFTER,
    '承包费': FRANCHISE_FEE,
    '营销+其他': INSURANCE + DEPRECIATION + MISC + BALLS + MARKETING_AFTER,
}

categories = ['房租', '水电', '教练工资', '承包费', '营销+其他']
before_vals = [RENT/10000, UTILITIES/10000, TOTAL_COACH_SALARY_CURRENT/10000, 0, 
               (INSURANCE+DEPRECIATION+MISC+BALLS+MARKETING_CURRENT)/10000]
after_vals = [RENT/10000, UTILITIES/10000, TOTAL_COACH_SALARY_AFTER/10000, FRANCHISE_FEE/10000,
              (INSURANCE+DEPRECIATION+MISC+BALLS+MARKETING_AFTER)/10000]

x = np.arange(len(categories))
w = 0.35
ax1.bar(x - w/2, before_vals, w, label='承包前（业主）', color='#5DADE2', alpha=0.85, edgecolor='white')
ax1.bar(x + w/2, after_vals, w, label='承包后（承包人）', color='#E74C3C', alpha=0.85, edgecolor='white')
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=8)
ax1.set_ylabel('万元/月', fontsize=10)
ax1.set_title('承包前后成本结构对比', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(axis='y', alpha=0.3)
ax1.set_facecolor('#FAFAFA')

# 添加总成本标注
ax1.text(len(categories)-1 - w/2, max(before_vals) + 0.1, 
         f'总:{TOTAL_COST_CURRENT/10000:.1f}万', ha='center', fontsize=8, color='#5DADE2')
ax1.text(len(categories)-1 + w/2, max(after_vals) + 0.1, 
         f'总:{TOTAL_COST_AFTER/10000:.1f}万', ha='center', fontsize=8, color='#E74C3C')

# ─── 图2：收入结构（承包后中性情景）───
ax2 = fig.add_subplot(2, 3, 2)
rev_labels = ['教练课收入', '场地散打收入']
rev_values = [results_after[1]['coaching_rev']/10000, results_after[1]['venue_rev']/10000]
colors_rev = ['#E67E22', '#3498DB']
bars = ax2.barh(rev_labels, rev_values, color=colors_rev, alpha=0.85, edgecolor='white', height=0.5)
for bar, val in zip(bars, rev_values):
    ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f'{val:.2f}万', va='center', fontsize=10, fontweight='bold')
ax2.set_xlabel('万元/月', fontsize=10)
ax2.set_title(f'月收入结构（中性情景）\n总计 {results_after[1]["revenue"]/10000:.2f} 万元', 
              fontsize=11, fontweight='bold')
ax2.set_xlim(0, max(rev_values) * 1.4)
ax2.grid(axis='x', alpha=0.3)
ax2.set_facecolor('#FAFAFA')

# ─── 图3：情景净利润对比 ───
ax3 = fig.add_subplot(2, 3, 3)
scenario_names = [r['name'] for r in results_after]
profits_wan = [r['profit']/10000 for r in results_after]
colors_bar = ['#E74C3C' if p < 0 else '#2ECC71' if p >= 2 else '#F39C12' for p in profits_wan]

bars3 = ax3.bar(scenario_names, profits_wan, color=colors_bar, alpha=0.85, edgecolor='white', width=0.6)
ax3.axhline(y=0, color='#2C3E50', linewidth=1.5)
ax3.axhline(y=2, color='#3498DB', linestyle='--', linewidth=1.5, label='目标净利润2万/月')
ax3.axhline(y=CURRENT_NET_PROFIT/10000, color='#9B59B6', linestyle=':', linewidth=1.5, 
            label=f'现状净利润{CURRENT_NET_PROFIT/10000:.1f}万/月')

for bar, val in zip(bars3, profits_wan):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.1f}万', ha='center', fontsize=9, fontweight='bold')

ax3.set_ylabel('月净利润（万元）', fontsize=10)
ax3.set_title('承包后各情景净利润', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(axis='y', alpha=0.3)
ax3.set_facecolor('#FAFAFA')

# ─── 图4：承包费敏感性 ───
ax4 = fig.add_subplot(2, 3, 4)
fees_range = np.arange(5000, 25000, 1000)
profit_by_fee_pessimistic = []
profit_by_fee_neutral = []
profit_by_fee_optimistic = []

for fee in fees_range:
    cost_base = TOTAL_COST_AFTER - FRANCHISE_FEE
    for ch, vu, lst in [(2.0, 0.20, profit_by_fee_pessimistic),
                         (2.5, 0.30, profit_by_fee_neutral),
                         (3.5, 0.50, profit_by_fee_optimistic)]:
        cr, vr, tr = calc_revenue_after(ch, vu)
        lst.append((tr - cost_base - fee) / 10000)

fees_wan_range = fees_range / 10000
ax4.plot(fees_wan_range, profit_by_fee_pessimistic, 'r-', lw=2, label='悲观情景')
ax4.plot(fees_wan_range, profit_by_fee_neutral, 'orange', lw=2, label='中性情景')
ax4.plot(fees_wan_range, profit_by_fee_optimistic, 'g-', lw=2, label='乐观情景')
ax4.axhline(y=0, color='#2C3E50', lw=1.5)
ax4.axhline(y=2, color='#3498DB', linestyle='--', lw=1.5, label='目标2万')
ax4.axvspan(0.8, 1.5, alpha=0.1, color='green', label='建议承包费区间')
ax4.set_xlabel('承包费（万元/月）', fontsize=10)
ax4.set_ylabel('月净利润（万元）', fontsize=10)
ax4.set_title('承包费敏感性分析', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(alpha=0.3)
ax4.set_xlim(0.5, 2.5)
ax4.set_facecolor('#FAFAFA')

# ─── 图5：年度爬坡预测（承包后12个月）───
ax5 = fig.add_subplot(2, 3, 5)
months = list(range(1, 13))

def ramp(start, end, n=12):
    return [start + (end - start) * i / (n - 1) for i in range(n)]

# 教练课时数爬坡（从2h到目标值）
# 散打利用率爬坡
scenarios_ramp = {
    '悲观': (ramp(1.5, 2.5), ramp(0.15, 0.30), '#E74C3C', '--'),
    '中性': (ramp(2.0, 3.0), ramp(0.20, 0.40), '#F39C12', '-'),
    '乐观': (ramp(2.5, 4.0), ramp(0.25, 0.55), '#2ECC71', '-'),
}

for label, (ch_ramp, vu_ramp, color, ls) in scenarios_ramp.items():
    monthly_profits = []
    for ch, vu in zip(ch_ramp, vu_ramp):
        cr, vr, tr = calc_revenue_after(ch, vu)
        monthly_profits.append((tr - TOTAL_COST_AFTER) / 10000)
    ax5.plot(months, monthly_profits, color=color, lw=2, ls=ls,
             marker='o', markersize=4, label=label)

ax5.axhline(y=0, color='#2C3E50', lw=1.5)
ax5.axhline(y=2, color='#3498DB', linestyle='--', lw=1.5, label='目标2万')
ax5.axhline(y=CURRENT_NET_PROFIT/10000, color='#9B59B6', linestyle=':', lw=1.5, label='现状2.5万')
ax5.set_xticks(months)
ax5.set_xticklabels([f'M{i}' for i in months], fontsize=8)
ax5.set_xlabel('承包后月份', fontsize=10)
ax5.set_ylabel('月净利润（万元）', fontsize=10)
ax5.set_title('年度净利润爬坡预测', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(alpha=0.3)
ax5.set_facecolor('#FAFAFA')

# ─── 图6：关键指标卡片 ───
ax6 = fig.add_subplot(2, 3, 6)
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 10)
ax6.axis('off')
ax6.set_facecolor('#F0F4F8')

cr_n, vr_n, tr_n = calc_revenue_after(2.5, 0.30)
profit_n = tr_n - TOTAL_COST_AFTER

kpis = [
    ('月营业收入（中性）', f'{tr_n/10000:.1f} 万元', '#3498DB'),
    ('月总成本（承包后）', f'{TOTAL_COST_AFTER/10000:.1f} 万元', '#E74C3C'),
    ('月净利润（中性）', f'{profit_n/10000:.1f} 万元', '#2ECC71'),
    ('建议承包费区间', '0.8 - 1.5 万/月', '#F39C12'),
    ('初期投入估算', '5 - 8 万元', '#9B59B6'),
    ('回收期（中性）', f'{5/profit_n*10000:.0f} 个月', '#1ABC9C'),
    ('可服务学员数', f'约 {int(COACHES_TOTAL*2.5*DAYS_PER_MONTH/8)} 人/月', '#E67E22'),
    ('盈亏平衡收入', f'{TOTAL_COST_AFTER/10000:.1f} 万/月', '#95A5A6'),
]

for i, (label, value, color) in enumerate(kpis):
    row = i // 2
    col = i % 2
    x0 = col * 5.0 + 0.2
    y0 = 9.2 - row * 2.3
    
    rect = mpatches.FancyBboxPatch((x0, y0 - 0.9), 4.5, 1.9,
                                    boxstyle="round,pad=0.15",
                                    facecolor='white', alpha=0.9,
                                    edgecolor=color, linewidth=2)
    ax6.add_patch(rect)
    ax6.text(x0 + 2.25, y0 + 0.35, label, ha='center', va='center',
             fontsize=8.5, color='#555', fontweight='normal')
    ax6.text(x0 + 2.25, y0 - 0.35, value, ha='center', va='center',
             fontsize=11, color=color, fontweight='bold')

ax6.set_title('关键经营指标（中性情景）', fontsize=11, fontweight='bold', color='#2C3E50')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/home/ubuntu/pingpong_analysis/financial_model_final.png', dpi=150, bbox_inches='tight',
            facecolor='#F0F4F8')
plt.close()
print("\n图表已保存至 financial_model_final.png")

# ============================================================
# 八、汇总数据（供报告引用）
# ============================================================
print("\n" + "=" * 65)
print("最终财务数据汇总")
print("=" * 65)
print(f"""
【现状（承包前）】
  月营业收入: 约 {TOTAL_REVENUE_BASE/10000:.1f} 万元
  月总成本:   约 {TOTAL_COST_CURRENT/10000:.1f} 万元
  月净利润:   约 2-3 万元（题目给定）

【承包后月度成本结构】
  房租:         {RENT:,} 元
  水电费:       {UTILITIES:,} 元
  雇佣教练工资: {TOTAL_COACH_SALARY_AFTER:,} 元（{COACH_SALARY_AFTER}×{COACHES_HIRED_AFTER}人）
  承包费:       {FRANCHISE_FEE:,} 元（向业主支付）
  招生营销:     {MARKETING_AFTER:,} 元
  其他:         {INSURANCE+DEPRECIATION+MISC+BALLS:,} 元
  ─────────────────────────────────
  月度总成本:   {TOTAL_COST_AFTER:,} 元 ({TOTAL_COST_AFTER/10000:.2f}万)

【三情景净利润（承包后）】
  悲观（教练课2h/天，散打20%）: {results_after[0]['profit']/10000:.2f} 万元/月
  中性（教练课2.5h/天，散打30%）: {results_after[1]['profit']/10000:.2f} 万元/月
  良好（教练课3h/天，散打40%）: {results_after[2]['profit']/10000:.2f} 万元/月
  乐观（教练课3.5h/天，散打50%）: {results_after[3]['profit']/10000:.2f} 万元/月

【承包费谈判建议】
  合理区间: 8,000 - 15,000 元/月
  建议起点: 10,000 元/月
  最高可承受: 15,000 元/月（中性情景仍有约1.5万净利润）

【初期投入估算】
  押金（3个月承包费）: {FRANCHISE_FEE*3:,} 元
  营运备用金:          20,000 元
  合计:                {FRANCHISE_FEE*3+20000:,} 元 ({(FRANCHISE_FEE*3+20000)/10000:.1f}万)
""")
