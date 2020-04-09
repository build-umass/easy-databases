#!/usr/bin/env python3
from shutil import which
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--volume=', action='store', dest='volume', help='The Docker volume should be bound to', default=None)
parser.add_argument('-n', '--name=', action='store', dest='name', help='The name of the Docker container', default=None)
parser.add_argument('-i', '--image=', action='store', dest='image', help='The image for instantiating the Docker container.', default=None)
subparsers = parser.add_subparsers(dest = 'sub')
build = subparsers.add_parser('build')
selection = ['mongo','postgres']
build.add_argument('build_choice', choices=selection, help='Building the image')
start = subparsers.add_parser('start')
start.add_argument('start_choice', choices=selection, help='Start the container')
stop = subparsers.add_parser('stop')
stop.add_argument('stop_choice', choices=selection, help='Stop the container')
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

def build_image(image_tag, location):
  print(f"Building image with tag: {image_tag}")
  if args.name:
    print("Warning: irrelevant flag -n/--name")
  if args.volume:
    print("Warning: irrevlant flag -v/--volume")
  if args.image:
    print("warning: irrelevant flag -i/--image")
  cmd = f"docker build -t {image_tag} ./{location}"
  easy_exec(cmd)

def start(name, volume, image, volume_location, port_binding):
  if args.name is None:
    args.name = name
  if args.volume is None:
    args.volume = volume
  if args.image is None:
    args.image = image
  print(f"Starting docker container with volume: {args.volume} and name: {args.name}")
  cmd = f"docker run --rm --volume {args.volume}:{volume_location} -d --name {args.name} -p {port_binding} --ip localhost {args.image}"
  easy_exec(cmd)

def stop(name):
  if args.name is None:
    args.name = name
  print(f"Stopping docker container with name {args.name}")
  if args.volume:
    print("Warning: irrelevant flag -v/--volume")
  if args.image:
    print("Warning: irrelevant flag -i/--image")
  cmd = f"docker stop {args.name}"
  easy_exec(cmd)

if args.sub == 'build':
  if args.build_choice == 'mongo':
    build_image("mongo-image", "mongo")
  elif args.build_choice == 'postgres':
    build_image("postgres-image", "postgres")    
elif args.sub == 'start':
  if args.start_choice == 'mongo':
    start("mongo_docker", "mongo-volume", "mongo-image:latest", "/data/db", "27017:27017")
  elif args.start_choice == 'postgres':
    start("pg_docker", "PGDATA", "postgres-image:latest", "/var/lib/postgresql/data", "5432:5432")
elif args.sub == 'stop':
  if args.stop_choice == 'mongo':
    stop("mongo_docker")
  elif args.stop_choice == 'postgres':
    stop("pg_docker")