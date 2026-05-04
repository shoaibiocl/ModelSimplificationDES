import pandas as pd
import re
import matplotlib.pyplot as plt

"""The code is used to count the number of instructions per arrival from Anylogic model output."""

FILE = r"/\AnylogicLogData.xlsx"

# Read both sheets
all_sheets = pd.read_excel(FILE, sheet_name=None)

process_states = all_sheets["Process States"]
sheet2 = all_sheets["Sheet2"]

# Extract agent ID from strings like '<population>[2] : 274'
def extract_agent_id(agent_str):
    match = re.search(r':\s*(\d+)$', str(agent_str).strip())
    return int(match.group(1)) if match else None

# Apply extraction
process_states["Agent ID"] = process_states["Agent"].apply(extract_agent_id)
sheet2["Agent ID"] = sheet2["Agent"].apply(extract_agent_id)

# Count occurrences per agent in each sheet
ps_counts = process_states.groupby("Agent ID").size().reset_index(name="Process States Count")
s2_counts = sheet2.groupby("Agent ID").size().reset_index(name="Sheet2 Count")

# Merge into one table
result = pd.merge(ps_counts, s2_counts, on="Agent ID", how="outer").fillna(0)
result[["Process States Count", "Sheet2 Count"]] = result[["Process States Count", "Sheet2 Count"]].astype(int)
result = result.sort_values("Agent ID").reset_index(drop=True)

# Combined total count
result["Total Count"] = result["Process States Count"] + result["Sheet2 Count"]

print(result)

# Frequency distribution
frequency_dist = (
    result["Total Count"]
    .value_counts()
    .reset_index()
)
frequency_dist.columns = ["Total Count", "Number of Agents"]
frequency_dist = frequency_dist.sort_values("Total Count").reset_index(drop=True)

print("\n=== Frequency Distribution ===")
print(frequency_dist.to_string(index=False))

# Save to Excel with two sheets
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    result.to_excel(writer, sheet_name="Agent Counts", index=False)
    frequency_dist.to_excel(writer, sheet_name="Frequency Distribution", index=False)

print("\nSaved to agent_counts_output.xlsx")

# Plot combined histogram
min_val = result["Total Count"].min()
max_val = result["Total Count"].max()

plt.figure(figsize=(10, 5))
plt.hist(result["Total Count"], bins=range(min_val, max_val + 2), color="steelblue", edgecolor="black")
plt.title("Combined Agent Call Frequency")
plt.xlabel("Number of Times Called")
plt.ylabel("Number of Agents")
plt.xticks(range(min_val, max_val + 1))
plt.tight_layout()
plt.savefig("agent_histogram.png", dpi=150)
plt.show()
print("Histogram saved to agent_histogram.png")

