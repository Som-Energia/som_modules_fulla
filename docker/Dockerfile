FROM ubuntu:20.04 AS clones
MAINTAINER Som-Energia

# Install Git
RUN apt-get update
RUN apt-get install -y git

# Get token from params `docker build --build-arg GITHUB_TOKEN=your_token_here`
ARG GITHUB_TOKEN

# Work on src directory
RUN mkdir src
WORKDIR /src

# Private clones
RUN git clone --depth 1 https://"${GITHUB_TOKEN}"@github.com/Som-Energia/erp.git -b developer
RUN git clone --depth 1 https://"${GITHUB_TOKEN}"@github.com/Som-Energia/libFacturacioATR.git

# GISCE public clones
RUN git clone --depth 1 https://github.com/gisce/oorq.git -b api_v5
RUN git clone --depth 1 https://github.com/gisce/ooop.git -b xmlrpc_transaction
RUN git clone --depth 1 https://github.com/gisce/mongodb_backend.git -b gisce
RUN git clone --depth 1 https://github.com/gisce/poweremail.git -b v5_backport
RUN git clone --depth 1 https://github.com/gisce/poweremail_oorq.git -b master
RUN git clone --depth 1 https://github.com/gisce/poweremail-modules.git
RUN git clone --depth 1 https://github.com/gisce/gestionatr.git
RUN git clone --depth 1 https://github.com/gisce/aeroolib.git
RUN git clone --depth 1 https://github.com/gisce/sepa.git
RUN git clone --depth 1 https://github.com/gisce/switching.git
RUN git clone --depth 1 https://github.com/gisce/libComXML.git
RUN git clone --depth 1 https://github.com/gisce/sippers.git
RUN git clone --depth 1 https://github.com/gisce/qreu.git
RUN git clone --depth 1 https://github.com/gisce/enerdata.git
RUN git clone --depth 1 https://github.com/gisce/arquia.git
RUN git clone --depth 1 https://github.com/gisce/ooquery.git
RUN git clone --depth 1 https://github.com/gisce/spawn_oop.git
RUN git clone --depth 1 https://github.com/gisce/openerp-sentry.git -b v5_legacy
RUN git clone --depth 1 https://github.com/gisce/ir_attachment_mongodb.git
RUN git clone --depth 1 https://github.com/gisce/crm_poweremail.git
RUN git clone --depth 1 https://github.com/gisce/viafirma.git
RUN git clone --depth 1 https://github.com/gisce/tipoinstalacion.git
RUN git clone https://github.com/gisce/ws_transactions.git

# Som Energia public clones
RUN git clone --depth 1 https://github.com/Som-Energia/erppeek_wst.git -b ws_transaction
RUN git clone --depth 1 https://github.com/Som-Energia/empowering.git
RUN git clone --depth 1 https://github.com/Som-Energia/erp-empowering.git
RUN git clone --depth 1 https://github.com/Som-Energia/amoniak.git
RUN git clone --depth 1 https://github.com/Som-Energia/sermepa.git
RUN git clone --depth 1 https://github.com/Som-Energia/somenergia-utils.git
RUN git clone --depth 1 https://github.com/Som-Energia/nombres-a-lletres.git
RUN git clone --depth 1 https://github.com/Som-Energia/distri-remesa-parser.git
RUN git clone --depth 1 https://github.com/Som-Energia/giscedata_facturacio_indexada_som.git
RUN git clone --depth 1 https://github.com/Som-Energia/plantmeter.git -b plantmeter-1.7.3
RUN git clone --depth 1 https://github.com/totaler/facturae.git
RUN git clone https://github.com/Som-Energia/openerp_som_addons.git
RUN git clone https://github.com/Som-Energia/somenergia-generationkwh.git
RUN git clone https://github.com/Som-Energia/som_modules_fulla.git

FROM python:2.7-slim

# Create virtualenv
RUN pip install virtualenv
RUN virtualenv erp

# Avoid apt-get interaction
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install packages
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends libxslt1-dev python-dev libxml2-dev \
    libxmlsec1-dev  zlib1g-dev libjpeg-dev libffi-dev  gcc g++ git fontconfig \
    fontconfig-config fonts-dejavu-core libfontconfig1 libxrender1 x11-common \
    xfonts-75dpi xfonts-base xfonts-encodings xfonts-utils libpq-dev pkg-config \
    libxmlsec1-openssl git openssh-server libpython2.7 libpq5 curl

# Copy clones
COPY --from=clones /src /src
RUN ln -s /src/poweremail /src/poweremail2
RUN ln -s /src/libFacturacioATR /src/libfacturacioatr

# Pip installs
COPY requirements.txt requirements.txt
RUN /erp/bin/pip install -r requirements.txt
RUN /erp/bin/pip install -r /src/erp/requirements.txt
RUN /erp/bin/pip install -r /src/erp/requirements-dev.txt

RUN (cd /src/somenergia-generationkwh; /erp/bin/pip install -e .)
RUN (cd /src/aeroolib/aeroolib; /erp/bin/pip install -e .)
RUN (cd /src/sepa; /erp/bin/pip install -e .)
RUN (cd /src/libFacturacioATR; /erp/bin/pip install -e .)
RUN (cd /src/switching; /erp/bin/pip install -e .)
RUN (cd /src/libComXML; /erp/bin/pip install -e .)
RUN (cd /src/sippers; /erp/bin/pip install -e .)
RUN (cd /src/qreu; /erp/bin/pip install -e .)
RUN (cd /src/enerdata; /erp/bin/pip install -e .)
RUN (cd /src/arquia; /erp/bin/pip install -e .)
RUN (cd /src/ooop; /erp/bin/pip install -e .)
RUN (cd /src/ooquery; /erp/bin/pip install -e .)
RUN (cd /src/gestionatr; /erp/bin/pip install -e .)
RUN (cd /src/sermepa; /erp/bin/pip install -e .)
RUN (cd /src/amoniak; /erp/bin/pip install -e .)
RUN (cd /src/distri-remesa-parser; /erp/bin/pip install -e .)
RUN (cd /src/plantmeter; /erp/bin/pip install -e .)
RUN (cd /src/facturae; /erp/bin/pip install -e .)
RUN (cd /src/viafirma; /erp/bin/pip install -e .)
RUN (cd /src/tipoinstalacion; /erp/bin/pip install -e .)

# Container env vars
ENV ERP_DB_HOST=localhost
ENV ERP_DB_NAME=erp
ENV ERP_DB_USER=erp
ENV ERP_DB_PASSWORD=erp
ENV OPENERP_DB_HOST=postgres
ENV OPENERP_DB_NAME=destral_db
ENV OPENERP_DB_USER=erp
ENV OPENERP_DB_PASSWORD=erp
ENV OPENERP_PRICE_ACCURACY=6
ENV OPENERP_ROOT_PATH=/src/erp/server/bin
ENV OPENERP_ADDONS_PATH=/src/erp/server/bin/addons
ENV OPENERP_REDIS_URL=redis://redis:6379/0
ENV OPENERP_MONGODB_URI=mongodb://mongo
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8
ENV PYTHONPATH=$OPENERP_ROOT_PATH:$OPENERP_ADDONS_PATH:/src/erp/server/sitecustomize

COPY somenergia.conf /root/somenergia.conf
COPY entrypoint.sh /
RUN chmod 700 /entrypoint.sh


EXPOSE 8069 22

ENTRYPOINT [ "/entrypoint.sh" ]

