import requests
from bs4 import BeautifulSoup
import time
import re
import webbrowser
import keyboard

# 获取用户输入
search = input("输入商品名: ")

def clean_url(url):
    """去除链接中的多余参数，保留基础 URL"""
    pattern = r'(https://[a-zA-Z0-9-]+\.en\.made-in-china\.com/?)'
    match = re.search(pattern, url)
    if match:
        base_url = match.group(1)
        return base_url.rstrip('/') + '/'
    return url

def get_web_info(url, max_pages=40, output_file='suppliers.txt'):
    """爬取供应商信息并保存到文件"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}
    suppliers = []
    
    for page in range(1, max_pages + 1):
        page_url = url.replace('1.html', f'{page}.html') if '1.html' in url else f"{url}{page}.html"
        print(f"正在处理页面: {page_url}")
        
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"页面 {page} 请求失败，状态码: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        page_suppliers = soup.select('.company-name a')
        if not page_suppliers:
            print(f"页面 {page} 无供应商信息，停止爬取")
            break
        
        for entry in page_suppliers:
            name = entry.text.strip()
            raw_link = 'https:' + entry['href'] if entry.get('href', '').startswith('//') else entry['href']
            clean_link = clean_url(raw_link)
            contact_link = clean_link + 'contact-info.html'
            suppliers.append({'name': name, 'link': contact_link})
        
        #time.sleep(1)  # 添加延时，避免触发反爬
    
    if suppliers:
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, supplier in enumerate(suppliers, 1):
                f.write(f"供应商 {i}:\n")
                f.write(f"  名称: {supplier['name']}\n")
                f.write(f"  链接: {supplier['link']}\n")
                f.write("-" * 40 + "\n")
        print(f"已保存 {len(suppliers)} 个供应商信息到 {output_file}")
    else:
        print("未获取到任何供应商信息")
    
    return suppliers

def read_links_from_file(file_path):
    """从文件中读取链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'链接: (https?://[^\s]+)', content)
    return links

def open_links_with_space(links):
    """按Space键逐个打开链接"""
    # 获取用户输入的起始点
    while True:
        try:
            start_index = int(input(f"请输入从第几条链接开始（1到{len(links)}）: "))
            if 1 <= start_index <= len(links):
                break
            else:
                print("输入的数字超出范围，请重新输入。")
        except ValueError:
            print("请输入一个有效的数字。")
    
    current_index = start_index - 1  # 转换为0-based索引
    print("按Space键打开下一条链接，或者按Esc键退出。")
    
    while current_index < len(links):
        # 等待Space键按下
        keyboard.wait('space')
        
        # 检查是否按下Esc键退出
        if keyboard.is_pressed('esc'):
            print("检测到Esc键，退出程序。")
            break
        
        link = links[current_index]
        print(f"正在打开: {link}")
        try:
            webbrowser.open(link)
        except Exception as e:
            print(f"打开链接 {link} 时出错: {e}")
        
        current_index += 1
    
    if current_index >= len(links):
        print("已打开所有链接。")

# 主程序
base_url = "https://www.made-in-china.com/company-search/" + search + "/C1/1.html"
result = get_web_info(base_url, max_pages=40, output_file='suppliers.txt')

# 输出结果到控制台（可选）
if result:
    for i, supplier in enumerate(result, 1):
        print(f"供应商 {i}:")
        print(f"  名称: {supplier['name']}")
        print(f"  链接: {supplier['link']}")
        print("-" * 40)

# 读取链接并按Space键打开
links = read_links_from_file('suppliers.txt')
if links:
    open_links_with_space(links)
else:
    print("没有找到任何链接。")