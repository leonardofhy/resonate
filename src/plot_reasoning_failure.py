import matplotlib.pyplot as plt
import numpy as np
import json
import os

def create_clean_chart():
    # ---------------------------------------------------------
    # 1. 數據準備
    # ---------------------------------------------------------
    # Locate paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'data', 'reasoning_failure_data.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    models = data['models']
    single_hop = data['single_hop']
    multi_hop = data['multi_hop']
    
    # ---------------------------------------------------------
    # 2. 畫布設置
    # ---------------------------------------------------------
    # 10x6 是很適合 PPT 的比例
    fig, ax = plt.subplots(figsize=(10, 6)) 

    # ---------------------------------------------------------
    # 3. 繪製圖表
    # ---------------------------------------------------------
    x = np.arange(len(models))
    width = 0.35

    # 專業配色：
    # Single-hop (Blue): 代表基礎能力
    # Multi-hop (Orange): 代表推理能力
    c_single = '#5B9BD5' 
    c_multi = '#ED7D31'  

    rects1 = ax.bar(x - width/2, single_hop, width, label='Single-hop Accuracy', color=c_single, edgecolor='black', alpha=0.9)
    rects2 = ax.bar(x + width/2, multi_hop, width, label='Multi-hop Accuracy', color=c_multi, edgecolor='black', alpha=0.9)

    # ---------------------------------------------------------
    # 4. 基準線 (Reference Lines) - 這是比較差異的關鍵，建議保留
    # ---------------------------------------------------------
    ax.axhline(y=88.0, color=c_single, linestyle='--', linewidth=2.5, alpha=0.7)
    ax.axhline(y=47.2, color=c_multi, linestyle='--', linewidth=2.5, alpha=0.7)

    # ---------------------------------------------------------
    # 5. 軸與外觀設置
    # ---------------------------------------------------------
    ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    # 標題留空或簡單寫，讓你在 PPT 裡自己下標
    ax.set_title('Performance Comparison: Single-hop vs. Multi-hop', fontsize=16, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100) # 固定 0-100%
    ax.legend(loc='upper right', frameon=True, fontsize=11)
    
    # 簡化網格，讓背景乾淨
    ax.grid(axis='y', linestyle='--', alpha=0.2) 
    
    # 移除上方和右方的邊框，讓圖表更現代化 (Spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ---------------------------------------------------------
    # 6. 數值標籤 (只保留數字)
    # ---------------------------------------------------------
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=11, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    # ---------------------------------------------------------
    # 7. 輸出
    # ---------------------------------------------------------
    plt.tight_layout()
    output_path = os.path.join(project_root, 'plots', 'reasoning_failure_comparison_chart.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path}")
    plt.show()

if __name__ == "__main__":
    create_clean_chart()