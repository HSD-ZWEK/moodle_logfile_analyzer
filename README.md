# Logfile Analyzer

This Python script processes CSV logfiles from a specified directory, extracts key information about course access, and summarizes the results in a new CSV file. It is designed to handle German date formats and course logs, distinguishing between guest and registered users.

---

## Features

- **Processes all CSV logfiles in a given directory**
- **Handles German month names and converts them to English for date parsing**
- **Extracts the earliest access date, course name, unique guest IPs, and unique registered users**
- **Outputs a summary CSV file (`export.csv`) with the results**
- **Skips malformed or incomplete rows gracefully**

---

## File Structure

- **Input Directory:** The script expects logfiles in the directory specified by the `PFAD` variable (default: `"2/"`).
- **Output File:** The summary is written to `export.csv` in the current working directory.

---

## How It Works

1. **Month Name Translation:**  
   The script uses the `MONATE` dictionary to translate German month names to English, enabling Python's `datetime` module to parse dates.

2. **File Processing:**  
   For each CSV logfile in the input directory:
   - Skips the header row.
   - For each row:
     - Extracts and parses the date, keeping track of the earliest date found.
     - Extracts the course name (first occurrence of a cell containing `"Kurs:"`).
     - Counts unique guest IPs (rows where the user field contains `"Gast"`).
     - Counts unique registered users (excluding those in the `BLACKLIST` and with usernames longer than 4 characters).

3. **Output:**  
   For each logfile, writes a row to `orca.csv` with:
   - Earliest access date
   - Course name
   - Number of unique guest IPs
   - Number of unique registered users

---

## Usage

1. **Prepare your logfiles:**  
   Place all CSV logfiles to be analyzed in the directory specified by `PFAD` (default: `"2/"`).

2. **Run the script:**  
   ```bash
   python your_script_name.py
