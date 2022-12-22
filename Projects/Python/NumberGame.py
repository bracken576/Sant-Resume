import random
# import os


def random_digits():
    numerators = ''.join(random.sample("123456789", 4))
    return str(numerators)


print("I have created a 4 digit pass code: there are no repeats or zeroes.")
print("I will give you hints along the way to help.")
print("However, if you do not guess it in 10 moves I will shutdown your computer. Good luck HAHAHAHAHAHA!!!")
print()

number = ""
counter = 1
yes = "y"
correct = ""
guesses = ["", "", "", "", "", "", "", "", "", ""]
rp = ["", "", "", "", "", "", "", "", "", ""]
rn = ["", "", "", "", "", "", "", "", "", ""]
guessess = ""
rpg = ""
rng = ""
while yes == "y":
    yes = ""
    number = random_digits()
    #    print(number)
    #    print()
    while counter <= 10:
        print("This is move " + str(counter))
        if counter > 1:
            for nu in range(counter - 2, counter - 1):
                guessess = guessess + " " + str(guesses[nu])
                rpg = rpg + " " + str(rp[nu])
                rng = rng + " " + str(rn[nu])
            print("Previous guesses: " + guessess + "\n" + "                  " + rpg + "\n""                  " + rng)

        lettersInString = True
        length = True
        repeat = True
        notTrue = True
        guess = ""
        while notTrue:
            notTrue = False

            letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0"
            numbered = 1

            guess = str(input("Guess: "))

            if (len(guess) == 0 or 1) and guess == "n":
                yes = "n"
                break

            if len(guess) != 4:
                notTrue = True
                print("You do not have the correct character amount")

            for let in guess:
                if let in letters:
                    notTrue = True
                    print("There are no letters or zeroes in the code")
                    break

            for lett in guess:
                for num in range(numbered, len(guess) - 1):
                    if lett == guess[num: num + 1]:
                        notTrue = True
                        print("There are no repeats in the code")
                        break

                numbered = numbered + 1
            for gues in guesses:
                if guess == gues:
                    notTrue = True
                    print("You already guessed that")

        if yes == "n":
            break
        guesses[counter - 1] = str(guess)
        print()
        if guess == number:
            if counter == 1:
                print("Wow, first try, that was really lucky.")
            if 1 < counter < 5:
                print("Wow, you actually guessed it. I guess I won't shutdown your computer good job!!!")
            if 5 <= counter < 8:
                print("Cutting it a little close but good job.")
            if 8 <= counter <= 10:
                print("Wow, nice guess but almost too late, good job")
            print()
            correct = "y"
        if correct == "y":
            break
        add = 1
        ad = 1
        rightp = 0
        rightn = 0
        for c in number:
            for g in guess:
                if c == g:
                    if c == g and add == ad:
                        rightp = rightp + 1
                        rightn = rightn + 1
                    else:
                        rightn = rightn + 1
                ad = ad + 1
            ad = 1
            add = add + 1
        print("The number of right places is " + str(rightp))
        print("The number of right numbers is " + str(rightn))
        rp[counter - 1] = "   " + str(rightp)
        rn[counter - 1] = "   " + str(rightn)

        counter = counter + 1
        if rightn == 0:
            print("Man that wasn't even close")
        if 0 < rightn <= 2:
            print("You are doing well, nice guess. JK loser. HAHAHAHAHAHAHA")
        if 2 < rightn <= 4:
            print("You are almost there, don't let me shut down your computer. HAHAHAHAHAHAHAHAHA")
        rightp = 0
        rightn = 0
        print()
    guesses=["", "", "", "", "", "", "", "", "", ""]
    print(str(number) + " is the code")
    print()
    # if counter >= 11:
    #    os.system("shutdown /s /t 1")
    counter = 1
    correct = ""
    guessess = ""
    rpg = ""
    rng = ""
    yes = str(input("Do you want to do it again? y or n: "))