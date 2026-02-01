
import matplotlib.pyplot as plt

def create_priority_chart(df):
    df.columns = df.columns.str.strip()

    top10 = (
        df.sort_values("priority_score", ascending=False)
          .head(10)
          .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(top10["kecamatan"], top10["priority_score"], color="#d62728", label="Nilai Prioritas")

    ax.set_title("10 Kecamatan dengan Nilai Prioritas Tertinggi", fontsize=14, fontweight='bold')
    ax.set_xlabel("Kecamatan")
    ax.set_ylabel("Nilai Prioritas")
    
    plt.xticks(rotation=45, ha="right")
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i, v in enumerate(top10["priority_score"]):
        ax.text(i, v + 2, f"{v:.1f}", ha='center', fontweight='bold')

    plt.tight_layout()
    return fig