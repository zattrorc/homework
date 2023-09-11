基于ChatGPT和Langchain实现的本地部署Code Interpreter，python版本3.9。<br />
基于RestrictedPython实现沙箱，目前只支持在沙盒里运行math,seaborn, os, pandas, numpy, sklearn, scipy。<br />
如果需要支持额外的包可以修改sanbox.py中的白名单列表<br />
运行方法<br />
先在backend.py填入你的openai key，然后启动前端<br />
```bash
   python3 webui.py
   ```
具体使用流程参照screenshot里面的视频，上传新excel表格会自动替代旧的，目前只支持csv格式
