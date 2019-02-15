#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    CONDA_VER = 'MacOSX'
else
    CONDA_VER = 'Linux'
fi

# download conda
CONDA_URL = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-${CONDA_VER}-x86_64.sh'
wget ${CONDA_URL} -o miniconda.sh

# install conda
sh miniconda.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"

# update and configure conda
conda config --set always_yes yes --set changeps1 no
conda activate
conda update -q conda
conda info -a
which python

case "${TOXENV}" in
    py34)
        PY_VER = '3.4'
        ;;
    py35)
        PY_VER = '3.5'
        ;;
    py36)
        PY_VER = '3.6'
        ;;
esac

# create environment and install python
conda create -n ${TOXENV} python=${PY_VER} -q