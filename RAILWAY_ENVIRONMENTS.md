# Railway Environments Setup Guide

## 3. **Переменные окружения для каждого environment**

### 🔴 **Production Variables**
```bash
# Backend
DATABASE_URL=postgresql://postgres:ZFbbYebbkRrtFpRDQTyRwnVotKdAHLUE@shinkansen.proxy.rlwy.net:15068/railway
API_ENV=production
DEBUG=false
CORS_ORIGINS=https://myapp-prod.railway.app

# Frontend
NEXT_PUBLIC_API_URL=https://frontend-production-8178.up.railway.app
NEXT_PUBLIC_WS_URL=wss://backend-production-7dfe.up.railway.app/ws/updates
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_GA_ID=GA-PRODUCTION-ID
```

### 🟢 **Development Variables**
```bash
# Backend
DATABASE_URL=postgresql://dev_user:dev_pass@dev_host:5432/dev_db
API_ENV=development
DEBUG=true
CORS_ORIGINS=https://backend-dev-962f.up.railway.app,http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=https://frontend-dev-7b28.up.railway.app
NEXT_PUBLIC_WS_URL=wss://backend-dev-962f.up.railway.app/ws/updates
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_GA_ID=GA-DEV-ID
```

## 4. **Workflow для разработки**

### 🔄 **Development → Production**

```bash
# 1. Разработка в develop
git checkout develop
git add .
git commit -m "feat: new feature"
git push origin develop

# 3. После успешного тестирования → production
git checkout main
git merge staging
git push origin main
```

## 5. **Автоматические деплои**

### Railway автоматически деплоит:
- `develop` → Development environment
- `main` → Production environment

## 6. **Настройка CORS для разных окружений**

Обновите `backend/main.py`:

```python
import os

# Получаем окружение
API_ENV = os.getenv("API_ENV", "development")

# Настройка CORS в зависимости от окружения
if API_ENV == "production":
    allowed_origins = [
        "backend-production-7dfe.up.railway.app",
    ]
else:  # development
    allowed_origins = [
        "http://localhost:3000",
        "https://backend-dev-962f.up.railway.app",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 7. **Мониторинг и логирование**

### Для каждого окружения:
```python
# backend/main.py
import logging

API_ENV = os.getenv("API_ENV", "development")

if API_ENV == "production":
    logging.basicConfig(level=logging.ERROR)
elif API_ENV == "staging":
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)
```

## 8. **Database Migrations**

### Для каждого окружения:
```bash
# В каждом Railway проекте установите:
ALEMBIC_CONFIG=alembic.ini
DATABASE_URL=<соответствующий URL>

# Миграции будут применяться автоматически при деплое
```

## 9. **Тестирование окружений**

### Checklist для каждого environment:
```bash
# ✅ Development
- [ ] Код работает локально
- [ ] API endpoints отвечают
- [ ] Database подключена
- [ ] Логи работают

# ✅ Staging  
- [ ] Все dev тесты пройдены
- [ ] Production-like данные
- [ ] Performance тесты
- [ ] Security проверки

# ✅ Production
- [ ] Staging полностью протестирован
- [ ] Backup создан
- [ ] Monitoring активен
- [ ] Rollback план готов
```

## 10. **Полезные команды Railway CLI**

```bash
# Переключение между проектами
railway link myapp-prod
railway link myapp-staging  
railway link myapp-dev

# Просмотр логов
railway logs

# Просмотр переменных
railway variables

# Управление сервисами
railway status
```

## 🎯 **Best Practices**

1. **Никогда не коммитьте прямо в main**
2. **Всегда тестируйте в staging перед production**
3. **Используйте feature branches для крупных изменений**
4. **Регулярно синхронизируйте окружения**
5. **Мониторьте производительность на каждом этапе**

## 🚨 **Важные замечания**

- Staging должен максимально соответствовать production
- Development может иметь отладочные функции
- Используйте разные базы данных для каждого окружения
- Регулярно обновляйте staging данными из production (без личных данных)