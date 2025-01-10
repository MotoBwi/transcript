# ai_model.py

def analyze_text(text):
    categories = {'Maintenance': ['faulty', 'broken', 'damaged'],
                  'Safety': ['hazard', 'unsafe', 'dangerous'],
                  'Structure': ['pillar', 'wall', 'foundation']}
    
    issue_category = "General"
    for category, keywords in categories.items():
        if any(keyword in text.lower() for keyword in keywords):
            issue_category = category
            break
    
    return issue_category
# Example ai_model.py
def analyze_text(transcription):
    # Example logic to categorize the issue based on the transcription
    if "paint" in transcription.lower():
        return "Paint"  # Return the department name (e.g., "Paint")
    elif "electrical" in transcription.lower():
        return "Electrical"
    else:
        return "General"  # Default category

