import sys
from mrjob.job import MRJob
from mrjob.protocol import ReprProtocol
import operator
import re

WORD_RE = re.compile(r"[A-Za-zА-Яа-я]+")


class MRWordFreqCount(MRJob):
    OUTPUT_PROTOCOL = ReprProtocol

    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, str(sum(counts))


if __name__ == '__main__':
    worker = MRWordFreqCount()
    worker.sandbox(open(sys.argv[1], 'rb'))

    result = dict()

    with worker.make_runner() as runner:
        runner.run()
        for key, value in worker.parse_output(runner.cat_output()):
            result[key] = value

        with open(sys.argv[2], 'w') as f:
            for item in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
                f.write(item[0] + " " + item[1] + "\n")

