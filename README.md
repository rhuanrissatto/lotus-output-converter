# lotus-output-converter
Automated converter for Lotus Suspensions Analysis outputs to structured excels spreadsheets using Python and Pandas

--

##Overview

Previously, simulation results from Lotus Suspension Analysis were manually rewritten into spreadsheets, making the process repetitive, time-consuming and susceptible to transcription errors.

This project automates the extraction to Excel spreadsheets from the text export from Lotus.

--

## Technologies Used

- Python
- Pandas
- OpenPyXL
- Regular Expressions (Regex)

--

## Installation

Clone the repository:

```bash
git clone https://github.com/rhuanrissatto/lotus-output-converter.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---
## Usage

Run the script:

```bash
python Lotus-Excel.py
```

Paste the Lotus output into the terminal.

Finish input with:

### Windows

```text
Ctrl + Z + Enter
```

### Linux / Mac

```text
Ctrl + D
```

The generated spreadsheet will be saved automatically as:

```text
lotus_output.xlsx
```

---

## Example Output Structure

The generated Excel file contains:

- Front Suspension Points
- Rear Suspension Points
- Front Bump Simulation
- Rear Bump Simulation
- Front Roll Simulation
- Rear Roll Simulation
- Steering Travel Simulation

## Download

Download the newest version in:



## Author

Rhuan Rissatto Araújo  
Formula UTFPR — 2026
