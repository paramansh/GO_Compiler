package main;

import (
	"fmt";
	"math/cmplx";
);

var (
	ToBe    bool     = false;
	MaxInt  int      = (1<<64) - 1;
	z       complex  = cmplx.Sqrt(-5 + 12i);
);

func main() {
	const f = "%T(%v)\n";
	fmt.Printf(f, ToBe, ToBe);
	fmt.Printf(f, MaxInt, MaxInt);
	fmt.Printf(f, z, z);
};