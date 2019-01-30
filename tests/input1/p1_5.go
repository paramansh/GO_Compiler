import (
	"fmt"
	"math"
)

type Abser interface {
	Abs() float
}

func main() {
	var a Abser
	f := MyFloat(-math.Sqrt2)
	v := Vertex{3, 4}

	a = f  // a MyFloat implements Abser
	a = &v // a *Vertex implements Abser

	// In the following line, v is a Vertex (not *Vertex)
	// and does NOT implement Abser.
	a = v

	fmt.Println(a.Abs())
}

type MyFloat float

func (f MyFloat) Abs() float {
	if f < 0 {
		return float(-f)
	}
	return float(f)
}

type Vertex struct {
	X, Y float
}

func (v *Vertex) Abs() float {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}