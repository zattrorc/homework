import os
from langchain.prompts import PromptTemplate
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import initialize_agent, AgentType
from util import output_praser, get_info, StreamHandler
os.environ["OPENAI_API_BASE"] = 'https://api.ai-yyds.com/v1'
os.environ["OPENAI_API_KEY"] = "sk-ALsXrDvVsHcx8xVQ15412f23EeF44f16Ae4a2fA5Fe88CeD4"
sth = StreamHandler()
llm = ChatOpenAI(temperature=0,
                 streaming=True,
                 verbose=True,
                 callbacks=[sth],
                 model_name="gpt-3.5-turbo")


EXCEL_QA_CODING_TEM = """
        You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
        Here is some information about this dataframe:{info} 
        Please tell us you idea and  solve this mission by writing a python script that analysis df.
        Code block in answer should be like following sample:
        
        ```python
        sorted_df = df.sort_values(by="价格")
        print(sorted_df[1])
        ```      
        
        This is the mission to be solve:{query}. 
        """




class CodeInterpreter():
    #定义tool
    def __init__(self, llm, df, file_path):
        self.llm = llm
        self.df = df
        self.file_path = file_path

    def get_response_with_coding(self, query) -> str:
        prompt = PromptTemplate(input_variables=["info", "query"],
        template=EXCEL_QA_CODING_TEM).format(
        info = get_info(self.df, self.file_path),
        query=query)
        llm_result = self.llm([HumanMessage(content=prompt)])
        tool_output = output_praser(self.df, self.file_path, llm_result.content)

        return tool_output


def generate_answer(question, df, file_path):
    code_interpreter = CodeInterpreter(llm, df, file_path)
    tools = [Tool(
                name="dataframe_analysis",
                func=code_interpreter.get_response_with_coding,
                description="write a python code according to query, input should be the question itself",
            )]
    openai_agent = initialize_agent(
        agent = AgentType.OPENAI_FUNCTIONS,
        tools = tools,
        llm = llm,
        max_iterations =5,
        return_intermediate_steps=True)

    for step in openai_agent.iter(question):
        for re in sth.generate_tokens():
            yield re
        if (output := step.get("intermediate_step")):
            yield output[-1][-1]
            yield "[SEP]"

# 以下是多线程取回LLM流式结果的尝试，但是只能取回第一段

# def a(question, q):
#     for step in zero_shot_agent.iter(question):
#         q.put(str(step))
#         # if (output := step.get("intermediate_step")):
#         #     q.put(output[-1][-1])
#
#
# def b(q):
#     for re in sth.generate_tokens():
#         q.put(re)
#
#
# def run_and_concatenate(question):
#     q = queue.Queue()

#     t1 = threading.Thread(target=a, args=(question, q))
#     t2 = threading.Thread(target=b, args=(q,))
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#
#
#     while not q.empty():
#         yield q.get()


