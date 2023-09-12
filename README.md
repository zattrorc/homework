基于ChatGPT和Langchain实现的本地部署Code Interpreter，python版本3.9。<br />
基于RestrictedPython实现沙箱，可以限制在沙盒里加载的库。<br />
如果需要支持特定的库可以修改sanbox.py中的白名单列表。<br />
运行方法：<br />
安装依赖：<br />
```bash
   pip install -r requirments.txt
   ```
先在backend.py填入你的openai key，然后启动前端：<br />
```bash
   python webui.py
   ```
具体使用流程参照screenshot里面的视频，上传新excel表格会自动替代旧的，目前只支持csv格式<br />
2023.9.12 修复了RestrictedPython中_write_报错的问题<br />
