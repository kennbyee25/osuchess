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

class CommaSeparatedSection(Section):
    def __init__(self):
        super().__init__()
        self.sequence = []

    def parse_line(self, line):
        self.sequence.append(line.split(','))


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
    def __init__(self):
        super().__init__()


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

        self.parse_osu_file(filepath)

    def parse_osu_file(self, filepath):
        model_dict = {
            "General": self.general,
            "Editor": self.editor,
            "Metadata": self.metadata,
            "Difficulty": self.difficulty,
            "Events": self.events,
            "TimingPoints": self.timing_points,
            "Colours": self.colours,
            "HitObjects": self.hit_objects,
        }

        section = None
        with open(filepath, "r") as f:
            self.file_format = f.readline()
            for line in f:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith("//"):
                    if line_stripped[0] == '[' and line_stripped[-1] == ']':
                        section_title = line_stripped[1:-1]
                        section = model_dict[section_title]
                    else:
                        section.parse_line(line_stripped)

        return

    def write(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        # convert data to string format and write to file
        return