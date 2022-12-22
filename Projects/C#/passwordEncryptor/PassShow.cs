class PassShow: HuffDecod{
    // reads lines from the file and prints out the decrypted passwords
    public void showPass(){

        List<string> arr = new List<string>();
        List<string> theBinary = new List<string>();
        string[] lines = File.ReadAllLines("passwords.dat");
        string[] arrays = File.ReadAllLines("arrays.dat");
        string website = "";

        for(int i = 0; i < arrays.Length; i++){
            arr = new List<string>();
            theBinary = new List<string>();

            foreach(string s in arrays[i].Split("  "))
                arr.Add(s);
            foreach(string s in lines[i].Split("  ")[1].Split(" "))
                theBinary.Add(s);
            website = lines[i].Split("  ")[0];

            arr.RemoveAt(arr.Count() - 1);
            theBinary.RemoveAt(theBinary.Count() - 1);
            
            Console.WriteLine(decode(theBinary, arr, website));
        }
    }
}