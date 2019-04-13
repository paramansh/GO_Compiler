package main;

func main() {
    var t0, t1, t2 int;
    n := 4;

    t0 = 0;
    t1 = 1;

    for i := 0; i < n; i++ {
        t2 = t1 + t0;
        t1 = t2;
        t0 = t1;
    };
};