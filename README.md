# 1Base - Simple CMS with Storyblok

Простая CMS система с возможностью редактирования контента локально и через Storyblok.

## Возможности

- 🎨 **Локальная CMS** - Редактируйте текст прямо на странице
- 📝 **Storyblok интеграция** - Управляйте контентом через Storyblok панель
- 🔧 **21st.dev Toolbar** - AI-powered редактирование через браузер
- 🎯 **React + TypeScript** - Современный стек разработки
- 💾 **Автосохранение** - Изменения сохраняются автоматически

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/Prezto5/1Base.git
cd 1Base

# Установить зависимости
pnpm install

# Создать .env файл
cp .env.example .env

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

## Команды

```bash
# Разработка
pnpm dev

# Сборка
pnpm build

# Превью сборки
pnpm preview

# Проверка типов
pnpm type-check
```

## Деплой

Проект настроен для деплоя на:
- ✅ Vercel
- ✅ Netlify
- ✅ GitHub Pages

## Ссылки

- [Storyblok редактор](https://app.storyblok.com/#/edit/64979012523641?region=eu-central-1)
- [21st.dev расширение](https://marketplace.visualstudio.com/items?itemName=21st.21st-extension)
- [Документация Storyblok](https://www.storyblok.com/docs)
