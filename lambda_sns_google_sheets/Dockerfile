FROM public.ecr.aws/lambda/python:3.8

WORKDIR /var/task

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt

# Copy module
COPY ./ .

# Overwrite the command by providing a different command directly in the template.
CMD ["app.handler"]