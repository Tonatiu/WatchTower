#manager = agent_manager.agent_manager()
#manager.add_agent("public", "192.168.0.103", 161)

"""
Emulate an oscilloscope.  Requires the animation API introduced in
matplotlib 1.0 SVN.
"""
from snmp_agent_managment import agent_manager
import time

manager = agent_manager.agent_manager()
manager.add_agent("public", "192.168.0.103", 161)


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 60.1), ylim=(-2, 100.1))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
cpuUsage = []
for i in range(3000):
    cpuUsage.append(0)
def animate(i):
    x = np.linspace(0, 60, 3000)
    #y = np.sin(2 * np.pi * (x - 0.01 * i))
    cpuUsage.pop(0)
    cpuUsage.append(manager.get_agent_cpuUsage(0))
    line.set_data(x, cpuUsage)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)


#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
