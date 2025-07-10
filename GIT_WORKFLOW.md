# Git Workflow для Railway Dev/Staging/Production

## 🌳 Структура веток

```
main (Production)     ← Стабильные релизы
  ↑
staging (Staging)     ← Тестирование перед продакшн
  ↑
dev (Development)     ← Активная разработка
```

## 📋 Ваши ветки на GitHub

- ✅ `main` - Production (уже настроено на Railway)
- ✅ `dev` - Development (только что создано)
- ✅ `staging` - Staging (только что создано)

## 🔄 Workflow для разработки

### 1. **Работа с новыми функциями**

```bash
# Переключиться на dev ветку
git checkout dev

# Убедиться, что у вас последняя версия
git pull origin dev

# Внести изменения в код
# ... редактируете файлы ...

# Закоммитить изменения
git add .
git commit -m "feat: добавил новую функцию"

# Отправить в dev ветку
git push origin dev
```

### 2. **Тестирование в Staging**

```bash
# Переключиться на staging
git checkout staging

# Подтянуть изменения из dev
git merge dev

# Отправить в staging
git push origin staging
```

### 3. **Релиз в Production**

```bash
# Переключиться на main
git checkout main

# Подтянуть изменения из staging
git merge staging

# Отправить в production
git push origin main
```

## 🚂 Настройка Railway для каждой ветки

### Следующие шаги:

1. **Создать 3 проекта на Railway:**
   - `myapp-prod` → подключить к ветке `main`
   - `myapp-staging` → подключить к ветке `staging`
   - `myapp-dev` → подключить к ветке `dev`

2. **Настроить переменные окружения:**
   - Каждый проект должен иметь свои переменные
   - Разные базы данных для каждого окружения

## 🎯 Полезные команды

```bash
# Посмотреть все ветки
git branch -a

# Переключиться на ветку
git checkout <branch-name>

# Узнать текущую ветку
git branch

# Статус изменений
git status

# История коммитов
git log --oneline
```

## 🚨 Важные правила

1. **Никогда не пушьте прямо в main!**
2. **Всегда работайте в dev ветке**
3. **Тестируйте в staging перед production**
4. **Делайте частые коммиты с понятными сообщениями**

## 📱 Текущий статус

- 🟢 **Текущая ветка:** `dev` (готова для разработки)
- 🔗 **GitHub:** https://github.com/Prezto5/1Base
- 📁 **Ветки:** main, staging, dev

## 🎉 Готово к использованию!

Теперь вы можете:
1. Разрабатывать в `dev` ветке
2. Тестировать в `staging`
3. Деплоить в `production` (main)

Каждая ветка будет автоматически деплоиться на Railway при push!