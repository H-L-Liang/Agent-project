#RAG主要功能
'''
总结服务类： 用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
'''

from xml.dom.minidom import Document
from rag.vector_store import VectorStoreServive
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt
#LHL



class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreServive()   #向量存储
        self.retriever = self.vector_store.get_retriever()  #检索器
        self.prompt_text = load_rag_prompts()        #文本
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)        #提示词模板
        self.model = chat_model
        self.chain = self._init_chain()


    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain
    

    def retriever_docs(self,query: str) -> list[Document]:
        return self.retriever.invoke(query)


    def rag_summarize(self, query: str) -> str:
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0

        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}] : 参考资料：{doc.page_content} | 参考数据：{doc.metadata}\n"

        return self.chain.invoke(   #通过调用{query}和{context}，把上面的东西通过模型概括回答去拿到结果
            {
                "input": query,
                "context": context,
            }
        )


if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("大户型适合哪些扫地机器人"))

