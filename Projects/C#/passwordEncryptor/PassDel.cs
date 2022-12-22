class PassDel{
    // removes the password and corresponding heap from the files and inputs the other passwords and heaps back in.
    public async Task removePass(){
        int number = 0;
        bool isNum = true;
        string[] lines = File.ReadAllLines("passwords.dat");
        string[] arrays = File.ReadAllLines("arrays.dat");

        while(isNum){
            isNum = false;
            Console.Write("Which would you like to remove? (Index begins with 1) ");
            try{
                number = Int32.Parse(Console.ReadLine())-1;
            }
            catch(System.FormatException){
                Console.WriteLine("\nThat is not a valid response it needs to be a number and needs to be within the range of passwords.\n");
                isNum = true;
            }
            if(!isNum && (number > lines.Length-1 || number <= 0)){
                Console.WriteLine("\nThat is not a valid response it needs to be a number and needs to be within the range of passwords.\n");
                isNum = true;
            }
        }

        File.Delete("passwords.dat");
        File.Delete("arrays.dat");
        
        for(int i = 0; i < lines.Length; i++){
            if(i != number){
                await File.AppendAllTextAsync("arrays.dat", arrays[i]+"\n");
                await File.AppendAllTextAsync("passwords.dat", lines[i]+"\n");
            }
        }
    }
}