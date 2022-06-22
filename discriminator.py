import random
from utils.point import Point
import matplotlib.pyplot as plt
from utils.get_pictures import *
from utils.get_pixels import select_points_on_pic_handly

from utils.plot_on_pic import plot_points_array
shift = [[1, 0], [0, 1], [0, -1], [-1, 0]]
class PointWithDiscr:
    def __init__(self, discr, points):
        self.discr = discr
        self.points = points
class Step:
    def __init__(self, dx, dy, id, event_flag, x_len=28, y_len=28):
        self.dx = dx
        self.dy = dy
        self.id = id
        self.event_flag = event_flag
        self.x_len = x_len
        self.y_len = y_len

    def sense(self, pic, point):
        xlen = 28
        ylen = 28
        if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
            return pic[point.y][point.x]
        else:
            return 0

    def run_id(self, pic, point, id=0):
        pic_0 = pic[0]
        if not isinstance(pic, list):
            pic_0 = pic
        result = self.sense(pic_0, point)
        print(f"bright: {result}")
        if result > 10:
            return 1
        else:
            return 0

    def run_step(self, pic, start_points, step):
        if not isinstance(step, Step):
            return []
        shifts = [[1, 0], [0, 1], [0, -1], [-1, 0]]
        surv_points = self.get_survived_points(start_points, shifts, pic)
        print("***SURVIVED_POINTS***")
        for point in surv_points:
            print(f"Point coords: x: {point.x}, y: {point.y}")
        return surv_points

    @staticmethod
    def get_shifts():
        return [[1, 0], [0, 1], [0, -1], [-1, 0]]

    def get_survived_points(self, start_points, shifts, pic):
        list = []
        surv_points = []
        discriminability = 0

        print(start_points)
        for every_shift in shifts:
            blacks = 0
            whites = 0
            blacks_list_tmp = []
            whites_list_tmp = []
            for point in start_points:
                new_point = Point(x=point.x + every_shift[0], y=point.y + every_shift[1])
                print(f"Old point coords: {point.x}, {point.y}")
                print(f"New point coords: {new_point.x}, {new_point.y}")
                result = self.run_id(pic, new_point)
                print(f"event_flag: {result}")
                if result == 1:
                    blacks = blacks + 1
                    blacks_list_tmp.append(point)
                else:
                    whites = whites + 1
                    whites_list_tmp.append(point)

            if whites > blacks:
                print(f"Whites more than blacks! whites: {whites}, blacks: {blacks}")
                discriminability = blacks / len(start_points)
                surv_points = blacks_list_tmp
            if blacks > whites:
                print(f"Blacks more than whites! whites: {whites}, blacks: {blacks}")
                discriminability = whites / len(start_points)
                surv_points = whites_list_tmp
            if blacks == whites:
                print(f"Blacks and whites equals! whites: {whites}, blacks: {blacks}")
                discriminability = whites / len(start_points)
                surv_points = whites_list_tmp
            print(f"discriminability: {discriminability}")

            list.append(PointWithDiscr(discriminability, surv_points))
        min = float('inf')
        min_list = []
        eps = 0.1
        for points_with_discr in list:
            if (points_with_discr.discr != 0.0) and (points_with_discr.discr <= min):
                min = points_with_discr.discr
        for points_with_discr in list:
            if (points_with_discr.discr == min) or (
                    (points_with_discr.discr <= min + eps) and (points_with_discr.discr != 0.0)):
                min_list.append(points_with_discr.points)
        if len(min_list) == 0:
            return start_points
        if len(min_list) == 1:
            return min_list[0]
        if len(min_list) < len(start_points):
            return self.get_survived_points(min_list[random.randint(0, len(min_list) - 1)], shifts, pic)
        if len(min_list) > 1:
            return self.get_survived_points(min_list[random.randint(0, len(min_list) - 1)])

    def make_simple_discriminator(self, start_points, pic, id=0):
        result_steps = []
        shifts = self.get_shifts()

        while True:
            step, power = self.create_step(pic, shifts, start_points, id=0)

            if step is None:
                break

            start_points = self.run_step(start_points, step)
            shifts = self.update_shifts(shifts, step.dx, step.dy)
            result_steps.append(step)
        return result_steps

    @staticmethod
    def update_shifts(shifts, dx, dy):
        for shift in shifts:
            if dx in shift and dy in shift:
                shifts.remove(shift)
                return shifts

        return shifts

    def run_discriminator(self, steps, points, pic):
        for step in steps:
            points = self.run_step(pic, points, step)
        return points

    def run_discriminator_visual(self, steps, points, pic):

        for step in steps:
            points = self.run_step(pic, points, step)
            plot_points_array( points, pic)

def main():
    step = Step(1, 1, 0, 1)
    pic = get_random_pic_of_type(1)
    steps = []
    start_points = select_points_on_pic_handly(pic)
    xs = start_points[0]
    ys = start_points[1]
    points_from_pic = []
    for i in range(len(xs)):
        points_from_pic.append(Point(x=xs[i], y=ys[i]))
    steps.append(step)
    step.run_discriminator_visual(steps, points_from_pic, pic)
    plt.show()

if __name__ == "__main__":
    main()
