from utils.load_data import load_data_from_json_file


class Literature:
    def __init__(self, literature_id, literature_name, **kwargs):
        """..."""
        self.literature_id = literature_id
        self.literature_name = literature_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "literature_description" in self.kwargs.keys():
            return self.kwargs.get("literature_description")

    def show_info(self):
        print(f"""
              文学作品名称：{self.literature_name}
              文学作品出品方：{self.kwargs.get("literature_publisher")}
              文学作品作者：{self.kwargs.get("literature_author")}
              文学作品的出版时间：{self.kwargs.get("literature_date")}
              """)


if __name__ == "__main__":
    f_path = r"static\jsons\cz_literature.json"
    data = load_data_from_json_file(f_path)
    literature = Literature(**data[0])
    literature.show_info()
    print(literature.get_description())