from utils.load_data import load_data_from_json_file


class History:
    def __init__(self, history_id, history_name, **kwargs):
        self.history_id = history_id
        self.history_name = history_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "history_description" in self.kwargs.keys():
            return self.kwargs.get("history_description")

    def show_info(self):
        print(f"""
            影视作品名称：{self.history_name}
            影视作品出品方：{self.kwargs.get("history_publisher")}
            影视作品的导演：{self.kwargs.get("history_director")}
            影视作品的主演：{self.kwargs.get("history_stars")}
            影视作品的首映时间：{self.kwargs.get("history_first_play_time")}
            """)


if __name__ == "__main__":
    f_path = r"static\jsons\history\his_zgzywyh_zywj_xl.json"
    data = load_data_from_json_file(f_path)
    print("Data loaded from JSON file:", data)  # 添加这行打印语句来检查加载的数据
    if data:
        history = History(**data[0])
        history.show_info()
        print(history.get_description())
    else:
        print("No data loaded from JSON file.")
