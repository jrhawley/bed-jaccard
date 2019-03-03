#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # download conda
    export URL='https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh'
elif [[ $TRAVIS_OS_NAME == 'linux' ]]; then
    # download conda
    export URL='https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh'
fi

# download and install conda
curl -o miniconda.sh $URL
sh miniconda.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"

# update and configure conda
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# get python version from current environment
export PY_VER=$(which python 2>&1 >/dev/null | cut -f 2 -d ' ' | cut -f 1-2 -d '.')
echo $PY_VER

# create conda environment to build
conda activate
conda install python=${PY_VER} conda-build anaconda-client

# pre-configure for auto upload to conda channel
conda config --set anaconda_upload yes

# build recipe
conda build --python ${PY_VER} --token ${ANACONDA_UPLOAD_TOKEN} .travis/meta.yaml
