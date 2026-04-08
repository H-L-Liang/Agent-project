#主程序使用页面
import time
import streamlit as st
from agent.react_agent import ReactAgent

#标题  LHL
st.title("智能扫地机器人AI客服")
st.divider()

if "agent" not in st.session_state:   #第一次运行创建类实例，不会重复创建
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:  #每次页面重新启动，把message从历史记录中提出来
    st.chat_message(message["role"]).write(message["content"])

#用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    response_messages = []
    with st.spinner("智能客服思考中。。。"):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)  #放入缓存
                
                for char in chunk:  #让程序一个字一个字的输出，真流式输出（而非一个块一个块的输出）
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream,response_messages))
        #流式输出过程中的内容都打印出来，输出完成后页面只保留最后一条信息
        st.session_state["message"].append({"role":"assistant","content":response_messages[-1]})
        #所有内容输出以后，让程序手动刷新页面
        st.rerun()


#LHL


