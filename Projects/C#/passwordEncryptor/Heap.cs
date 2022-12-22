class Heap{
    private List<string> arr = new List<string>();
    // sets the list in the heap
    public void setArr(List<string> replaceArray){
        arr = replaceArray;
    }
    // returns the list
    public List<string> getArr(){
        return arr;
    }
    // swaps smaller values for larger values.
    public void swap(int a, int b){
        string c = arr[a];
        arr[a] = arr[b];
        arr[b] = c;
    }
    // heapifies the list
    public void heapify(int length, int i){
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        char[] separator = {' '};
        if(left < length && Int16.Parse(arr[left].Split(separator)[1]) > Int16.Parse(arr[largest].Split(separator)[1]))
            largest = left;
        if(right < length && Int16.Parse(arr[right].Split(separator)[1]) > Int16.Parse(arr[largest].Split(separator)[1]))
            largest = right;
        
        if(largest != i){
            swap(i, largest);
            heapify(length, largest);
        }
    }
    // builds the heap through heapify
    public void buildHeap(int length){
        int stIndex = (length / 2) - 1;
        for(int i = stIndex; i >= 0; i--){
            heapify(length, i);
        }
    }
}