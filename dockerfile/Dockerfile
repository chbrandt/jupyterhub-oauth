FROM continuumio/miniconda3

RUN conda install -y -c conda-forge jupyterhub &&\
    conda install -y notebook

RUN pip install oauthenticator

RUN useradd -m -d /home/user user &&\
    echo "user:123456" | chpasswd
