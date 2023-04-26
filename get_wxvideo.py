import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Requests Viewer")
        self.root.geometry("800x600")


        self.label_url = tk.Label(self.root, text="URL:")
        self.entry_url = tk.Entry(self.root)
        self.button_load = tk.Button(self.root, text="Load Requests", command=self.load_requests)
        self.text_requests = tk.Text(self.root, height=30, width=100)
        self.scrollbar_requests = tk.Scrollbar(self.root, command=self.text_requests.yview)


        self.label_url.pack(side="top", padx=5, pady=5)
        self.entry_url.pack(side="top", padx=5, pady=5)
        self.button_load.pack(side="top", padx=5, pady=5)
        self.text_requests.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.scrollbar_requests.pack(side="left", fill="y")

    def load_requests(self):
        # 获取输入的网页地址
        url = self.entry_url.get()

        # 启动Chrome浏览器并打开目标网页
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless") # 可选，使Chrome在后台运行
        chrome_service = ChromeService(executable_path="/path/to/chromedriver")
        chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        chrome_driver.get(url)

        # 等待页面加载完成
        chrome_driver.implicitly_wait(180) # 等待最多10秒

        # 获取所有网络请求
        network_requests = chrome_driver.execute_script("return performance.getEntriesByType('resource')")

        # 将所有网络请求显示在文本框中
        self.text_requests.delete("1.0", tk.END) # 清空文本框
        for request in network_requests:
            url = request["name"]
            if url.startswith("https://mpvideo.qpic.cn"):
                self.text_requests.insert(tk.END, url + "\n")

        # 关闭浏览器
        chrome_driver.quit()

# 创建主窗口并运行程序
root = tk.Tk()
app = App(root)
root.mainloop()
