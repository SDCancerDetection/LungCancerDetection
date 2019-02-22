from __future__ import print_function
from segment_dicom import main as segment_dicom
import sys
import zerorpc

class PythonApi(object):
    def hello(self, text):
        try:
            return segment_dicom(text);
        except Exception as e:
            return 0.0
    def echo(self, text):
        return text

def parse_port():
    return 4242

def main():
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(PythonApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
