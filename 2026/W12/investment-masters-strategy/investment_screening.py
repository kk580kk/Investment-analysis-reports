#!/usr/bin/env python3
"""
投资大师选股策略演示版
使用模拟数据展示格雷厄姆、巴菲特、彼得·林奇等投资大师的选股逻辑
"""

import pandas as pd
import numpy as np
import json

class InvestmentScreenerDemo:
    """投资选股筛选器演示版"""
    
    def __init__(self):
        # 创建模拟的A股数据
        self.sample_stocks = self.create_sample_data()
        
    def create_sample_data(self):
        """创建模拟的A股股票数据"""
        np.random.seed(42)  # 确保结果可重现
        
        stocks = []
        stock_codes = [
            ('000001', '平安银行'), ('000002', '万科A'), ('000858', '五粮液'),
            ('000876', '新希望'), ('002415', '海康威视'), ('002594', '比亚迪'),
            ('300059', '东方财富'), ('300750', '宁德时代'), ('600000', '浦发银行'),
            ('600036', '招商银行'), ('600519', '贵州茅台'), ('600887', '伊利股份'),
            ('000568', '泸州老窖'), ('002304', '洋河股份'), ('600276', '恒瑞医药'),
            ('000063', '中兴通讯'), ('002142', '宁波银行'), ('600030', '中信证券'),
            ('000725', '京东方A'), ('002230', '科大讯飞'), ('300015', '爱尔眼科'),
            ('600585', '海螺水泥'), ('000338', '潍柴动力'), ('002027', '分众传媒'),
            ('600104', '上汽集团'), ('000895', '双汇发展'), ('002008', '大族激光'),
            ('300142', '沃森生物'), ('600809', '山西汾酒'), ('000596', '古井贡酒')
        ]
        
        for code, name in stock_codes:
            # 生成随机但合理的财务指标
            pe_ratio = np.random.uniform(5, 50)
            pb_ratio = np.random.uniform(0.5, 8)
            roe = np.random.uniform(0.05, 0.35)
            current_ratio = np.random.uniform(0.8, 4.0)
            debt_ratio = np.random.uniform(0.1, 0.8)
            revenue_growth = np.random.uniform(-0.1, 0.5)
            profit_margin = np.random.uniform(0.02, 0.3)
            market_cap = np.random.uniform(100, 50000)  # 亿元
            
            # 为一些知名股票设置更合理的数据
            if name in ['贵州茅台', '五粮液', '泸州老窖']:
                pe_ratio = np.random.uniform(20, 35)
                pb_ratio = np.random.uniform(3, 8)
                roe = np.random.uniform(0.20, 0.35)
                profit_margin = np.random.uniform(0.25, 0.45)
            elif name in ['招商银行', '平安银行', '宁波银行']:
                pe_ratio = np.random.uniform(6, 12)
                pb_ratio = np.random.uniform(0.8, 1.5)
                roe = np.random.uniform(0.12, 0.18)
                current_ratio = np.random.uniform(1.2, 2.0)
            elif name in ['宁德时代', '比亚迪', '海康威视']:
                pe_ratio = np.random.uniform(15, 40)
                pb_ratio = np.random.uniform(2, 6)
                roe = np.random.uniform(0.15, 0.25)
                revenue_growth = np.random.uniform(0.2, 0.6)
            
            stocks.append({
                'code': code,
                'name': name,
                'pe_ratio': round(pe_ratio, 2),
                'pb_ratio': round(pb_ratio, 2),
                'roe': round(roe, 4),
                'current_ratio': round(current_ratio, 2),
                'debt_ratio': round(debt_ratio, 2),
                'revenue_growth': round(revenue_growth, 4),
                'profit_margin': round(profit_margin, 4),
                'market_cap': round(market_cap, 1),
                'price': round(np.random.uniform(5, 200), 2)
            })
        
        return pd.DataFrame(stocks)

