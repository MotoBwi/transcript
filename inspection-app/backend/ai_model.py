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
