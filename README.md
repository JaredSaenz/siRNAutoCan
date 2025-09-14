# siRNAutoCan
This python script automates the evaluation of siRNA candidates using the siDirect 2.0 web service and scores them based on criteria from Fakhr et al. (2016). It generates two CSV files: one with raw siRNA candidates from siDirect and another with quality scores derived from the article's Excel-based methodology.
## Overview
The tool:
Reads a FASTA file containing a target sequence.
Submits the sequence to siDirect 2.0 using Selenium for web scraping.
Extracts siRNA candidates and their attributes (e.g., target position, sequences, Tm values, mismatches).
Evaluates candidates based on automated criteria (6–8, 11–18) from Fakhr, E., Zare, F., & Teimoori-Toolabi, L. (2016). Precise and efficient siRNA design: a key point in competent gene silencing. Cancer Gene Therapy, 23(4), 73–82. DOI:10.1038/cgt.2016.4.
Outputs two CSV files:
siRNA_results.csv: Contains raw siRNA candidate data from siDirect, including target positions, guide/passenger sequences, Ui-Tei scores, and effective siRNA predictions (higher numbers indicate better predicted effectiveness, corresponding to siDirect's blue color coding).
quality_results.csv: Includes selected data from siRNA_results.csv plus quality scores based on the article's automated criteria. Rows are sorted by quality (highest to lowest).

## Files
main_sirnas.py: Main script that handles web scraping, data processing, and CSV generation.
quality_nopage_v2.py: Contains the get_quality function to score siRNA candidates based on criteria 6–8 and 11–18 from Fakhr et al. (2016).
siRNA_results.csv: Output with raw siDirect data.
quality_results.csv: Output with quality scores and sorted results.

## Requirements
Python 3.x
Libraries: selenium, beautifulsoup4, python-dotenv, csv, os
ChromeDriver (compatible with your Chrome version)
A FASTA file (.fa or .fasta) with the target sequence

Install dependencies:
pip install selenium beautifulsoup4

## Usage
Place ChromeDriver in ~/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe (update path in main_sirnas.py if needed).
Create a .env file in the project root to store sensitive data (optional, not implemented in current code).
Run the script:python main_sirnas.py

Enter the FASTA file name when prompted (e.g., sequence.fa or sequence.fasta).
The script generates siRNA_results.csv and quality_results.csv.

## Notes
Quality Scoring: The quality_results.csv file includes a quality column reflecting scores from automated criteria (6–8, 11–18). Manual criteria (1–5, 9–10) from Fakhr et al. (2016) are not yet implemented.
Effective siRNA Candidates: Higher values in this column (e.g., 4 for blue-coded siRNAs on siDirect) indicate better predicted effectiveness.
Limitations: Requires a stable internet connection for siDirect access and ChromeDriver compatibility with your Chrome version.
Future Improvements: Add support for manual criteria (1–5, 9–10) and integrate .env for secure configuration.

Citation
Fakhr, E., Zare, F., & Teimoori-Toolabi, L. (2016). Precise and efficient siRNA design: a key point in competent gene silencing. Cancer Gene Therapy, 23(4), 73–82. DOI:10.1038/cgt.2016.4.
