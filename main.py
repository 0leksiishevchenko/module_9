import functools
from inspect import signature
contacts = {}

def input_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            return f"Input error: {str(e)}"
    return wrapper

@input_error
def add_contact(name, phone):
    if name in contacts.keys():
        raise ValueError(f"Contact {name} already exists")
    
    contacts[name] = phone
    
    return f"Contact {name} added with phone {phone}"

@input_error
def change_contact(name, phone):
    if name not in contacts.keys():
        raise KeyError(f"Contact {name} not found")
        
    contacts[name] = phone
    return f"Phone number for contact {name} changed to {phone}"

@input_error
def get_phone(name):
    if name not in contacts.keys():
        raise KeyError(f"Contact {name} not found")
        
    return f"The phone number for {name} is {contacts[name]}"

@input_error
def show_all():
    if not contacts:
        return "No contacts available"
    contacts_list = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    return contacts_list

@input_error
def hello():
    return "How can I help you?"

@input_error
def good_bye():
    return "Good bye!"

@input_error
def get_handler(command):
    handlers = {
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "show all": show_all,
    }

    _, *args = command.split(" ")
    for key, handler in handlers.items():
        if key in command.lower():
            expected_args = len(signature(handler).parameters)
            if len(args) != expected_args:
                
                return handler()

            return handler(*args)
                                    
    return "Invalid command. Please try again."

def main():
    
    while True:
        command = input("Enter a command: ").lower()
        
        if command in ["good bye", "close", "exit"]:
            print(get_handler(command))
            break
            
        print(get_handler(command))

if __name__ == "__main__":
    main()