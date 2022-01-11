import random


print("--------------------------")
print("    M&M guessing game     ")
print("--------------------------")

mm_count = random.randint(1, 10)
attempt_limit = 5
attempts = 0


while attempts < attempt_limit:
    guess_text = input("How many M&Ms are in the jar? ")
    guess = int(guess_text)
    attempts += 1
    print(guess)
    print("")

    if mm_count == guess:
        print("")
        print(f"You are a winner! It Was {guess}.")
        break
    elif guess < mm_count:
            print("Sorry, that's too LOW!")
            print("")
    else:
            print("That's too HIGH!")
            print("")
            
print("")
print(f"Bye, you're done in {attempts}!")





