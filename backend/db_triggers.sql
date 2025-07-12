-- Универсальная функция для отправки уведомлений о изменениях в базе данных
-- Эта функция может быть использована для любой таблицы через триггеры

CREATE OR REPLACE FUNCTION notify_data_change()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
    table_name TEXT;
    operation TEXT;
    row_data JSON;
BEGIN
    -- Получаем имя таблицы
    table_name := TG_TABLE_NAME;
    operation := TG_OP;
    
    -- Формируем JSON с данными строки в зависимости от операции
    IF operation = 'DELETE' THEN
        row_data := row_to_json(OLD);
    ELSE
        row_data := row_to_json(NEW);
    END IF;
    
    -- Создаем полезную нагрузку (payload) для уведомления
    payload := json_build_object(
        'table', table_name,
        'operation', operation,
        'data', row_data,
        'timestamp', extract(epoch from now())
    );
    
    -- Отправляем уведомление в канал 'data_updates'
    PERFORM pg_notify('data_updates', payload::text);
    
    -- Возвращаем соответствующую строку
    IF operation = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггеры для таблицы products
DROP TRIGGER IF EXISTS trigger_products_notify ON products;
CREATE TRIGGER trigger_products_notify
    AFTER INSERT OR UPDATE OR DELETE ON products
    FOR EACH ROW
    EXECUTE FUNCTION notify_data_change();

-- Создаем триггеры для таблицы product_variants
DROP TRIGGER IF EXISTS trigger_product_variants_notify ON product_variants;
CREATE TRIGGER trigger_product_variants_notify
    AFTER INSERT OR UPDATE OR DELETE ON product_variants
    FOR EACH ROW
    EXECUTE FUNCTION notify_data_change();

-- Комментарии для документации
COMMENT ON FUNCTION notify_data_change() IS 'Универсальная функция для отправки уведомлений о изменениях данных через PostgreSQL NOTIFY. Используется с триггерами для real-time обновлений.';
COMMENT ON TRIGGER trigger_products_notify ON products IS 'Триггер для отправки уведомлений об изменениях в таблице products';
COMMENT ON TRIGGER trigger_product_variants_notify ON product_variants IS 'Триггер для отправки уведомлений об изменениях в таблице product_variants'; 