from utils.load_data import load_data_from_json_file


class Battle:
    def __init__(self, battle_id, battle_name, **kwargs):
        self.battle_id = battle_id
        self.battle_name = battle_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "battle_description" in self.kwargs.keys():
            return self.kwargs.get("battle_description")

    def show_info(self):
        print(f"""
            影视作品名称：{self.battle_name}
            影视作品出品方：{self.kwargs.get("battle_site")}
            影视作品的导演：{self.kwargs.get("battle_date")}
            影视作品的主演：{self.kwargs.get("battle_references")}
            影视作品的首映时间：{self.kwargs.get("battle_ending")}
            """)


if __name__ == "__main__":
    f_path = r"static\jsons\battle\bat_gangchengbaoweizhan.json"
    data = load_data_from_json_file(f_path)
    battle = Battle(**data[0])
    battle.show_info()
    print(battle.get_description())
