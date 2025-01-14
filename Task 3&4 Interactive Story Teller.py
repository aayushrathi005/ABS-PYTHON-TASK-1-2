def start_story():
    print("Welcome to the Interactive Story Generator!")
    print("You are about to embark on a thrilling adventure.")
    print("Make your choices wisely, as they will affect the outcome of the story.")
    print("Let's begin!\n")

    first_choice()

def first_choice():
    print("You find yourself in a dark forest. There are two paths ahead.")
    print("1. Take the left path.")
    print("2. Take the right path.")
    
    choice = input("Which path do you choose? (1/2): ")
    
    if choice == "1":
        left_path()
    elif choice == "2":
        right_path()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        first_choice()

def left_path():
    print("\nYou take the left path and encounter a friendly deer.")
    print("The deer offers you two gifts.")
    print("1. A magical sword.")
    print("2. A healing potion.")
    
    choice = input("Which gift do you choose? (1/2): ")
    
    if choice == "1":
        print("\nYou take the magical sword and continue your journey.")
        print("With the sword in hand, you feel invincible.")
        print("You eventually find your way out of the forest and live happily ever after.")
    elif choice == "2":
        print("\nYou take the healing potion and continue your journey.")
        print("The potion heals your wounds and restores your energy.")
        print("You eventually find your way out of the forest and live happily ever after.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        left_path()

def right_path():
    print("\nYou take the right path and encounter a fierce dragon.")
    print("The dragon gives you two options.")
    print("1. Fight the dragon.")
    print("2. Befriend the dragon.")
    
    choice = input("What do you choose? (1/2): ")
    
    if choice == "1":
        print("\nYou decide to fight the dragon. It's a tough battle, but you manage to defeat it.")
        print("You find a treasure chest filled with gold and gems.")
        print("You eventually find your way out of the forest and live a wealthy life.")
    elif choice == "2":
        print("\nYou decide to befriend the dragon. The dragon is surprised but accepts your friendship.")
        print("The dragon helps you find your way out of the forest and you both become lifelong friends.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        right_path()

# Start the interactive story
start_story()