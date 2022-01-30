from beatmap import Beatmap

src_fp = r"C:\Users\Kenneth\AppData\Local\osu!\Songs\694119 Aimer - everlasting snow\Aimer - everlasting snow (Wafu) [Snow].osu"
dest_fp = r"C:\Users\Kenneth\AppData\Local\osu!\Songs\694119 Aimer - everlasting snow\testdiff.osu"

b = Beatmap(src_fp)
b.write(dest_fp)