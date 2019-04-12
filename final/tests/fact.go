package main;

func factorial(x int) int {
	if x < 0 {
		return 0;
	};
   if x <= 1 {
       return 1;
   }
   else {
		return x * factorial(x-1);
   };
};

func main() {
    var a int = 9;
    var x int;
    x = factorial(a);
};