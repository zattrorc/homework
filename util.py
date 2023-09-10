import re
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from sandbox import execute_in_sandbox
import pdb

class StreamHandler(StreamingStdOutCallbackHandler):
    #修改回调函数，取LLM输出
    def __init__(self):
        self.num = 0
        self.tokens = []
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens.append(token)

    def on_llm_end(self, response, **kwargs) -> None:
        self.finish = True

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass

def get_info(df, file_path):
    #获取dataframe的列名和前几行信息
    INFO = """
    Local file path: {file_path}.
    This dataframe has following columns:{columns}
    Here are the first few rows of this dataframe:
    {rows}
    """
    columns = ','.join(list(df.columns.values))
    rows = str(df.head(min(len(df),5)).to_markdown())
    return INFO.format(file_path = file_path, columns=columns, rows=rows)


def extract_python_code(chatgpt_response: str) -> tuple:
    #从LLM输出提取代码部分
    parts = re.split(r'```python(.*?)```', chatgpt_response, flags=re.DOTALL)
    no_code_parts = parts[0::2]
    code_parts = parts[1::2]
    no_code = ''.join(no_code_parts).strip()
    code = ''.join(code_parts).strip()
    return code, no_code


def split_format_statements(code: str) -> str:
    #沙盒中不支持str.format，替换format命令
    match = re.match(r'^(.*\{.*\})(\.format\((.*)\))$', code)
    if not match:
        return code
    before_format, format_call, arguments = match.groups()
    output_code = f'print({before_format}, end="")\n'
    output_code += f'print({arguments})'
    # print(output_code)

    return output_code


def output_praser(df,file_path, s):
    #解析LLM输出，在沙盒中执行代码并取回结果
    code, no_code = extract_python_code(s)
    code = code.replace("C:/path/to/your/file.csv",file_path).replace("read_csv(","read_csv(r")
    obj = execute_in_sandbox(df, split_format_statements(code))

    return obj['text']