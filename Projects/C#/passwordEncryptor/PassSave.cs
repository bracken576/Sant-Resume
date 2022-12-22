class PassSave{
    // saves the encrypted password to the passwords file and the heap to the arrays file.
    public async Task savePass(List<string> theBinary, List<string> arr, string website){
        string binary = "";
        string array = "";
        for(int i = 0; i < theBinary.Count(); i++){
                binary += theBinary[i] + " ";
                if(i < arr.Count())
                    array += arr[i] + "  ";
        }
        await File.AppendAllTextAsync("arrays.dat", array+"\n");
        await File.AppendAllTextAsync("passwords.dat", website+"  "+binary+"\n");
    }
}