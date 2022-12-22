class HuffDecod : Binary{
    // decodes the binary into the password
    public string decode(List<string> theBinary, List<string> arr, string? website){
        website += " - ";
        for(int i = 0; i < theBinary.Count; i++)
            website += arr[getBinary(theBinary[i])].Split(" ")[0];
        return website;
    }
    // gets the index from the binary list to put into the heap.
    public int getBinary(string theBinary){
        for(int i = 0; i < binary.Count(); i++)
            if(binary[i] == theBinary)
                return i;
        return -1;
    }
}