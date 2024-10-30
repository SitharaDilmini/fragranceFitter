import chardet
import pandas as pd


file = 'data/Original.csv'
with open(file, 'rb') as f:      # Opens the file in binary mode
    encoding = chardet.detect(f.read())['encoding']

try:
    data = pd.read_csv(file, encoding=encoding)
except UnicodeDecodeError:
    print(f"Failed to read the file with detected encoding '{encoding}', trying 'ISO-8859-1'.")
    data = pd.read_csv(file, encoding='ISO-8859-1')

def extract_occasion(description, notes,intensity):
  occasion_keywords = {
        'Professional Event': [
            'interview', 'job', 'career', 'meeting', 'business', 'office', 'work', 'corporate', 'professional', 
            'low intensity', 'moderate intensity', 'subtle', 'soft', 'delicate', 'airy', 'gentle', 'steady', 
            'musk', 'cedar', 'vetiver', 'sandalwood', 'bergamot', 'cardamom', 'cypress', 'iris'
        ],
        'Party': [
            'party', 'celebration', 'fun', 'festive', 'moderate intensity', 'high intensity', 'prominent', 
            'distinct', 'bold', 'club', 'nightclub', 'dance', 'impactful', 'vivid', 'strong', 
            'amber', 'patchouli', 'vanilla', 'tonka bean', 'leather', 'tobacco', 'rum', 'oud'
        ],
        'Casual Event': [
            'casual', 'everyday', 'routine', 'relaxed', 'shopping', 'mall', 'store', 'retail', 
            'apple', 'pear', 'peach', 'melon', 'apricot', 'plum', 'cherry', 'basil', 'mint'
        ],
        'Formal Event': [
            'formal', 'elegant', 'sophisticated', 'black-tie', 'rich', 'deep', 'robust', 'graduation', 
            'ceremony', 'commencement', 'theater', 'play', 'drama', 'prominent', 
            'jasmine', 'rose', 'gardenia', 'lily', 'tuberose', 'orchid', 'ylang-ylang', 'mimosa'
        ],
        'Sports Event': [
            'sports', 'exercise', 'workout', 'gym', 'fitness', 'mint', 'eucalyptus', 'pine', 
            'juniper', 'grapefruit', 'lemon', 'lime', 'orange', 'mandarin', 'ginger', 'peppermint'
        ],
        'Romantic': [
            'romantic', 'love', 'intimate', 'floral', 'date', 'dinner', 'evening', 'appealing', 
            'wedding', 'marriage', 'bride', 'groom', 'lavender', 'violet', 'peony', 'freesia', 
            'magnolia', 'honeysuckle', 'narcissus', 'hyacinth', 'heliotrope'
        ],
        'Outdoor Event': [
            'picnic', 'outdoor', 'park', 'nature', 'beach', 'seaside', 'coast', 'ocean', 'vacation', 
            'holiday', 'trip', 'travel', 'journey', 'adventure', 'sea salt', 'driftwood', 'algae', 
            'kelp', 'pineapple', 'coconut', 'tiare flower', 'frangipani', 'marine notes'
        ],
        'Religious Event': [
            'religious', 'service', 'ritual', 'worship', 'incense', 'myrrh', 'frankincense', 
            'sandalwood', 'rosewood', 'patchouli', 'spikenard'
        ]
    }

  description = str(description) if pd.notnull(description) else ''
  notes = str(notes) if pd.notnull(notes) else ''
  intensity = str(intensity) if pd.notnull(intensity) else ''

  text = description.lower() + ' ' + notes.lower() + ' ' + intensity.lower()

  detected_occasions = []
  for occasion, keywords in occasion_keywords.items(): #The .items() method on a dictionary returns a list of its key-value pairs, which are unpacked into occasion and keywords during each iteration of the loop.
    if any(keyword in text for keyword in keywords):
      detected_occasions.append(occasion)

  return ', '.join(detected_occasions) if detected_occasions else ''


