# National-ID-OCR-Extractor
Python script to extract Egyptian National ID (14-digit) using Gemini's Vision API and converting Arabic numerals.
🇪🇬 National ID OCR Extractor

This Python script uses the Gemini API for multimodal analysis and OCR (Optical Character Recognition) to extract the 14-digit Egyptian National ID number from an image.

It automatically handles the conversion from Eastern Arabic numerals (like ٣٠٤٠٨١٢١١٨٧١) found on the ID card to standard Western Arabic numerals (304081211871), providing a clean, usable string.

⚙️ Prerequisites

Python 3 installed on your system.

requests library: This is used for making API calls.

pip install requests


A Gemini API Key: You must obtain a personal API key for free from the Google AI Studio API Key Page.

🔑 Security Setup (CRITICAL)

Never hardcode your API key in the source code. To run this script securely, you must set your Gemini API Key as an environment variable named GEMINI_API_KEY.

Operating System

Command to Set Key (Temporary for current session)

Windows (Command Prompt)

set GEMINI_API_KEY=YOUR_NEW_API_KEY

macOS / Linux

export GEMINI_API_KEY="YOUR_NEW_API_KEY"

Note: For a permanent setup on macOS/Linux, add the export command to your shell's configuration file (~/.bashrc or ~/.zshrc).

🚀 How to Run the Script

Save the file: Ensure the extract_national_id.py script is saved locally.

Set the API Key: Run the appropriate command above to set your GEMINI_API_KEY.

Execute the script: Run the file from your terminal.

python extract_national_id.py


Provide the Path: The script will prompt you to enter the full path to the image file containing the Egyptian ID.

📝 Project Structure

extract_national_id.py: The core Python script containing the API logic and conversion functions.

README.md: This file.

.gitignore: Configured to ignore environment files (.env) and Python compilation artifacts for security.

Disclaimer

This script is intended for educational purposes and personal use with legally obtained images. Always comply with local privacy and data protection laws when handling sensitive personal information.
