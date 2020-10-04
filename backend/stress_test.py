import subprocess, time, _thread, argparse

proc = None

ROOT_PATH = '/home/ubuntu/headless'

def test(id):
    print(f'GAMA No.{id} Started')
    time_start=time.time()
    proc = subprocess.Popen(f'bash {ROOT_PATH}/gama-headless.sh {ROOT_PATH}/CSS2020.xml {ROOT_PATH}/CSS2020', shell=True, stdout=subprocess.PIPE)
    while proc.poll() is None:
        pass
    time_end=time.time()
    print(f'GAMA No.{id} time cost: ',time_end-time_start,'s')

parser = argparse.ArgumentParser()
parser.add_argument('threads', type=int, help='number of threads', default=2)
args = parser.parse_args()

for i in range(args.threads):
    _thread.start_new_thread(test, (i+1,))

while 1:
    pass
