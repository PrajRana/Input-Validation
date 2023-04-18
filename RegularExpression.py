import re
phone_number = input("Enter your phone number: ")
pattern = re.compile("^((\+?(?!0)|(00|011))?[ .-]?(\d{1,3})?[ .-]?\(?(?!0)[0-9]{2,3}\)?[ .-]?)?(\d{3})[ -.](\d{4})$")
print(pattern.search(phone_number))
name = input("Enter your full name: ")
pattern = re.compile("^([A-Z]?[a-z]*[ ]?[A-Z][’]?)?([A-Z][a-z]*[-,]\s?)?[A-Z][a-z]*[ ]?[A-Z]?[a-z]*$")
print(pattern.search(name))

