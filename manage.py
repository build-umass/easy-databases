#!/usr/bin/env python3
from shutil import which
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--volume=', action='store', dest='volume', help='The Docker volume should be bound to', default=None)
parser.add_argument('-n', '--name=', action='store', dest='name', help='The name of the Docker container', default=None)
parser.add_argument('-i', '--image=', action='store', dest='image', help='The image for instantiating the Docker container.', default=None)
parser.add_argument('-p', '--publish=', action='store', dest='publish', help='Publish a container\'s ports or range of ports to host.', default=None)
subparsers = parser.add_subparsers(dest = 'sub')
build = subparsers.add_parser('build')
selection = ['mongo','postgres']
build.add_argument('build_choice', choices=selection, help='Building the image')
start = subparsers.add_parser('start')
start.add_argument('start_choice', choices=selection, help='Start the container')
stop = subparsers.add_parser('stop')
stop.add_argument('stop_choice', choices=selection, help='Stop the container')
args = parser.parse_args()
print(args)

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

def build_image(location):
  image_tag = f"buildumass/easy-{location}:latest"
  print(f"Building image with tag: {image_tag}")
  if args.name:
    print("Warning: irrelevant flag -n/--name")
  if args.volume:
    print("Warning: irrevlant flag -v/--volume")
  if args.image:
    print("warning: irrelevant flag -i/--image")
  cmd = f"docker build -t {image_tag} ./{location}"
  easy_exec(cmd)

def start(choice):
  if args.name is None:
    args.name = f"{choice}_docker"
  if args.volume is None:
    args.volume = f"{choice}_volume"
  if args.image is None:
    args.image = f"buildumass/easy-{choice}:latest"
  if args.publish is None:
    args.publish = "27017:27017" if choice is "mongo" else "5432:5432"
  volume_location_in_container = "/data/db" if choice is "mongo" else "/var/lib/postgresql/data"
  print(f"Starting docker container with volume: {args.volume} and name: {args.name}")
  cmd = f"docker run --rm --volume {args.volume}:{volume_location_in_container} -d --name {args.name} -p {args.publish} --ip localhost {args.image}"
  easy_exec(cmd)

def stop(choice):
  if args.name is None:
    args.name = f"{choice}_docker"
  print(f"Stopping docker container with name {args.name}")
  if args.volume:
    print("Warning: irrelevant flag -v/--volume")
  if args.image:
    print("Warning: irrelevant flag -i/--image")
  cmd = f"docker stop {args.name}"
  easy_exec(cmd)

if args.sub == 'build':
  build_image(args.build_choice)
elif args.sub == 'start':
  start(args.start_choice)
elif args.sub == 'stop':
  stop(args.stop_choice)