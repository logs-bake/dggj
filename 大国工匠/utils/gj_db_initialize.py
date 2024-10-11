from mongodb_util import MongoProc
import os

from utils.load_data import load_data_from_json_file


class CZProc:
    # 构造方法，读入配置文件，创建数据库和相关集合
    def __init__(self):
        self.mongo_proc = MongoProc("gj_conf.json")
        self.mongo_proc.createColl(
            tbs=self.mongo_proc.confs["db_colls"],
            db_name=self.mongo_proc.db)

    # 将文档数据保存到指定的集合中
    def save_docs(self, col, docs):
        """ col： 集合名称， docs： 要保存到集合中的文档列表"""
        self.mongo_proc.insertDoc(
            tb=col,
            docs=docs,
            db_name=self.mongo_proc.db)


if __name__ == "__main__":
    # base_path = r"E:\学习资料\Flask Web\11~13\作业\ltj_26_cz\static\jsons"  # jsons文件夹的路径
    base_path = r"/home/大国工匠/static/jsons"
    # 要读取的json文件名（与配置文件中的db_colls相同）
    cat_names = ['gj_battle', 'gj_hero', 'gj_history', 'gj_literature', 'gj_memorial', 'gj_video']
    proc = CZProc()  # 创建CZProc类的实例
    for cat in cat_names:  # 循环读取各个json文件，并将相应数据保存到数据库对应的集合中
        documents = load_data_from_json_file(os.path.join(base_path, cat + '.json'))
        proc.save_docs(col=cat, docs=documents)
