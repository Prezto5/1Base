# Railway Environments Setup Guide

## 🏗️ Архитектура окружений

```
Production (main)     ← Stable releases
     ↑
Staging (staging)     ← Testing before production  
     ↑
Development (develop) ← Active development
```

## 1. **Создание Git веток**

```bash
# Создаем ветку для разработки
git checkout -b develop

# Создаем ветку для staging
git checkout -b staging

# Возвращаемся в main
git checkout main

# Пушим новые ветки
git push -u origin develop
git push -u origin staging
```

## 2. **Настройка Railway Projects**

### A. **Production Environment**
```yaml
Project Name: myapp-prod
Branch: main
Services:
  - Backend (FastAPI)
  - Frontend (Next.js)
  - Database (PostgreSQL)
```

### B. **Staging Environment**
```yaml
Project Name: myapp-staging
Branch: staging
Services:
  - Backend (FastAPI)
  - Frontend (Next.js)
  - Database (PostgreSQL)
```

### C. **Development Environment**
```yaml
Project Name: myapp-dev
Branch: develop
Services:
  - Backend (FastAPI)
  - Frontend (Next.js)
  - Database (PostgreSQL)
```

## 3. **Переменные окружения для каждого environment**

### 🔴 **Production Variables**
```bash
# Backend
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/prod_db
API_ENV=production
DEBUG=false
CORS_ORIGINS=https://myapp-prod.railway.app

# Frontend
NEXT_PUBLIC_API_URL=https://myapp-prod-backend.railway.app
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_GA_ID=GA-PRODUCTION-ID
```

### 🟡 **Staging Variables**
```bash
# Backend
DATABASE_URL=postgresql://staging_user:staging_pass@staging_host:5432/staging_db
API_ENV=staging
DEBUG=true
CORS_ORIGINS=https://myapp-staging.railway.app

# Frontend
NEXT_PUBLIC_API_URL=https://myapp-staging-backend.railway.app
NEXT_PUBLIC_ENV=staging
NEXT_PUBLIC_GA_ID=GA-STAGING-ID
```

### 🟢 **Development Variables**
```bash
# Backend
DATABASE_URL=postgresql://dev_user:dev_pass@dev_host:5432/dev_db
API_ENV=development
DEBUG=true
CORS_ORIGINS=https://myapp-dev.railway.app,http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=https://myapp-dev-backend.railway.app
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_GA_ID=GA-DEV-ID
```

## 4. **Workflow для разработки**

### 🔄 **Development → Staging → Production**

```bash
# 1. Разработка в develop
git checkout develop
git add .
git commit -m "feat: new feature"
git push origin develop

# 2. Merge в staging для тестирования
git checkout staging
git merge develop
git push origin staging

# 3. После успешного тестирования → production
git checkout main
git merge staging
git push origin main
```

## 5. **Автоматические деплои**

### Railway автоматически деплоит:
- `develop` → Development environment
- `staging` → Staging environment  
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
        "https://myapp-prod.railway.app",
    ]
elif API_ENV == "staging":
    allowed_origins = [
        "https://myapp-staging.railway.app",
    ]
else:  # development
    allowed_origins = [
        "http://localhost:3000",
        "https://myapp-dev.railway.app",
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