from __future__ import print_function
import lung_to_patches
from lung_to_patches import setupDirectories as setup
import sys
import zerorpc

class PythonApi(object):
    def echo(self, text):
        return text
    def dirSetup(self, text, ml_alg):
        try:
            return setup(text, ml_alg)
        except Exception as e:
            return e

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
