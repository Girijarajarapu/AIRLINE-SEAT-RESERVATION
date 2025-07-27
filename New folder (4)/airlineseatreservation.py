class Node:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.left = None
        self.right = None
        self.height = 1
        self.is_reserved = False
        self.passenger_name = None


class AVLTree:
    def insert(self, root, seat_number):
        if not root:
            return Node(seat_number)
        elif seat_number < root.seat_number:
            root.left = self.insert(root.left, seat_number)
        else:
            root.right = self.insert(root.right, seat_number)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancing
        if balance > 1 and seat_number < root.left.seat_number:
            return self.right_rotate(root)
        if balance < -1 and seat_number > root.right.seat_number:
            return self.left_rotate(root)
        if balance > 1 and seat_number > root.left.seat_number:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and seat_number < root.right.seat_number:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def find_seat(self, root, seat_number):
        if not root:
            return None
        if seat_number < root.seat_number:
            return self.find_seat(root.left, seat_number)
        elif seat_number > root.seat_number:
            return self.find_seat(root.right, seat_number)
        else:
            return root

    def reserve_seat(self, root, seat_number, passenger_name):
        node = self.find_seat(root, seat_number)
        if not node:
            print("Seat", seat_number, "not found.")
            return
        if node.is_reserved:
            print(f"Seat {seat_number} is already reserved by {node.passenger_name}.")
        else:
            node.is_reserved = True
            node.passenger_name = passenger_name
            print(f"Seat {seat_number} successfully reserved for {passenger_name}.")

    def cancel_reservation(self, root, seat_number):
        node = self.find_seat(root, seat_number)
        if not node:
            print("Seat", seat_number, "not found.")
            return
        if not node.is_reserved:
            print(f"Seat {seat_number} is not currently reserved.")
        else:
            print(f"Reservation for seat {seat_number} (Passenger: {node.passenger_name}) has been cancelled.")
            node.is_reserved = False
            node.passenger_name = None

    def update_passenger_name(self, root, seat_number, new_name):
        node = self.find_seat(root, seat_number)
        if not node:
            print("Seat", seat_number, "not found.")
            return
        if not node.is_reserved:
            print(f"Seat {seat_number} is not currently reserved.")
        else:
            print(f"Passenger name for seat {seat_number} updated from {node.passenger_name} to {new_name}.")
            node.passenger_name = new_name

    def display_seats(self, root):
        if not root:
            return
        self.display_seats(root.left)
        status = "Reserved" if root.is_reserved else "Available"
        name = f"({root.passenger_name})" if root.passenger_name else ""
        print(f"Seat {root.seat_number}: {status} {name}")
        self.display_seats(root.right)


# === MAIN PROGRAM ===
if __name__ == "__main__":
    avl = AVLTree()
    root = None

    # Create seats
    for seat in range(1, 21):   # 20 seats
        root = avl.insert(root, seat)

    while True:
        print("\n===== Airline Seat Reservation =====")
        print("1. Display seats")
        print("2. Reserve a seat")
        print("3. Cancel reservation")
        print("4. Update passenger name")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            avl.display_seats(root)
        elif choice == '2':
            seat_no = int(input("Enter seat number to reserve: "))
            name = input("Enter passenger name: ")
            avl.reserve_seat(root, seat_no, name)
        elif choice == '3':
            seat_no = int(input("Enter seat number to cancel: "))
            avl.cancel_reservation(root, seat_no)
        elif choice == '4':
            seat_no = int(input("Enter seat number to update passenger name: "))
            new_name = input("Enter new passenger name: ")
            avl.update_passenger_name(root, seat_no, new_name)
        elif choice == '5':
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Try again.")

