FROM airbyte/integration-base-singer:0.1.1

# Bash is installed for more convenient debugging.
RUN apt-get update && apt-get install -y bash gcc && rm -rf /var/lib/apt/lists/*

ENV CODE_PATH="./source-shopify-singer/source_shopify_singer"
ENV AIRBYTE_IMPL_MODULE="source_shopify_singer"
ENV AIRBYTE_IMPL_PATH="SourceShopifySinger"

WORKDIR /airbyte/integration_code
COPY . ./
COPY $CODE_PATH ./$CODE_PATH
RUN pip install .
RUN pip install source-shopify-singer/.

LABEL io.airbyte.version=0.2.3
LABEL io.airbyte.name=airbyte/source-shopify-singer
