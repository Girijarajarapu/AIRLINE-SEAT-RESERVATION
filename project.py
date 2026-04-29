import sys

# ======================= AVL Tree Implementation =======================
class AVLNode:
    def _init_(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def _init_(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        self._update_height(z)
        self._update_height(y)
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        self._update_height(z)
        self._update_height(y)
        return y

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
            
        self._update_height(node)
        balance = self._balance_factor(node)
        
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
            
        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, key):
        if not node:
            return node
            
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
                
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
            
        if not node:
            return node
            
        self._update_height(node)
        balance = self._balance_factor(node)
        
        # Balancing
        if balance > 1:
            if self._balance_factor(node.left) >= 0:
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        if balance < -1:
            if self._balance_factor(node.right) <= 0:
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)
                
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.key)
            self._in_order(node.right, result)

    def in_order_traversal(self):
        result = []
        self._in_order(self.root, result)
        return result

# ======================= Seat Management System =======================
class SeatManager:
    def _init_(self, capacity):
        self.available_seats = AVLTree()
        self.booked_seats = AVLTree()
        for seat in range(1, capacity + 1):
            self.available_seats.insert(seat)

    def book_seat(self, seat_number):
        if not self.available_seats.search(seat_number):
            raise ValueError("Seat not available")
        self.available_seats.delete(seat_number)
        self.booked_seats.insert(seat_number)

    def cancel_booking(self, seat_number):
        if not self.booked_seats.search(seat_number):
            raise ValueError("Seat not booked")
        self.booked_seats.delete(seat_number)
        self.available_seats.insert(seat_number)

    def view_available_seats(self):
        return self.available_seats.in_order_traversal()

    def view_bookings(self):
        return self.booked_seats.in_order_traversal()

# ======================= User Interface =======================
def display_menu():
    print("\nAirline Seat Reservation System")
    print("1. View available seats")
    print("2. Book a seat")
    print("3. Cancel booking")
    print("4. View all bookings")
    print("5. Exit")

def main():
    capacity = 50
    manager = SeatManager(capacity)
    
    while True:
        display_menu()
        try:
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                print("Available seats:", manager.view_available_seats())
                
            elif choice == "2":
                seat = int(input("Enter seat number to book: "))
                manager.book_seat(seat)
                print(f"Seat {seat} booked successfully!")
                
            elif choice == "3":
                seat = int(input("Enter seat number to cancel: "))
                manager.cancel_booking(seat)
                print(f"Booking for seat {seat} canceled!")
                
            elif choice == "4":
                print("Booked seats:", manager.view_bookings())
                
            elif choice == "5":
                print("Thank you for using our system!")
                sys.exit()
                
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except KeyboardInterrupt:
            print("\nOperation canceled by user.")
            sys.exit()

if "_name_" == "_main_":
    min()

    
    