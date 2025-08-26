## 简介

> 2025-08-21 10:33:41

用于172 网站相关的爬虫

我的店铺链接:

[链接](https://h5.lot-ml.com/ProductEn/Index/ad6c8ab0079c1140)

获取到卡之后，就自动 上传的到飞书表格中，

[我的](https://mcne840229gb.feishu.cn/base/CrxTb4kzgazMEasEoM0cAcGvnff?table=tbluyRlwgdGVrYI1&view=vewwQrTbYI)

获取数据的时候需要补充 web_code.py 方法里面 get_all_webdata 的参数 (Authorization, cid) (去手机端抓包)

## 运行

> 2025-08-25 14:13:46

此项目 目前使用uv进行管理，

可以用下面的命令同步环境和运行代码

```bash
uv sync
uv run main.py
```

## 项目架构

该项目是一个数据采集和存储系统，主要用于从特定API获取"卡"的数据，并将其存储到飞书多维表格中。

### 架构流程图

```mermaid
graph TD
    A[程序启动] --> B[加载环境变量]
    B --> C[创建 AllKa 实例]
    C --> D[获取所有卡数据]
    D --> E[创建 FsApi 实例]
    E --> F[创建新的数据表]
    F --> G{尝试批量插入数据}
    G -->|成功| H[完成]
    G -->|失败| I[逐个插入数据]
    I --> H
    
    subgraph web_code.py
    C
    D
    end
    
    subgraph fs.py
    E
    F
    G
    I
    end
```

### 模块说明

项目由三个主要模块组成：

1. **主程序模块 (main.py)**
   - 作为程序入口点
   - 协调 web_code.py 和 fs.py 模块的交互
   - 初始化 AllKa 和 FsApi 实例
   - 获取卡数据并将其存储到飞书表格中

2. **网络请求模块 (web_code.py)**
   - WebClient 类：处理 HTTP 请求的通用客户端
   - AllKa 类：专门用于获取和处理卡数据
   - 从 API 获取数据，并将其转换为结构化的字典列表

3. **飞书 API 模块 (fs.py)**
   - FsApi 类：与飞书多维表格 API 交互
   - 创建数据表
   - 插入单条或批量数据

### 数据流

1. 程序启动，加载环境变量
2. 创建 AllKa 实例，调用 get_all_ka() 方法获取所有卡数据
3. 创建 FsApi 实例，调用 add_data_table() 方法创建新的数据表
4. 尝试将所有卡数据一次性插入表中，如果失败则逐个插入

## 环境变量（重要）

本项目依赖若干环境变量，请参考下面说明并在本地创建 `.env` （或者将 `.env.example` 复制为 `.env` 并填写）：
注意：仓库中已将 `.env` 列入 `.gitignore`，请勿将包含敏感信息的 `.env` 推送到远程仓库。

重要变量列表：
- `FS_app_token`：飞书多维表的 app_token（必填）。用于调用飞书 bitable API。
- `FS_APP_ID` / `FS_APP_SECRET`：飞书应用的 App ID 与 App Secret（必填）。
- `FS_Authorization`：可选的飞书授权头（当需要使用 bearer token 时）。
- `AUTHORIZATION`：目标 API 的 Authorization 请求头（通常为 "Bearer <token>"，从客户端抓包获取）。
- `CID`：请求头中的 cid（可选，部分接口需要）。
- `ZKL`：折扣率，控制返现金额的计算，默认建议 0.9（示例：0.9 表示你得到 90%）。
- `PRODUCTS_API_URL`：产品列表的 API 地址，默认值已在 `.env.example` 中提供；当上游接口地址变化时可在此覆盖。
- `172_index_url`：店铺/商品页面 URL（仅作参考，不一定在代码中使用）。

示例（将 `.env.example` 复制为 `.env` 后填写真实值）：
```bash
cp .env.example .env
# 编辑 .env 填写真实 token、cid 等
```

抓包说明（获取 `AUTHORIZATION` / `CID`）：
1. 在手机上安装抓包工具（如 Charles、Fiddler 或使用带代理功能的抓包 App）。
2. 在目标 APP 中完成一次访问（打开商品列表），在抓包记录中找到请求的 Authorization 与 cid。
3. 将抓到的完整 Authorization（包含 "Bearer " 前缀）和 cid 填入 `.env`。

安全提示：
- 永远不要把 `.env` 上传到公共仓库。
- 如果凭证泄露，请尽快在对应服务中重置/撤销。

