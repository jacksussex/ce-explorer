FROM python:3.9
#LABEL authors="Jack Pay"

ENV DASH_DEBUG_MODE True

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_trf

COPY assets/ /code/assets/

COPY components/sidebars/ /code/components/sidebars/
COPY components/solara_components/ /code/components/solara_components/
COPY components/views/ /code/components/views/

COPY data/example_data/ /code/data/example_data/

COPY pages/ /code/pages/

COPY tools/ /code/tools/

COPY english-stopwords.txt /code/english-stopwords.txt
COPY fields.py /code/fields.py

ENV PYTHONPATH="${PYTHONPATH}:/code"

EXPOSE 8080
CMD ["cd", "/code"]
CMD ["solara", "run", "./pages", "--host=0.0.0.0", "--port=8080"]