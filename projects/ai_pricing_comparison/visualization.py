import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['LXGW WenKai Mono']
plt.rcParams['axes.unicode_minus'] = False

# 创建输出目录
os.makedirs('projects/ai_pricing_comparison/images', exist_ok=True)

# 1. 模型价格对比（每百万tokens）
def plot_model_pricing():
    models = ['豆包AI\n(后付费)', 'DeepSeek-V2', 'DeepSeek-V3', 'DeepSeek-R1']
    input_prices = [0.8, 1, 2, 4]  # 输入价格（未命中缓存）
    output_prices = [2, 2, 8, 16]  # 输出价格
    
    x = np.arange(len(models))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, input_prices, width, label='输入价格')
    rects2 = ax.bar(x + width/2, output_prices, width, label='输出价格')
    
    ax.set_ylabel('价格（元/百万tokens）')
    ax.set_title('各模型输入输出价格对比')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    
    # 添加数值标签
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}元',
                       xy=(rect.get_x() + rect.get_width()/2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('projects/ai_pricing_comparison/images/model_pricing.png', dpi=300)
    plt.close()

# 2. 使用成本对比（每月）
def plot_usage_cost():
    usage_millions = np.array([1, 10, 50, 100])  # 每月百万tokens用量
    
    # 豆包AI成本（后付费模式）
    doubaiai_cost = usage_millions * (0.8 + 2)  # 输入+输出成本
    
    # DeepSeek-V3成本
    deepseek_v3_cost_low = usage_millions * (0.5 + 8)  # 缓存命中
    deepseek_v3_cost_high = usage_millions * (2 + 8)   # 缓存未命中
    
    plt.figure(figsize=(12, 6))
    plt.plot(usage_millions, doubaiai_cost, 'o-', label='豆包AI')
    plt.fill_between(usage_millions, deepseek_v3_cost_low, deepseek_v3_cost_high, 
                    alpha=0.2, color='orange')
    plt.plot(usage_millions, deepseek_v3_cost_low, '--', color='orange', 
            label='DeepSeek-V3 (缓存命中)')
    plt.plot(usage_millions, deepseek_v3_cost_high, '--', color='orange', 
            label='DeepSeek-V3 (缓存未命中)')
    
    plt.title('月度使用量与成本关系')
    plt.xlabel('月使用量（百万tokens）')
    plt.ylabel('月度成本（元）')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('projects/ai_pricing_comparison/images/usage_cost.png', dpi=300)
    plt.close()

# 3. 特性对比热力图
def plot_feature_comparison():
    features = ['价格稳定性', '成本优化空间', '模型迭代速度', '定价灵活度', '综合性价比']
    products = ['豆包AI', 'DeepSeek AI']
    
    # 评分矩阵 (0-5分)
    scores = np.array([
        [5, 3, 3, 4, 5],  # 豆包AI
        [3, 5, 5, 4, 4]   # DeepSeek AI
    ])
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(scores, annot=True, cmap='YlOrRd', xticklabels=features, 
                yticklabels=products, fmt='d')
    plt.title('特性对比评分 (5分制)')
    
    plt.tight_layout()
    plt.savefig('projects/ai_pricing_comparison/images/feature_comparison.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    plot_model_pricing()
    plot_usage_cost()
    plot_feature_comparison() 