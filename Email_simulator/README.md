# Email Simulator

A beginner-friendly Python project that simulates sending, receiving, reading, and deleting emails between users.

The project demonstrates object-oriented programming concepts including:

- Classes and objects
- Constructors with `__init__`
- Instance attributes
- Methods
- Object relationships
- Lists used as collections
- String representations with `__str__`
- Basic state changes
- Input validation through index checks

The main implementation is in [`main.py`](main.py).

## Project Goal

The goal is to model a small email system using Python objects.

Instead of representing an email as a loose collection of variables, the program creates an `Email` object. Instead of storing users as simple names, it creates `User` objects. Each user owns an `Inbox`, and the inbox stores the emails received by that user.

The resulting relationship is:

```text
User
 |
 +-- Inbox
      |
      +-- Email objects
```

An email also keeps references to its sender and receiver:

```text
Sender User ----> Email <---- Receiver User
```

This structure makes the program easier to understand because each object is responsible for a specific part of the system.

## Files

```text
Email_simulator/
|
+-- main.py       # Email, User, Inbox, and demonstration code
+-- README.md     # Project explanation and learning notes
+-- 1.ipynb       # Notebook file associated with the exercise
```

## Classes and Responsibilities

### `Email`

The `Email` class represents one email message.

It stores:

- `sender`: the `User` who sent the message
- `receiver`: the `User` who receives the message
- `subject`: the email subject
- `body`: the message content
- `timestamp`: the time when the email object was created
- `read`: whether the message has been opened

The constructor starts every new email with `read = False`, because a newly received email should initially be unread.

### `User`

The `User` class represents a person using the email simulator.

Each user has:

- A `name`
- An `inbox`

The user-facing actions are also placed on this class:

- `send_email()` sends a message to another user.
- `check_inbox()` displays the user's inbox.
- `read_email()` opens one email.
- `delete_email()` removes one email.

This design allows the program to read naturally:

```python
ramy.send_email(tory, 'Hello', 'Hi Tory!')
ramy.check_inbox()
ramy.read_email(1)
ramy.delete_email(1)
```

### `Inbox`

The `Inbox` class manages a user's collection of received emails.

It stores emails in the `emails` list and provides methods to:

- Receive an email
- List all emails
- Read an email by number
- Delete an email by number

The `User` class forwards inbox-related actions to its `Inbox` object. This keeps email collection management inside the `Inbox` class while giving users a simple public interface.

## Step-by-Step Reasoning

### Step 1: Create an `Email` class

The project begins with a class because an email has both data and behavior.

```python
class Email:
    pass
```

The empty class creates the type first. Later steps add the information and actions that an email needs.

### Step 2: Add the email constructor

The constructor receives the values needed to create an email:

```python
def __init__(self, sender, receiver, subject, body):
```

`self` refers to the individual email object being created. The other parameters describe the message.

The values are stored as instance attributes:

```python
self.sender = sender
self.receiver = receiver
self.subject = subject
self.body = body
```

This is important because parameters only exist while the constructor is running. Assigning them to `self` allows the values to remain available after the object has been created.

### Step 3: Add email state

The email receives two additional attributes:

```python
self.timestamp = datetime.datetime.now()
self.read = False
```

The timestamp records when the email was created. The `read` flag records the email's current state.

This is a useful object-oriented pattern: the object stores both its information and its current condition.

### Step 4: Add `mark_as_read()`

The method changes the email state:

```python
def mark_as_read(self):
    self.read = True
```

A method is used instead of changing the attribute throughout the program because it gives the state change a clear name and a single place to maintain.

### Step 5: Add `display_full_email()`

This method displays the complete message. Before displaying it, it calls `mark_as_read()`:

```python
def display_full_email(self):
    self.mark_as_read()
```

Reading an email therefore has two effects:

1. The email details are displayed.
2. The email changes from unread to read.

The method accesses `self.sender.name` and `self.receiver.name` because the sender and receiver are `User` objects, not plain text names.

The timestamp is formatted with:

```python
self.timestamp.strftime('%Y-%m-%d %H:%M')
```

This produces a readable date and time such as `2026-09-08 14:30`.

### Step 6: Add `__str__()`

The `__str__()` method controls how an email appears when it is printed:

```python
def __str__(self):
    status = 'Read' if self.read else 'Unread'
    return f"[{status}] From: {self.sender.name} | Subject: {self.subject} | Time: ..."
```

Without `__str__()`, printing an email would show a technical object representation such as:

```text
<Email_simulator.main.Email object at 0x...>
```

With `__str__()`, the inbox displays useful information for the user, including whether the email is read or unread.

### Step 7: Create the `User` class

A user needs a name and an inbox:

```python
class User:
    def __init__(self, name):
        self.name = name
        self.inbox = Inbox()
```

The line `self.inbox = Inbox()` demonstrates composition: a `User` contains an `Inbox` object.

The `Inbox` class is defined later in the file, but Python looks up `Inbox` when the `User` constructor runs. By that time, the whole module has been loaded and the class is available.

### Step 8: Implement sending email

The `send_email()` method creates an email using the current user as the sender:

```python
email = Email(sender=self, receiver=receiver, subject=subject, body=body)
```

Here, `self` is the user calling the method. The new email is then delivered to the receiver's inbox:

```python
receiver.inbox.receive_email(email)
```

This is the main object interaction in the program:

1. A user creates an email.
2. The email stores references to the sender and receiver.
3. The receiver's inbox stores the email.

### Step 9: Add `check_inbox()`

The method gives the user a personalized heading and delegates listing to the inbox:

```python
def check_inbox(self):
    print(f"\n{self.name}'s Inbox:")
    self.inbox.list_emails()
```

The `User` class provides the user-facing command, while the `Inbox` class performs the collection-specific work.

