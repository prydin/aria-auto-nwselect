FROM photon:3.0-20200609

ADD src/main/scripts /scripts

RUN chmod +x /scripts/*.sh && \
    tdnf install -y python3-pip.noarch python3-devel gcc glibc-devel binutils linux-api-headers shadow && \
    pip3 install --upgrade pip setuptools && \
    pip3 install certifi

CMD /scripts/resolve_dependencies.sh && \
    echo Collecting-dependencies-complete
