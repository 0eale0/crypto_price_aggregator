# Team 3
## Cryptocurrency price aggregator


**Проблема, которую мы решаем:**

Большинство не знает, что такое криптовалюта и какие возможности она дает:
- Почему? Потому что относятся к этой сфере пренебрежительно.
- Почему? Потому что боятся.
- Почему? Потому что думают что все сложно.
- Почему? Потому что нет наглядного сайта, который все бы показывал, 
рассказывал (есть блин на самом деле, даже несколько).

**Целевая аудитория:**

Люди,интересующиеся инвестированием.

**Наше видение проекта:**

Приложение будет предствлять собой агрегатор показателей ведущих криптовалют (цену, изменение цены за 24ч, 7д,
капитализацию, объем торгов за 24ч).
Так же можно перейти на страницу конкретной валюты и прочитать более подробную информацию про нее.
А в своем аккаунте человек может создать свой список избранных монет, за которыми он может следить.

**Ссылка на Trello:**

https://trello.com/b/aTtXpuks/aggregator-of-cryptocurrency-prices

**Ссылка на макеты в Figma:**

https://www.figma.com/team_invite/redeem/orgamP0G9yQzTZrD01QPTm

**Local setup**
You can also install FastAPI app locally using Poetry(`pip install poetry` if you does not have Poetry).
- `cd team-3`
- `poetry config virtualenvs.in-project true` - create .venv in project directory
- `poetry shell` - creates and enters to Poetry virtual environment
- `poetry install` - installs all dependencies of FastAPI app (using `pyproject.toml` and `poetry.lock` files)