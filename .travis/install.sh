#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # download conda
    curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    
    # diagnose conda download issues
    wc -l miniconda.sh
    head -n 100 miniconda.sh
    tail -n 100 miniconda.sh
    echo ""
    echo "Conda file check works out"

    # install conda
    # chmod +x miniconda.sh
    sh miniconda.sh -b -p $HOME/miniconda3
    export PATH="$HOME/miniconda3/bin:$PATH"

    # update and configure conda
    conda config --set always_yes yes --set changeps1 no
    conda update -q conda
    conda info -a
    which python

    case "${TOXENV}" in
        py35)
            export PY_VER="3.5"
            ;;
        py36)
            export PY_VER="3.6"
            ;;
    esac

    # create environment and install python
    conda create -n ${TOXENV} python=${PY_VER} -q
    conda activate ${TOXENV}
fi

python setup.py install
