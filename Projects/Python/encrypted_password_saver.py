import random
from cryptography.fernet import Fernet

def file_print():
    file = open('passwords.txt', 'r')
    for line in file:
        print(line)
    
def key(the_key):
    unlock = open('unlock.key', 'wb')
    unlock.write(the_key)

def remove_password(num):
    passwords = open("passwords.txt", "r+")
    copy = open("the_copy.txt", "a")
    count = 0
    for line in passwords:      
        if count != num:
            copy.write(line)
        count += 1
    passwords.truncate(0)
    passwords.close()
    copy.close()
    passwords = open("passwords.txt", "a")
    copy = open("the_copy.txt", "r+")
    for line in copy:
        passwords.write(line)
    copy.truncate(0)
    copy.close()
    passwords.close()
    
def delete_newlines(file, copy):
    file_f = open(file, 'r+')
    copy_f = open(copy, "a")
    for line in file_f:
        if len(line.strip()) > 0:
            copy_f.write(line)
    file_f.truncate(0)
    file_f.close()
    copy_f.close()
    file_f = open(file, 'a')
    copy_f = open(copy, 'r+')
    for line in copy_f:
        if len(line.strip()) > 0:
            file_f.write(line)
    copy_f.truncate(0)
    file_f.close()
    copy_f.close()
    
def encrypt_password(the_key):
    f = Fernet(the_key)
    passwords = open('passwords.txt','rb+')
    encrypted_file = open('the_copy.txt', 'ab')
    for line in passwords:
        encrypted = f.encrypt(line)
        encrypted_file.write(encrypted+b"\n")
    passwords.truncate(0)
    delete_newlines('the_copy.txt', 'passwords.txt')
    passwords = open('passwords.txt', 'ab')
    encrypted_file = open('the_copy.txt', 'rb+')
    for line in encrypted_file:
        passwords.write(line+b"\n")
    encrypted_file.truncate(0)
    passwords.close()
    encrypted_file.close()
    delete_newlines('passwords.txt', 'the_copy.txt')
        
def decrypt_password():
    unlock = open('unlock.key', 'rb')
    key = unlock.readline()
    f = Fernet(key)
    encrypted_file = open('passwords.txt', 'rb+')
    decrypted_file = open('the_copy.txt', 'ab')
    for line in encrypted_file:
        if len(line.strip()) > 10:
            decrypted = f.decrypt(line)
            decrypted_file.write(decrypted+b"\n")
    encrypted_file.truncate(0)
    delete_newlines('the_copy.txt', 'passwords.txt')
    encrypted_file.close()
    decrypted_file.close()
    decrypted_file = open("the_copy.txt", 'r+')
    writ = open("passwords.txt", 'w')
    for line in decrypted_file:
        writ.write(line+"\n")
    decrypted_file.truncate(0)
    decrypted_file.close()
    writ.close()
    delete_newlines('passwords.txt', 'the_copy.txt')   

def letters():
    letters_string = ""
    for x in range(0,3):
        letters = ''.join(random.sample(("pyth0n", "g30rg3", "h3ll0", "dre@m", "h@v1ng", "bu1lding", "t1m0thy", "g@di@nt0n", "gl@d1@t0r", "l@qu@c10us"), 1))
        letters_string = letters_string + letters + "_"
    letters_string = letters_string[0:len(letters_string)-1]
    return letters_string

def numbers():
    numbers_string = ""
    for x in range(0,7):
        numbers = ''.join(random.sample("1234567890", 1))
        numbers_string = numbers_string + numbers
    return numbers_string
    
def symbols():
    symbols_string = ""
    for x in range(0,7):
        symbols = ''.join(random.sample("!@#$%^&*()|?/_", 1))
        symbols_string = symbols_string + symbols
    return symbols_string

def combine(letters, numbers, symbols):
    phrase = letters.split("_")
    combined= "".join(random.sample(numbers+symbols, 14))
    password = phrase[0] + combined[0:7] + phrase[1] + combined[7:len(combined)] + phrase[2]
    return password

while True:
    the_key = Fernet.generate_key()
    decrypt_password()
    print("The file has been decrypted.")   
    while True:
        yes_no = input("Would you like to get another password? yes, no: ")
        print()
        while yes_no.lower() == "yes":
            website = input("What website will this password be used for? ")
            password = combine(letters(), numbers(), symbols())
            print(password + " - " + website.strip() + "\n")
            f = open('passwords.txt', 'a')
            f.write("\n" + password + " - " + website)
            print("The password and the website has been inputted\n")
            f.close()
            yes_no = input("Would you like to generate another password? yes, no: ")
            print()
        
        yes_no = input("Would you like to input a password that you already have? yes, no: ")
        print()
        while yes_no.lower() == "yes":
            password = input("What is the password? ")
            website = input("What website will this password be used for? ")
            print()
            print(password + " - " + website.strip())
            f = open('passwords.txt', 'a')
            f.write("\n" + password + " - " + website)
            print("The password and website has been inputted.")
            f.close()
            yes_no = input("Would you like to put in another password? yes, no: ")
            print()
        
        yes_no = input("Would you like to remove a password? yes, no: ")
        print()
        while yes_no.lower() == "yes":
            delete_newlines('passwords.txt', 'the_copy.txt')
            file_print()
            num = int(input("Which password would you like to remove? Enter a number: "))
            print()
            remove_password(num - 1)
            print("The password has been deleted.\n")
            yes_no = input("Would you like to remove another password? ")
            
        yes_no = input("Would you like to go through these choices again? yes, no: ")
        print()
        if yes_no.lower() != "yes":
            break

    key(the_key)
    encrypt_password(the_key)
    print("The file has been encrypted.\n")

    decrypted = False
    num = int(input("Hello, would you like to encrypt or decrypt and print out passwords or break? "))
    print()
    while True:
        if num == 1 and decrypted:
            key(the_key)
            encrypt_password(the_key)
            decrypted = False
            print("The file has been encrypted.\n")
        elif num == 2 and not decrypted:
            decrypt_password()
            decrypted = True
            print("The file has been decrpted.\n")
            file_print()
        elif num == 3 and not decrypted:
            break
        else:
            print("You have either chosen an incorrect number, attempted to encrypt an already encrypted file,\ndecrypt an already decrypted file, or leave without encrypting the file.\n")
        num = int(input("Hello, would you like to encrypt or decrypt or break? "))
        print()
        
    yes_no = input("Would you like to go through the choices again? yes, no: ")
    print()
    if yes_no.lower() != "yes":
        print("Good bye, I hope you were able to have an enjoyable experience.\n")
        break