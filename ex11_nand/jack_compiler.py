
import sys
from CompiliationEngine import *

class JackCompiler:
    directory = ''

    def __init__(self,directory):
        self.directory = directory
        if (os.path.isfile(self.directory)):  # if it's a file
            tokenizer = JackTokenizer(self.directory)
            CompiliationEngine(tokenizer, self.directory)

        else:
            for filename in os.listdir(directory):  # if it's a folder
                if filename.endswith(".jack"):
                    tokenizer = JackTokenizer(self.directory + '/' + filename)
                    CompiliationEngine(tokenizer, self.directory + '/' + filename)


if __name__ == '__main__':
    directory = sys.argv[1]
    JackCompiler(directory)
