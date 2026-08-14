import time
import random

name = input("What is your name? ")
print("Hello, " + name, "Time to play hangman!")
time.sleep(1)

genre = input("What genre of words would you like to play with? (e.g. animals, movies, food, sports, countries): ").strip().lower()

#Word bank for given genre
word_bank = {
    'animals': ['elephant', 'giraffe', 'penguin', 'dolphin', 'kangaroo', 'octopus', 'cheetah', 'gorilla'],
    'movies': ['inception', 'titanic', 'avatar', 'gladiator', 'jaws', 'frozen', 'joker', 'up'],
    'food': ['pizza', 'burger', 'sushi', 'pasta', 'tacos', 'noodles', 'sandwich', 'pancake'],
    'sports': ['football', 'cricket', 'tennis', 'hockey', 'boxing', 'rugby', 'golf', 'swimming'],
    'countries': ['canada', 'brazil', 'japan', 'germany', 'egypt', 'australia', 'france', 'india'],
    'programming': ['python', 'javascript', 'variable', 'function', 'algorithm', 'compiler', 'database', 'syntax'],
    'data_analysis':['mathematics', 'statistics', 'python', 'programming', 'sql', 'excel', 'powerbi', 'analysis']
}

# If the genre exists in our bank, use it; otherwise fall back to a default set
if genre in word_bank:
    available_words = word_bank[genre]
else:
    print(f"\n Game doesn't have '{genre}' yet, so here's a general knowledge set instead!")
    default_set = ['mathematics', 'statistics', 'python', 'programming', 'sql', 'excel', 'powerbi', 'analysis']

# Pick 6 random words from the chosen genre (or fewer if the list is smaller)
words = random.sample(available_words, min(6, len(available_words)))

print("\nStart guessing...\n")
time.sleep(0.5)

word = random.choice(words)
guesses = ''
turns = 5

while turns > 0:
    failed = 0
    for char in word:
        if char in guesses:
            print(char, end="")
        else:
            print("_", end="")
            failed += 1
    if failed == 0:
        print("\nYou won")
        break
    guess = input("\nguess a character:")
    guesses += guess
    if guess not in word:
        turns -= 1
        print("\nWrong")
        print("\nYou have", turns, 'more guesses')
        if turns == 0:
            print("\nYou Lose")
            print("The word was:", word)
