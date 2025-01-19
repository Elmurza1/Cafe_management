# Cafe Management System

##  Описание проекта
Cafe Management System — это веб-приложение для управления кафе, позволяющее работать со столами, заказами, блюдами и сменами.

##  Функциональность
- Управление столами (создание, удаление)
- Создание и редактирование заказов
- Добавление и удаление блюд
- Управление сменами (открытие и закрытие)
- Подсчёт общей выручки за смену
- Автоматические тесты для проверки основных функций

## 🛠 Используемые технологии
- **Backend:** Python, Django, Django ORM
- **Database:** SQLite
- **Frontend:** HTML, CSS
- **Тестирование:** Django `TestCase`

---

## ⚙️ Установка и запуск
### 1️⃣ Клонирование репозитория
```sh
git clone <ссылка-на-репозиторий>
```

### 2️⃣ Создание виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate   
```

### 3️⃣ Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4️⃣ Применение миграций
```sh
python manage.py migrate
```

### 5️⃣ Создание суперпользователя
```sh
python manage.py createsuperuser
```

### 6️⃣ Запуск сервера
```sh
python manage.py runserver
```
Теперь проект доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Тестирование
Чтобы запустить тесты, используй команду:
```sh
python manage.py test 
```

---

## 📩 Контакты
Автор: **Элмырза**  
Email: **elmyrza217@gmail.com**  
GitHub: (https://github.com/Elmyrza1)

---



