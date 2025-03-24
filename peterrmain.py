from peterr import register, login

print("1. Register\n2. Login")

choice = input("Choose: ")

# If the user chooses 1, it will have them register
if choice == "1":
    register()
# If user chooses 2, it will have them login
elif choice == "2":
    success = login()
    if not success:
        exit()
# If the user enters anything other than 1 or 2
else: 
    print("Invalid choice.")
    exit()