# --- 1. Import Libraries ---
import tkinter as tk
from tkinter import scrolledtext
import nltk
import re

# --- 2. Download Necessary Data (One-time setup) ---
print("Please wait, downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('punkt_tab', quiet=True)
print("Download complete!")

# --- 3. Prepare Tools ---
# These are the tools we use to process words
english_stopwords = set(nltk.corpus.stopwords.words('english'))
my_stemmer = nltk.stem.PorterStemmer()
my_lemmatizer = nltk.stem.WordNetLemmatizer()

# --- 4. My Sentences ---
# A list of sentences to choose from
sentence_list = [
    "They picnicked by the pool, then lay back on the grass and looked at the stars.",
    "Apple today announced the second generation iPhone SE featuring a powerful new iPhone.",
    "The presentation highlighted the key achievements of the project's development.",
    "Doc worked carefully washing the glasses.",
    "My 2 favorite numbers are 19 and 42."
]

# --- 5. The Analysis Function ---
# This function runs when you click the button
def run_analysis():
    # Get the selected sentence number (index)
    selected_index = listbox.curselection()
    
    # Check if user actually selected something
    if not selected_index:
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.END, "Please select a sentence first!")
        return

    # Get the actual text of the selected sentence
    sentence = listbox.get(selected_index)
    
    # Clear the result area
    result_area.delete(1.0, tk.END)
    
    # --- Step 1: Preprocessing ---
    # Make lowercase
    lower_text = sentence.lower()
    # Remove punctuation (keep only letters, numbers, spaces)
    clean_text = re.sub(r'[^a-z0-9\s]', '', lower_text)
    # Tokenize (split into words)
    tokens = nltk.tokenize.word_tokenize(clean_text)
    
    result_area.insert(tk.END, "=== 1. Preprocessing ===\n")
    result_area.insert(tk.END, f"Original: {sentence}\n")
    result_area.insert(tk.END, f"Tokens:   {tokens}\n\n")

    # --- Step 2: Stopword Removal ---
    # Create a new list with only important words
    filtered_words = []
    for word in tokens:
        if word not in english_stopwords:
            filtered_words.append(word)
            
    result_area.insert(tk.END, "=== 2. Stopword Removal ===\n")
    result_area.insert(tk.END, f"{filtered_words}\n\n")

    # --- Step 3: Stemming ---
    # Chop off word endings
    stemmed_words = []
    for word in filtered_words:
        stemmed_word = my_stemmer.stem(word)
        stemmed_words.append(stemmed_word)
        
    result_area.insert(tk.END, "=== 3. Stemming ===\n")
    result_area.insert(tk.END, f"{stemmed_words}\n\n")

    # --- Step 4: Lemmatization ---
    # Find the dictionary root word
    lemmatized_words = []
    for word in filtered_words:
        lemma = my_lemmatizer.lemmatize(word)
        lemmatized_words.append(lemma)
        
    result_area.insert(tk.END, "=== 4. Lemmatization ===\n")
    result_area.insert(tk.END, f"{lemmatized_words}\n\n")

    # --- Step 5: POS Tagging ---
    # Identify Nouns, Verbs, Adjectives, etc.
    # We use the original tokens for better context
    pos_tags = nltk.pos_tag(tokens)
    
    result_area.insert(tk.END, "=== 5. POS Tagging ===\n")
    result_area.insert(tk.END, f"{pos_tags}\n\n")

    # --- Step 6: Named Entity Recognition (NER) ---
    # Find names of People, Organizations, Locations
    # We must re-tokenize the ORIGINAL sentence (with Capital letters)
    original_tokens = nltk.tokenize.word_tokenize(sentence)
    original_tags = nltk.pos_tag(original_tokens)
    ner_tree = nltk.ne_chunk(original_tags)
    
    result_area.insert(tk.END, "=== 6. NER (Named Entities) ===\n")
    
    found_entities = []
    # Look through the NER tree
    for item in ner_tree:
        if hasattr(item, 'label'):
            entity_name = ' '.join(c[0] for c in item)
            entity_type = item.label()
            found_entities.append(f"{entity_name} ({entity_type})")
            
    if len(found_entities) > 0:
        result_area.insert(tk.END, f"{found_entities}\n")
    else:
        result_area.insert(tk.END, "No named entities found.\n")

# --- 6. Build the User Interface ---
window = tk.Tk()
window.title("Beginner NLP Tool")
window.geometry("700x600")

# Instruction Label
lbl = tk.Label(window, text="Click a sentence below:", font=("Arial", 12, "bold"))
lbl.pack(pady=5)

# Listbox (Simpler than dropdown)
listbox = tk.Listbox(window, width=80, height=6)
for s in sentence_list:
    listbox.insert(tk.END, s)
listbox.pack(pady=5)
# Select the first item by default
listbox.select_set(0)

# Button
btn = tk.Button(window, text="Analyze Selected Sentence", command=run_analysis, bg="lightblue")
btn.pack(pady=10)

# Result Area
result_area = scrolledtext.ScrolledText(window, width=80, height=20)
result_area.pack(pady=10)

# Start the main loop
window.mainloop()