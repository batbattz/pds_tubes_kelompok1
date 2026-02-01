
import matplotlib.pyplot as plt

def create_top_10_chart(df):
    df.columns = df.columns.str.strip()

    top10_sppg = (
        df.sort_values("jumlah_sppg", ascending=False)
          .head(10)
          .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(top10_sppg["kecamatan"], top10_sppg["jumlah_sppg"], color="#ff7f0e", label="Jumlah SPPG")

    ax.set_title("Top 10 Kecamatan dengan SPPG Terbanyak", fontsize=14, fontweight='bold')
    ax.set_xlabel("Kecamatan")
    ax.set_ylabel("Jumlah SPPG")
    
    ax.set_ylim(0, 60)
    
    for i, v in enumerate(top10_sppg["jumlah_sppg"]):
        ax.text(i, v + 1, str(int(v)), ha='center', fontweight='bold')

    plt.xticks(rotation=45, ha="right")
    ax.legend()
    
    plt.tight_layout()
    return fig