def extract_season(description, notes):
    seasons = {
        "spring": [
            "blossom", "fresh", "floral", "green", "light", "renewal", "awakening", "crisp", "blooming", 
            "verdant", "dew-kissed", "lilac", "daffodil", "hyacinth", "peony", "cherry blossom", "new growth", "rain", 
            "grass", "herbal", "tulip", "narcissus"
        ],
        "summer": [
            "sunny", "bright", "citrus", "vibrant", "oceanic", "beachy", "refreshing", "lively", "solar", "energetic", 
            "juicy", "tropical fruit", "melon", "watermelon", "pineapple", "mango", "coconut", "suntan lotion", 
            "saltwater", "marine", "aquatic", "breezy"
        ],
        "autumn": [
            "cozy", "spicy", "amber", "woody", "earthy", "rustic", "harvest", "golden", "nutty", "smoky", "crisp", 
            "cinnamon", "clove", "nutmeg", "pumpkin", "maple", "apple cider", "bonfire", "fall leaves", "moss", "chestnut"
        ],
        "winter": [
            "frosty", "rich", "musky", "balsamic", "deep", "comforting", "warm", "smoky", "incense", "creamy", "pine", 
            "vanilla", "peppermint", "fir", "cedar", "eucalyptus", "myrrh", "frankincense", "cashmere", "cocoa", "gingerbread"
        ],
        "tropical": [
            "exotic", "lush", "island", "paradise", "coconut", "tropical", "sultry", "fragrant", "juicy", "rainforest", 
            "hibiscus", "plumeria", "passionfruit", "papaya", "guava", "tiare", "frangipani", "monoi", "sandalwood", "banana"
        ]
    }


    description = str(description) if pd.notnull(description) else ''
    notes = str(notes) if pd.notnull(notes) else ''

    text = description.lower() + ' ' + notes.lower()

    detected_seasons = []
    for season, keywords in seasons.items():
        if any(keyword in text for keyword in keywords):
            detected_seasons.append(season)

    return ', '.join(detected_seasons) if detected_seasons else ''


def extract_weather(description, notes):
    weather_keywords = {
        "sunny": [
            "bright", "clear", "warm", "hot", "sunny", "radiant", "sunny skies", "blazing", "sunshine", "golden", 
            "citrus", "vibrant", "solar", "energetic", "fresh", "fruity", "dry", "tropical", "breezy", "luminous"
        ],
        "rainy": [
            "wet", "rainy", "showers", "drizzle", "downpour", "stormy", "damp", "puddles", "overcast", "soggy", 
            "aquatic", "dewy", "fresh", "earthy", "herbal", "green", "moist", "humid", "misty", "mossy"
        ],
        "cloudy": [
            "overcast", "cloudy", "grey", "gloomy", "dull", "misty", "hazy", "foggy", "murky", "covered skies", 
            "soft", "powdery", "light", "clean", "airy", "musk", "subtle", "muted", "diffused", "gentle", "dim"
        ],
        "snowy": [
            "snowy", "cold", "frosty", "icy", "snow-covered", "wintry", "blizzard", "flakes", "freezing", "white", 
            "spicy", "warm", "rich", "woody", "balsamic", "smoky", "comforting", "crisp", "chilly", "pine", "eucalyptus"
        ]
    }


    description = str(description) if pd.notnull(description) else ''
    notes = str(notes) if pd.notnull(notes) else ''

    text = description.lower() + ' ' + notes.lower()

    detected_weathers = []
    for weather, keywords in weather_keywords.items():
        if any(keyword in text for keyword in keywords):
            detected_weathers.append(weather)

    return ', '.join(detected_weathers) if detected_weathers else ''



