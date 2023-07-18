FROM ubuntu:20.04

WORKDIR /workspace
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
COPY . /workspace/
ENTRYPOINT [ "/usr/sbin/sshd", "-D" ]
