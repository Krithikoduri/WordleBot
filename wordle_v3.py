import random
import urllib.request

# ANSI Color Codes
GREEN_BG = "\033[42m\033[30m\033[1m"   # Bright Green BG, Black Bold Text
YELLOW_BG = "\033[43m\033[30m\033[1m"  # Bright Yellow BG, Black Bold Text
GRAY_BG = "\033[100m\033[97m"          # Dark Gray BG, White Text
RESET = "\033[0m"                       # Reset styling

def load_sowpods_words():
    """Download and load valid 5-letter words from the standard SOWPODS dictionary."""
    url = "https://raw.githubusercontent.com/jesstess/Scrabble/master/scrabble/sowpods.txt"
    print("Loading dictionary...")
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            words = set(word.strip().upper() for word in text.splitlines() if len(word.strip()) == 5)
            return words
    except Exception as e:
        print(f"Error loading SOWPODS online: {e}")
        return {"CRANE", "SLATE", "PLANT", "SHARK", "TRAIN", "GHOST", "WORLD", "APPLE"}

def evaluate_guess(guess, secret):
    """
    Evaluates guess against secret using Wordle logic:
    - 'G': Correct letter, correct spot
    - 'Y': Letter in word, wrong spot (limited by remaining letter counts)
    - 'B': Letter not in word / duplicate count exceeded
    """
    res = ['B'] * 5
    secret_counts = {}

    # Pass 1: Mark Greens
    for i in range(5):
        if guess[i] == secret[i]:
            res[i] = 'G'
        else:
            secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1

    # Pass 2: Mark Yellows
    for i in range(5):
        if res[i] == 'G':
            continue
        
        letter = guess[i]
        if secret_counts.get(letter, 0) > 0:
            res[i] = 'Y'
            secret_counts[letter] -= 1

    return "".join(res)

def format_styled_output(guess, feedback):
    """
    Combines ANSI colors with symbol notation for visual & screen-reader accessibility:
    - Correct (G)   : [ X ] rendered on Green background
    - Present (Y)   : ( X ) rendered on Yellow background
    - Absent (B)    :   X   rendered on Dark Gray background
    """
    styled_tokens = []
    
    for char, status in zip(guess, feedback):
        if status == 'G':
            # Bracketed notation with Green BG
            styled_tokens.append(f"{GREEN_BG}[ {char} ]{RESET}")
        elif status == 'Y':
            # Parenthesis notation with Yellow BG
            styled_tokens.append(f"{YELLOW_BG}( {char} ){RESET}")
        else:
            # Plain spacing with Gray BG
            styled_tokens.append(f"{GRAY_BG}  {char}  {RESET}")
            
    return " ".join(styled_tokens)

def play_wordle():
    sowpods_words = load_sowpods_words()
    secret_word = random.choice(list(sowpods_words))
    max_attempts = 6

    print("\n--- Welcome to Wordle (ANSI + Accessible Notation) ---")
    print("Feedback Legend:")
    print(f"  {GREEN_BG}[ X ]{RESET} : Correct letter & position")
    print(f"  {YELLOW_BG}( X ){RESET} : Present in word, wrong position")
    print(f"  {GRAY_BG}  X  {RESET} : Not in word / count exceeded\n")

    for attempt in range(1, max_attempts + 1):
        while True:
            guess = input(f"Attempt {attempt}/{max_attempts} > ").strip().upper()
            
            if len(guess) != 5 or not guess.isalpha():
                print("Invalid input. Please enter a 5-letter word.")
            elif guess not in sowpods_words:
                print("Not a valid word in SOWPODS list!")
            else:
                break

        feedback = evaluate_guess(guess, secret_word)
        display_result = format_styled_output(guess, feedback)
        
        print(f"Result:    {display_result}\n")

        if feedback == "GGGGG":
            print(f"🎉 Winner! You guessed '{secret_word}' in {attempt} attempts!")
            return

    print(f"💥 Game Over! The secret word was: {secret_word}")

if __name__ == "__main__":
    play_wordle()
