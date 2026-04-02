FROM inseefrlab/onyxia-python-pytorch:py3.12.6

ENV TIMEOUT=3600

ENV PROJ_LIB=/opt/conda/share/proj

# set api as the current work dir
WORKDIR /api

# copy the requirements list
COPY requirements_app.txt requirements_app.txt

# install all the requirements
RUN conda install -c conda-forge gdal=3.9.3 -y &&\
    pip install --no-cache-dir --upgrade -r requirements_app.txt &&\
    wget -q -O /api/nuts_2021.gpkg https://minio.lab.sspcloud.fr/projet-hackathon-ntts-2025/NUTS_RG_01M_2021_4326_LEVL_3.gpkg

# copy the main code of fastapi
COPY ./app /api/app

# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "app.main:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "3600"]