### Step 10: Add `read_email()` and `delete_email()` to `User`

These methods act as simple forwarding methods:

```python
def read_email(self, index):
    self.inbox.read_email(index)

def delete_email(self, index):
    self.inbox.delete_email(index)
```

This keeps the calling code simple while allowing `Inbox` to own the actual list operations.

### Step 11: Build the `Inbox` class

The inbox starts with an empty list:

```python
class Inbox:
    def __init__(self):
        self.emails = []
```

When an email arrives, `receive_email()` adds it to the list:

```python
def receive_email(self, email):
    self.emails.append(email)
```

### Step 12: List emails

`list_emails()` first handles the empty inbox case. If emails exist, it uses `enumerate()` with `start=1` so the displayed numbers match the numbers a user would naturally choose.

```python
for i, email in enumerate(self.emails, start=1):
    print(f'{i}. {email}')
```

The displayed number is not the same as the list's zero-based index. The program handles that conversion when reading or deleting.

### Step 13: Read and delete by number

The user sees email numbers beginning at 1, so the methods convert the chosen number to a Python list index:

```python
actual_index = index - 1
```

Before accessing the list, the code checks whether the number is valid:

```python
if actual_index < 0 or actual_index >= len(self.emails):
    print('Invalid email number.\n')
    return
```

This prevents an invalid number from causing an `IndexError`.

Reading calls `display_full_email()`, which also marks the email as read. Deleting uses `del` to remove the selected email from the inbox list.

### Step 14: Run the demonstration

The `main()` function creates two users and demonstrates the complete workflow:

```python
tory = User('Tory')
ramy = User('Ramy')

tory.send_email(ramy, 'Hello', 'Hi Ramy, just saying hello!')
ramy.send_email(tory, 'Re: Hello', 'Hi Tory, hope you are fine.')
ramy.check_inbox()
ramy.read_email(1)
ramy.delete_email(1)
ramy.check_inbox()
```

The final condition:

```python
if __name__ == '__main__':
    main()
```

means that the demonstration runs when `main.py` is executed directly, but does not run automatically when the file is imported into another Python file.

## How to Run

Open a terminal in the `Email_simulator` directory and run:

```text
python main.py
```

The program uses only the Python standard library, so no external packages are required.

## Final Output

The exact timestamp depends on when the program is run. The output follows this pattern:

```text
Email sent from Tory to Ramy!

Email sent from Ramy to Tory!

Ramy's Inbox:

Your Emails:
1. [Unread] From: Tory | Subject: Hello | Time: 2026-09-08 14:30

--- Email ---
From: Tory
To: Ramy
Subject: Hello
Received: 2026-09-08 14:30
Body: Hi Ramy, just saying hello!
------------

Email deleted.

Ramy's Inbox:
Your inbox is empty.
```

The date and time shown above are examples. The actual timestamp is generated by `datetime.datetime.now()` and will be different on each run.

The output demonstrates the complete lifecycle:

1. Tory sends an email to Ramy.
2. Ramy sends an email to Tory.
3. Ramy checks the inbox and sees an unread message.
4. Ramy reads the message.
5. The message becomes read.
6. Ramy deletes the message.
7. Ramy's inbox becomes empty.

## Important Design Decisions

### Why use separate classes?

Each class has a focused responsibility:

- `Email` models message data and message state.
- `User` models people and user actions.
- `Inbox` manages the email collection.

Separating these responsibilities makes the program easier to expand and debug.

### Why store users as objects in an email?

The email stores the sender and receiver as `User` objects. This makes it possible to access their names through `self.sender.name` and `self.receiver.name`. It also leaves room for users to gain more properties later, such as an email address or user ID.

### Why use forwarding methods on `User`?

A user should be able to say `ramy.read_email(1)` without needing to know how the inbox stores its list. This hides implementation details and creates a cleaner interface for the rest of the program.

### Why use an unread flag?

An inbox summary should distinguish new messages from messages that have already been opened. The `read` Boolean stores that state and `__str__()` displays it.

### Why validate email numbers?

A user may choose a number that is too small, too large, or choose an email when the inbox is empty. The checks prevent crashes and give the user a clear message instead.

## What I Learned

As a learner, this project taught me that a class is more than a container for variables. A class can combine data, actions, and state in one meaningful object.

I learned that:

- `__init__()` runs when an object is created and is used to set up its initial attributes.
- `self` refers to the particular object currently being used.
- Parameters must be assigned to `self.attribute` if they need to remain available after a method finishes.
- A method can change an object's state, such as changing an email from unread to read.
- One object can contain another object, as a `User` contains an `Inbox`.
- Objects can interact by calling methods on one another.
- A list is useful for storing multiple objects of the same type.
- `enumerate(..., start=1)` makes list items easier for users to select.
- Python list indexes start at 0, so user-facing numbers often need conversion.
- `__str__()` makes objects easier to display and understand.
- A Boolean such as `read` can represent a simple but useful state.
- Separating responsibilities across classes produces clearer code.
- Defensive checks make a program more reliable when users provide invalid input.
- `if __name__ == '__main__':` separates reusable code from code intended to run as a demonstration.

The most important lesson was learning to design the objects before writing all the methods. Once the relationships were clear, the behavior became easier to organize:

```text
A User sends an Email.
The Email is placed in another User's Inbox.
The Inbox lists, reads, and deletes Email objects.
```

## Possible Next Improvements

This simulator could be extended with:

- A command-line menu for interactive use
- User email addresses
- A sent-mail folder
- Reply functionality
- Forwarding functionality
- Search by sender or subject
- Saving messages to a file
- Loading messages when the program starts
- Confirmation before deleting an email
- Automated tests using `unittest` or `pytest`
- More precise validation for email addresses and empty subjects
