# Final-Project

## Bracken Sant: bracken576@outlook.com or bsant576@byui.edu

## Required Software: 
VS Code: https://code.visualstudio.com/download and .NET https://dotnet.microsoft.com/en-us/download

## Description: 
This project was made to help keep track of passwords and to encrypt them. It utilizes an algorithm that is generally used to compress data called Huffman encoding, however, I believe that on a small scale it is also useful to encrypt data, such as a list of passwords.

## Project Structure:
### Binary: is the parent class for HuffDecod and HuffEncod. Inheritance, polymorphism, encapsulation.
The Binary class has the binary list for all of instances in the heap and an empty class getBinary that will be changed by HuffDecod and HuffEncod.

### Heap: Uses encapsulation and abstraction. 
The Heap class changes the list or array given to it into a heap.

### HuffDecod: is the child class of Binary and the parent class of PassShow. Inheritance, polymorphism, abstraction.
The HuffDecod class decodes the Huffman encoded password into its original form.

### HuffEncod: is the child class of Binary. Inheritance, polymorphism, abstraction.
The HuffEncod class encodes the password with Huffman encoding. 

### MakeList: Abstraction.
The MakeList class takes the string password and makes a string list out of it. It takes the characters and the amount of time each one appears in the password and puts it in the list separated by a space: ex. L 2

### PassDel: Abstraction.
The PassDel class gets user input for which password is to be deleted by number. It then reads from both “arrays.dat” and “passwords.dat” and deletes the desired password and then inputs the passwords that weren’t deleted back into the file.

### PassGen: Encapsulation and abstraction.
The PassGen class generates a password with Random. It takes a user input from the Runner class for the length of the password and then splits it between the 3 type of characters: numbers, letters, and special characters. It then randomly selects from the 3 types to input into the password and then the password is randomly generated from those characters.

### PassSave: Abstraction.
The PassSave class saves the binary list version of the password as a string in the passwords file and the list version of the password in the arrays file.

### PassShow: is the child class of HuffDecod. Inheritance and abstraction.
The PassShow class takes the lists of strings from the passwords and arrays files and decodes the passwords to display on the screen. 

### Runner: 
The Runner class runs the program and goes through the user input process for various questions and calls other classes to utilize their code.

![Screenshot 2022-12-10 112723](https://user-images.githubusercontent.com/62550662/206869951-8aeb5074-3d09-47e0-a3dd-2e4dfee44f74.png)

