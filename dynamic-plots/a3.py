#!/usr/bin/env python 
import matplotlib.pyplot as plt
import numpy as np
def setup_backend(backend='TkAgg'):
    import sys
    del sys.modules['matplotlib.backends']
    del sys.modules['matplotlib.pyplot']
    import matplotlib as mpl
    mpl.use(backend)  # do this before importing pyplot
    import matplotlib.pyplot as plt
    return plt

def animate():
    # http://www.scipy.org/Cookbook/Matplotlib/Animations
    mu, sigma = 100, 15
    N = 4
    x = mu + sigma * np.random.randn(N)
    rects = plt.bar(range(N), x, align='center')
    for i in range(50):
        x = mu + sigma * np.random.randn(N)
        for rect, h in zip(rects, x):
            rect.set_height(h)
        fig.canvas.draw()

plt = setup_backend()
fig = plt.figure()
win = fig.canvas.manager.window
win.after(3, animate)
plt.show()



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_line(num, data, line):
    line.set_data(data[...,:num])
    return line,

fig1 = plt.figure()

data = np.random.rand(2, 25)
l, = plt.plot([], [], 'r-')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
    interval=50, blit=False)
#line_ani.save('lines.mp4')

fig2 = plt.figure()

x = np.arange(-9, 10)
y = np.arange(-9, 10).reshape(-1, 1)
base = np.hypot(x, y)
ims = []
for add in np.arange(15):
    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
    blit=False)
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

plt.show()