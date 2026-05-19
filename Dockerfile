FROM inseefrlab/onyxia-python-pytorch:py3.13.12-gpu

ENV TIMEOUT=3600
ENV PROJ_LIB=/opt/conda/share/proj
ENV PATH="/api/.venv/bin:$PATH"

# set api as the current work dir
WORKDIR /api

# copy uv
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# install
RUN uv sync --frozen

# copy the main code of fastapi
COPY ./app /api/app

# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "3600"]