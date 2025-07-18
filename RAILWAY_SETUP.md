# Настройка Railway для деплоя

## 🚂 Шаг 1: Определение URL бэкенд-сервиса

Ваш бэкенд должен быть задеплоен на Railway. URL будет выглядеть примерно так:
```
https://your-backend-production-xxxx.up.railway.app
```

## 🔧 Шаг 2: Настройка переменной окружения на Railway

### Для фронтенда:
1. Откройте ваш проект на Railway
2. Перейдите в сервис **FRONTEND**
3. Откройте вкладку **Variables**
4. Создайте новую переменную окружения:
   - **Имя переменной:** `NEXT_PUBLIC_API_URL`
   - **Значение:** `https://your-backend-production-xxxx.up.railway.app`
   
   ⚠️ **Важно:** URL должен включать `https://` и НЕ должен заканчиваться слешем

### Для бэкенда:
1. Убедитесь, что в сервисе **BACKEND** настроена переменная `PORT`
2. Если используете базу данных, настройте `DATABASE_URL`

## 📁 Шаг 3: Структура проекта

Код уже настроен для использования переменной окружения:

```typescript
// frontend/src/lib/api.ts
import { ProductVariantDetail, RegionInfo, ProductInfo } from '@/types';

// Используем переменную окружения с fallback для локальной разработки
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

## 🔄 Шаг 4: Деплой

1. Сделайте commit и push изменений:
   ```bash
   git add .
   git commit -m "feat: configure API URL environment variable"
   git push origin main
   ```

2. Railway автоматически подхватит изменения и запустит деплой

## 🧪 Шаг 5: Проверка

После деплоя проверьте:
1. Фронтенд загружается без ошибок
2. API запросы работают корректно
3. В логах нет ошибок 404 для API

## 🔍 Возможные проблемы и решения

### Проблема: "fetch failed" во время сборки
**Решение:** Убедитесь, что:
- Переменная `NEXT_PUBLIC_API_URL` правильно задана
- Бэкенд доступен по указанному URL
- URL не содержит лишних символов

### Проблема: CORS ошибки
**Решение:** Проверьте настройки CORS в бэкенде:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.railway.app",
        "https://*.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📋 Чек-лист для деплоя

- [ ] Бэкенд задеплоен и доступен
- [ ] В фронтенде настроена переменная `NEXT_PUBLIC_API_URL`
- [ ] Код закоммичен и запушен
- [ ] Деплой прошел успешно
- [ ] Сайт открывается и работает

## 📞 Контакты

При возникновении проблем:
- Проверьте логи в Railway
- Убедитесь, что все переменные окружения настроены правильно
- Проверьте, что API эндпоинты отвечают корректно 