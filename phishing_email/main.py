from campaign import campaign_interface
from emails import email_interface



def main():
    while True:
        print("== PHISHING TRAINING MAIN MENU INTERFACE ==")
        print('\n' * 2)
        print("1. Campaign Menu ")
        print("2. Exit")

        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number as your selection")
        
        if choice == 1:
            campaign_interface()
        elif choice == 2:
            break
        else:
            print("Invalid choice")
    

if __name__=="__main__":
    main()