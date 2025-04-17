# Power Query + Python: Merging and Analyzing Contract Periods

## 📌 Purpose

This Power Query script, enhanced with embedded Python code, is designed to:

- Retrieve data from a SQL database,
- Merge overlapping or adjacent date ranges (e.g., contract periods) for each unique ID,
- Filter only the ranges that include **today's date**,
- Calculate the number of **continuous active days on contract** without a break longer than a specified number of days (`Parameter1`).

## ⚙️ How It Works

### 1. **Input**
- **Parameter1**: a number indicating the maximum allowed gap (in days) between contract periods to still treat them as continuous.
- Source data is retrieved using `Sql.Database`.

### 2. **Python – Merging Date Ranges**
- The Python script sorts the dataset by `ID` and `Start` date.
- For each `ID`, it merges overlapping or adjacent periods (where the next period's `Start` is earlier than or equal to the previous `End`).
- The result is a new DataFrame with:
  - `ID`
  - `Start Date`
  - `End Date`

### 3. **Power Query – Transformations & Analysis**
- Converts columns to appropriate data types (`date`, `text`).
- Adds an index column.
- Adjusts the `End Date` by subtracting `Parameter1` days — interpreted as the allowable gap.
- Filters only those date ranges that include today's date.
- Calculates the number of days from `Start Date` to today — treated as continuous active period length.

## 🧪 Example Usage

If `Parameter1 = 30`, then:

- Contract periods with a gap of **up to 30 days** between them are merged into one continuous range.
- Any range that **does not include today** is filtered out.
- The final column shows:  
  **"Current days on contracts in row (without a break longer than 30 days)"**

## 🧰 Requirements

- Power BI or Power Query environment
- Python scripting enabled (with `pandas` library installed)
- Access to the SQL data source

## 📁 Final Output

A table with the following columns:

- `ID`
- `Start Date`
- `End Date`
- `Index`
- `Today`
- `Current days on contracts in row (without a break longer than X days)`

---

