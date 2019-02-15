package main;

import "fmt";

func badlog(y, x int) (int) {
	count := 0;
	for i := 1; i < y ; i *= x {
		count += 1;
	};
	return count;
};

func baddiv(q, p int) (int) {
	count := 0;
	for  q > 0 {
		count += 1;
		q -= p;
	};
	return count;
};

func main() {
	fact := 1;
	for i:= 1; i < 7; i++ {
		fact *= i;
	};
	fmt.Println(fact);
	fmt.Println(badlog(9, 2));
	fmt.Println(baddiv(7, 2));
};