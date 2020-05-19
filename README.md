# News clustering backend

## Необходимный инструментарий для установки

- Python 3.7+
- [Poetry](https://python-poetry.org/)
- PostgreSQL 11+

## Инструкция по установке и запуску

1. `poetry install`
2. Скачать [датасеты](https://drive.google.com/open?id=1n6C660SAq63hPeZ7sSdPoPNSFT6Q8HJo) и распаковать их в `news_clustering/datasets/`
3. Скачать [модель](http://files.deeppavlov.ai/embeddings/ft_native_300_ru_wiki_lenta_lower_case/ft_native_300_ru_wiki_lenta_lower_case.bin) и положить её в `news_clustering/embeddings/`
4.  В корне скопировать `.env.example` в `.env` и сконфигурировать проект
5. `poetry run python manage.py migrate`
6. `poetry run python manage.py runserver`
