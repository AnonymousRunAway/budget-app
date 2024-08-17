class Category:

    def __init__(self, name) -> None:
        self.ledger = []
        self.categoryName = name
        self.__balance = 0

    def __repr__(self):
        header = self.categoryName.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total

    def deposit(self, amount, desc='') -> None:
        self.ledger.append({'amount' : amount, 'description' : desc})
        self.__balance += amount
    
    def withdraw(self, amount, desc='') -> None:
        if self.check_funds(amount):
            self.deposit(-amount, desc)
            return True
        return False
    
    def get_balance(self):
        return self.__balance
    
    def check_funds(self, query):
        return self.get_balance() >= query
    
    def transfer(self, amount, destination):
        if self.check_funds(amount):
            self.deposit(-amount, f'Transfer to {destination.categoryName}')
            destination.deposit(amount, f'Transfer from {self.categoryName}')
            return True
        return False
    
def create_spend_chart(categories):
    # Calculate the total and withdrawals for each category
    withdraws = []
    names = []
    
    for category in categories:
        s = 0
        for item in category.ledger:
            if item['amount'] < 0:
                s += item['amount']
        withdraws.append(-s)  # Withdrawals should be positive
        names.append(category.categoryName)
    
    total = sum(withdraws)
    withdraws = [x * 100 // total for x in withdraws]  # Calculate percentage
    n = len(withdraws)

    # Create the chart
    res = ""

    for percent in range(100, -10, -10):
        line = f'{percent:>3}' + '| '
        for level in withdraws:
            line += 'o  ' if level >= percent else '   '
        res += line + '\n'
    
    res += '    ' + '-' * (n * 3 + 1) + '\n'
    
    # Prepare the category names
    max_length = max(len(name) for name in names)
    names = [name.ljust(max_length) for name in names]  # Pad names to the same length
    
    for i in range(max_length):
        line = '     '
        for name in names:
            line += name[i] + '  '
        res += line + '\n'
    
    print(res)

if __name__ == "__main__":
    categories = []
    while True:
        print("\nWhat would you like to do?")
        print("1. Create a new category")
        print("2. Add income to a category")
        print("3. Add expense to a category")
        print("4. Transfer funds between categories")
        print("5. Print a category ledger")
        print("6. Show spending chart")
        print("7. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter category name: ")
            categories.append(Category(name))
            print(f"Category '{name}' created!")
        elif choice == '2':
            if not categories:
                print("No categories created yet!")
                continue
            category_name = input("Enter the category name: ")
            category = [c for c in categories if c.categoryName == category_name]
            if not category:
                print("Category not found!")
                continue
            amount = float(input("Enter the amount: "))
            desc = input("Enter a description (optional): ")
            category[0].deposit(amount, desc)
            print(f"Deposited ${amount:.2f} to '{category_name}'.")
        elif choice == '3':
            if not categories:
                print("No categories created yet!")
                continue
            category_name = input("Enter the category name: ")
            category = [c for c in categories if c.categoryName == category_name]
            if not category:
                print("Category not found!")
                continue
            amount = float(input("Enter the amount: "))
            desc = input("Enter a description (optional): ")
            if category[0].withdraw(amount, desc):
                print(f"Withdrew ${amount:.2f} from '{category_name}'.")
            else:
                print(f"Insufficient funds in '{category_name}'.")
        elif choice == '4':
            if not categories:
                print("No categories created yet!")
                continue
            source_name = input("Enter the source category: ")
            source = [c for c in categories if c.categoryName == source_name]
            if not source:
                print("Source category not found!")
                continue
            dest_name = input("Enter the destination category: ")
            dest = [c for c in categories if c.categoryName == dest_name]
            if not dest:
                print("Destination category not found!")
                continue
            amount = float(input("Enter the amount: "))
            if source[0].transfer(amount, dest[0]):
                print(f"Transferred ${amount:.2f} from '{source_name}' to '{dest_name}'.")
            else:
                print(f"Insufficient funds in '{source_name}'.")
        elif choice == '5':
            if not categories:
                print("No categories created yet!")
                continue
            category_name = input("Enter the category name: ")
            category = [c for c in categories if c.categoryName == category_name]
            if not category:
                print("Category not found!")
                continue
            print(category[0])
        elif choice == '6':
            if not categories:
                print("No categories created yet!")
                continue
            create_spend_chart(categories)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")