class GrahamScreenerDemo:
    """格雷厄姆价值投资筛选器演示版"""
    
    def __init__(self):
        self.criteria = {
            'pe_ratio_max': 15,  # PE ≤ 15
            'pb_ratio_max': 1.5,  # PB ≤ 1.5
            'pe_pb_product_max': 22.5,  # PE × PB ≤ 22.5
            'current_ratio_min': 2.0,  # 流动比率 ≥ 2
            'debt_ratio_max': 0.5,  # 债务比率 ≤ 50%
            'roe_min': 0.10,  # ROE ≥ 10%
        }
    
    def screen_stocks(self, stocks_df):
        """格雷厄姆选股筛选"""
        print("\n=== 格雷厄姆价值投资筛选 ===")
        print("筛选标准:")
        print(f"1. 市盈率(PE) ≤ {self.criteria['pe_ratio_max']}")
        print(f"2. 市净率(PB) ≤ {self.criteria['pb_ratio_max']}")
        print(f"3. PE × PB ≤ {self.criteria['pe_pb_product_max']}")
        print(f"4. 流动比率 ≥ {self.criteria['current_ratio_min']}")
        print(f"5. 债务比率 ≤ {self.criteria['debt_ratio_max']}")
        print(f"6. 净资产收益率(ROE) ≥ {self.criteria['roe_min']}")
        
        qualified_stocks = []
        
        for idx, stock in stocks_df.iterrows():
            criteria_met = 0
            total_criteria = 6
            details = []
            
            # 1. PE ≤ 15
            if stock['pe_ratio'] <= self.criteria['pe_ratio_max']:
                criteria_met += 1
                details.append("✓ PE合格")
            else:
                details.append("✗ PE过高")
            
            # 2. PB ≤ 1.5
            if stock['pb_ratio'] <= self.criteria['pb_ratio_max']:
                criteria_met += 1
                details.append("✓ PB合格")
            else:
                details.append("✗ PB过高")
            
            # 3. PE × PB ≤ 22.5
            pe_pb_product = stock['pe_ratio'] * stock['pb_ratio']
            if pe_pb_product <= self.criteria['pe_pb_product_max']:
                criteria_met += 1
                details.append("✓ PE×PB合格")
            else:
                details.append("✗ PE×PB过高")
            
            # 4. 流动比率 ≥ 2
            if stock['current_ratio'] >= self.criteria['current_ratio_min']:
                criteria_met += 1
                details.append("✓ 流动比率合格")
            else:
                details.append("✗ 流动比率不足")
            
            # 5. 债务比率 ≤ 50%
            if stock['debt_ratio'] <= self.criteria['debt_ratio_max']:
                criteria_met += 1
                details.append("✓ 债务比率合格")
            else:
                details.append("✗ 债务比率过高")
            
            # 6. ROE ≥ 10%
            if stock['roe'] >= self.criteria['roe_min']:
                criteria_met += 1
                details.append("✓ ROE合格")
            else:
                details.append("✗ ROE不足")
            
            # 计算得分
            score = criteria_met / total_criteria
            
            # 格雷厄姆要求较严格，至少满足4个条件
            if criteria_met >= 4:
                # 计算安全边际（简化）
                intrinsic_value = self.calculate_intrinsic_value(stock)
                safety_margin = (intrinsic_value - stock['price']) / intrinsic_value if intrinsic_value > 0 else 0
                
                qualified_stocks.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'pe_ratio': stock['pe_ratio'],
                    'pb_ratio': stock['pb_ratio'],
                    'pe_pb_product': pe_pb_product,
                    'current_ratio': stock['current_ratio'],
                    'debt_ratio': stock['debt_ratio'],
                    'roe': stock['roe'],
                    'price': stock['price'],
                    'intrinsic_value': intrinsic_value,
                    'safety_margin': safety_margin,
                    'score': score,
                    'criteria_met': criteria_met,
                    'details': details
                })
        
        # 按得分和安全边际排序
        qualified_stocks.sort(key=lambda x: (x['score'], x['safety_margin']), reverse=True)
        
        print(f"\n筛选结果: 找到 {len(qualified_stocks)} 只符合格雷厄姆标准的股票")
        
        return qualified_stocks
    
    def calculate_intrinsic_value(self, stock):
        """计算格雷厄姆内在价值"""
        eps = stock['price'] / stock['pe_ratio'] if stock['pe_ratio'] > 0 else 0
        # 简化的格雷厄姆公式: V = EPS × (8.5 + 2G)
        # 假设增长率为5%
        growth_rate = 5
        intrinsic_value = eps * (8.5 + 2 * growth_rate)
        return round(intrinsic_value, 2)

