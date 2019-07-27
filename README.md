# quizXue v1.1
## 学习强国 挑战答题

> 改进脚本，同时支持手机和MuMu模拟器，此外提供了xpath规则的扩展能力，可自行根据设备设计xpath规则

采用adb模块获取手机UI布局的xml文件，通过lxml解析出题目内容和选项，答案提交并判断正确后将本题保存到数据库。



> OCR截图： 不需针对不同案例设计相应的XPATH规则，但是对截图区域的设置提出要求，得到的数据准确度较高

> XML解析：需要根据具体情况设置合适的XPATH规则，获得的数据准确度极高


### 使用步骤
1. 安装[ADB](https://adb.clockworkmod.com/),并配置环境变量
> 参考[https://github.com/Skyexu/TopSup](https://github.com/Skyexu/TopSup)

2. 手机连接电脑，开启USB调试模式 或者 下载安装[MuMu模拟器](http://mumu.163.com/)

3. python安装虚拟环境和模块
> 脚本中使用了f-string特性，请安装python3.6及以上版本
```python
python -m venv venv
(venv)$:pip install -r requirements.txt
```

4. 进入挑战答题

5. 运行脚本
> --device 参数指定xpath规则(必须)：huawei_p20, mumu

> --count 参数指定本次作答题数(可选)
```python
# MuMu模拟器
(venv)$:python main.py --device mumu
# 华为P20
(venv)$:python main.py --device huawei_p20
```

6. 由于终端设备差异导致UI布局不尽相同，对于未兼容的设备，欢迎大家在config.ini中增加xpath规则

> TODO: 阅读文章、观看视频