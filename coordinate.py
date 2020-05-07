import math


class COORDINATE(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dist(self, rhs):
        return math.sqrt(pow((self.x - rhs.x), 2) + pow((self.y - rhs.y), 2))

    def output(self):
        temp_x = str(self.x).split('.')
        temp_y = str(self.x).split('.')
        # x = temp_x[0] +'.' + temp_x[1][:2]
        # y = temp_y[0] +'.' + temp_y[1][:2]
        x = round(self.x,1)
        y = round(self.y,1)
        return str(x) + ',' + str(y)

    def print(self):
        print('coordinate x: ', self.x, ' coordinate y: ', self.y)
