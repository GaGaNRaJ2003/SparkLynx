import mysql.connector as mysql
import db_config

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="sparklynx"
    )

def register_user():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    name = input("Enter full name: ")
    contact = input("Enter contact details: ")
    user_type = input("Enter user type (Customer/Admin): ")
    
    try:
        cursor.execute("INSERT INTO USERS (Username, Password, Name, ContactDetails, UserType) VALUES (%s, %s, %s, %s, %s)", (username, password, name, contact, user_type))
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def login_user():
    conn = db_config.get_connection()
    cursor = conn.cursor(buffered=True)
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    try:
        cursor.execute("SELECT UserID, Password, UserType, IsBlocked FROM USERS WHERE Username = %s", (username,))
        record = cursor.fetchone()
        
        if record and not record[3]:  # Check if user is not blocked
            if password == record[1]:
                print("Login successful!")
                return record[0], record[2]  # Return UserID and UserType
            else:
                cursor.execute("UPDATE USERS SET LoginAttempts = LoginAttempts + 1 WHERE UserID = %s", (record[0],))
                conn.commit()
                print("Incorrect password. Please try again.")
        else:
            print("Account is blocked or user does not exist.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()
        

def view_order_history(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT OrderID, PickupLocation, DropOffLocation, DeliveryTime FROM ORDERS WHERE UserID = %s", (user_id,))
        orders = cursor.fetchall()
        if orders:
            print("Order History:")
            for order in orders:
                print(f"Order ID: {order[0]}, Pickup Location: {order[1]}, Dropoff Location: {order[2]}, Delivery Time: {order[3]}")
        else:
            print("No orders found in the history.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def view_promotions():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT Description, DiscountAmount, StartDate, EndDate FROM PROMOTIONS")
        promotions = cursor.fetchall()
        if promotions:
            print("Current Promotions:")
            for promo in promotions:
                print(f"Description: {promo[0]}, Discount: {promo[1]}, Valid from {promo[2]} to {promo[3]}")
        else:
            print("No promotions available.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def contact_support(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    issue_description = input("Describe your issue: ")
    try:
        cursor.execute("INSERT INTO CUSTOMER_SUPPORT (UserID, IssueDescription, Status) VALUES (%s, %s, 'Open')", (user_id, issue_description))
        conn.commit()
        print("Support ticket created successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def manage_users():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT UserID, Username, UserType, IsBlocked FROM USERS")
        users = cursor.fetchall()
        if users:
            print("All Users:")
            for user in users:
                print(f"UserID: {user[0]}, Username: {user[1]}, User Type: {user[2]}, Blocked: {'Yes' if user[3] else 'No'}")
        else:
            print("No users found.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def block_unblock_user():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    user_id = input("Enter the user ID to block/unblock: ")
    try:
        cursor.execute("SELECT IsBlocked FROM USERS WHERE UserID = %s", (user_id,))
        record = cursor.fetchone()
        if record:
            is_blocked = not record[0]
            cursor.execute("UPDATE USERS SET IsBlocked = %s WHERE UserID = %s", (is_blocked, user_id))
            conn.commit()
            print("User status updated successfully!")
        else:
            print("User not found.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def delete_user():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    user_id = input("Enter the user ID to delete: ")
    try:
        cursor.execute("DELETE FROM USERS WHERE UserID = %s", (user_id,))
        conn.commit()
        print("User deleted successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def manage_orders():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT OrderID, UserID, PickupLocation, DropOffLocation, DeliveryTime FROM ORDERS")
        orders = cursor.fetchall()
        if orders:
            print("All Orders:")
            for order in orders:
                print(f"Order ID: {order[0]}, User ID: {order[1]}, Pickup Location: {order[2]}, Dropoff Location: {order[3]}, Delivery Time: {order[4]}")
        else:
            print("No orders found.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def cancel_order_by_admin():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    order_id = input("Enter the order ID to cancel: ")
    try:
        cursor.execute("DELETE FROM ORDERS WHERE OrderID = %s", (order_id,))
        conn.commit()
        print("Order canceled successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def view_support_tickets():
    conn = db_config.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT TicketID, UserID, IssueDescription, Status FROM CUSTOMER_SUPPORT")
        tickets = cursor.fetchall()
        if tickets:
            print("Support Tickets:")
            for ticket in tickets:
                print(f"Ticket ID: {ticket[0]}, User ID: {ticket[1]}, Issue: {ticket[2]}, Status: {ticket[3]}")
        else:
            print("No support tickets found.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()


def update_user_info(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()

    new_contact = input("Enter new contact details: ")
    try:
        cursor.execute("UPDATE USERS SET ContactDetails = %s WHERE UserID = %s", (new_contact, user_id))
        conn.commit()
        print("Contact information updated successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def place_order(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    pickup_location = input("Enter pickup location: ")
    dropoff_location = input("Enter dropoff location: ")
    delivery_time = input("Enter delivery time (YYYY-MM-DD HH:MM:SS): ")
    instructions = input("Any additional instructions? ")
    
    try:
        cursor.execute("INSERT INTO ORDERS (UserID, PickupLocation, DropOffLocation, DeliveryTime, AdditionalInstructions) VALUES (%s, %s, %s, %s, %s)", (user_id, pickup_location, dropoff_location, delivery_time, instructions))
        conn.commit()
        print("Order placed successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def cancel_order():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    order_id = input("Enter the order ID to cancel: ")
    
    try:
        cursor.execute("DELETE FROM ORDERS WHERE OrderID = %s", (order_id,))
        conn.commit()
        print("Order canceled successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def track_order():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    order_id = input("Enter order ID to track: ")
    
    try:
        cursor.execute("SELECT Status, Location FROM TRACKING WHERE OrderID = %s", (order_id,))
        status = cursor.fetchone()
        
        if status:
            print(f"Order Status: {status[0]}, Current Location: {status[1]}")
        else:
            print("No such order found.")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def manage_support_ticket(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    issue_description = input("Describe your issue: ")
    try:
        cursor.execute("INSERT INTO CUSTOMER_SUPPORT (UserID, IssueDescription, Status) VALUES (%s, %s, 'Open')", (user_id, issue_description))
        conn.commit()
        print("Support ticket created successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()
        
def process_payment(order_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    amount = float(input("Enter payment amount: "))
    payment_method = input("Enter payment method (Credit Card, Debit Card, Cash): ")
    
    try:
        cursor.execute("INSERT INTO PAYMENTS (OrderID, Amount, PaymentMethod) VALUES (%s, %s, %s)", (order_id, amount, payment_method))
        conn.commit()
        print("Payment processed successfully!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def rate_order(user_id):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    order_id = input("Enter order ID to rate: ")
    rating = int(input("Rate the order from 1 to 5: "))
    feedback = input("Provide feedback (optional): ")
    
    try:
        cursor.execute("INSERT INTO RATINGS (UserID, OrderID, Rating, Feedback) VALUES (%s, %s, %s, %s)", (user_id, order_id, rating, feedback))
        conn.commit()
        print("Thank you for your feedback!")
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def manage_promotions():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    action = input("Do you want to add a new promotion or view existing ones? (Add/View): ")
    
    if action.lower() == 'add':
        description = input("Enter promotion description: ")
        discount_amount = float(input("Enter discount amount: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        try:
            cursor.execute("INSERT INTO PROMOTIONS (Description, DiscountAmount, StartDate, EndDate) VALUES (%s, %s, %s, %s)", (description, discount_amount, start_date, end_date))
            conn.commit()
            print("Promotion added successfully!")
        except mysql.connector.Error as err:
            print("Error: ", err)
    elif action.lower() == 'view':
        try:
            cursor.execute("SELECT PromotionID, Description, DiscountAmount, StartDate, EndDate FROM PROMOTIONS")
            promotions = cursor.fetchall()
            if promotions:
                print("Current Promotions:")
                for promo in promotions:
                    print(f"ID: {promo[0]}, Description: {promo[1]}, Discount: {promo[2]}, Valid from {promo[3]} to {promo[4]}")
            else:
                print("No promotions available.")
        except mysql.connector.Error as err:
            print("Error: ", err)
            
        finally:    
            cursor.close()
            conn.close()  
    else:
        print("Invalid action.")
              

def admin_reports():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT Username, ContactDetails FROM USERS")
        users = cursor.fetchall()
        print("All users:")
        for user in users:
            print(user)

        cursor.execute("SELECT OrderID, PickupLocation, DeliveryTime FROM ORDERS")
        orders = cursor.fetchall()
        print("\nAll orders:")
        for order in orders:
            print(order)
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def user_dashboard(user_id, user_type):
    while True:
        print("\nUser Dashboard:")
        print("1. Place an order")
        print("2. Cancel an order")
        print("3. Track an order")
        print("4. View order history")
        print("5. View promotions")
        print("6. Contact customer support")
        print("7. Update my contact details")
        print("8. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            place_order(user_id)
        elif choice == '2':
            cancel_order()
        elif choice == '3':
            track_order()
        elif choice == '4':
            view_order_history(user_id)
        elif choice == '5':
            view_promotions()
        elif choice == '6':
            contact_support(user_id)
        elif choice == '7':
            update_user_info(user_id)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please select again.")


def admin_login():
    conn = db_config.get_connection()
    cursor = conn.cursor(buffered=True)

    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    try:
        cursor.execute("SELECT AdminID FROM ADMIN WHERE Username = %s AND Password = %s", (username, password))
        record = cursor.fetchone()
        
        if record:
            print("Admin login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def admin_dashboard():
    while True:
        print("\nAdmin Dashboard:")
        print("1. Manage users")
        print("2. Manage orders")
        print("3. View and manage promotions")
        print("4. View and manage support tickets")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_users()
            action = input("Do you want to block/unblock or delete a user? (Block/Unblock/Delete/None): ")
            if action.lower() == 'block' or action.lower() == 'unblock':
                block_unblock_user()
            elif action.lower() == 'delete':
                delete_user()
        elif choice == '2':
            manage_orders()
            cancel = input("Do you want to cancel any order? (Yes/No): ")
            if cancel.lower() == 'yes':
                cancel_order_by_admin()
        elif choice == '3':
            manage_promotions()
        elif choice == '4':
            view_support_tickets()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select again.")


def admin_reports():
    conn = db_config.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT Username, ContactDetails FROM USERS")
        users = cursor.fetchall()
        print("All users:")
        for user in users:
            print(user)

        cursor.execute("SELECT OrderID, PickupLocation, Delivery Time FROM ORDERS")
        orders = cursor.fetchall()
        print("\nAll orders:")
        for order in orders:
            print(order)
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        conn.close()

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            user_id, user_type = login_user()
            if user_id:
                user_dashboard(user_id, user_type)
        elif choice == '3':
            if admin_login():
                admin_dashboard()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main_menu()
