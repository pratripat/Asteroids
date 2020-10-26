#Checking the points are collinear or not
def is_collinear(a, b, c):
    one = a.x * (b.y - c.y)
    two = b.x * (c.y - a.y)
    three = c.x * (a.y - b.y)

    formula = (one + two + three) / 2

    return formula == 0