class BuffettScreenerDemo:
    """巴菲特质量成长筛选器演示版"""
    
    def __init__(self):
        self.criteria = {
            'roe_min': 0.15,  # ROE ≥ 15%
            'roe_consistency': True,  # ROE稳定性
            'debt_ratio_max': 0.5,  # 债务比率 ≤ 50%
            'profit_margin_min': 0.10,  # 净利率 ≥ 10%
            'revenue_growth_min': 0.07,  # 营收增长 ≥ 7%
            'pe_reasonable_max': 25,  # 合理PE上限
        }
    
    def screen_stocks(self, stocks_df):
        """巴菲特质量成长筛选"""
        print("\n=== 巴菲特质量成长筛选 ===")
        print("筛选标准:")
        print(f"1. 净资产收益率(ROE) ≥ {self.criteria['roe_min']*100}%")
        print(f"2. 债务比率 ≤ {self.criteria['debt_ratio_max']*100}%")
        print(f"3. 净利率 ≥ {self.criteria['profit_margin_min']*100}%")
        print(f"4. 营收增长率 ≥ {self.criteria['revenue_growth_min']*100}%")
        print(f"5. 市盈率 ≤ {self.criteria['pe_reasonable_max']}")
        print("6. 具有护城河和竞争优势")
        
        qualified_stocks = []
        
        for idx, stock in stocks_df.iterrows():
            criteria_met = 0
            total_criteria = 6
            details = []
            
            # 1. ROE ≥ 15%
            if stock['roe'] >= self.criteria['roe_min']:
                criteria_met += 1
                details.append("✓ ROE优秀")
            else:
                details.append("✗ ROE不足")
            
            # 2. 债务比率 ≤ 50%
            if stock['debt_ratio'] <= self.criteria['debt_ratio_max']:
                criteria_met += 1
                details.append("✓ 债务健康")
            else:
                details.append("✗ 债务过高")
            
            # 3. 净利率 ≥ 10%
            if stock['profit_margin'] >= self.criteria['profit_margin_min']:
                criteria_met += 1
                details.append("✓ 盈利能力强")
            else:
                details.append("✗ 盈利能力弱")
            
            # 4. 营收增长 ≥ 7%
            if stock['revenue_growth'] >= self.criteria['revenue_growth_min']:
                criteria_met += 1
                details.append("✓ 成长性好")
            else:
                details.append("✗ 成长性不足")
            
            # 5. PE ≤ 25
            if stock['pe_ratio'] <= self.criteria['pe_reasonable_max']:
                criteria_met += 1
                details.append("✓ 估值合理")
            else:
                details.append("✗ 估值偏高")
            
            # 6. 护城河评估（简化）
            moat_score = self.assess_moat(stock)
            if moat_score >= 0.6:
                criteria_met += 1
                details.append("✓ 具有护城河")
            else:
                details.append("✗ 护城河不明显")
            
            # 计算得分
            score = criteria_met / total_criteria
            
            # 巴菲特要求高质量，至少满足4个条件
            if criteria_met >= 4:
                # 计算DCF估值（简化）
                dcf_value = self.calculate_dcf_value(stock)
                
                qualified_stocks.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'roe': stock['roe'],
                    'debt_ratio': stock['debt_ratio'],
                    'profit_margin': stock['profit_margin'],
                    'revenue_growth': stock['revenue_growth'],
                    'pe_ratio': stock['pe_ratio'],
                    'price': stock['price'],
                    'dcf_value': dcf_value,
                    'moat_score': moat_score,
                    'score': score,
                    'criteria_met': criteria_met,
                    'details': details
                })
        
        # 按得分排序
        qualified_stocks.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n筛选结果: 找到 {len(qualified_stocks)} 只符合巴菲特标准的股票")
        
        return qualified_stocks
    
    def assess_moat(self, stock):
        """评估护城河（简化）"""
        # 基于行业和财务指标简化评估
        moat_score = 0
        
        # 高ROE通常表明有竞争优势
        if stock['roe'] > 0.20:
            moat_score += 0.3
        elif stock['roe'] > 0.15:
            moat_score += 0.2
        
        # 高净利率表明定价权
        if stock['profit_margin'] > 0.20:
            moat_score += 0.3
        elif stock['profit_margin'] > 0.15:
            moat_score += 0.2
        
        # 稳定增长
        if stock['revenue_growth'] > 0.10:
            moat_score += 0.2
        
        # 低债务比率表明财务稳健
        if stock['debt_ratio'] < 0.3:
            moat_score += 0.2
        
        return round(moat_score, 2)
    
    def calculate_dcf_value(self, stock):
        """计算DCF价值（简化）"""
        # 简化的DCF计算
        current_earnings = stock['price'] / stock['pe_ratio'] if stock['pe_ratio'] > 0 else 0
        growth_rate = stock['revenue_growth']
        discount_rate = 0.10  # 10%折现率
        
        # 假设10年DCF
        dcf_value = 0
        for year in range(1, 11):
            future_earnings = current_earnings * ((1 + growth_rate) ** year)
            present_value = future_earnings / ((1 + discount_rate) ** year)
            dcf_value += present_value
        
        return round(dcf_value, 2)

