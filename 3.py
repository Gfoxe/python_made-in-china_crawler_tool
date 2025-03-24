import os
import cv2
import numpy as np
from mss import mss
import pytesseract
import pyautogui
import time
import webbrowser

# 设置 Tesseract 可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 设置 TESSDATA_PREFIX 环境变量
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

def find_text_on_screen(target_text, lang='chi_sim+eng'):
    # 其余代码保持不变
    sct = mss()
    screenshot = sct.grab(sct.monitors[1])
    img = np.array(screenshot)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, lang=lang)

def find_text_on_screen(target_text, lang='chi_sim+eng'):
    # 创建 mss 对象
    sct = mss()
    
    # 捕获全屏截图
    screenshot = sct.grab(sct.monitors[1])  # monitors[1] 为主显示器
    
    # 转换为 numpy 数组并转为 BGR 格式
    img = np.array(screenshot)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    
    # 转换为灰度图像
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # 使用 Tesseract OCR 获取文字数据
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, lang=lang)
    
    # 查找目标文字并获取坐标
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if target_text in data['text'][i]:
            # 获取边界框坐标
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            
            # 计算中心坐标
            center_x = x + w // 2
            center_y = y + h // 2
            
            print(f"找到 '{target_text}' 在屏幕位置:")
            print(f"左上角: ({x}, {y})")
            print(f"右下角: ({x+w}, {y+h})")
            print(f"中心点: ({center_x}, {center_y})")
            
            return (x, y, x+w, y+h), (center_x, center_y)
    
    print(f"未找到 '{target_text}'")
    return None



# 使用示例
if __name__ == "__main__":
    # 指定要查找的文字
    target_text = "Contact"
    a = input("请输入搜索名称:")
    final = "https://www.made-in-china.com/companysearch.do?subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0&isOpenCorrection=1&org=&keyword=&file=&searchType=1&word="+a
    webbrowser.open(final)
    time.sleep(3)
    pyautogui.moveTo(391,717,duration=0.5)
    pyautogui.click()
    time.sleep(5)
    # 执行查找
    result = find_text_on_screen(target_text)
    if result:
        bounding_box, center = result
        print(f"边界框坐标: {bounding_box}")
        print(f"中心坐标: {center}")
        pyautogui.moveTo(center,duration=0.3)
        pyautogui.click()
        time.sleep(1)
        pyautogui.scroll(-1000)
        pyautogui.moveTo(416,640,duration=0.3)
