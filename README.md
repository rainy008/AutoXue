# quizXue
## 学习强国 挑战答题

> 正如每日、每周、专项答题一样，目的是为了巩固知识，该脚本实现挑战答题辅助功能，可导出Excel题库或**磨题帮**题库。

采用adb模块获取手机UI布局的xml文件，通过lxml解析出题目内容和选项，答案提交并判断正确后将本题保存到数据库。



> OCR截图： 不需针对不同案例设计相应的XPATH规则，但是对截图区域的设置提出要求，得到的数据准确度较高

> XML解析：需要根据具体情况设置合适的XPATH规则，获得的数据准确度极高


### 使用步骤
1. 安装[ADB](https://adb.clockworkmod.com/),并配置环境变量
> 参考[https://github.com/Skyexu/TopSup](https://github.com/Skyexu/TopSup)

2. 手机连接电脑，开启USB调试模式

3. python安装虚拟环境和模块
```python
python -m venv venv
(venv)$:pip install -r requirements.txt
```

4. 手机进入挑战答题

5. 运行脚本
```python
(venv)$:python main.py
```

6. 直接执行model.py可将数据库导出到[题库](./data/data-dev.md)，可直接使用Ctrl+F搜索答案，也可直接下载使用[Excel版本](./data)。

```python
(venv)$:python model.py
```

> 展望： 数据库中未检索到记录时需要手机上提交之后在控制台手动提交添加记录到数据库，希望通过*adb shell getevent*获取手机输入事件，直接驱动脚本完成数据库的添加和转入下一流程