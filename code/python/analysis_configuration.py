KILOBYTE = 1024

DOMINANT_RATE = 0.8

EARLIEST_ANALYZED_YEAR = 2014
GITHUB_START_YEAR = 2008

lang_name = ['C++', 'C#', 'Java', 'JavaScript', 'PHP', 'Python', 'Shell']
lang_extension = {'C++': '.cpp'
    , 'C#': '.cs'
    , 'Java': '.java'
    , 'JavaScript': '.js'
    , 'PHP': '.php'
    , 'Python': '.py'
    , 'Shell': '.sh'}

language_extensions = list(lang_extension.values())

def lang_by_extension(extension):
    return list(lang_extension.keys())[list(lang_extension.values()).index(extension)]
