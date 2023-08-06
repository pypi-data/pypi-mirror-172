from io import open

from setuptools import find_packages, setup


def read(filename):
   """Прочитаем наш README.md для того, чтобы установить большое описание."""
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(
    name="lit_lib",
    version="1.0-alpha", # Версия твоего проекта. ВАЖНО: менять при каждом релизе
    description="Короткое описание твоего проекта на PyPi",
    long_description=read("README.md"), # Здесь можно прописать README файл с длинным описанием
    long_description_content_type="text/markdown", # Тип контента, в нашем случае text/markdown
    author="Ilya G",
    author_email="phone.mas@yandex.ru",
    url="https://github.com/DiorDS/lit_lib", # Страница проекта
    keywords="localisation lit translate", # Ключевые слова для упрощеннего поиска пакета на PyPi
    packages=find_packages(), # Ищем пакеты, или можно передать название списком: ["package_name"]
    requires=["deep_translator"]
)