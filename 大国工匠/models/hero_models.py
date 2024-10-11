from utils.load_data import load_data_from_json_file


class Hero:
    def __init__(self, hero_id, hero_name, **kwargs):
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "hero_description" in self.kwargs.keys():
            return self.kwargs.get("hero_description")

    def show_info(self):
        print(f"""
            影视作品名称：{self.hero_name}
            影视作品出品方：{self.kwargs.get("hero_publisher")}
            影视作品的导演：{self.kwargs.get("hero_director")}
            影视作品的主演：{self.kwargs.get("hero_stars")}
            影视作品的首映时间：{self.kwargs.get("hero_first_play_time")}
            """)


if __name__ == "__main__":
    f_path = r"static\jsons\hero\hero_guowenchang.json"
    data = load_data_from_json_file(f_path)
    hero = Hero(**data[0])
    hero.show_info()
    print(hero.get_description())
