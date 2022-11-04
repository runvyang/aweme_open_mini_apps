from public-cn-beijing.cr.volces.com/public/python:3.9.15

RUN mkdir -p /opt/application
WORKDIR /opt/application
COPY trade/ /opt/application
RUN pip install -r requirements.txt
RUN chmod +x run.sh

ENTRYPOINT ["/bin/bash", "/opt/application/run.sh"]
EXPOSE 8000
