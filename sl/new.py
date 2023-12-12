import tkinter as tk
from tkinter import Toplevel, Button, Label, Frame
from PIL import Image, ImageTk
import random as rd
import copy


def als(x=10, y=10, n=15, ltse=None):
    Step_count = []
    light_count = []

    class Obj:
        width = 40
        height = 40
        end = 0

        def __init__(self, p1, p2):
            self.Left = None
            self.Right = None
            self.color = "#1c62f9"
            self.t_type = "0"
            self.location = [p1, p2]
            self.canvas = None
            self.photo = None
            self.image_item = None
            self.index = None
            self.int = 0

        def LeftClick(self, event=None):
            # print(self.location)
            # 更改画板背景颜色
            self.canvas.config(bg="red")

            # 使用PIL打开图像
            pil_image = Image.open("index1.png")

            # 调整图像大小
            pil_image = pil_image.resize((self.width, self.height), Image.BICUBIC)

            # 将PIL图像转换为Tkinter的PhotoImage
            self.photo = ImageTk.PhotoImage(pil_image)
            # 更新图片位置
            self.image_item = self.canvas.create_image(self.width / 2,
                                                       self.height / 2, image=self.photo)
            # 更新canvas上的图像
            self.canvas.itemconfig(self.image_item, image=self.photo)

            def open_next(i):
                if i < len(quan):
                    quan[i].LeftClick_if()
                    root.after(5, open_next, i + 1)  # 在200毫秒后调用open_next函数

            # 失败判断
            if self.end == 0:
                Obj.end = 1
                open_next(0)  # 开始逐个打开
                create_window("你输了！！")

        def LeftClick_on(self, event=None):
            # 更改背景
            if self.end == 0:
                Step_count.append(self.index)
            use(Step_count)
            self.canvas.config(bg="white")
            # print(text[self.index])
            # print(self.index)
            if text[self.index] != 0:
                self.canvas.create_text(20, 20, text=str(text[self.index]), font=("Arial", 14), fill="black")

        # 判断左键点击的元素
        def LeftClick_if(self, event=None):
            if self.index not in Step_count and self.index not in  light_count:
                if self in tu:
                    self.LeftClick(event)
                else:
                    self.LeftClick_on(event)
                    if text[self.index] == 0:
                        if self.end == 0:
                            calculate(self.index, Select_sequence, text)

                # text是与quan元素相对应的地雷个数 tu是被选中地雷的元素，na是被选中的元素的序列 quan是包含所有类的一个列表
                # calculate(self.index, na, text)

        def RightClick(self, event=None):
            # print(self.location[0] + self.width / 2)
            pil_image = Image.open("旗标.png")
            pil_image = pil_image.resize((self.width, self.height), Image.BICUBIC)
            self.photo = ImageTk.PhotoImage(pil_image)
            self.image_item = self.canvas.create_image(self.width / 2,
                                                       self.height / 2, image=self.photo)
            self.canvas.itemconfig(self.image_item, image=self.photo)

        def RightClickOn(self, event=None):
            self.canvas.delete(self.image_item)

        def Right_if(self, event):
            if self.index not in Step_count:  # 判断是否为已经点击元素
                if self.int == 0:
                    self.RightClick(event)
                    self.int = 1
                    light_count.append(self.index)
                else:
                    self.RightClickOn(event)
                    self.int = 0
                    light_count.remove(self.index)

    # 生成实例
    def yes():
        # 实例化一个对象
        ts = []
        for net in range(x):
            for ls in range(y):
                # print(net * 10 + ls)
                ts.append(Obj(ls * 40, net * 40))
                ts[net * y + ls].index = net * y + ls
                ts[net * y + ls].canvas = tk.Canvas(root, width=ts[net * y + ls].width,
                                                     height=ts[net * y + ls].height, bg=ts[net * y + ls].color)
                ts[net * y + ls].canvas.place(x=ts[net * y + ls].location[0], y=ts[net * y + ls].location[1])
                ts[net * y + ls].Left = ts[net * y + ls].canvas.bind("<Button-1>",
                                                                     ts[net * y + ls].LeftClick_if)  # 绑定左键单击事件
                ts[net * y + ls].Right = ts[net * y + ls].canvas.bind("<Button-3>",
                                                                      ts[net * y + ls].Right_if)  # 绑定右键单击事件

        return ts

    # 对在列表中随机选择地雷
    def random_n(ts, lis):
        if ltse is None:
            nt = copy.copy(rd.sample(ts, lis))
            ns = [ts.index(item) for item in nt]
            return nt, ns

        else:
            nt = []
            for i in ltse:
                nt.append(ts[i])
            ns = ltse
            return nt, ns

    # 计算方块周围地雷个数
    def nes(ns):
        mx = []
        for i in range(x):
            mx.append([])
            for j in range(y):
                mx[i].append(j + y * i)
        ls = [0] * x * y
        for i in range(x):
            for j in range(y):
                # 检查以当前元素为中心的3*3九宫格
                for now in range(max(0, i - 1), min(x, i + 2)):
                    for t in range(max(0, j - 1), min(y, j + 2)):
                        # 检查是否为第二个列表中的元素
                        if mx[now][t] in ns:
                            # 更新结果列表对应位置的计数
                            ls[mx[i][j]] += 1
        return ls

    # 用于计算空白的范围
    def get_neighbors(index):
        row = index // y
        col = index % y
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = [(row + dr, col + dc) for dr, dc in directions]
        return [r * y + c for r, c in neighbors if 0 <= r < x and 0 <= c < y]

    # 序列 被选中元素  被选中元素序列
    def calculate(index, na, b):
        result = []
        visited = set()

        def dfs(num):
            if num in visited or num >= len(b) or num < 0 or num in na or b[num] != 0:
                return
            visited.add(num)
            result.append(num)
            for j in get_neighbors(num):
                dfs(j)

        dfs(index)
        # print(result)

        for i in result:
            quan[i].LeftClick_on()
        return result

    # 胜利判定
    def use(li):

        # print(len(li))
        li = list(set(li))
        if len(li) == x * y - n:
            create_window("你赢了！！")

    # 游戏结束弹窗
    def create_window(txt):
        new_window = Toplevel(root)
        new_window.title("游戏结束!")
        new_window.geometry("300x80+600+300")
        Label(new_window, width=20, height=2, text=txt).pack()  # 直接将txt作为text参数传递给Label
        frame = Frame(new_window, width=200, height=20, bg="green")  # 创建一个新的Frame
        frame.pack()
        # 重新开始新的游戏
        one = Button(frame, text="重开",
                     command=lambda: [new_window.destroy(), root.destroy(), als(x,y,n)])  # 在Frame中添加Button
        # 地雷同上一局
        two = Button(frame, text="继续",
                     command=lambda: [new_window.destroy(), root.destroy(), als(x, y, n, Select_sequence)])
        one.pack(side="left")  # 在Frame中放置Button
        two.pack(side="right")  # 在Frame中放置Button

    root = tk.Tk()
    root.title("扫雷")
    root.geometry(f"{y * 40 + 4}x{x * 40 + 30}+300+200")
    root.iconbitmap("index1.ico")

    """
    ol = Obj(0, 0)
    ol.canvas = tk.Canvas(root, width=ol.width, height=ol.height, bg=ol.color)
    ol.canvas.place(x=ol.location[0], y=ol.location[1])
    ol.Left = ol.canvas.bind("<Button-1>", ol.LeftClick)  # 绑定左键单击事件
    ol.Right = ol.canvas.bind("<Button-3>", ol.Right_if)  # 绑定右键单击事件
    """

    def do_job():
        print()

    def is_digit(char):
        return char.isdigit()

    def validate_input(char, entry_value):
        return is_digit(char) or char == ""
    def do_job1():
        new_window1 = Toplevel(root)
        new_window1.title("难度")
        new_window1.geometry("200x200")
        tk.Label(new_window1, text="请选择难度！").pack()
        var2 = tk.StringVar()
        lb = tk.Listbox(new_window1, listvariable=var2, height=4,width=10)
        var2.set(("10x10,20", "15x10,30", "15*15,40"))
        lb.pack()
        hei = tk.Frame(new_window1)

        def only_numeric_input(entry):
            entry.config(validate="key", validatecommand=(entry.register(validate_input), "%S", "%P"))
        x1 = tk.Entry(hei, font=('Arial', 12), width=3)
        y1 = tk.Entry(hei, font=('Arial', 12), width=3)
        n1 = tk.Entry(hei, font=('Arial', 12), width=3)
        hei.pack()
        tk.Label(hei, text="自定义：").grid(row=0, column=0)
        x1.grid(row=1, column=0)
        y1.grid(row=1, column=1)
        n1.grid(row=1, column=2)
        # 销毁此窗口
        one = Button(new_window1, text="取消",
                     command=lambda: [new_window1.destroy()])  # 在Frame中添加Button
        one.pack(side="left")

        # 确认更改
        def light():
            try:
                value = lb.get(lb.curselection()[0])
            except IndexError:
                value = None

            def ret():
                new_window1.destroy()
                root.destroy()

            if value == "10x10,20":
                ret()
                als(10, 10, 20)
            elif value == "15x10,30":
                ret()
                als(15, 10, 30)
            elif value == "15*15,40":
                ret()
                als(15, 15, 40)

            else:
                if not x1.get() or not y1.get() or not n1.get():
                    # 如果有任何一个输入为空，不进行处理
                    new_window1.destroy()
                    return

                try:
                    x2 = int(x1.get())
                    y2 = int(y1.get())
                    n2 = int(n1.get())
                except IndexError:
                    new_window1.destroy()
                    return

                ret()
                als(x2, y2, n2)

        two = Button(new_window1, text="确定", command=light)
        two.pack(side="right")

    # 创建控制栏
    menubar = tk.Menu(root)
    # 创建控制栏中的一个模块
    filemenu = tk.Menu(menubar, tearoff=0)
    # 给这个模块命名
    menubar.add_cascade(label="菜单", menu=filemenu)
    # 创建模块下拉菜单内容
    filemenu.add_command(label="开始", command=lambda: [root.destroy(), als()])
    filemenu.add_command(label="难度", command=do_job1)
    filemenu.add_command(label="Save", command=do_job)
    # 创建下拉菜单分割线
    filemenu.add_separator()
    root.config(menu=menubar)

    # 函数调用
    quan = yes()
    # quan是包含所有实例的一个列表
    tu, Select_sequence = random_n(quan, n)
    # print(tu, "\n", Select_sequence)
    # tu是被选中地雷的元素， Select_sequence是被选中的元素的序列
    text = nes(Select_sequence)
    # text是与quan元素相对应的地雷个数
    root.mainloop()


if __name__ == "__main__":
    als()
