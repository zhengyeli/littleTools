# little_tools

#### 介绍
略

#### 软件架构
pycharm + pyqt6


#### 安装教程

1.  安装软件
（1）先安装python3.9版本以上
（2）安装pycharm

2.  配置环境
（1）配置pyqt6环境
![选择interpreter](https://foruda.gitee.com/images/1663588903605263901/3ceebd05_10497968.png "屏幕截图")
![选择interpreter](https://foruda.gitee.com/images/1663589066150605749/1fec7fb8_10497968.png "屏幕截图")
![安装pyqt6](https://foruda.gitee.com/images/1663589095927706363/f342bb5b_10497968.png "屏幕截图")
（2）配置额外工具
setting -> external tool -> 
[uic]
program: D:\python3.10\Scripts\pyuic6.exe
arguments: $FileName$ -o $FileNameWithoutExtension$.py
working directory:$FileDir$

[designer]
program: D:\python3.10\Lib\site-packages\PySide6\designer.exe
arguments: 
working directory:$FileDir$

[pyinstaller]
program: E:\Python3.9\Scripts\pyinstaller.exe
arguments: -D -w $FileName$
working directory:$FileDir$
usage:pyinstaller.exe -D -w main.py 

[PYRCC]
program: E:\Python3.9\Scripts\pyside6-rcc.exe
arguments: $FileName$ -o $FileNameWithoutExtension$.py
working directory:$FileDir$
3.  xxxx

#### 使用说明


#### 参与贡献



#### 特技

