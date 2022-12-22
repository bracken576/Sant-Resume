class MakeList{
    // makes the list out of the password ad reverses it.
    public List<string> makeList(string str){
        List<string> letters = new List<string>();
        List<string> arr = new List<string>();
        int count = 0;
        for(int i = 0; i < str.Length; i++){
            for(int j = i; j < str.Length; j++)
                if(Equals(str.Substring(i, 1), str.Substring(j, 1)) && !(letters.Contains(str.Substring(i, 1))))
                    count++;
            if(count != 0){
                letters.Add(str.Substring(i, 1));
                arr.Add(str.Substring(i, 1)+" "+count);
            }
            count = 0;
        }
        arr.Reverse();
        return arr;
    }
}