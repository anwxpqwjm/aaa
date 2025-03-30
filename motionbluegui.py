import cv2
import numpy as np
import pyautogui
import keyboard
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import Toplevel

# モーションブラーのカーネルを作成
def motion_blur_kernel(size, direction):
    kernel = np.zeros((size, size))
    if direction == 'horizontal':
        kernel[int((size-1)/2), :] = np.ones(size)  # 横方向にブラーをかける
    elif direction == 'vertical':
        kernel[:, int((size-1)/2)] = np.ones(size)  # 縦方向にブラーをかける
    else:
        angle = np.deg2rad(direction)  # 斜め方向の場合
        x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
        kernel = np.exp(-((x*np.cos(angle) + y*np.sin(angle))**2)/0.1)
    kernel = kernel / kernel.sum()  # 正規化
    return kernel

# 画面全体にモーションブラーを適用
def apply_motion_blur(image, kernel_size=15, direction='horizontal'):
    kernel = motion_blur_kernel(kernel_size, direction)
    blurred_image = cv2.filter2D(image, -1, kernel)
    return blurred_image

# リアルタイムでスクリーンショットを取得しモーションブラーを適用
def real_time_motion_blur():
    global is_blur_active
    screen_window.after(10, real_time_motion_blur)  # 10ミリ秒ごとに再帰呼び出し
    if is_blur_active:
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        blurred_screen = apply_motion_blur(screen, kernel_size=15, direction='horizontal')
        img = Image.fromarray(blurred_screen)
    else:
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        img = Image.fromarray(screen)

    img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img, anchor=tk.NW)
    canvas.image = img  # 保存しておかないと画像が表示されない

# モーションブラーのオン・オフを切り替え
def toggle_motion_blur():
    global is_blur_active
    is_blur_active = not is_blur_active
    update_status_label()  # ステータスラベルを更新

# ステータスラベルを更新
def update_status_label():
    if is_blur_active:
        status_label.config(text="Motion Blur: ON", fg="#50C878")
    else:
        status_label.config(text="Motion Blur: OFF", fg="red")

# GUIの設定
is_blur_active = False  # 初期状態ではモーションブラーはオフ

# Tkinterウィンドウを設定
screen_window = tk.Tk()
screen_window.title("Future Motion Blur")
screen_window.geometry("200x100+0+0")  # 左上に固定
screen_window.configure(bg="#1a1a1a")  # ダークテーマ背景
screen_window.attributes("-topmost", True)  # 常に最前面に表示
screen_window.attributes("-alpha", 0.85)  # 半透明

# キャンバス設定
canvas = tk.Canvas(screen_window, width=200, height=100, bg="black")
canvas.pack()

# トグルボタン（モーションブラーのオン・オフ）
toggle_button = tk.Button(screen_window, text="Toggle Motion Blur", command=toggle_motion_blur, 
                          font=("Roboto", 12), bg="#333333", fg="#50C878", bd=0, relief="flat", width=20)
toggle_button.pack(side=tk.BOTTOM, pady=10)

# ステータスラベル（モーションブラーの状態表示）
status_label = tk.Label(screen_window, text="Motion Blur: OFF", font=("Roboto", 10), bg="#1a1a1a", fg="red")
status_label.pack(side=tk.TOP)

# ホログラム風のボタンエフェクト
def hover_effect(event):
    event.widget.config(bg="#006400", fg="#ffffff")

def leave_effect(event):
    event.widget.config(bg="#333333", fg="#50C878")

toggle_button.bind("<Enter>", hover_effect)
toggle_button.bind("<Leave>", leave_effect)

# モーションブラーのリアルタイムプレビューを開始
real_time_motion_blur()

# GUIのメインループを開始
screen_window.mainloop()
