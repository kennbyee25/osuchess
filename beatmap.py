from typing import List


class Section:
    def __init__(self):
        pass

    def parse_line(self, line):
        pass


class KeyValueSection(Section):
    def __init__(self):
        super().__init__()

    def parse_line(self, line):
        [key, value] = line.split(':')
        self.__setattr__(key.strip(), value.strip())

    def __str__(self):
        strout = ""
        for key, value in self.__dict__.items():
            strout += f"{key}:{value}\n"
        return strout


class CommaSeparatedSection(Section):
    def __init__(self):
        super().__init__()
        self.sequence = []

    def parse_line(self, line):
        self.sequence.append(line.split(','))

    def __str__(self):
        strout = ""
        for item in self.sequence:
            strout += f"{','.join(item)}\n"
        return strout


class General(KeyValueSection):
    def __init__(self):
        super().__init__()


class Editor(KeyValueSection):
    def __init__(self):
        super().__init__()


class Metadata(KeyValueSection):
    def __init__(self):
        super().__init__()


class Difficulty(KeyValueSection):
    def __init__(self):
        super().__init__()


class Events(CommaSeparatedSection):
    def __init__(self):
        super().__init__()


class TimingPoints(CommaSeparatedSection):
    def __init__(self):
        super().__init__()


class Colours(KeyValueSection):
    def __init__(self):
        super().__init__()


class ObjectParams():
    def __init__(self, seq_str):
        pass


class HitSample:
    normal_set: int = 0
    addition_set: int = 0
    index: int = 0
    volume: int = 0
    filename: str = ""
    """
    # Custom hit samples
    # Usage of hitSample can further customise the sounds that play. It defaults to 0:0:0:0: if it is not written.
    # 
    # Hit sample syntax: normalSet:additionSet:index:volume:filename
    # 
    # normalSet (Integer): Sample set of the normal sound.
    # additionSet (Integer): Sample set of the whistle, finish, and clap sounds.
    # index (Integer): Index of the sample. If this is 0, the timing point's sample index will be used instead.
    # volume (Integer): Volume of the sample from 1 to 100. If this is 0, the timing point's volume will be used instead.
    # filename (String): Custom filename of the addition sound.
    # normalSet and additionSet can be any of the following:
    # 
    # 0: No custom sample set
    # For normal sounds, the set is determined by the timing point's sample set.
    # For additions, the set is determined by the normal sound's sample set.
    # 1: Normal set
    # 2: Soft set
    # 3: Drum set
    # All of these options (besides volume) are used to determine which sound file to play for a given hitsound. The filename is <sampleSet>-hit<hitSound><index>.wav, where:
    # 
    # sampleSet is normal, soft, or drum, determined by either normalSet or additionSet depending on which hitsound is playing
    # hitSound is normal, whistle, finish, or clap
    # index is the same index as above, except it is not written if the value is 0 or 1
    # The sound file is loaded from the first of the following directories that contains a matching filename:
    # 
    # Beatmap, if index is not 0
    # Skin, with the index removed
    # Default osu! resources, with the index removed
    # When filename is given, no addition sounds will be played, and this file in the beatmap directory is played instead.
    """

    def __init__(self, seq_str):
        [self.normal_set, self.addition_set, self.index, self.volume, self.filename] = seq_str.split(':')

    def __str__(self):
        return ':'.join([self.normal_set, self.addition_set, self.index, self.volume, self.filename])


class HitObject:
    x: int
    y: int
    time: int
    type: int
    hit_sound: int
    object_params: ObjectParams
    hit_sample: HitSample
    """
    # x,y,time,type,hitSound,objectParams,hitSample
    # x (Integer) and y (Integer): Position in osu! pixels of the object.
    # time (Integer): Time when the object is to be hit, in milliseconds from the beginning of the beatmap's audio.
    # type (Integer): Bit flags indicating the type of the object. See the type section.
    # hitSound (Integer): Bit flags indicating the hitsound applied to the object. See the hitsounds section.
    # objectParams (Comma-separated list): Extra parameters specific to the object's type.
    # hitSample (Colon-separated list): Information about which samples are played when the object is hit. It is closely
    #   related to hitSound; see the hitsounds section. If it is not written, it defaults to 0:0:0:0:.
    # TODO implement a way to either isolate the HitSample from the end of the list or recognize object type
    #    e.g. check last item in list and check if it contains colons
    #    otherwise, 
    # TODO add functionality to add hit object (note, slider, extras)
    # TODO create function (outside of beatmap) that converts a chess game to a set of coordinated or something
    # TODO create a function that converts a set of coordinates to a beatmap using add_object()
    """

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                self.init_from_string(args[0])
        else:
            [self.x, self.y, self.time, self.type, self.hit_sound, self.object_params, self.hit_sample] = args

    def init_from_string(self, arg_str):
        arg_list = arg_str.split(',')

        [self.x, self.y, self.time, self.type, self.hit_sound] = [int(x) for x in arg_list[:5]]
        self.hit_sample = HitSample(self.sequence[-1])
        self.object_params = ObjectParams(self.sequence[5:-1])


class HitObjects(CommaSeparatedSection):
    sequence: List[HitObject]

    def __init__(self):
        super().__init__()
        self.process_sequence()

    # since the list can contain sub-lists, we need to process these after reading. Perhaps it would be good to create a
    # custom parse_line() function
    def process_sequence(self):
        for i, obj_str in enumerate(self.sequence):
            self.sequence[i] = HitObject(obj_str)

    def clear(self):
        self.sequence = []

    def add_object(self, *args):
        self.sequence.append(HitObject(args))


class Beatmap:
    file_format: str
    general: General
    editor: Editor
    metadata: Metadata
    difficulty: Difficulty
    events: Events
    timing_points: TimingPoints
    colours: Colours
    hit_objects: HitObjects

    def __init__(self, filepath):
        self.filepath = filepath
        self.file_format = ""

        self.general = General()
        self.editor = Editor()
        self.metadata = Metadata()
        self.difficulty = Difficulty()
        self.events = Events()
        self.timing_points = TimingPoints()
        self.colours = Colours()
        self.hit_objects = HitObjects()

        self.model_dict = {
            "General": self.general,
            "Editor": self.editor,
            "Metadata": self.metadata,
            "Difficulty": self.difficulty,
            "Events": self.events,
            "TimingPoints": self.timing_points,
            "Colours": self.colours,
            "HitObjects": self.hit_objects,
        }

        self.parse_osu_file(filepath)

    def parse_osu_file(self, filepath):
        section = None
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.file_format = lines[0]
            for line in lines[1:]:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith("//"):
                    if line_stripped[0] == '[' and line_stripped[-1] == ']':
                        section_title = line_stripped[1:-1]
                        section = self.model_dict[section_title]
                    else:
                        section.parse_line(line_stripped)
        return

    def write(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(self.file_format)
            for section_name, model in self.model_dict.items():
                f.write(f"\n[{section_name}]\n")
                f.write(model.__str__())
        return
