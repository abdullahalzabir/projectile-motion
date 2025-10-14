import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import gridspec

# --- USER INPUT ---
v0 = float(input("Enter initial velocity (m/s): "))
theta = float(input("Enter launch angle with horizontal (degrees): "))
y0_input = input("Enter initial height from x-axis (default 0): ")
y0 = float(y0_input) if y0_input else 0

# --- CONSTANTS ---
g = 9.8  # gravity m/s^2
theta_rad = math.radians(theta)
dt = 0.05  # smaller dt for smoother animation

# --- TOTAL FLIGHT TIME ---
t_max = (v0 * math.sin(theta_rad) + math.sqrt((v0 * math.sin(theta_rad))**2 + 2 * g * y0)) / g

# --- CALCULATE POINTS AND VELOCITIES ---
points = []
t = 0
while t <= t_max:
    x = v0 * math.cos(theta_rad) * t
    y = y0 + v0 * math.sin(theta_rad) * t - 0.5 * g * t**2
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad) - g * t
    speed = math.sqrt(vx**2 + vy**2)
    points.append([t, x, y, vx, vy, speed])
    t += dt

# --- EXTRACT DATA ---
times, xs, ys, vxs, vys, speeds = zip(*points)

# --- SETUP FIGURE WITH GRIDSPEC ---
fig = plt.figure(figsize=(10,7))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

# Trajectory subplot
ax_traj = fig.add_subplot(gs[0])
ax_traj.set_xlim(0, max(xs)*1.1)
ax_traj.set_ylim(0, max(ys)*1.2)
ax_traj.set_xlabel("x (m)")
ax_traj.set_ylabel("y (m)")
ax_traj.set_title("Projectile Motion Animation with Motion Details")
ax_traj.grid(True)
trajectory_line, = ax_traj.plot([], [], 'b-', lw=2)
point, = ax_traj.plot([], [], 'ro', markersize=6)

# Table subplot
ax_table = fig.add_subplot(gs[1])
ax_table.axis('off')
table_data = [["Time(s)", "x(m)", "y(m)", "Vx(m/s)", "Vy(m/s)", "Speed(m/s)"]]
for row in points[::max(1, len(points)//20)]:  # sample 20 points for table
    table_data.append([f"{row[0]:.2f}", f"{row[1]:.2f}", f"{row[2]:.2f}",
                       f"{row[3]:.2f}", f"{row[4]:.2f}", f"{row[5]:.2f}"])
ax_table.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.13]*6)

# --- ANIMATION FUNCTION ---
def update(frame):
    trajectory_line.set_data(xs[:frame], ys[:frame])
    point.set_data(xs[frame], ys[frame])
    return trajectory_line, point

ani = FuncAnimation(fig, update, frames=len(xs), interval=50, blit=True)

plt.tight_layout()
plt.show()