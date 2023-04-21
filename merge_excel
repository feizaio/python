import shutil
import sys
import xlwt
import xlrd
import tkinter as tk
from tkinter import filedialog

def select_file():
    """
    打开文件选择对话框
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def save_file():
    """
    打开保存文件对话框
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename()
    return file_path

def merge_excel():
    # 打开表1
    print("请选择要匹配的表格1")
    file1 = select_file()
    wb1 = xlrd.open_workbook(filename=file1)

    # 打开表2
    print("请选择要匹配的表格2")
    file2 = select_file()
    wb2 = xlrd.open_workbook(filename=file2)

    # 获取表1要匹配的列索引，目标数据列索引，以及表1的sheet
    print("请输入表1要匹配的列索引")
    hid_index1 = int(input())
    print("请输入表1目标数据列索引")
    target_index1 = int(input())
    sheet1 = wb1.sheet_by_index(0)
    rowNum1 = sheet1.nrows
    colNum1 = sheet1.ncols

    # 获取表2要匹配的列索引，目标数据列索引，以及表2的sheet
    print("请输入表2要匹配的列索引")
    hid_index2 = int(input())
    print("请输入表2目标数据列索引")
    target_index2 = int(input())
    sheet2 = wb2.sheet_by_index(0)
    rowNum2 = sheet2.nrows
    colNum2 = sheet2.ncols

    # xlwt准备生成一个新的文件
    write_workbook = xlwt.Workbook()
    write_sheet = write_workbook.add_sheet('sheet1', cell_overwrite_ok=True)

    # 复制表2的数据到新文件
    for index2 in range(0, rowNum2):
        for col_index in range(0, colNum2):
            write_sheet.write(index2, col_index, sheet2.cell_value(index2, col_index))
            if col_index == target_index2:
                # 在遍历列过程中,如果碰到目标数据列索引.即需要补充的字段,则进行遍历表1,判断的id索引匹配
                for index1 in range(1, rowNum1):
                    hid1 = sheet1.cell_value(index1, hid_index1)
                    if hid1 == sheet2.cell_value(index2, hid_index2):
                        # 如果两个表的id相同则把表1的单元内容设置到表2对应的单元格
                        write_sheet.write(index2, col_index, sheet1.cell_value(index1, target_index1))

    # 保存新的文件
    print("请选择新文件保存路径及文件名")
    write_file = save_file()
    write_workbook.save(write_file)

    print("文件合并成功！")

if __name__ == '__main__':
    merge_excel()

