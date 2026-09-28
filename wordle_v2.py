import random
import urllib.request

def load_sowpods_words():
    """Download and load valid 5-letter words from the standard SOWPODS dictionary."""
    url = "https://raw.githubusercontent.com/jesstess/Scrabble/master/scrabble/sowpods.txt"
    print("Loading dictionary...")
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            # Extract 5-letter uppercase words
            words = set(word.strip().upper() for word in text.splitlines() if len(word.strip()) == 5)
            return words
    except Exception as e:
        print(f"Error loading SOWPODS online: {e}")
        # Fallback minimal word list if internet connection fails
        return {"CRANE", "SLATE", "PLANT", "SHARK", "TRAIN", "GHOST", "WORLD", "APPLE"}

def evaluate_guess(guess, secret):
    """
    Evaluates guess against secret using Wordle logic with exact duplicate rules:
    - 'G': Correct letter, correct spot
    - 'Y': Letter in word, wrong spot (limited by remaining letter counts)
    - 'B': Letter not in word / duplicate count exceeded
    """
    res = ['B'] * 5
    secret_counts = {}

    # Pass 1: Mark Greens and count remaining unmatched letters in secret
    for i in range(5):
        if guess[i] == secret[i]:
            res[i] = 'G'
        else:
            secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1

    # Pass 2: Mark Yellows for remaining matches
    for i in range(5):
        if res[i] == 'G':
            continue
        
        letter = guess[i]
        if secret_counts.get(letter, 0) > 0:
            res[i] = 'Y'
            secret_counts[letter] -= 1

    return "".join(res)

def play_wordle():
    sowpods_words = load_sowpods_words()
    secret_word = random.choice(list(sowpods_words))
    
    max_attempts = 6
    print("\n--- Welcome to Wordle (SOWPODS Rules) ---")
    print("Guess the 5-letter word! Feedback symbols:")
    print("  G : Correct letter & position")
    print("  Y : Letter present, wrong position")
    print("  B : Letter not in word (or duplicate count exceeded)\n")

    for attempt in range(1, max_attempts + 1):
        while True:
            guess = input(f"Guess {attempt}/{max_attempts}: ").strip().upper()
            
            if len(guess) != 5 or not guess.isalpha():
                print("Invalid input. Please enter a 5-letter word.")
            elif guess not in sowpods_words:
                print("Not a valid word in SOWPODS!")
            else:
                break

        feedback = evaluate_guess(guess, secret_word)
        print(f"       {guess}")
        print(f"       {feedback}\n")

        if feedback == "GGGGG":
            print(f"Congratulations! You guessed the word in {attempt} tries!")
            return

    print(f"Game Over! The secret word was: {secret_word}")

if __name__ == "__main__":
    play_wordle()