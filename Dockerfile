FROM hypriot/rpi-alpine

# Update
RUN apk add --update python py-pip

COPY templates /templates
COPY static /static
COPY mv.py /mv.py
COPY requirements.txt /requirements.txt
# Install app dependencies
RUN pip install -r /requirements.txt
ENV MVG_CHECKER '["marienplatz", "karlsplatz"]'

EXPOSE  5000
CMD ["python", "/mv.py"]