class LynchScreenerDemo:
    """彼得·林奇成长股筛选器演示版"""
    
    def __init__(self):
        self.criteria = {
            'peg_max': 1.0,  # PEG ≤ 1.0
            'peg_ideal': 0.5,  # PEG ≤ 0.5 (理想)
            'growth_rate_min': 0.15,  # 增长率 ≥ 15%
            'growth_rate_max': 0.50,  # 增长率 ≤ 50%
            'pe_max': 40,  # PE不超过40
        }
    
    def screen_stocks(self, stocks_df):
        """彼得·林奇成长股筛选"""
        print("\n=== 彼得·林奇成长股筛选 ===")
        print("筛选标准:")
        print(f"1. PEG比率 ≤ {self.criteria['peg_max']}")
        print(f"2. PEG比率 ≤ {self.criteria['peg_ideal']} (理想)")
        print(f"3. 增长率 {self.criteria['growth_rate_min']*100}%-{self.criteria['growth_rate_max']*100}%")
        print(f"4. 市盈率 ≤ {self.criteria['pe_max']}")
        print("5. 业务简单易懂")
        
        qualified_stocks = []
        
        for idx, stock in stocks_df.iterrows():
            # 使用营收增长率作为增长率
            growth_rate = stock['revenue_growth']
            
            # 计算PEG
            if growth_rate > 0:
                peg_ratio = stock['pe_ratio'] / (growth_rate * 100)
            else:
                peg_ratio = float('inf')
            
            criteria_met = 0
            total_criteria = 5
            details = []
            
            # 1. PEG ≤ 1.0
            if peg_ratio <= self.criteria['peg_max']:
                criteria_met += 1
                details.append("✓ PEG合理")
            else:
                details.append("✗ PEG过高")
            
            # 2. PEG ≤ 0.5 (理想)
            if peg_ratio <= self.criteria['peg_ideal']:
                criteria_met += 1
                details.append("✓ PEG理想")
            else:
                details.append("✗ PEG非理想")
            
            # 3. 增长率在合理范围
            if self.criteria['growth_rate_min'] <= growth_rate <= self.criteria['growth_rate_max']:
                criteria_met += 1
                details.append("✓ 增长率合理")
            else:
                details.append("✗ 增长率不合理")
            
            # 4. PE ≤ 40
            if stock['pe_ratio'] <= self.criteria['pe_max']:
                criteria_met += 1
                details.append("✓ PE可接受")
            else:
                details.append("✗ PE过高")
            
            # 5. 业务简单易懂（简化评估）
            business_simplicity = self.assess_business_simplicity(stock)
            if business_simplicity >= 0.6:
                criteria_met += 1
                details.append("✓ 业务易懂")
            else:
                details.append("✗ 业务复杂")
            
            # 计算得分
            score = criteria_met / total_criteria
            
            # 林奇相对宽松，至少满足3个条件
            if criteria_met >= 3:
                qualified_stocks.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'pe_ratio': stock['pe_ratio'],
                    'growth_rate': growth_rate,
                    'peg_ratio': round(peg_ratio, 2) if peg_ratio != float('inf') else 'N/A',
                    'price': stock['price'],
                    'business_simplicity': business_simplicity,
                    'score': score,
                    'criteria_met': criteria_met,
                    'details': details
                })
        
        # 按PEG和得分排序
        qualified_stocks.sort(key=lambda x: (x['score'], -float(x['peg_ratio']) if x['peg_ratio'] != 'N/A' else 0), reverse=True)
        
        print(f"\n筛选结果: 找到 {len(qualified_stocks)} 只符合林奇标准的股票")
        
        return qualified_stocks
    
    def assess_business_simplicity(self, stock):
        """评估业务简单性（简化）"""
        # 基于股票名称简化判断
        simple_businesses = ['银行', '白酒', '食品', '医药', '地产', '保险', '水泥']
        
        for business in simple_businesses:
            if business in stock['name']:
                return 0.8
        
        return 0.4  # 默认中等复杂度

