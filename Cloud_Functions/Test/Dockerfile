FROM python:3.9.4-slim

# Set the working directory to /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install Flask
ADD test.py /app
ADD tag-build.sh /app/
RUN mkdir /app/static
RUN /app/tag-build.sh > /app/static/build.txt

RUN ls -R
RUN cat /app/static/build.txt

EXPOSE 5040

# Run app.py when the container launches
CMD ["python3", "test.py"]