def extract_intensity(description, notes):

    intensity_keywords = {
        'Light': [
            'subtle', 'gentle', 'mild', 'soft', 'delicate', 'airy', 'light', 'faint', 'whisper', 'soft touch', 
            'barely there', 'hint', 'touch', 'feather-light', 'evanescent', 'gossamer', 'floral', 'transparent', 
            'ethereal', 'diaphanous', 'slight', 'nuanced', 'fragile'
        ],
        'Moderate': [
            'balanced', 'moderate', 'medium', 'even', 'steady', 'consistent', 'noticeable', 'discernible', 'present', 
            'average', 'prominent', 'distinct', 'clear', 'evident', 'marked', 'perceptible', 'appreciable', 
            'sufficient', 'ample', 'measured', 'controlled', 'tempered', 'reasonable'
        ],
        'Strong': [
            'strong', 'powerful', 'bold', 'intense', 'potent', 'robust', 'concentrated', 'rich', 'deep', 'vivid', 
            'heavy', 'impactful', 'profound', 'extreme', 'overpowering', 'dominant', 'commanding', 'Ginger', 
            'piercing', 'forceful', 'unyielding', 'penetrating', 'vehement', 'resounding', 'demanding', 
            'vigorous', 'stark', 'unmistakable', 'assertive', 'fierce'
        ]
    }

    description = str(description) if pd.notnull(description) else ''
    notes = str(notes) if pd.notnull(notes) else ''

    text = description.lower() + ' ' + notes.lower()

    light_score = sum(word in text for word in intensity_keywords["Light"])
    moderate_score = sum(word in text for word in intensity_keywords["Moderate"])
    intense_score = sum(word in text for word in intensity_keywords["Strong"])

    if light_score > moderate_score and light_score > intense_score:
        return "Light"
    elif moderate_score > light_score and moderate_score > intense_score:
        return "Moderate"
    else:
        return "Strong" if intense_score else 'Moderate'

def extract_gender(description, notes):
    gen_keywords = {
        "Male": [
            "woody", "spicy", "rugged", "masculine", "leather", "tobacco", "earthy", "musk", "strong", "bold", "dark", "intense", 
            "cedar", "vetiver", "amber", "oud", "sandalwood", "pepper", "smoke", "pine", "birch", "animalic", "patchouli", 
            "his", "him", "balsamic", "cumin", "clove", "labdanum", "oakmoss", "styrax", "suede", "cognac", "rum", "whiskey", 
            "resinous", "tar", "woody oriental"
        ],
        "Female": [
            "floral", "sweet", "romantic", "delicate", "feminine", "lush", "soft", "rose", "violet", "jasmine", "elegant", 
            "sensual", "fruity", "vanilla", "gardenia", "tuberose", "peony", "lily", "orchid", "honeysuckle", "powdery", 
            "peach", "berry", "magnolia", "orange blossom", "neroli", "ylang-ylang", "cherry blossom", "she", "her", "mimosa", 
            "freesia", "daffodil", "lilac", "linden blossom", "heliotrope", "rosewood", "tonka bean", "white musk", "creamy"
        ],
        "Unisex": [
            "fresh", "clean", "citrus", "herbal", "balanced", "neutral", "universal", "modern", "green", "aquatic", 
            "bergamot", "lemon", "lime", "mint", "tea", "lavender", "sage", "thyme", "rosemary", "juniper", "aldehydic", 
            "neroli", "ginger", "grapefruit", "eucalyptus", "salt", "sea", "fig", "bamboo", "vetiver", "cedarwood", 
            "cypress", "cardamom", "musk", "spicy", "fougère", "ambergris", "violet leaf", "cucumber", "mint", "ozonic", 
            "maritime", "basil", "anise", "clary sage"
        ]
    }



    description = str(description) if pd.notnull(description) else ''
    notes = str(notes) if pd.notnull(notes) else ''

    text = description.lower() + ' ' + notes.lower()

    male_score = sum(word in text for word in gen_keywords["Male"])
    female_score = sum(word in text for word in gen_keywords["Female"])
    unisex_score = sum(word in text for word in gen_keywords["Unisex"])

    if male_score > female_score and male_score > unisex_score:
        return "male"
    elif female_score > male_score and female_score > unisex_score:
        return "female"
    else:
        return "unisex"


data['Season'] = data.apply(lambda row: extract_season(row['Description'], row['Notes']), axis=1)
data['Weather'] = data.apply(lambda row: extract_weather(row['Description'], row['Notes']), axis=1)
data['Intensity'] = data.apply(lambda row: extract_intensity(row['Description'], row['Notes']), axis=1)
data['Gender'] = data.apply(lambda row: extract_gender(row['Description'], row['Notes']), axis=1)
data['Occasion'] = data.apply(lambda row: extract_occasion(row['Description'], row['Notes'], row['Intensity']), axis=1)


data.to_csv('data/updated_dataset_new.csv', index=False)
print("Dataset has been updated.")


data.head()