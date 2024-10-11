from utils.load_data import load_data_from_json_file


class Memorial:
    def __init__(self, memorial_id, memorial_name, **kwargs):
        self.memorial_id = memorial_id
        self.memorial_name = memorial_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "memorial_description" in self.kwargs.keys():
            return self.kwargs.get("memorial_description")

    def show_info(self):
        print(f"""
            影视作品名称：{self.memorial_name}
          
            """)


if __name__ == "__main__":
    f_path = r"static\jsons\memorial\mem_dggjjng_bj.json"
    data = load_data_from_json_file(f_path)
    memorial = Memorial(**data[0])
    memorial.show_info()
    print(memorial.get_description())
