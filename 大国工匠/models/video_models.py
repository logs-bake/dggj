from utils.load_data import load_data_from_json_file


class Video:
    def __init__(self, video_id, video_name, **kwargs):
        self.video_id = video_id
        self.video_name = video_name
        self.kwargs = kwargs

    def get_description(self):
        if self.kwargs and "video_description" in self.kwargs.keys():
            return self.kwargs.get("video_description")

    def show_info(self):
        print(f"""
            影视作品名称：{self.video_name}
            影视作品出品方：{self.kwargs.get("video_publisher")}
            影视作品的导演：{self.kwargs.get("video_director")}
            影视作品的主演：{self.kwargs.get("video_stars")}
            影视作品的首映时间：{self.kwargs.get("video_first_play_time")}
            """)


if __name__ == "__main__":
    f_path = r"static\jsons\video\vid_changzheng_ds.json"
    data = load_data_from_json_file(f_path)
    video = Video(**data[0])
    video.show_info()
    print(video.get_description())
