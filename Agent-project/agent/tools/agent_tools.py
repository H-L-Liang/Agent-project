#agent工具的调用，从外部文件检索用户数据
import os
import random
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path  #获取绝对路径
from utils.logger_handler import logger

rag = RagSummarizeService()


user_ids = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",]
month_arr = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
             "2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12", ]

external_data = {}



@tool(description="从向量存储中检索参考资料")  #向量的检索工具
def rag_summarize(query: str) -> str:  #rag向量总结服务
    return rag.rag_summarize(query)


@tool(description="获取指定城市天气，以消息字符串的形式返回")   #获取天气
def get_weather(city: str) -> str:  
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，最近6小时降雨概率低"


@tool(description="获取用户所在城市的名称，以纯字符串的形式返回")#获取用户定位
def get_user_location() -> str:
    return random.choice(["广州","中山","肇庆"])


@tool(description="获取用户的ID，以纯字符串的形式返回")   
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")  
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    '''
    {
        "user_id":{
            "month":{"特征":xxx, "效率":xxx, ....}
            "month":{"特征":xxx, "效率":xxx, ....}
            "month":{"特征":xxx, "效率":xxx, ....}
            ....
        },
        "user_id":{
            "month":{"特征":xxx, "效率":xxx, ....}
            "month":{"特征":xxx, "效率":xxx, ....}
            "month":{"特征":xxx, "效率":xxx, ....}
        },
        .....
    }
    :return:
    '''

    if not external_data:    #如果是第一次进来则填充，否则跳过
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")
        
        with open(external_data_path,"r",encoding="utf-8")as f:
            for line in f.readlines()[1:]:  #从文件第二行开始读取
                arr :list[str] = line.strip().split(",")  #CSV逗号分隔

                uid: str = arr[0].replace('"',"")  #把双引号转为空字符串
                feature: str = arr[1].replace('"',"")
                efficiency: str = arr[2].replace('"',"")
                consumables: str = arr[3].replace('"',"")
                comparison: str = arr[4].replace('"',"")
                time: str = arr[5].replace('"',"")

                if uid not in external_data:
                    external_data[uid] = {}

                external_data[uid][time] = {  #传入数据
                    "特征":feature,
                    "效率":efficiency,
                    "耗材":consumables,
                    "对比":comparison,
                }



@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()


    try:
        return str(external_data[user_id][month])
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户: {user_id}在{month}的使用记录数据")
        return ""
    

@tool(description="无入参，无返回值，调用后出发中间件自动触发中间件自动为报告生成的场景注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

#LHL
#if __name__ == '__main__':
#    print(fetch_external_data("01","2026-02"))
