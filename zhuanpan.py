import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import math
import os

class LunchSpinner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("今天吃什么?")
        
        # 创建主框架并设置为透明
        self.main_frame = tk.Frame(self.root, bg='')
        self.main_frame.pack(expand=True, fill='both')
        
        # 创建画布并铺满整个窗口
        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, highlightthickness=0)
        self.canvas.pack(expand=True, fill='both')
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 加载并调整背景图片大小以铺满窗口
        self.bg_image = Image.open(os.path.join(current_dir, 'background.jpg'))
        self.update_background()
        
        self.options = ["冒菜", "老麻抄手", "螺蛳粉", "饭堂", 
                       "羊肉汤", "饺子", "港式茶餐厅"]
        # 马卡龙色系
        self.colors = ["#FFB5C2", "#97D2FB", "#FFE5A5", "#C5FAD5",
                      "#FFCCF9", "#AFF8DB", "#FFC8A2"]
        
        self.angle = 0
        self.spinning = False
        
        self.draw_wheel()
        
        # 创建悬浮按钮
        self.spin_button = tk.Button(self.main_frame, text="转动", command=self.spin,
                                   bg='white', relief='raised', font=('Arial', 12))
        self.spin_button.place(relx=0.5, rely=0.85, anchor='center')
        
        # 绑定窗口大小改变事件
        self.root.bind('<Configure>', self.on_resize)
        
    def update_background(self):
        # 获取当前窗口大小
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if width > 1 and height > 1:  # 确保窗口尺寸有效
            resized_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
    def on_resize(self, event):
        # 窗口大小改变时更新背景
        self.update_background()
        self.draw_wheel()
        
    def draw_wheel(self):
        self.canvas.delete("all")
        
        # 绘制背景图片
        if hasattr(self, 'bg_photo'):
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')
        
        center_x = 200
        center_y = 200
        radius = 150
        slice_angle = 360 / len(self.options)
        
        # 创建半透明效果
        for i in range(len(self.options)):
            start_angle = i * slice_angle + self.angle
            end_angle = (i + 1) * slice_angle + self.angle
            
            # 将颜色转换为RGBA格式并设置透明度为50%
            color = self.colors[i]
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            alpha = int(255 * 0.5)  # 50% 透明度
            
            # 绘制扇形(使用白色边框分隔)
            self.canvas.create_arc(center_x-radius, center_y-radius,
                                 center_x+radius, center_y+radius,
                                 start=start_angle, extent=slice_angle,
                                 fill=color, outline="white", width=2,
                                 stipple='gray25')  # 使用stipple实现50%透明效果
            
            # 添加加粗文字，字号增大
            text_angle = math.radians(start_angle + slice_angle/2)
            text_x = center_x + radius * 0.7 * math.cos(text_angle)
            text_y = center_y - radius * 0.7 * math.sin(text_angle)
            self.canvas.create_text(text_x, text_y, text=self.options[i],
                                  font=('Arial', 12, 'bold'))  # 字号从10改为12
            
        # 绘制指针
        self.canvas.create_polygon(195, 50, 205, 50, 200, 70, fill="red")
        
    def spin(self):
        if not self.spinning:
            self.spinning = True
            self.spin_wheel()
            
    def spin_wheel(self):
        if self.spinning:
            speed = random.uniform(5, 15)
            self.angle -= speed
            self.draw_wheel()
            
            if random.random() < 0.02:  # 2%的概率停止
                self.spinning = False
                final_angle = -(self.angle % 360)
                slice_angle = 360 / len(self.options)
                selected_index = int((final_angle + slice_angle/2) / slice_angle) % len(self.options)
                result = self.options[selected_index]
                messagebox.showinfo("结果", f"今天吃：{result}")
            else:
                self.root.after(50, self.spin_wheel)

if __name__ == "__main__":
    spinner = LunchSpinner()
    spinner.root.mainloop()