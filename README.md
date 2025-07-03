# 1Base - Storyblok Headless CMS

Простое приложение с интеграцией Storyblok для управления контентом через headless CMS.

## Возможности

- 📝 **Storyblok CMS** - Управляйте контентом через Storyblok панель
- 🔧 **21st.dev Toolbar** - AI-powered редактирование через браузер  
- 🎯 **React + TypeScript** - Современный стек разработки
- 🔒 **HTTPS поддержка** - Для работы с Storyblok Visual Editor
- ⚡ **Реальное время** - Изменения отображаются мгновенно

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
- HTTPS: https://localhost:3010 (для Storyblok Visual Editor)

### Настройка Preview URL в Storyblok
1. Перейдите в Settings → Visual Editor
2. Установите Preview URL: `https://localhost:3010/`
3. Теперь Visual Editor будет работать!

### Управление контентом
- Перейдите в [Storyblok редактор](https://app.storyblok.com/)
- Создайте и редактируйте контент в Visual Editor
- Изменения отобразятся на сайте в реальном времени
- Публикуйте изменения для production

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

### Контент не загружается
1. Проверьте API ключ в `.env` файле
2. Убедитесь, что контент опубликован в Storyblok
3. Проверьте консоль браузера на ошибки

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

### Настройка production
1. Обновите Preview URL в Storyblok на ваш production домен
2. Убедитесь, что переменные окружения настроены на хостинге
3. Настройте webhooks для автоматической перестройки

## Ссылки

- [Storyblok редактор](https://app.storyblok.com/#/edit/64979012523641?region=eu-central-1)
- [21st.dev расширение](https://marketplace.visualstudio.com/items?itemName=21st.21st-extension)
- [Документация Storyblok](https://www.storyblok.com/docs)
- [mkcert документация](https://github.com/FiloSottile/mkcert)
