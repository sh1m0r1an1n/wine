# 🍷 Генератор сайта винодельни из Excel-файла

---

### 🐍 **1. Установите Python**
[Скачайте Python](https://www.python.org/downloads/) → запустите установку →  
✅ Обязательно отметьте **Add Python to PATH**.

### ⚙️ **2. Добавьте Excel-файл с винами в папку, либо укажите свой путь к файлу**:
- Создайте файл `config.ini`
```ini
[DEFAULT]
path = путь/к/вашей/папке/wine.xlsx  # Путь к вашему Excel-файлу
```

### 📥 **3. Установите зависимости**
1. **Откройте командную строку**:
- На Windows: `Win + R` → введите `cmd` → нажмите **Enter**.
- На macOS/Linux: откройте **Terminal**.
2. **Перейдите в папку с проектом**:
```bash
cd путь/к/вашей/папке
```
3. **Выполните команду**:
```bash
pip install -r requirements.txt
```

### ▶️ **4. Запустите программу**
```bash
python main.py
python main.py --path <путь/к/файлу>
```
- По умолчанию: путь **wine.xlsx**.
- Чтобы изменить → отредактируйте `config.ini` ⚙️ или укажите свой `<путь/к/файлу>`.

Сайт можно увидеть, открыв файл `index.html` в этой же папке, либо по адресу `http://localhost:8000`.

---

## 📌 **Как это работает?**
1. Программа читает Excel-файл с винами
2. Формирует красивый HTML-сайт
3. Запускает локальный веб-сервер

---

## ⚠️ **Требования**
Файл Excel быть в таком формате:
```
| Категория   | Название   | Сорт      | Цена | Картинка    | Акция   |
|-------------|------------|-----------|------|-------------|---------|
| Красные     | Мерло      | Каберне   | 450  | merlo.png   | Скидка  |
```

## 📸 **Изображения**
Поместите картинки вин в папку `images/` в формате PNG/JPEG.  

---

## 📚 **Цель проекта**

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).