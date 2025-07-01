import pandas as pd
from scipy.stats import mannwhitneyu, kruskal
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Daten einlesen
file_path = "data/full_data_transformed.csv"
df = pd.read_csv(file_path, parse_dates=["timestamp"])

# 2. Zeitkomponenten extrahieren
df["hour"]    = df["timestamp"].dt.hour
df["minute"]  = df["timestamp"].dt.minute
df["weekday"] = df["timestamp"].dt.weekday  # 0=Mo … 6=So

# 3. Filterung 01:00–01:29 und echte Kopie
df_filtered = df[(df["hour"] == 1) & (df["minute"] < 30)].copy()

# 4. day_type-Spalte mit .loc setzen
df_filtered.loc[:, "day_type"] = df_filtered["weekday"] \
    .apply(lambda x: "Werktag (Mo-Sa)" if x < 6 else "Sonntag")

# 5. Hypothesentest: Mann–Whitney-U
group_wd = df_filtered.loc[df_filtered["day_type"]=="Werktag (Mo-Sa)", "1.7.0"]
group_so = df_filtered.loc[df_filtered["day_type"]=="Sonntag",        "1.7.0"]
stat_mw, p_mw = mannwhitneyu(group_wd, group_so, alternative="two-sided")

# 6. Erweiterung: Kruskal–Wallis-Test über alle Wochentage
grouped_by_day = [df_filtered[df_filtered["weekday"] == i]["1.7.0"] for i in range(7)]
stat_kw, p_kw = kruskal(*grouped_by_day)

# 7. Boxplot direkt im Long-Format
plt.figure(figsize=(10,5))
sns.boxplot(
    x="weekday",
    y="1.7.0",
    data=df_filtered,
    order=list(range(7))
)
plt.title("Stromverbrauch 01:00–01:30 nach Wochentag")
plt.xlabel("Wochentag (0=Mo, …, 6=So)")
plt.ylabel("Verbrauch (Watt)")
plt.tight_layout()

os.makedirs("visualize", exist_ok=True)
plt.savefig("visualize/boxplot_0100_0130_by_weekday.png")
plt.show()

# 8. Ergebnis in native Python-Typen
result = {
    "Mittelwert Werktage (Mo-Sa)":  group_wd.mean().item(),
    "Mittelwert Sonntag":           group_so.mean().item(),
    "Mann–Whitney-U Teststatistik": stat_mw.item(),
    "Mann–Whitney-U p-Wert":        p_mw.item(),
    "Kruskal–Wallis Teststatistik": stat_kw,
    "Kruskal–Wallis p-Wert":        p_kw,
    "Signifikanzniveau α":          0.05,
    "Mann–Whitney H0 abgelehnt":    bool(p_mw < 0.05),
    "Kruskal–Wallis H0 abgelehnt":  bool(p_kw < 0.05)
}

print(result)
