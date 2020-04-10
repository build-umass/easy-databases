#!/usr/bin/env python3
from shutil import which
import argparse
import subprocess

def add_flags(parser, *flags):
  if 'volume' in flags:
    parser.add_argument('-v', '--volume', action='store', dest='volume', help='The Docker volume should be bound to', default=None)
  if 'image' in flags:
    parser.add_argument('-i', '--image', action='store', dest='image', help='The image for instantiating the Docker container.', default=None)
  if 'name' in flags:
    parser.add_argument('-n', '--name', action='store', dest='name', help='The name of the Docker container', default=None)
  if 'port' in flags:
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port on the host machine which is mapped to the database port inside the container.', default=None)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest = 'command')
selection = ['mongo','postgres']

build = subparsers.add_parser('build')
build.add_argument('build_choice', choices=selection, help='Which image to build')

start = subparsers.add_parser('start')
start.add_argument('start_choice', choices=selection, help='Which container to start')
add_flags(start, 'volume', 'image', 'name', 'port')

stop = subparsers.add_parser('stop')
stop.add_argument('stop_choice', choices=selection, help='Which container to stop')
add_flags(stop, 'name')

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

def build_image(location):
  image_tag = f"buildumass/easy-{location}:latest"
  print(f"Building image with tag: {image_tag}")
  cmd = f"docker build -t {image_tag} ./{location}"
  easy_exec(cmd)

def start(choice):
  if args.name is None:
    args.name = f"{choice}_docker"
  if args.volume is None:
    args.volume = f"{choice}_volume"
  if args.image is None:
    args.image = f"buildumass/easy-{choice}:latest"
  is_mongo = choice == "mongo"
  # https://docs.docker.com/engine/reference/run/#expose-incoming-ports
  container_port = "27017" if is_mongo else "5432"
  if args.port is None:
    args.port = "27017" if is_mongo else "5432"
  port_binding = f"{args.port}:{container_port}"
  volume_location_in_container = "/data/db" if choice == "mongo" else "/var/lib/postgresql/data"
  print(f"Starting docker container with volume: {args.volume} and name: {args.name}")
  cmd = f"docker run --rm --volume {args.volume}:{volume_location_in_container} -d --name {args.name} --publish {port_binding} --ip localhost {args.image}"
  easy_exec(cmd)

def stop(choice):
  if args.name is None:
    args.name = f"{choice}_docker"
  print(f"Stopping docker container with name {args.name}")
  cmd = f"docker stop {args.name}"
  easy_exec(cmd)

if args.command == 'build':
  build_image(args.build_choice)
elif args.command == 'start':
  start(args.start_choice)
elif args.command == 'stop':
  stop(args.stop_choice)