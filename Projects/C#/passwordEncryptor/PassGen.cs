class PassGen{
    // generates a random password
    private string[] letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};
    private string[] numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"};
    private string[] symbols = {"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "+", "<", ">", "?", "~"};
    private List<string> combined = new List<string>();
    private Random random = new Random();

    // gets the random letters for teh passwords
    void randomLetters(int num){
        for(int i = 0; i < num; i++){
            combined.Add(letters[random.Next(0, letters.Length)]);
        }
    }
    // gets the random numbers for the passwords
    void randomNumbers(int num){
        for(int i = 0; i < num; i++){
            combined.Add(numbers[random.Next(0, numbers.Length)]);
        }
    }
    // gets the random symbols for the passwords
    void randomSymbols(int num){
        for(int i = 0; i < num; i++){
            combined.Add(symbols[random.Next(0, symbols.Length)]);
        }
    }
    // combines the random characters together and then puts them into a random order
    public string randomPassword(int num){
        string password = "";
        if(num % 3 == 0){
            randomLetters(num/3);
            randomNumbers(num/3);
            randomSymbols(num/3);
        }
        else if(num % 3 == 1){
            randomLetters((int)num/3);
            randomNumbers((int)num/3);
            randomSymbols((int)num/3 + 1);
        }
        else if(num % 3 == 2){
            randomLetters((int)num/3);
            randomNumbers((int)num/3 + 1);
            randomSymbols((int)num/3 + 1);
        }
        int index = 0;
        while(combined.Count > 0){
            index = random.Next(0, combined.Count);
            password += combined[index];
            combined.RemoveAt(index);
        }
        return password;
    }
}