class Runner{
    public static async Task Main(string[] args){
        PassGen pass = new PassGen();
        PassShow show = new PassShow();
        PassSave save = new PassSave();
        PassDel del = new PassDel();
        HuffEncod enc = new HuffEncod();
        HuffDecod dec = new HuffDecod();
        MakeList list = new MakeList();
        Heap h = new Heap();

        // Prompts the user to see if they want a new random password.
        Console.Write("Would you like to make a random password? (y/n): ");
        string? yes_no = Console.ReadLine();

        string? num = "";
        int number = 0;
        string str = "";
        string? website = "";
        bool b = true;
        List<string> arr = new List<string>();
        List<string> theBinary = new List<string>();

        // While loop for making new passwords and encrypting and saving them to the passwords file along with the corresponding array to the arrays file.
        while(Equals(yes_no, "y")){
            // While loop to ensure that a number is put in for the number of characters in the password.
            while(b){
                b = false;
                Console.Write("How many characters would you like your password to be? ");
                num = Console.ReadLine();
                try{
                    number = Int32.Parse(num);
                    b = false;
                }
                catch(System.FormatException){
                    b = true;
                    Console.WriteLine("You need to input a number and the number needs to be 31 or less.\n");
                }
                if(!b)
                    if(number > 31){
                        b = true;
                        Console.WriteLine("You need to input a number and the number needs to be 31 or less.\n");
                    }
            }
            b = true;
            // generates the random password
            str = pass.randomPassword(number);

            // generates the list for the password
            arr = list.makeList(str);
            // resets the theBinary list if the loop has already gone through once.
            theBinary = new List<string>();

            // sets the list in the Heap class and then makes a heap out of the list.
            h.setArr(arr);
            h.buildHeap(arr.Count);
            arr = h.getArr();

            // gets the corresponding binary for the password and sets it in the theBinary list.
            theBinary = enc.encode(str, arr.Count, arr);
            Console.WriteLine("\n"+str);

            // prompts the user to see if they want to save the password and if they do it then saves it and the corresponding website.
            Console.Write("\nWould you like to save this password? (y/n): ");
            yes_no = Console.ReadLine();

            if(Equals(yes_no, "y")){
                Console.Write("\nWhat website or app is this for? ");
                website = Console.ReadLine();
                await save.savePass(theBinary, arr, website);
            }

            Console.Write("\nWould you like to make another password? (y/n): ");
            yes_no = Console.ReadLine();
        }

        Console.Write("\nWould you like to look at the passwords? (y/n): ");
        yes_no = Console.ReadLine();
        Console.WriteLine();
        // shows the passwords if the user wants to see them
        if(Equals(yes_no, "y")){
            show.showPass();
        }

        Console.Write("\nWould you like to remove a password from the file? (y/n): ");
        yes_no = Console.ReadLine();
        Console.WriteLine();

        // removes passwords as long as the user wants to. Will break if there are no passwords left.
        while(Equals(yes_no, "y")){
            show.showPass();
            await del.removePass();

            try{
                string[] lines = File.ReadAllLines("passwords.dat");
            }
            catch(System.IO.FileNotFoundException){
                Console.WriteLine("There are no more passwords to delete.");
                break;
            }

            Console.Write("\nWould you like to remove another password from the file? (y/n): ");
            yes_no = Console.ReadLine();
            Console.WriteLine();
        }
    }
}