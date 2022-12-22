class HuffEncod : Binary{
    // encodes the password into the binary
    public List<string> encode(string str, int length, List<string> arr){
        List<string> theBinary = new List<string>();
        for(int i = 0; i < str.Length; i++)
            for (int j = 0; j < length; j++)
                if(Equals(arr[j].Split(" ")[0], str.Substring(i, 1)))
                    theBinary.Add(getBinary(j));
        return theBinary;
    }
    // gets the binary from the index of the corresponding character in the heap
    public string getBinary(int index){
        return binary[index];
    }
}