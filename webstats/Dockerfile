FROM python:3.6

# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/flask/app/webstats
WORKDIR /home/flask/app/webstats

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)

COPY requirements.txt /home/flask/app/webstats
RUN pip install --no-cache-dir -r requirements.txt


# Copy the source code into the container
COPY . /home/flask/app/webstats

RUN chown -R flask:flaskgroup /home/flask

USER flask

WORKDIR /home/flask/app/webstats

CMD [ "/usr/local/bin/gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "webstats:app" ]
