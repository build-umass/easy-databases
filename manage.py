#!/usr/bin/env python3
from shutil import which
import argparse
import subprocess
from operator import xor

parser = argparse.ArgumentParser('Quickly start/stop a Postgres Docker container')
parser.add_argument('-s', '--start', action='store_true', help='Start the Postgres container', default=False)
parser.add_argument('-k', '--kill', action='store_true', help='Stop the Postgres container')
parser.add_argument('-v', '--volume=', action='store', dest='volume', help='The Docker volume /var/lib/postgresql/data should be bound to', default='PGDATA')
parser.add_argument('-n', '--name=', action='store', dest='name', help='The name of the Docker container', default='pg_docker')
parser.add_argument('-i', '--image=', action='store', dest='image', help='The image for instantiating the Docker container.', default='postgres-image:latest')

args = parser.parse_args()

if which('docker') is None:
    print('ERROR: Could not find "docker" on your path.')
    exit(1)

if not args.start and not args.kill:
    print('ERROR: Either one of -s, --start, -k, --kill must be specified')
    exit(1)

if args.start and args.kill:
    print('ERROR: Both a start flag(-s or --start) and kill flag (-k --kill) cannot be specified.')
    exit(1)

assert xor(args.start, args.kill)

msg_end = f"docker container with volume: {args.volume} and name: {args.name}"

def easy_exec(cmd):
    print("Running command: ", end="")
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("Output:")
    for line in p.stdout.readlines():
        print(line.decode('ascii'), end="")
    print("------")
    retval = p.wait()
    if retval != 0:
        print(f"Error executing command. The process returned {retval}.")
    return retval == 0

if args.start:
    print("Starting " + msg_end)
    cmd = f"docker run --rm --volume {args.volume}:/var/lib/postgresql/data -d --name {args.name} -p 5432:5432 --ip localhost {args.image}"
    easy_exec(cmd)
else:
    print("Stopping " + msg_end)
    if args.volume:
        print("Warnining: irrelevant flag -v/--volume")
    if args.image:
        print("Warnining: irrelevant flag -i/--image")
    cmd = f"docker stop {args.name}"
    easy_exec(cmd)