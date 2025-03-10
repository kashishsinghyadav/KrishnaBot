import re
import json

def extract_gita_text(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    structured_data = {}
    current_chapter = None
    current_verses = {}

    for line in content:
        line = line.strip()

        # Ignore empty lines and non-Gita text
        if not line or "Srimad-Bhagavad-Gita" in line or "[p." in line or "<page" in line:
            continue

        # Detect Chapter Titles (Matches "I. THE GRIEF OF ARJUNA")
        chapter_match = re.match(r'^([IVXLCDM]+)\.\s+(.*)', line)
        if chapter_match:
            if current_chapter:
                structured_data[current_chapter] = current_verses  # Store previous chapter
            chapter_number = chapter_match.group(1)
            chapter_name = chapter_match.group(2).strip()
            current_chapter = f"CHAPTER {chapter_number} - {chapter_name}"
            current_verses = {}  # Reset verses for the new chapter
            continue

        # Detect Verse Numbers and Text (e.g., "1.1 Some text here")
        verse_match = re.match(r'^(\d+\.\d+)\s+(.+)', line)
        if verse_match:
            verse_number = verse_match.group(1).strip()
            verse_text = verse_match.group(2).strip()
            current_verses[verse_number] = verse_text
            continue

        # Append multi-line text to the last detected verse
        if current_verses and line:
            last_verse = list(current_verses.keys())[-1]
            current_verses[last_verse] += " " + line  # Append to the last verse

    # Save last chapter data
    if current_chapter:
        structured_data[current_chapter] = current_verses

    # Save as JSON
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

# Run the extraction
input_file = "sbg.txt"
output_file = "gita_data.json"
extract_gita_text(input_file, output_file)

print(f"✅ Extraction complete! JSON saved at: {output_file}")
