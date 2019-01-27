class Video(object):

    def __init__(self, identifier, size):
        self.identifier = identifier
        self.size = size

    def __repr__(self):
        return '{name}({args})'.format(
            name=self.__class__.__name__,
            args=', '.join([
                'identifier={}'.format(self.identifier),
                'size={}'.format(self.size),
            ])
        )
      
