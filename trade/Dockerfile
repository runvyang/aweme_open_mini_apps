from python:3.9.15

RUN echo $HOME
RUN mkdir -p $HOME/apps/trade
WORKDIR $HOME/apps/trade
COPY src ./
RUN pip install -r requirements.txt
CMD ["./run.sh"]
