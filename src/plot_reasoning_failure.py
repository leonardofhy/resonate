import matplotlib.pyplot as plt
import numpy as np

def create_reasoning_failure_chart():
    # ---------------------------------------------------------
    # 1. 數據準備 (Data Preparation)
    # ---------------------------------------------------------
    models = ['Qwen2-Audio\n(Base Model)', 'Audio Reasoner\n(SFT)', 'R1-AQA\n(RL)']
    
    # Accuracy Data
    single_hop = [88.0, 67.2, 66.8]
    multi_hop = [47.2, 33.4, 48.7]
    
    # ---------------------------------------------------------
    # 2. 畫布設置 (Figure Setup)
    # ---------------------------------------------------------
    # 設置高寬比，留出下方空間給 Table
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
    plt.subplots_adjust(hspace=0.3) # 調整上下圖間距

    # ---------------------------------------------------------
    # 3. 上半部：柱狀圖 (Bar Chart)
    # ---------------------------------------------------------
    x = np.arange(len(models))
    width = 0.35  # 柱子寬度

    # 繪製柱子
    rects1 = ax1.bar(x - width/2, single_hop, width, label='Single-hop Accuracy', color='#4A90E2', edgecolor='black', alpha=0.9)
    rects2 = ax1.bar(x + width/2, multi_hop, width, label='Multi-hop Accuracy', color='#F5A623', edgecolor='black', alpha=0.9)

    # 添加 Base Model 的基準線 (Reference Lines)
    ax1.axhline(y=88.0, color='#4A90E2', linestyle='--', linewidth=1.5, alpha=0.6)
    ax1.axhline(y=47.2, color='#F5A623', linestyle='--', linewidth=1.5, alpha=0.6)
    
    # 標註基準線文字
    ax1.text(2.6, 88.0, 'Base Single-hop', va='center', ha='left', color='#4A90E2', fontweight='bold')
    ax1.text(2.6, 47.2, 'Base Multi-hop', va='center', ha='left', color='#F5A623', fontweight='bold')

    # 設置標籤與標題
    ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Does Explicit Reasoning Help? (Visualizing the Failure)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=11)
    ax1.set_ylim(0, 100)
    ax1.legend(loc='upper right', frameon=True)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # 自動標註數值 (Auto-label values)
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f'{height}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    # 添加強調失敗的紅色箭頭與文字 (Failure Annotations)
    # Audio Reasoner Drop
    ax1.annotate('Performance\nCollapse', xy=(1, 67.2), xytext=(1, 80),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 ha='center', color='red', fontweight='bold')
    
    # R1-AQA Marginal Gain
    ax1.annotate('No Significant\nGain', xy=(2, 48.7), xytext=(2, 60),
                 arrowprops=dict(facecolor='gray', shrink=0.05),
                 ha='center', color='gray', fontweight='bold')

    # ---------------------------------------------------------
    # 4. 下半部：詳細分析表格 (Detailed Table)
    # ---------------------------------------------------------
    ax2.axis('off') # 隱藏坐標軸
    
    # 表格內容
    table_data = [
        ["Method", "Technique", "Critical Failure / Observation"],
        ["Audio Reasoner [1]", "SFT on Reasoning Template", "❌ 10x Slower Inference (Latency Bottleneck)\n❌ Catastrophic Forgetting (Accuracy Drops)"],
        ["R1-AQA [2]", "RL (GRPO) Post-training", "⚠️ Sparse Reward Issue: Rewards format, not logic.\n⚠️ Single-hop degrades; Multi-hop gain is marginal."]
    ]
    
    # 繪製表格
    table = ax2.table(cellText=table_data, 
                      loc='center', 
                      cellLoc='left',
                      colWidths=[0.2, 0.25, 0.55]) # 調整列寬

    # 表格樣式美化
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5) # 調整表格高度

    # 設置 Header 樣式
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#333333') # Header 背景色
        else:
            cell.set_facecolor('#f5f5f5' if row % 2 else 'white') # 斑馬紋背景
        
        # 增加一點 Padding
        cell.set_height(0.15)

    # ---------------------------------------------------------
    # 5. 輸出
    # ---------------------------------------------------------
    plt.tight_layout()
    
    # 存檔 (可選)
    # plt.savefig('reasoning_failure_analysis.png', dpi=300, bbox_inches='tight')
    
    plt.show()

if __name__ == "__main__":
    create_reasoning_failure_chart()