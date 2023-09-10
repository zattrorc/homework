基于ChatGPT和Langchain实现的本地部署Code Interpreter，python版本3.9。<br />
基于RestrictedPython实现沙箱，目前只支持在沙盒里运行math,seaborn, os, pandas, numpy, sklearn, scipy。<br />
如果需要支持额外的包可以修改sanbox.py中的白名单列表<br />
运行方法<br />
```bash
   python3 webui.py
   ```
<br />
具体使用流程参照screenshot里面的视频，上传新闻及会自动替代旧的