def generate_comprehensive_report(graham_results, buffett_results, lynch_results):
    """生成综合分析报告"""
    print("\n" + "="*80)
    print("投资大师选股策略综合分析报告")
    print("="*80)
    
    # 统计各策略结果
    print(f"\n策略筛选结果统计:")
    print(f"格雷厄姆价值投资策略: {len(graham_results)} 只股票")
    print(f"巴菲特质量成长策略: {len(buffett_results)} 只股票")
    print(f"彼得·林奇成长股策略: {len(lynch_results)} 只股票")
    
    # 找出被多个策略同时选中的股票
    graham_codes = {stock['code'] for stock in graham_results}
    buffett_codes = {stock['code'] for stock in buffett_results}
    lynch_codes = {stock['code'] for stock in lynch_results}
    
    # 三个策略都选中的股票
    triple_selected = graham_codes & buffett_codes & lynch_codes
    # 两个策略选中的股票
    double_selected = (graham_codes & buffett_codes) | (graham_codes & lynch_codes) | (buffett_codes & lynch_codes)
    double_selected = double_selected - triple_selected
    
    print(f"\n多策略重叠分析:")
    print(f"被三个策略同时选中: {len(triple_selected)} 只股票")
    print(f"被两个策略同时选中: {len(double_selected)} 只股票")
    
    if triple_selected:
        print(f"\n三策略共同推荐股票:")
        for code in triple_selected:
            # 找到股票名称
            for stock in graham_results:
                if stock['code'] == code:
                    print(f"  {code} - {stock['name']}")
                    break
    
    # 各策略前3名推荐
    print(f"\n各策略前3名推荐:")
    
    strategies = [
        ("格雷厄姆价值投资", graham_results),
        ("巴菲特质量成长", buffett_results),
        ("彼得·林奇成长股", lynch_results)
    ]
    
    for strategy_name, results in strategies:
        print(f"\n{strategy_name}策略前3名:")
        for i, stock in enumerate(results[:3], 1):
            print(f"  {i}. {stock['code']} - {stock['name']} (得分: {stock['score']:.2f})")
            if strategy_name == "格雷厄姆价值投资":
                print(f"     PE: {stock['pe_ratio']}, PB: {stock['pb_ratio']}, 安全边际: {stock['safety_margin']:.2%}")
            elif strategy_name == "巴菲特质量成长":
                print(f"     ROE: {stock['roe']:.2%}, 净利率: {stock['profit_margin']:.2%}, 护城河: {stock['moat_score']}")
            elif strategy_name == "彼得·林奇成长股":
                print(f"     PEG: {stock['peg_ratio']}, 增长率: {stock['growth_rate']:.2%}")
    
    return {
        'triple_selected': list(triple_selected),
        'double_selected': list(double_selected),
        'strategy_counts': {
            'graham': len(graham_results),
            'buffett': len(buffett_results),
            'lynch': len(lynch_results)
        }
    }

def main():
    """主函数"""
    print("=== 投资大师选股策略演示系统 ===")
    
    # 创建演示数据
    demo = InvestmentScreenerDemo()
    stocks_df = demo.sample_stocks
    
    print(f"分析样本: {len(stocks_df)} 只A股股票")
    print("\n样本股票列表:")
    for idx, stock in stocks_df.iterrows():
        print(f"  {stock['code']} - {stock['name']}")
    
    # 初始化各策略筛选器
    graham_screener = GrahamScreenerDemo()
    buffett_screener = BuffettScreenerDemo()
    lynch_screener = LynchScreenerDemo()
    
    # 执行筛选
    graham_results = graham_screener.screen_stocks(stocks_df)
    buffett_results = buffett_screener.screen_stocks(stocks_df)
    lynch_results = lynch_screener.screen_stocks(stocks_df)
    
    # 生成综合报告
    summary = generate_comprehensive_report(graham_results, buffett_results, lynch_results)
    
    # 保存详细结果
    results = {
        'graham': graham_results,
        'buffett': buffett_results,
        'lynch': lynch_results,
        'summary': summary
    }
    
    # 保存到文件
    with open('/home/ubuntu/screening_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n详细结果已保存到 screening_results.json")
    
    return results

if __name__ == "__main__":
    results = main()

