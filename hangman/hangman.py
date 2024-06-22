import random

def get_hangman_stage(tries, max_tries):
    stages = [
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        ---------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        ---------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        ---------
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        ---------
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        ---------
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        ---------
        """,
        """
           -----
           |   |
               |
               |
               |
               |
        ---------
        """
    ]

    # Adjust stages to the max_tries
    extended_stages = ["\n".join(stage.split("\n")[1:]) for stage in stages]  # Remove top borders
    while len(extended_stages) < max_tries + 1:
        extended_stages.insert(0, "\n" * 6 + "--------")  # Add empty stages at the beginning
    
    return extended_stages[max_tries - tries]

def get_hint(word):
    hints = {
        'python': 'A popular programming language.',
        'hangman': 'The name of this game.',
        'game': 'An activity for entertainment.',
        'development': 'The process of creating something.'
        # Add more words and hints here
    }
    return hints.get(word, 'No hint available.')

def hangman():
    words = ['python', 'hangman', 'game', 'development']  # Add more words here
    word = random.choice(words).lower()
    guessed_letters = []
    score = 0

    print("Welcome to Hangman! Let's make it cool and fun!")
    print("Choose a difficulty level:")
    print("1. Easy (8 tries)")
    print("2. Medium (6 tries)")
    print("3. Hard (4 tries)")

    difficulty = input("Enter your choice (1/2/3): ")
    if difficulty == '1':
        tries = 8
    elif difficulty == '2':
        tries = 6
    elif difficulty == '3':
        tries = 4
    else:
        print("Invalid choice, defaulting to Medium difficulty.")
        tries = 6

    max_tries = tries  # Store the initial number of tries
    print("\nHint: " + get_hint(word))

    while tries > 0:
        print("\n" + get_hangman_stage(tries, max_tries))
        for letter in word:
            if letter in guessed_letters:
                print(letter, end=" ")
            else:
                print("_", end=" ")

        guess = input("\n\nGuess a letter: ").lower()

        if len(guess) != 1:
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You've already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess not in word:
            tries -= 1
            print("Wrong guess. You have", tries, "tries left.")
        else:
            score += 10
            print("Good guess! Your score is:", score)

        if set(word) <= set(guessed_letters):
            print("\nCongratulations! You guessed the word:", word)
            print("Your final score is:", score)
            break

    if tries == 0:
        print("\nGame over. The word was:", word)
        print("Your final score is:", score)

    encouragements = [
        "Keep it up!",
        "You can do this!",
        "Almost there!",
        "Don't give up!",
        "Nice try!"
    ]
    print(random.choice(encouragements))

hangman()
