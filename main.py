import os
from dotenv import load_dotenv

from fs import FsApi
from web_code import AllKa

load_dotenv()  


if __name__ == '__main__':
    ka = AllKa()
    
    # 获取所有的卡
    ka.all_ka

    fs = FsApi()
    table_id = fs.add_data_table()
    print('table_id',table_id)
    if not fs.insert_any_data(ka.all_ka, table_id):
        for  ka in ka.all_ka:
            fs.insert_any_data(ka, table_id)
            
            

    