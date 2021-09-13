# first stage
FROM python:3.8 AS builder

# install dependencies to the local user directory (eg. /root/.local)
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.8-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./consumer.py .

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

CMD [ "./consumer.py" ]
