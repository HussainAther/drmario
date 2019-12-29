class Pos(object):

    def init(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        if isinstance(other, self):
            return Pos(self.x + other.x, self.y + other.y)
        elif isinstance(other, (tuple, list)):
            return Pos(self.x + other[0], self.y + other[1])
        else:
            raise TypeError("Unknown object in Pos add")

    radd = add
    iadd = add

    def eq(self, other):
        if isinstance(other, self):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, (tuple, list)):
            return self.x == other[0] and self.y == other[1]
        else:
            raise TypeError("Unknown object in Pos eq")

    def ne(self, other):
        return not self.eq(other)
