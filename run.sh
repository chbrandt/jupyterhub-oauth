#!/bin/bash
set -ue

usage () {
  echo "Usage: $0 {ultraauth|github}"
  exit
}

[[ $# -eq 1 ]] || usage

APP='app'
source "${APP}/${1}.env"
jupyterhub --config="${APP}/${1}_jupyter_config.py"
