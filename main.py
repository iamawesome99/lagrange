import numpy as np

from polynomial import Polynomial
import matplotlib.pyplot as plt

# how much to scale the axes to determine the bounding boxes for the dots
SCALE_PERCENTAGE = 0.01
# which dot is currently selected
selected = None


def find_curve(x, y):
    # find the lagrange polynomial from a list of x and y values.

    # if we have a duplicated x value
    if len(set(x)) != len(x):
        raise Exception("Duplicated X value.")

    # start with 0
    end = Polynomial([0])

    # https://en.wikipedia.org/wiki/Lagrange_polynomial#Examples
    # you thought they were cool and here we are
    for xn, yn in zip(x, y):
        new = Polynomial([yn])
        for i in x:
            if i == xn:
                continue

            new *= Polynomial([1, - i])
            new *= Polynomial([1 / (xn - i)])

        end += new

    return end


def button_press_callback(event):
    # called when we click a button
    global selected

    # if we already picked up a dot set it down
    if selected is not None:
        selected = None
        return
    # if we aren't in the axes or clicking the left button why are we here?
    if event.inaxes is None or event.button != 1:
        return

    # simple bounding box algorithm
    def in_box(p1, p2):
        return p1[0] + x_delta > p2[0] > p1[0] - x_delta and p1[1] + y_delta > p2[1] > p1[1] - y_delta

    # ehe~
    x_delta = (ax.get_ylim()[1] - ax.get_ylim()[0]) * SCALE_PERCENTAGE
    y_delta = (ax.get_ylim()[1] - ax.get_ylim()[0]) * SCALE_PERCENTAGE

    # get the xy coordinates of the cursor
    xy = ax.transData.inverted().transform([event.x, event.y])

    # for each dot
    for count, x, y in zip(range(len(px)), px, py):
        # if it's in the bounding box pick it up
        if in_box([x, y], xy):
            selected = count
            print("Selected " + str(selected))
            return
    # otherwise just leave.


# noinspection PyTypeChecker
def motion_notify_callback(event):
    # called on a mouse movement
    global px, py
    # where even are we?
    if event.inaxes is None:
        return
    # make sure we have a dot selected
    if selected is None:
        return

    # grab the new xy coordinates of the dot
    xy = ax.transData.inverted().transform([event.x, event.y])

    # and put the new xy coordinates of the dot in.
    # yes i know there's a warning here.
    # i don't know how to make it go away
    # nvm i suppressed it
    px[selected] = xy[0]
    py[selected] = xy[1]

    # and update the canvas
    update_canvas()


def update_canvas():
    # updates the canvas based on what's in px and py

    # reload the dots plot
    dots.set_xdata(px)
    dots.set_ydata(py)

    # recalculate the curve
    end = find_curve(px, py)

    # reset the title of the plot
    ax.title.set_text(repr(end))

    # recalculate the values of the curve
    function_x = np.linspace(*ax.get_xlim(), 3000)
    function_y = end(function_x)

    # and reload it's plot
    line.set_xdata(function_x)
    line.set_ydata(function_y)

    # make sure we be drawing them.
    fig.canvas.draw_idle()


# number of points
# you could theoretically make this as large as you want...
# but things explode in a factorial fashion.
# 5-10 is a good number.
# also it becomes slower but not fast enough to be worried about
number = 5


# starts off with a boring squares polynomial
px = list(range(number))
py = [x ** 2 for x in px]

# it's x^2 but let's humour the program
end = find_curve(px, py)

fig, ax = plt.subplots()

# set the title
ax.title.set_text(repr(end))

# plot the dots
dots, = ax.plot(px, py, "ro")

# use the matplotlib auto things to figure out the linear space for the line
function_x = np.linspace(*ax.get_xlim())
function_y = end(function_x)

# plot the line
line, = ax.plot(function_x, function_y)

# add the listeners
fig.canvas.mpl_connect('motion_notify_event', motion_notify_callback)
fig.canvas.mpl_connect('button_press_event', button_press_callback)

# and get the party started
plt.show()
