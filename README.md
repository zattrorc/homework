基于ChatGPT和Langchain实现的本地部署Code Interpreter，python版本3.9。
基于RestrictedPython实现沙箱，目前只支持在沙盒里运行math,seaborn, os， pandas, numpy, sklearn，scipy。
如果需要支持额外的包可以修改sanbox.py中的白名单列表
运行方法
```bash
   python3 webui.py
   ```