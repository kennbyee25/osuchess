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


class HitObjects(CommaSeparatedSection):
    '''
    # TODO include setup of hit object i.e. x, y, t, ... etc format
    # TODO handle '|' character
    # TODO add functionality to add hit object (note, slider, extras)
    # TODO create function (outside of beatmap) that converts a chess game to a set of coordinated or something
    # TODO create a function that converts a set of coordinates to a beatmap using add_object()
    '''
    def __init__(self):
        super().__init__()

    def add_object(self):


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
