FROM debian

RUN mkdir -p molika/config && mkdir molika/script && mkdir molika/log && mkdir /var/run/sshd
RUN apt update && apt install -y pipx openssh-server
RUN pipx install wakeonlan


RUN echo 'root:admin' | chpasswd

COPY id_rsa.pub /root/.ssh/authorized_keys

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22

COPY Molika.py molika/
COPY Task.py molika/
COPY setup.sh molika/
COPY ./script/* molika/script
COPY ./config/conditions.py molika/
COPY ./config/simi.txt molika/
COPY ./config/task.csv molika/

RUN chmod 777 molika/setup.sh
RUN echo "alias molika='python3 /molika/Molika.py'" >> /root/.bashrc

CMD ["/bin/bash", "-c", "/usr/sbin/sshd && /usr/bin/python3 /molika/Task.py && /molika/setup.sh"]