import sqlite3

conn = sqlite3.connect('lab7.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

class MessengerApp:
    def __init__(self, db_path='lab7.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_message(self, sender, receiver, message):
        self.cursor.execute('''
            INSERT INTO messages (sender, receiver, message)
            VALUES (?, ?, ?)
        ''', (sender, receiver, message))
        self.conn.commit()

    def read_messages(self, sender=None, receiver=None):
        query = 'SELECT * FROM messages'
        params = ()
        if sender:
            query += ' WHERE sender = ?'
            params += (sender,)
        if receiver:
            if not sender:
                query += ' WHERE'
            else:
                query += ' AND'
            query += ' receiver = ?'
            params += (receiver,)

        self.cursor.execute(query, params)
        messages = self.cursor.fetchall()
        for msg in messages:
            print(msg)

    def update_message(self, message_id, new_message):
        self.cursor.execute('''
            UPDATE messages
            SET message = ?
            WHERE id = ?
        ''', (new_message, message_id))
        self.conn.commit()

    def delete_message(self, message_id):
        self.cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

messenger_app = MessengerApp()

while True:
    print("\n1. Create Message\n2. Read Messages\n3. Update Message\n4. Delete Message\n5. Exit")
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        sender = input("Enter sender: ")
        receiver = input("Enter receiver: ")
        message = input("Enter message: ")
        messenger_app.create_message(sender, receiver, message)

    elif choice == '2':
        sender = input("Enter sender (leave blank to get all messages): ")
        receiver = input("Enter receiver (leave blank to get all messages): ")
        messenger_app.read_messages(sender, receiver)

    elif choice == '3':
        message_id = int(input("Enter message ID to update: "))
        new_message = input("Enter new message: ")
        messenger_app.update_message(message_id, new_message)

    elif choice == '4':
        message_id = int(input("Enter message ID to delete: "))
        messenger_app.delete_message(message_id)

    elif choice == '5':
        messenger_app.close_connection()
        print("Exiting the Messenger App. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
