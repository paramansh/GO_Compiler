package main;

func fib(x int) int {
   if x <= 1 {
       return 1;
   }
   else {
		return fib(x-1) + fib(x-2);
   };
};

func main() {
    var a int = 9;
    var x int;
    x = fib(a);
};