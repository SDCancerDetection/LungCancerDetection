from __future__ import print_function
from greenlet import greenlet
import segment_dicom
from segment_dicom import evaluate as eval
import sys
import zerorpc

class PythonApi(object):
    def hello(self, text):
        try:
            return eval(text)
        except Exception as e:
            return e
    def echo(self, text):
        return text

def parse_port():
    return 4242

def main():
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(PythonApi(), heartbeat=None)
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
