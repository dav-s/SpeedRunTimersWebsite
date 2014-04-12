
class Run(object):

    def __init__(self, name, segments=None):
        self.name = name
        self.segments = segments


class SegmentList(object):

    def __init__(self):
        self.segments = None

    def __init__(self, *segments):
        self.segments = list(segments)

    def add_segment(self, segment):
        self.segments.append(segment)


class Trial(object):

    def __init__(self):
        pass


class Segment(object):

    def __init__(self, name):
        pass