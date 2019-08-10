# 学习强国 AutoXue 2.0

> 由于增加了视听学习功能，故将项目改名为 AutoXue

## 环境要求
* os：推荐Win10
* Python：python 3.6+ 推荐python 3.7.4
* ADB：ADB1.0.39+ 推荐[ADB 1.0.40](./xuexi/src/assets/ADB_1_0_40.7z)
* device：Android 推荐[MuMu模拟器](http://mumu.163.com/)2.2.12

## 使用方法
0. 很重要！首先请确认自己的操作系统，XP系统只能安装python3.4-，请不要往下看了，项目要求python版本最低3.6，因为python3.6+加入了本项目使用的f-string特性，另、操作系统太低可能无法安装使用模拟器，所以，系统不符合的用户真心不要浪费时间往下看了
1. 安装好Python、ADB、MuMu模拟器，并添加python和ADB环境变量
2. 安装[ADBBoardkey](./xuexi/src/assets/ADBKeyboard.apk)输入法（解决输入中文）
3. 安装[学习强国](https://www.xuexi.cn/)APP
4. 双击运行初次安装.bat， 或者
```python
# 安装虚拟环境
python -m venv venv
# 安装项目依赖
(venv)$:python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
4. 打开MuMu模拟器（连接安卓手机需要开启USB调试），登录学习强国APP并置于首页
> 经测试，华为手机【我要答题】在一个容器中，无法获取布局，其他手机未测试。大家还是踏踏实实用模拟器吧，别再提无理要求了。
5. 双击开始积分.bat， 或者
```python
# 运行脚本程序
(venv)$:python -m xuexi -a -c -d -v
''' 请在首页运行, 参数按需添加
参数说明
    -a[--article]:      阅读文章(实现中)
    -c[--challenge]:    挑战答题(已完成)
    -d[--daily]:        每日答题(已完成)
    -v[--video]:        视听学习(已完成)
'''
(venv)$:python -m xuexi.quiz.challenge -c 30 -v True|False
'''请进入挑战答题后运行，手机也支持，
参数说明
    -c[--count] 挑战答题题数<int>, 自己指定， 默认10
    -v[--virtual] 是否模拟器<bool>，配和config使用
    eg.
        (venv)$:python -m xuexi.quiz.challenge -c 30 -v # 模拟器中使用
        (venv)$:python -m xuexi.quiz.challenge -c 30 # 手机中使用
'''
(venv)$:python -m xuexi.media.viewer -c 20 -d 30 -v True|False
'''请在首页运行
参数说明
    -c[--count] 观看视频数<int>, 自己指定, 默认36
    -d[--delay] 每个视频观看时间<int>, 自己指定， 默认30
    -v[--virtual] 是否模拟器<bool>，配和config使用
    eg.
        (venv)$:python -m xuexi.media.viewer -c 20 -d 30 -v # 模拟器中使用
        (venv)$:python -m xuexi.media.viewer -c 20 -d 30 # 手机中使用 
'''
```
