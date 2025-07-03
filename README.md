# 1Base - Simple CMS with Storyblok

Простая CMS система с возможностью редактирования контента локально и через Storyblok.

## Возможности

- 🎨 **Локальная CMS** - Редактируйте текст прямо на странице
- 📝 **Storyblok интеграция** - Управляйте контентом через Storyblok панель
- 🔧 **21st.dev Toolbar** - AI-powered редактирование через браузер
- 🎯 **React + TypeScript** - Современный стек разработки
- 💾 **Автосохранение** - Изменения сохраняются автоматически
- 🔒 **HTTPS поддержка** - Для работы с Storyblok Visual Editor

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/Prezto5/1Base.git
cd 1Base

# Установить зависимости
pnpm install

# Создать .env файл
cp .env.example .env

# Настроить HTTPS (для Storyblok Visual Editor)
mkcert -install
mkcert localhost

# Запустить проект
pnpm dev
```

## Настройка Storyblok

1. Создайте аккаунт в [Storyblok](https://app.storyblok.com/)
2. Создайте новый Space
3. Получите API ключ
4. Добавьте его в `.env` файл:
```
VITE_STORYBLOK_ACCESS_TOKEN=ваш_api_ключ
```

## Использование

### Обычная разработка
```bash
pnpm dev
# Приложение доступно на http://localhost:5173
```

### Для работы с Storyblok Visual Editor
```bash
# Терминал 1: Запуск dev сервера
pnpm dev

# Терминал 2: Запуск HTTPS прокси
pnpm dev:https
```

**Теперь приложение доступно на:**
- HTTP: http://localhost:5173 (обычная разработка)
- HTTPS: https://localhost:3010 (для Storyblok)

### Настройка Preview URL в Storyblok
1. Перейдите в Settings → Visual Editor
2. Установите Preview URL: `https://localhost:3010/`
3. Теперь Visual Editor будет работать!

### Локальная CMS
- Наведите курсор на текст для появления кнопки редактирования
- Нажмите "Редактировать" для изменения контента
- Сохраните изменения - они автоматически сохраняются в localStorage

### Storyblok
- Перейдите в [Storyblok редактор](https://app.storyblok.com/)
- Редактируйте контент в Visual Editor
- Изменения отобразятся на сайте в реальном времени

### 21st.dev Toolbar
- Инструмент автоматически запускается в development режиме
- Выбирайте элементы на странице для AI-редактирования
- Работает только с установленным расширением VS Code

## Стек технологий

- **React 18** - UI библиотека
- **TypeScript** - Типизация
- **Vite** - Сборщик
- **Tailwind CSS** - Стилизация
- **shadcn/ui** - UI компоненты
- **Storyblok** - Headless CMS
- **21st.dev** - AI-powered editing
- **mkcert** - SSL сертификаты для разработки

## Команды

```bash
# Разработка
pnpm dev                    # HTTP на порту 5173

# Разработка с HTTPS (для Storyblok)
pnpm dev:https             # HTTPS прокси на порту 3010

# Сборка
pnpm build

# Превью сборки
pnpm preview

# Проверка типов
pnpm type-check
```

## Решение проблем

### "http:// is not allowed" в Storyblok
1. Убедитесь, что установлен mkcert: `brew install mkcert`
2. Создайте сертификаты: `mkcert localhost`
3. Запустите HTTPS прокси: `pnpm dev:https`
4. Используйте https://localhost:3010/ в Storyblok

### Проблемы с сертификатами
```bash
# Переустановка CA
mkcert -uninstall
mkcert -install

# Пересоздание сертификатов
rm localhost*.pem
mkcert localhost
```

## Деплой

Проект настроен для деплоя на:
- ✅ Vercel (с HTTPS по умолчанию)
- ✅ Netlify (с HTTPS по умолчанию)
- ✅ GitHub Pages

## Ссылки

- [Storyblok редактор](https://app.storyblok.com/#/edit/64979012523641?region=eu-central-1)
- [21st.dev расширение](https://marketplace.visualstudio.com/items?itemName=21st.21st-extension)
- [Документация Storyblok](https://www.storyblok.com/docs)
- [mkcert документация](https://github.com/FiloSottile/mkcert)
