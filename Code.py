import math

# Class to represent a point
class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point") -> float:
        # Calculate the Euclidean distance between two points using the Pythagorean theorem
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx**2 + dy**2)

# Class to represent a line
class Line:
    def __init__(self, start_point: Point, end_point: Point) -> None:
        self.start_point = start_point
        self.end_point = end_point
        # Calculate the length of the line segment between two points
        self.length = start_point.compute_distance(end_point)

# Base class for shapes
class Shape:
    def __init__(self, points: list[Point]) -> None:
        if len(points) < 3:
            raise ValueError("A polygon must have at least 3 points")
        self.points = points
        # Calculate the edges of the shape by connecting consecutive points
        self.edges = [Line(points[i], points[(i + 1) % len(points)]).length for i in range(len(points))]

    def compute_perimeter(self) -> float:
        return sum(self.edges)

    def compute_angles(self) -> list[float]:
        angles = []
        for i in range(len(self.points)):
            p1 = self.points[i - 1]
            p2 = self.points[i]
            p3 = self.points[(i + 1) % len(self.points)]

            a = p1.compute_distance(p2)
            b = p2.compute_distance(p3)
            c = p1.compute_distance(p3)

            # Calculate angles using the law of cosines
            angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
            angles.append(math.degrees(angle))
        return angles

    def is_regular(self) -> bool:
        # Check if all edges are equal and all angles are approximately the same
        return len(set(self.edges)) == 1 and len(set(self.compute_angles())) == 1

# Class to represent a triangle
class Triangle(Shape):
    def __init__(self, points: list[Point]) -> None:
        if len(points) != 3:
            raise ValueError("A triangle must have exactly 3 points")
        super().__init__(points)

    def compute_area(self) -> float:
        a, b, c = self.edges
        s = self.compute_perimeter() / 2
        # Use Heron's formula to calculate the area of a triangle
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

# Subclasses of triangles
class Equilateral(Triangle):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)

class Isosceles(Triangle):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)

class Scalene(Triangle):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)

class RightTriangle(Triangle):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)

# Function to determine the type of triangle
def define_triangle(points: list[Point]) -> Triangle:
    triangle = Triangle(points)
    edges = sorted(triangle.edges)

    tolerance = 1e-9

    # Check if all edges are equal for an equilateral triangle
    if len(set(edges)) == 1:
        return Equilateral(points)
    # Check if two edges are equal for an isosceles triangle
    elif len(set(edges)) == 2:
        return Isosceles(points)
    # Check if the Pythagorean theorem holds within the tolerance for a right triangle
    elif abs(edges[0]**2 + edges[1]**2 - edges[2]**2) < tolerance:
        # abs(edges[0]**2 + edges[1]**2 - edges[2]**2 < tolerance) checks if the sum of squares for a right triangle is approximately valid
        return RightTriangle(points)
    else:
        return Scalene(points)

# Class to represent a rectangle
class Rectangle(Shape):
    def __init__(self, points: list[Point]) -> None:
        if len(points) != 4:
            raise ValueError("A rectangle must have exactly 4 points")
        super().__init__(points)
        # Verify if the points form a valid rectangle
        if not self._is_rectangle():
            raise ValueError("The points do not form a rectangle")

    def _is_rectangle(self) -> bool:
        tolerance = 1e-9
        # Check if all angles are approximately 90 degrees using a tolerance comparison
        return all(abs(angle - 90) < tolerance for angle in self.compute_angles())

    def compute_area(self) -> float:
        return self.edges[0] * self.edges[1]

# Subclass to represent a square
class Square(Rectangle):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)
        # Ensure that all four sides are equal
        if not self.is_regular():
            raise ValueError("A square must have 4 equal sides and right angles")

# Example usage
if __name__ == "__main__":
    triangle_points = [Point(0, 0), Point(4, 0), Point(2, math.sqrt(12))]
    triangle = define_triangle(triangle_points)
    print(f"The type of triangle is: {type(triangle).__name__}")
    print(f"Area of the triangle: {triangle.compute_area()}")
    print(f"Perimeter of the triangle: {triangle.compute_perimeter()}")

    rectangle_points = [Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)]
    rectangle = Rectangle(rectangle_points)
    print(f"Area of the rectangle: {rectangle.compute_area()}")
    print(f"Perimeter of the rectangle: {rectangle.compute_perimeter()}")

    square_points = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
    square = Square(square_points)
    print(f"Area of the square: {square.compute_area()}")
    print(f"Perimeter of the square: {square.compute_perimeter()}")
