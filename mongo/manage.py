#!/usr/bin/env python3
from shutil import which
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('choice', choices=['start', 'stop'], help='Start or stop the MongoDB container')
parser.add_argument('-v', '--volume=', action='store', dest='volume', help='The Docker volume /data/db should be bound to', default=None)
parser.add_argument('-n', '--name=', action='store', dest='name', help='The name of the Docker container', default=None)
parser.add_argument('-i', '--image=', action='store', dest='image', help='The image for instantiating the Docker container.', default=None)

args = parser.parse_args()

if which('docker') is None:
    print('ERROR: Could not find "docker" on your path.')
    exit(1)

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

if args.name is None:
    args.name = "mongo_docker"

if args.choice == 'start':
    if args.volume is None:
        args.volume = "mongo-volume"
    if args.image is None:
        args.image = "ayzlex/easy-umass-mongo"
    print(f"Starting docker container with volume: {args.volume} and name: {args.name}")
    cmd = f"docker run --rm --volume {args.volume}:/data/db -d --name {args.name} -p 27017:27017 --ip localhost {args.image}"
    easy_exec(cmd)
else:
    print(f"Stopping docker container with name {args.name}")
    if args.volume:
        print("Warning: irrelevant flag -v/--volume")
    if args.image:
        print("Warning: irrelevant flag -i/--image")
    cmd = f"docker stop {args.name}"
    easy_exec(cmd)