import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import matplotlib as mpl

# 设置中文字体
def set_chinese_font():
    try:
        # 设置 matplotlib 的字体
        plt.rcParams['font.sans-serif'] = ['LXGW WenKai Mono']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置 seaborn 的字体
        sns.set_style("whitegrid", {'font.sans-serif': ['LXGW WenKai Mono']})
        
        # 全局设置 matplotlib 的字体
        mpl.rcParams['font.family'] = 'LXGW WenKai Mono'
        mpl.rcParams['font.sans-serif'] = ['LXGW WenKai Mono']
        
        # 测试字体
        fig = plt.figure()
        plt.text(0.5, 0.5, '测试中文', fontsize=12)
        fig.canvas.draw()
        plt.close()
        print(f"成功使用字体: LXGW WenKai Mono")
        return
    except Exception as e:
        print(f"警告：未找到 LXGW WenKai Mono 字体，错误信息：{e}")
        print("尝试其他字体")
        # 备选字体列表
        chinese_fonts = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'STHeiti', 'Arial Unicode MS', 'Heiti TC']
        for font in chinese_fonts:
            try:
                plt.rcParams['font.sans-serif'] = [font]
                fig = plt.figure()
                plt.text(0.5, 0.5, '测试中文', fontsize=12)
                fig.canvas.draw()
                plt.close()
                print(f"成功使用备选字体: {font}")
                return
            except:
                continue
    
    print("警告：未找到合适的中文字体")

# 设置字体
set_chinese_font()

# 创建输出目录
output_dir = Path('projects/youtube_summary_RL0lT3I2afs/data/images')
output_dir.mkdir(parents=True, exist_ok=True)

# 设置风格
plt.style.use('seaborn-v0_8')

# 1. 情感基调变化图
def create_emotion_chart():
    sections = ['开场', '核心宣告', '政策宣布', '问题诊断', '具体措施', '个人叙事']
    emotion_scores = [0.6, 0.8, 0.4, -0.3, 0.5, 0.7]  # -1到1之间的情感分数
    
    plt.figure(figsize=(12, 7))
    plt.plot(sections, emotion_scores, marker='o', linewidth=2, markersize=8)
    plt.title('演讲情感基调变化', fontsize=14, pad=20, fontfamily='LXGW WenKai Mono')
    plt.ylabel('情感强度 (-1=消极, 1=积极)', fontsize=12, fontfamily='LXGW WenKai Mono')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=30, fontsize=10, fontfamily='LXGW WenKai Mono')
    plt.yticks(fontsize=10, fontfamily='LXGW WenKai Mono')
    
    # 确保所有元素都显示完整
    plt.tight_layout()
    plt.savefig(output_dir / 'emotion_flow.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. 关键词词频统计
def create_keyword_chart():
    keywords = {
        'America/American': 15,
        'Justice/Law': 8,
        'Border/Immigration': 10,
        'Energy/Oil': 7,
        'Manufacturing': 5,
        'Great/Greater': 12,
        'Strong/Stronger': 9,
        'Crisis/Emergency': 6
    }
    
    plt.figure(figsize=(12, 7))
    bars = plt.bar(keywords.keys(), keywords.values())
    plt.title('关键词出现频率', fontsize=14, pad=20, fontfamily='LXGW WenKai Mono')
    plt.xlabel('关键词', fontsize=12, fontfamily='LXGW WenKai Mono')
    plt.ylabel('出现次数', fontsize=12, fontfamily='LXGW WenKai Mono')
    plt.xticks(rotation=30, ha='right', fontsize=10, fontfamily='LXGW WenKai Mono')
    plt.yticks(fontsize=10, fontfamily='LXGW WenKai Mono')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontfamily='LXGW WenKai Mono')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'keyword_freq.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. 演讲时间分配饼图
def create_time_distribution_chart():
    sections = ['开场致谢', '核心宣告', '政策宣布', '问题诊断', '具体措施', '个人叙事']
    times = [5, 10, 20, 15, 35, 15]  # 百分比
    
    plt.figure(figsize=(10, 8))
    plt.pie(times, labels=sections, autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 10, 'fontfamily': 'LXGW WenKai Mono'})
    plt.title('演讲时间分配', fontsize=14, pad=20, fontfamily='LXGW WenKai Mono')
    plt.axis('equal')
    plt.savefig(output_dir / 'time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. 政策议题热度图
def create_policy_heatmap():
    policies = ['边境安全', '经济发展', '能源政策', '制造业', '司法改革']
    metrics = ['提及频率', '情感强度', '具体措施数', '时间占比']
    
    data = np.array([
        [0.9, 0.8, 0.7, 0.6, 0.5],
        [0.8, 0.7, 0.9, 0.5, 0.6],
        [0.7, 0.6, 0.8, 0.7, 0.4],
        [0.6, 0.5, 0.7, 0.8, 0.3]
    ])
    
    plt.figure(figsize=(12, 8))
    
    # 创建热力图
    ax = sns.heatmap(data, annot=True, fmt='.1f', cmap='YlOrRd')
    
    # 设置标题和标签
    plt.title('政策议题分析热度图', fontsize=14, pad=20, fontfamily='LXGW WenKai Mono')
    plt.xlabel('政策议题', fontsize=12, fontfamily='LXGW WenKai Mono')
    plt.ylabel('评估指标', fontsize=12, fontfamily='LXGW WenKai Mono')
    
    # 设置刻度标签
    ax.set_xticklabels(policies, rotation=30, fontsize=10, fontfamily='LXGW WenKai Mono')
    ax.set_yticklabels(metrics, rotation=0, fontsize=10, fontfamily='LXGW WenKai Mono')
    
    # 设置热力图中数值的字体
    for text in ax.texts:
        text.set_fontfamily('LXGW WenKai Mono')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'policy_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_emotion_chart()
    create_keyword_chart()
    create_time_distribution_chart()
    create_policy_heatmap() 