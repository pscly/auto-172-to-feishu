import json
import time
import os
from dotenv import load_dotenv

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


load_dotenv()  


class FsApi:
    def __init__(self):
        app_id =  os.getenv("FS_APP_ID")
        app_secret =  os.getenv("FS_APP_SECRET")
        self.app_token =  os.getenv("FS_app_token")
        self.last_table_id = ''
        self.last_view_id = ''
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()

    # SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
    # 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
    # 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
    def insert_any_data(self, any_data:list, table_id):
        s_data = []

        for i in any_data:
            for k, v in i.items():
                if k in ['宣传图片', '推广链接']:
                    i[k] = {
                        "link": v,
                        "text": "点击查看",
                    }
            s_data.append(AppTableRecord.builder().fields(i).build())

        client = self.client
        # 构造请求对象
        request: BatchCreateAppTableRecordRequest = BatchCreateAppTableRecordRequest.builder() \
            .app_token(self.app_token) \
            .table_id(table_id) \
            .request_body(BatchCreateAppTableRecordRequestBody.builder()
                .records(
                    # [
                    #     AppTableRecord.builder().fields({"人员":[{"id":"ou_2910013f1e6456f16a0ce75ede950a0a"},{"id":"ou_e04138c9633dd0d2ea166d79f548ab5d"}],"单向关联":["recHTLvO7x","recbS8zb2m"],"单选":"选项1","双向关联":["recHTLvO7x","recbS8zb2m"],"地理位置":"116.397755,39.903179","复选框":true,"多选":["选项1","选项2"],"数字":100,"文本":"文本内容","日期":1674206443000,"条码":"qawqe","电话号码":"13026162666","群组":[{"id":"oc_cd07f55f14d6f4a4f1b51504e7e97f48"}],"评分":3,"货币":3,"超链接":{"link":"https://www.feishu.cn/product/base","text":"飞书多维表格官网"},"进度":0.25,"附件":[{"file_token":"Vl3FbVkvnowlgpxpqsAbBrtFcrd"}]}).build(),
                    # ]zz
                    s_data
                    )
                .build()) \
            .build()

        # 发起请求
        response: BatchCreateAppTableRecordResponse = client.bitable.v1.app_table_record.batch_create(request)

        # 处理失败返回
        if not response.success():
            print('插入 数据 失败')

            lark.logger.error(f"client.bitable.v1.app_table_record.batch_create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return 0

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        print('插入 数据 成功 ')
        return 1 




    def insert_one_data(self, one_data:dict, table_id):

        request: CreateAppTableRecordRequest = CreateAppTableRecordRequest.builder() \
            .app_token(self.app_token) \
            .table_id(table_id) \
            .request_body(AppTableRecord.builder()
                .fields(one_data)\
                .build()) \
            .build()

        # 发起请求
        response: CreateAppTableRecordResponse = self.client.bitable.v1.app_table_record.create(request)

        # 处理失败返回
        if not response.success():
            print('插入 数据 失败')
            lark.logger.error(  f"client.bitable.v1.app_table_record.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return 0

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        print('插入 数据 成功 ')
        return  1



    # SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
    # 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
    # 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
    def add_data_table(self):
        # 创建client
        client = self.client
        table_name = time.strftime("y-数据表%Y-%m-%dT%H-%M-%S", time.localtime())

        # 构造请求对象
        request: CreateAppTableRequest = CreateAppTableRequest.builder().app_token(self.app_token).request_body(CreateAppTableRequestBody.builder()
                .table(ReqTable.builder()
                    .name(table_name)
                    .default_view_name("默认的表格视图")
                    .fields([
                        AppTableCreateHeader.builder().field_name("标题").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("推广链接").type(15).build(), 
                        AppTableCreateHeader.builder().field_name("宣传图片").type(15).build(), 
                        AppTableCreateHeader.builder().field_name("返现类型").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("运营商").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("返现金额").type(2).build(), 
                        AppTableCreateHeader.builder().field_name("归属地").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("规则").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("通用流量").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("定向流量").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("通话时长").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("不发货地区").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("最小年龄").type(2).build(), 
                        AppTableCreateHeader.builder().field_name("最大年龄").type(2).build(), 
                        AppTableCreateHeader.builder().field_name("首冲价格").type(1).build(), 
                        AppTableCreateHeader.builder().field_name("更新时间").type(1).build(), 
                        
                        # AppTableCreateHeader.builder()
                        # .field_name("单选")
                        # .type(3).ui_type("SingleSelect").property(AppTableFieldProperty.builder().options([AppTableFieldPropertyOption.builder().name("Enabled").color(0)
                        #         .build(), 
                        #         AppTableFieldPropertyOption.builder()
                        #         .name("Disabled")
                        #         .color(1)
                        #         .build(), 
                        #         AppTableFieldPropertyOption.builder()
                        #         .name("Draft")
                        #         .color(2)
                        #         .build()
                        #         ]).build()).build()
                        ])
                    .build())
                .build()) \
            .build()

        # 发起请求
        response: CreateAppTableResponse = client.bitable.v1.app_table.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.bitable.v1.app_table.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        jsondata = json.loads(lark.JSON.marshal(response.data))
        self.last_table_id = jsondata.get('table_id')
        self.last_view_id = jsondata.get('default_view_id')
        return jsondata.get('table_id')

if __name__ == "__main__":
    a = {
        "宣传图片": "https://haokaapi.lot-ml.com/upload/ProductUpDateImage/20250821/d7e980160f7c40b5894a0c270061b8d9.jpg",
        "推广链接": "https://h5.lot-ml.com/h5orderEn/index?pudID=9e574c95642328a6&userid=ad6c8ab0079c1140",
        "标题": "电信星卡【39元180G】",
        "返现类型": "次月返",
        "运营商": "电信",
        "返现金额": 90.0,
        "归属地": "随机",
        "不发货地区": "北京,海南海口市,海南三亚市,海南琼海市,海南万宁市,海南儋州市,海南东方市,海南文昌市,海南五指山市,海南定安县,海南屯昌县,海南澄迈县,海南临高县,海南三沙市,云南昆明市,云南曲靖市,云南玉溪市,云南昭通市,云南楚雄彝族自治州,云南红河哈尼族彝族自治州,云南普洱市,云南西双版纳傣族自治州,云南大理白族自治州,云南保山市,云南德宏傣族景颇族自治州,云南丽江市,云南怒江傈僳族自治州,云南迪庆藏族自治州,云南临沧市,西藏拉萨市,西藏阿里地区,新疆乌鲁木齐市,新疆克拉玛依市,新疆吐鲁番地区,新疆哈密地区,新疆昌吉回族自治州,新疆博尔塔拉蒙古自治州,新疆巴音郭楞蒙古自治州,新疆阿克苏地区,新疆克孜勒苏柯尔克孜自治州,新疆喀什地区,新疆和田地区,新疆伊犁哈萨克自治州,新疆塔城地区,新疆阿勒泰地区,新疆石河子市",
        "规则": "激活当月专属渠道充值100元话费，次月底结算(结算的前提是当月次月不欠费、不销户、不单停、不三无、不更改套餐且开机)",
        "最小年龄": 18,
        "最大年龄": 60,
        "通用流量": "180G",
        "定向流量": "30G",
        "通话时长": "0分钟",
        "首冲价格": "100",
        "更新时间": "2025-08-21 14:31:11"
    }
    f = FsApi()
    table_id = f.add_data_table()
    print('table_id',table_id)
    f.insert_one_data(a, table_id)
