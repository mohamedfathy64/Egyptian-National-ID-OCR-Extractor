import requests
import base64
import json
import time
import os

# --- Configuration ---
# IMPORTANT: Set your Gemini API Key as an environment variable named GEMINI_API_KEY.
API_KEY = os.environ.get('GEMINI_API_KEY', 'PUT_YOUR_API_KEY_HERE')
API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"

# --- Utility Functions ---
def image_to_base64(filepath):
    """Converts a local image file to a base64 encoded string."""
    print(f"Loading image from: {filepath}")
    try:
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Image file not found at path: {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the image: {e}")
        return None

def manual_conversion_fallback(text):
    """Convert Eastern Arabic digits to Western Arabic digits (final fallback)."""
    ARABIC_TO_WESTERN = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    western_digits = ''.join(ARABIC_TO_WESTERN.get(c, c) for c in text)
    final_id = ''.join(filter(str.isdigit, western_digits))
    return final_id[:14] if len(final_id) >= 14 else None

def extract_id_from_image(image_path):
    """Send image to Gemini API and extract 14-digit Egyptian National ID."""
    base64_image = image_to_base64(image_path)
    if not base64_image:
        return None

    mime_type = "image/jpeg"
    system_instruction = (
        "You are an OCR and data extraction expert focused on identifying Egyptian National "
        "ID numbers (14 digits) from images. The number is typically written in Eastern "
        "Arabic numerals. You MUST find the 14-digit sequence, convert it to Western Arabic "
        "numerals (0-9), and return *only* the 14-digit string. Do not include spaces, "
        "explanations, or any surrounding text. The required length is exactly 14 characters."
    )
    user_query = "Extract the 14-digit National ID from the image."

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": user_query},
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": base64_image
                        }
                    }
                ]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
    }

    url = API_URL_TEMPLATE.format(model=MODEL_NAME, key=API_KEY)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"Attempting API call (Attempt {attempt + 1}/{max_retries})...")
            response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            response.raise_for_status()

            result = response.json()
            if result.get('candidates'):
                text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                cleaned_id = ''.join(filter(str.isdigit, text))

                if len(cleaned_id) == 14:
                    print("✅ Extraction successful.")
                    return cleaned_id
                else:
                    print(f"⚠️ Extracted string not 14 digits. Using manual conversion fallback.")
                    return manual_conversion_fallback(text)

            print("⚠️ API response did not contain valid content.")
            return None

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            if e.response.status_code in [429, 500, 503] and attempt < max_retries - 1:
                delay = 2 ** attempt
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    print("❌ API call failed after multiple retries.")
    return None

# --- Main Execution ---
if __name__ == "__main__":
    if API_KEY == "PUT_YOUR_API_KEY_HERE":
        print("\n*** ERROR: Please set your GEMINI_API_KEY environment variable. ***\n")
    else:
        IMAGE_FILE_PATH = input("Enter full path to ID image file: ")
        print("--- Starting National ID Extraction ---")
        extracted_id = extract_id_from_image(IMAGE_FILE_PATH)

        if extracted_id:
            print("\n=============================================")
            print(f"Extracted National ID (14 digits): {extracted_id}")
            print("=============================================")
        else:
            print("\n❌ Failed to extract the 14-digit National ID.")
        print("--- Extraction Complete ---")
