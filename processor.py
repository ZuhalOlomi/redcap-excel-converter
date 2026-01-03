import pandas as pd

# This is the processor file. It contains the core logic to process the uploaded REDCap Excel file
# and convert it from long format to wide (landscape) format.

def process_file(uploaded_file):
    # ----------------------------
    # read excel file -- should be named "input.xlsx"
    # ----------------------------
    df = pd.read_excel(uploaded_file)

    # ----------------------------
    # COLUMN INDICES (0-based) -- this is a flawed approach but works for now
    # ----------------------------
    ID_IDX = 0            # Subject number
    YEAR_IDX = 2          # Repeat Instance
    DATE_IDX = 15         # Date

    LEFT_PAIN_L = 16
    LEFT_DIS_L = 17
    LEFT_TOTAL_L = 18
    RIGHT_PAIN_R = 19
    RIGHT_DIS_R = 20
    RIGHT_TOTAL_R = 21
    PCS_IDX = 22
    MCS_IDX = 23

    BASELINE_YEAR = 999
    MAX_YEAR = 50


    df.iloc[:, YEAR_IDX] = pd.to_numeric(df.iloc[:, YEAR_IDX], errors="coerce")

    # Only rows that actually have a year
    df = df[df.iloc[:, YEAR_IDX].notna()]

    # ----------------------------
    # output file
    # ----------------------------
    subjects = df.iloc[:, ID_IDX].unique()
    out = pd.DataFrame({"Subject number": subjects})

    # ----------------------------
    # baseline measures
    # ----------------------------
    base = df[df.iloc[:, YEAR_IDX] == BASELINE_YEAR].set_index(df.columns[ID_IDX])

    out["Baseline Date"] = out["Subject number"].map(base.iloc[:, DATE_IDX])

    out["Baseline Left Pain L"] = out["Subject number"].map(base.iloc[:, LEFT_PAIN_L])
    out["Baseline Disability L"] = out["Subject number"].map(base.iloc[:, LEFT_DIS_L])
    out["Baseline Total L"] = out["Subject number"].map(base.iloc[:, LEFT_TOTAL_L])

    out["Baseline Left Pain R"] = out["Subject number"].map(base.iloc[:, RIGHT_PAIN_R])
    out["Baseline Disability R"] = out["Subject number"].map(base.iloc[:, RIGHT_DIS_R])
    out["Baseline Total R"] = out["Subject number"].map(base.iloc[:, RIGHT_TOTAL_R])

    out["Baseline PCS"] = out["Subject number"].map(base.iloc[:, PCS_IDX])
    out["Baseline MCS"] = out["Subject number"].map(base.iloc[:, MCS_IDX])

    # ----------------------------
    # f/u years 
    # ----------------------------
    for year in range(1, MAX_YEAR + 1):
        yr = df[df.iloc[:, YEAR_IDX] == year].set_index(df.columns[ID_IDX])

        out[f"F/U Year {year} Date"] = out["Subject number"].map(yr.iloc[:, DATE_IDX])

        out[f"F/U Yr {year} Left Pain L"] = out["Subject number"].map(yr.iloc[:, LEFT_PAIN_L])
        out[f"F/U Yr {year} Disability L"] = out["Subject number"].map(yr.iloc[:, LEFT_DIS_L])
        out[f"F/U Yr {year} Total L"] = out["Subject number"].map(yr.iloc[:, LEFT_TOTAL_L])

        out[f"F/U Yr {year} Left Pain R"] = out["Subject number"].map(yr.iloc[:, RIGHT_PAIN_R])
        out[f"F/U Yr {year} Disability R"] = out["Subject number"].map(yr.iloc[:, RIGHT_DIS_R])
        out[f"F/U Yr {year} Total R"] = out["Subject number"].map(yr.iloc[:, RIGHT_TOTAL_R])

        out[f"F/U Yr {year} PCS"] = out["Subject number"].map(yr.iloc[:, PCS_IDX])
        out[f"F/U Yr {year} MCS"] = out["Subject number"].map(yr.iloc[:, MCS_IDX])

    return out

# Made with ❤️ by Zuhal