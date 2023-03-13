#!/bin/bash
#
# run.sh
#

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit
fi

set -o errexit
set -o nounset
set -o pipefail

export COMNETSEMU_AUTOTEST_MODE=1

PYTHON="python3"

run_dimanic_router() {
        
    if [[ "$(docker images -q dinamic_router:latest 2>/dev/null)" == "" ]]; then
        bash ./build_docker_images.sh
    fi


    sed -ri "s/hostname .+/hostname $HOSTNAME/" /etc/quagga/zebra.conf
    sed -ri "s/hostname .+/hostname $HOSTNAME/" /etc/quagga/ripd.conf
    sed -ri "s/hostname .+/hostname $HOSTNAME/" /etc/quagga/ospfd.conf
    sed -ri "s/hostname .+/hostname $HOSTNAME/" /etc/quagga/vtysh.conf

    echo "- Run ./rip_router."
    #Edit which routing protocols are to run
    echo 'zebra=yes' >> /etc/quagga/daemons
    echo 'bgpd=no' >> /etc/quagga/daemons
    echo 'ospfd=no' >> /etc/quagga/daemons
    echo 'ospf6d=no' >> /etc/quagga/daemons
    echo 'ripd=yes' >> /etc/quagga/daemons
    echo 'ripngd=no' >> /etc/quagga/daemons
    echo 'isisd=no' >> /etc/quagga/daemons
    echo 'babeld=no' >> /etc/quagga/daemons
    $PYTHON ./rip_router.py

    echo "- Run ./ospf_router."
    # Edit which routing protocols are to run
    echo 'ospfd=yes' >> /etc/quagga/daemons
    echo 'ripd=no' >> /etc/quagga/daemons
    $PYTHON ./ospf_router.py
}

if [[ "$#" -eq 0 ]]; then
    run_dimanic_router
else
    echo "ERROR: Unknown option."
    usage
fi

export COMNETSEMU_AUTOTEST_MODE=0