import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.widgets as widgets
import json
import os
from datetime import datetime
import numpy as np

class ProjectileMotionSimulator:
    def __init__(self):
        self.current_points = []
        self.animations = []
        self.is_animating = False
        self.projectiles = []
        self.current_projectile_id = 0
        
        # Modern color palette
        self.colors = {
            'background': '#2C3E50',
            'panel_bg': '#34495E',
            'text_light': '#ECF0F1',
            'text_dark': '#2C3E50',
            'accent1': '#3498DB',
            'accent2': '#E74C3C',
            'accent3': '#2ECC71',
            'accent4': '#F39C12',
            'grid': '#7F8C8D'
        }
        
        # Default parameters for new projectiles
        self.default_params = {
            'v0': 20,
            'theta': 45,
            'g': 9.8,
            'y0': 0,
            'color': '#3498DB',
            'name': 'Projectile'
        }
        
        # Available colors for projectiles
        self.available_colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', 
                               '#9B59B6', '#1ABC9C', '#D35400', '#C0392B']
        
        plt.style.use('dark_background')
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the modern user interface"""
        self.fig = plt.figure(figsize=(16, 12), facecolor=self.colors['background'])
        self.fig.suptitle('🏹 Advanced Projectile Motion Simulator', 
                         fontsize=20, fontweight='bold', 
                         color=self.colors['text_light'], pad=20)
        
        # Create main layout with better spacing
        gs_main = plt.GridSpec(3, 2, figure=self.fig, height_ratios=[3, 1, 1], 
                              hspace=0.4, wspace=0.4)
        
        # Trajectory plot
        self.ax_traj = self.fig.add_subplot(gs_main[0, 0])
        self.setup_trajectory_plot()
        
        # Current data display
        self.ax_data = self.fig.add_subplot(gs_main[0, 1])
        self.setup_data_display()
        
        # Projectile management
        self.ax_manage = self.fig.add_subplot(gs_main[1, 0])
        self.setup_projectile_management()
        
        # Settings panel
        self.ax_settings = self.fig.add_subplot(gs_main[1, 1])
        self.setup_settings_panel()
        
        # Import/Export panel
        self.ax_io = self.fig.add_subplot(gs_main[2, :])
        self.setup_import_export()
        
        # Initialize with one projectile
        self.add_projectile()
        
    def setup_trajectory_plot(self):
        """Setup the modern trajectory plot area"""
        self.ax_traj.set_facecolor(self.colors['panel_bg'])
        self.ax_traj.set_xlabel("Horizontal Distance (m)", fontsize=12, 
                              color=self.colors['text_light'], fontweight='bold')
        self.ax_traj.set_ylabel("Height (m)", fontsize=12, 
                              color=self.colors['text_light'], fontweight='bold')
        
        # Enhanced grid and styling
        self.ax_traj.grid(True, alpha=0.3, color=self.colors['grid'], linestyle='--')
        self.ax_traj.tick_params(colors=self.colors['text_light'])
        
        # Remove spines and add custom border
        for spine in self.ax_traj.spines.values():
            spine.set_color(self.colors['text_light'])
            spine.set_linewidth(2)
            
        self.ax_traj.set_title('🎯 Projectile Trajectories', fontsize=14, 
                             fontweight='bold', color=self.colors['text_light'], pad=15)
        
    def setup_data_display(self):
        """Setup the modern real-time data display"""
        self.ax_data.set_facecolor(self.colors['panel_bg'])
        self.ax_data.axis('off')
        
        # Create a beautiful info panel
        title = self.ax_data.text(0.5, 0.95, '📊 REAL-TIME DATA', 
                                transform=self.ax_data.transAxes, fontsize=14, 
                                fontweight='bold', color=self.colors['text_light'],
                                ha='center', va='top')
        
        self.data_text = self.ax_data.text(0.05, 0.75, '🚀 Click "Run Simulation" to start', 
                                         transform=self.ax_data.transAxes, fontsize=11, 
                                         verticalalignment='top', fontfamily='monospace',
                                         color=self.colors['text_light'],
                                         bbox=dict(boxstyle="round,pad=1", 
                                                 facecolor="#1A5276", 
                                                 edgecolor=self.colors['accent1'],
                                                 alpha=0.9))
        
        # Add some decorative elements
        self.ax_data.plot([0.1, 0.9], [0.9, 0.9], color=self.colors['accent1'], 
                         linewidth=3, alpha=0.7)
        
    def setup_projectile_management(self):
        """Setup modern projectile management controls"""
        self.ax_manage.set_facecolor(self.colors['panel_bg'])
        self.ax_manage.axis('off')
        self.ax_manage.set_title('🎮 Projectile Management', pad=15, 
                               fontweight='bold', color=self.colors['text_light'], fontsize=13)
        
        # Create management buttons with better layout
        management_gs = plt.GridSpec(2, 4, self.ax_manage, hspace=0.4, wspace=0.3)
        
        # Modern button styling
        button_style = {
            'hovercolor': '0.975',
            'borderwidth': 1,
            'edgecolor': 'white'
        }
        
        ax_add = self.fig.add_subplot(management_gs[0, 0])
        self.add_btn = widgets.Button(ax_add, '➕ Add Projectile', 
                                    color='#27AE60', hovercolor='#2ECC71')
        self.add_btn.on_clicked(self.add_projectile)
        ax_add.set_title("Add New", color=self.colors['text_light'], fontsize=9)
        
        ax_remove = self.fig.add_subplot(management_gs[0, 1])
        self.remove_btn = widgets.Button(ax_remove, '🗑️ Remove Last', 
                                       color='#E74C3C', hovercolor='#EC7063')
        self.remove_btn.on_clicked(self.remove_projectile)
        ax_remove.set_title("Remove", color=self.colors['text_light'], fontsize=9)
        
        ax_clear = self.fig.add_subplot(management_gs[0, 2])
        self.clear_btn = widgets.Button(ax_clear, '🧹 Clear All', 
                                      color='#F39C12', hovercolor='#F7DC6F')
        self.clear_btn.on_clicked(self.clear_all_projectiles)
        ax_clear.set_title("Clear", color=self.colors['text_light'], fontsize=9)
        
        ax_run = self.fig.add_subplot(management_gs[0, 3])
        self.run_btn = widgets.Button(ax_run, '🚀 Run Simulation', 
                                    color='#3498DB', hovercolor='#5DADE2')
        self.run_btn.on_clicked(self.run_simulation)
        ax_run.set_title("Run", color=self.colors['text_light'], fontsize=9)
        
        # Projectile list display with modern styling
        self.ax_list = self.fig.add_subplot(management_gs[1, :])
        self.ax_list.set_facecolor('#2C3E50')
        self.ax_list.axis('off')
        self.ax_list.set_title('📋 Active Projectiles', color=self.colors['text_light'], 
                             fontsize=11, pad=10)
        
        self.projectile_list_text = self.ax_list.text(0.02, 0.85, '', 
                                                    transform=self.ax_list.transAxes, 
                                                    fontsize=10, fontfamily='monospace', 
                                                    verticalalignment='top',
                                                    color=self.colors['text_light'])
        self.update_projectile_list()
        
    def setup_settings_panel(self):
        """Setup the modern settings panel with sliders"""
        self.ax_settings.set_facecolor(self.colors['panel_bg'])
        self.ax_settings.axis('off')
        self.ax_settings.set_title('⚙️ Projectile Parameters', pad=15, 
                                 fontweight='bold', color=self.colors['text_light'], fontsize=13)
        
        settings_gs = plt.GridSpec(5, 2, self.ax_settings, hspace=0.5, wspace=0.4)
        
        # Modern slider styling
        slider_style = {
            'facecolor': self.colors['accent1'],
            'edgecolor': 'white'
        }
        
        track_style = {
            'facecolor': self.colors['grid'],
            'edgecolor': self.colors['grid']
        }
        
        # Velocity input
        ax_v0 = self.fig.add_subplot(settings_gs[0, 0])
        ax_v0.set_facecolor(self.colors['panel_bg'])
        ax_v0.set_title('🎯 Initial Velocity (m/s)', color=self.colors['text_light'], pad=10)
        self.v0_slider = widgets.Slider(ax_v0, '', 1, 100, 
                                      valinit=self.default_params['v0'], valstep=1,
                                      **slider_style, track_color=track_style['facecolor'])
        ax_v0.tick_params(colors=self.colors['text_light'])
        
        # Angle input
        ax_theta = self.fig.add_subplot(settings_gs[0, 1])
        ax_theta.set_facecolor(self.colors['panel_bg'])
        ax_theta.set_title('📐 Launch Angle (°)', color=self.colors['text_light'], pad=10)
        self.theta_slider = widgets.Slider(ax_theta, '', 1, 89, 
                                         valinit=self.default_params['theta'], valstep=1,
                                         **slider_style, track_color=track_style['facecolor'])
        ax_theta.tick_params(colors=self.colors['text_light'])
        
        # Gravity input
        ax_g = self.fig.add_subplot(settings_gs[1, 0])
        ax_g.set_facecolor(self.colors['panel_bg'])
        ax_g.set_title('🌍 Gravity (m/s²)', color=self.colors['text_light'], pad=10)
        self.g_slider = widgets.Slider(ax_g, '', 1, 20, 
                                     valinit=self.default_params['g'], valstep=0.1,
                                     **slider_style, track_color=track_style['facecolor'])
        ax_g.tick_params(colors=self.colors['text_light'])
        
        # Initial height input
        ax_y0 = self.fig.add_subplot(settings_gs[1, 1])
        ax_y0.set_facecolor(self.colors['panel_bg'])
        ax_y0.set_title('📏 Initial Height (m)', color=self.colors['text_light'], pad=10)
        self.y0_slider = widgets.Slider(ax_y0, '', 0, 50, 
                                      valinit=self.default_params['y0'], valstep=1,
                                      **slider_style, track_color=track_style['facecolor'])
        ax_y0.tick_params(colors=self.colors['text_light'])
        
        # Name input
        ax_name = self.fig.add_subplot(settings_gs[2, 0])
        ax_name.set_facecolor(self.colors['panel_bg'])
        ax_name.set_title('🏷️ Projectile Name', color=self.colors['text_light'], pad=10)
        ax_name.axis('off')
        self.name_text = ax_name.text(0.5, 0.3, self.default_params['name'], fontsize=11, 
                                    ha='center', color=self.colors['text_light'],
                                    bbox=dict(facecolor='#1A5276', edgecolor=self.colors['accent1'],
                                            boxstyle="round,pad=0.8", alpha=0.9))
        
        # Color selection
        ax_color = self.fig.add_subplot(settings_gs[2, 1])
        ax_color.set_facecolor(self.colors['panel_bg'])
        ax_color.set_title('🎨 Color', color=self.colors['text_light'], pad=10)
        ax_color.axis('off')
        self.color_text = ax_color.text(0.5, 0.3, self.default_params['color'], fontsize=11, 
                                      ha='center', 
                                      bbox=dict(facecolor=self.default_params['color'], 
                                              edgecolor='white', boxstyle="round,pad=0.8"),
                                      color='white' if self.get_brightness(self.default_params['color']) < 128 else 'black')
        
        # Color cycle button
        ax_color_cycle = self.fig.add_subplot(settings_gs[3, 1])
        self.color_cycle_btn = widgets.Button(ax_color_cycle, 'Cycle Color', 
                                            color='#9B59B6', hovercolor='#BB8FCE')
        self.color_cycle_btn.on_clicked(self.cycle_color)
        
        # Update button
        ax_update = self.fig.add_subplot(settings_gs[4, :])
        self.update_btn = widgets.Button(ax_update, '🔄 Update Current Projectile', 
                                       color='#F39C12', hovercolor='#F7DC6F')
        self.update_btn.on_clicked(self.update_current_projectile)
        
    def setup_import_export(self):
        """Setup modern import/export controls"""
        self.ax_io.set_facecolor(self.colors['panel_bg'])
        self.ax_io.axis('off')
        self.ax_io.set_title('💾 Import/Export', pad=15, 
                           fontweight='bold', color=self.colors['text_light'], fontsize=13)
        
        io_gs = plt.GridSpec(2, 4, self.ax_io, hspace=0.4, wspace=0.3)
        
        ax_export = self.fig.add_subplot(io_gs[0, 0])
        self.export_btn = widgets.Button(ax_export, '📤 Export to JSON', 
                                       color='#27AE60', hovercolor='#58D68D')
        self.export_btn.on_clicked(self.export_to_json)
        ax_export.set_title("Export", color=self.colors['text_light'], fontsize=9)
        
        ax_import = self.fig.add_subplot(io_gs[0, 1])
        self.import_btn = widgets.Button(ax_import, '📥 Import from JSON', 
                                       color='#3498DB', hovercolor='#5DADE2')
        self.import_btn.on_clicked(self.import_from_json)
        ax_import.set_title("Import", color=self.colors['text_light'], fontsize=9)
        
        ax_save_img = self.fig.add_subplot(io_gs[0, 2])
        self.save_img_btn = widgets.Button(ax_save_img, '🖼️ Save as Image', 
                                         color='#F39C12', hovercolor='#F7DC6F')
        self.save_img_btn.on_clicked(self.save_as_image)
        ax_save_img.set_title("Save Image", color=self.colors['text_light'], fontsize=9)
        
        ax_reset = self.fig.add_subplot(io_gs[0, 3])
        self.reset_btn = widgets.Button(ax_reset, '🔄 Reset View', 
                                      color='#E74C3C', hovercolor='#EC7063')
        self.reset_btn.on_clicked(self.reset_view)
        ax_reset.set_title("Reset", color=self.colors['text_light'], fontsize=9)
        
        # Status message with modern styling
        self.ax_status = self.fig.add_subplot(io_gs[1, :])
        self.ax_status.set_facecolor('#2C3E50')
        self.ax_status.axis('off')
        self.status_text = self.ax_status.text(0.02, 0.6, '✅ Ready', fontsize=11, 
                                             color=self.colors['text_light'],
                                             bbox=dict(facecolor='#1A5276', 
                                                     edgecolor=self.colors['accent1'],
                                                     boxstyle="round,pad=0.8"))
    
    def get_brightness(self, hex_color):
        """Calculate brightness of a hex color to determine text color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (r * 299 + g * 587 + b * 114) / 1000
    
    def cycle_color(self, event=None):
        """Cycle through available colors"""
        current_color = self.color_text.get_text()
        if current_color in self.available_colors:
            current_index = self.available_colors.index(current_color)
            next_index = (current_index + 1) % len(self.available_colors)
        else:
            next_index = 0
        
        new_color = self.available_colors[next_index]
        self.color_text.set_text(new_color)
        self.color_text.set_bbox(dict(facecolor=new_color, edgecolor='white', 
                                    boxstyle="round,pad=0.8"))
        self.color_text.set_color('white' if self.get_brightness(new_color) < 128 else 'black')
        plt.draw()
    
    def reset_view(self, event=None):
        """Reset the plot view"""
        self.auto_scale_plot()
        self.update_status("View reset")
    
    def calculate_trajectory(self, v0, theta, g, y0):
        """Calculate projectile motion points"""
        theta_rad = math.radians(theta)
        dt = 0.05
        
        discriminant = (v0 * math.sin(theta_rad))**2 + 2 * g * y0
        if discriminant < 0:
            discriminant = 0
        t_max = (v0 * math.sin(theta_rad) + math.sqrt(discriminant)) / g
        
        points = []
        t = 0
        while t <= t_max:
            x = v0 * math.cos(theta_rad) * t
            y = y0 + v0 * math.sin(theta_rad) * t - 0.5 * g * t**2
            if y < 0:
                y = 0
            vx = v0 * math.cos(theta_rad)
            vy = v0 * math.sin(theta_rad) - g * t
            speed = math.sqrt(vx**2 + vy**2)
            points.append([t, x, y, vx, vy, speed])
            t += dt
        
        return points
    
    def add_projectile(self, event=None, params=None):
        """Add a new projectile"""
        if params is None:
            params = self.default_params.copy()
            params['name'] = f'Projectile_{self.current_projectile_id}'
            params['color'] = self.available_colors[self.current_projectile_id % len(self.available_colors)]
            self.current_projectile_id += 1
        
        projectile = {
            'id': len(self.projectiles),
            'name': params['name'],
            'v0': params['v0'],
            'theta': params['theta'],
            'g': params['g'],
            'y0': params['y0'],
            'color': params['color'],
            'points': [],
            'trajectory_line': None,
            'point': None
        }
        
        self.projectiles.append(projectile)
        self.update_projectile_list()
        self.update_status(f"✅ Added {projectile['name']}")
        
    def remove_projectile(self, event=None):
        """Remove the last projectile"""
        if self.projectiles:
            removed = self.projectiles.pop()
            self.update_projectile_list()
            self.update_status(f"🗑️ Removed {removed['name']}")
            self.clear_plot()
        else:
            self.update_status("⚠️ No projectiles to remove")
    
    def clear_all_projectiles(self, event=None):
        """Clear all projectiles"""
        self.projectiles.clear()
        self.current_projectile_id = 0
        self.update_projectile_list()
        self.clear_plot()
        self.update_status("🧹 All projectiles cleared")
    
    def update_current_projectile(self, event=None):
        """Update the current projectile parameters"""
        if not self.projectiles:
            self.update_status("⚠️ No projectiles to update")
            return
            
        current = self.projectiles[-1]
        current.update({
            'v0': self.v0_slider.val,
            'theta': self.theta_slider.val,
            'g': self.g_slider.val,
            'y0': self.y0_slider.val,
            'name': self.name_text.get_text(),
            'color': self.color_text.get_text()
        })
        
        self.update_projectile_list()
        self.update_status(f"🔄 Updated {current['name']}")
    
    def update_projectile_list(self):
        """Update the projectile list display"""
        if not self.projectiles:
            text = "📝 No projectiles\nAdd one using the button above"
        else:
            text = "🎯 Active Projectiles:\n\n"
            for i, p in enumerate(self.projectiles):
                color_box = f"█"  # Color indicator
                text += f"{color_box} {i+1}. {p['name']}\n"
                text += f"   v₀={p['v0']} m/s, θ={p['theta']}°, h={p['y0']} m\n\n"