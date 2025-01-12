import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import math
from flask import Flask, jsonify, request

app = Flask(__name__)

class LunchSpinner:
    def __init__(self):
        self.options = ["冒菜", "老麻抄手", "螺蛳粉", "饭堂", 
                       "羊肉汤", "饺子", "港式茶餐厅"]
        self.angle = 0
        self.spinning = False

    def spin(self):
        # 模拟转盘旋转
        spins = random.randint(20, 30) # 转动20-30次
        final_index = random.randint(0, len(self.options)-1)
        result = self.options[final_index]
        return result

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/run-spinner', methods=['POST'])
def run_spinner():
    spinner = LunchSpinner()
    result = spinner.spin()
    return f"今天吃：{result}"

if __name__ == "__main__":
    app.static_folder = 'c:/Users/Administrator/Desktop/webpages'
    app.run(port=5000)