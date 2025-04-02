from peterr import register, login, show_leaderboard

def menu():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. View Leaderboard")
        print("4. Exit")

        # If the user chooses 1, it will have them register
        choice = input("Choose: ")

        if choice == "1":
            register()

        # If user chooses 2, it will have them login
        elif choice == "2":
            user = login()
            if user:
                print(f"Welcome, {user}! You are now logged in.")
                break  # Exit the loop after successful login
        
        # If the user chooses 3, it will display the leaderboard
        elif choice == "3":
            show_leaderboard()

        # If the user chooses 4, it will exit them out the program
        elif choice == "4":
            print("Goodbye!")
            exit()

        # If user enters anything other than 1–4
        else:
            print("Invalid choice.")
