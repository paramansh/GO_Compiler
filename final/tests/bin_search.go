package main;

var n int = 10;

func bin_search(x [n]int, l, r, key int) int {
    // return 1;
   if l > r {
      return -1;
   };
   m := (l+r) / 2;
   if x[m] == key {
       return m;
   }
   else if x[m] < key {
      return bin_search(x, l, m-1, key);
   };
};

func main() {
	var a [n]int;
    x := 4;
    y := bin_search(a, 0, n-1, x);
};