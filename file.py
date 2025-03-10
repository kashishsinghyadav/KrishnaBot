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

        # Ignore empty lines and unwanted metadata
        if not line or "[p." in line or "[*" in line or "Srimad-Bhagavad-Gita" in line:
            continue

        # Detect Chapter Titles (e.g., "FIRST CHAPTER")
        chapter_match = re.match(r'^(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|ELEVENTH|TWELFTH|THIRTEENTH|FOURTEENTH|FIFTEENTH|SIXTEENTH|SEVENTEENTH|EIGHTEENTH)\s+CHAPTER', line, re.IGNORECASE)
        if chapter_match:
            if current_chapter:
                structured_data[current_chapter] = current_verses  # Store previous chapter
            current_chapter = chapter_match.group(1).title() + " Chapter"
            current_verses = {}  # Reset verses for the new chapter
            continue

        # Detect Verse Numbers (e.g., "1. Tell me, O Sanjaya!")
        verse_match = re.match(r'^(\d+)\.\s+(.+)', line)
        if verse_match:
            verse_number = verse_match.group(1).strip()
            verse_text = verse_match.group(2).strip()
            current_verses[verse_number] = verse_text
            continue

        # Detect Multi-line Verses & Ensure Correct Numbering
        multi_verse_match = re.match(r'^(\d+-\d+)\.\s+(.+)', line)  # Matches "32-34. Text..."
        if multi_verse_match:
            verse_range = multi_verse_match.group(1).strip()
            verse_text = multi_verse_match.group(2).strip()
            start, end = map(int, verse_range.split('-'))  # Extract start and end verse numbers
            for i in range(start, end + 1):
                current_verses[str(i)] = verse_text
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
output_file = "gita_data_fixed.json"
extract_gita_text(input_file, output_file)

print(f"✅ Extraction complete! JSON saved at: {output_file}")
