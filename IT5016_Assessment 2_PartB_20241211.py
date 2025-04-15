import datetime

global_requisition_counter = 1000  # Initialize global requisition ID counter

class RequisitionSystem:
    def __init__(self, date="", staff_id="", staff_name="", status="Pending"):
        global global_requisition_counter
        self.date = date or datetime.date.today().strftime("%Y-%m-%d")
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = global_requisition_counter
        global_requisition_counter += 1
        self.total = 0
        self.status = status
        self.approval_reference = ""
        self.items = [] # list to store items and prices

    def staff_info(self):
        # Collects staff information.
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.staff_id = input("Enter Staff ID: ")
        self.staff_name = input("Enter Staff Name: ")

    def requisitions_details(self):
        # Collects requisition items and calculates the total.
        self.items = []
        self.total = 0  # Reset total in case method is called again
        while True:
            item_name = input("Enter item name (or type 'done' to finish): ")
            if item_name.lower() == "done":
                break

            if item_name.isdigit():
                print("Item name cannot be a number. Please enter valid text.")
                continue

            while True:
                try:
                    item_price = input(f"Enter price for {item_name}: ")
                    # Check for alphabetic characters in item_price
                    if any(char.isalpha() for char in item_price):
                        raise ValueError("Price cannot contain letters. Please enter a number.")
                    item_price = float(item_price)  # Convert to float after validation

                    if item_price < 0:
                        raise ValueError("Price cannot be negative.")

                    self.items.append((item_name, item_price))
                    self.total += item_price
                    break
                except ValueError as e:
                    print(f"Invalid input for price: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

        return self.total

    def requisition_approval(self):
        # Approves or rejects a requisition based on the total amount.
        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]
        else:
            self.status = "Pending"

    def display_requisition(self):
        # Displays requisition information.
        print(f"\nDate: {self.date}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Total: ${self.total:.2f}")
        print(f"Status: {self.status}")
        if self.approval_reference:
            print(f"Approval Reference Number: {self.approval_reference}")
        print("Items:")
        for item, price in self.items:
            print(f"- {item}: ${price:.2f}")
        print("-" * 20)

def respond_requisition(requisitions, requisition_id, decision):
    # Allows a manager to respond to a pending requisition."""
    for requisition in requisitions:
        if requisition.requisition_id == requisition_id:
            if decision.lower() == "approved":
                requisition.status = "Approved"
                requisition.approval_reference = requisition.staff_id + str(requisition.requisition_id)[-3:]
            elif decision.lower() == "not approved":
                requisition.status = "Not Approved"
            else:
                print("Invalid decision. Please enter 'Approved' or 'Not Approved'.")
            return
    print(f"Requisition with ID {requisition_id} not found.")

def requisition_statistics(requisitions):
    # Calculates and displays requisition statistics."""
    approved_count = sum(1 for req in requisitions if req.status == "Approved")
    pending_count = sum(1 for req in requisitions if req.status == "Pending")
    not_approved_count = sum(1 for req in requisitions if req.status == "Not Approved")
    total_count = len(requisitions)

    print("\nRequisition Statistics:")
    print(f"Total Requisitions Submitted: {total_count}")
    print(f"Total Approved Requisitions: {approved_count}")
    print(f"Total Pending Requisitions: {pending_count}")
    print(f"Total Not Approved Requisitions: {not_approved_count}")

if __name__ == "__main__":
    requisitions = []

    for i in range(5):
        req = RequisitionSystem()
        req.staff_info()
        req.requisitions_details()
        req.requisition_approval()
        requisitions.append(req)

    print("\nInitial Requisition Information:")
    for req in requisitions:
        req.display_requisition()

    requisition_statistics(requisitions)

    # Simulate manager responses
    respond_requisition(requisitions, requisitions[1].requisition_id, "Approved")
    respond_requisition(requisitions, requisitions[3].requisition_id, "Not Approved")
    respond_requisition(requisitions, 9999, "Approved")  # Non-existent ID test

    print("\nUpdated Requisition Information:")
    for req in requisitions:
        req.display_requisition()

    requisition_statistics(requisitions)