"""add_websocket_triggers_for_realtime_updates

Revision ID: abc123456789
Revises: 96b5d1f5670d
Create Date: 2025-01-31 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc123456789'
down_revision: Union[str, Sequence[str], None] = '96b5d1f5670d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаем универсальную функцию для отправки уведомлений
    op.execute("""
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
    """)
    
    # Создаем триггеры для таблицы products
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_products_notify ON products;
        CREATE TRIGGER trigger_products_notify
            AFTER INSERT OR UPDATE OR DELETE ON products
            FOR EACH ROW
            EXECUTE FUNCTION notify_data_change();
    """)
    
    # Создаем триггеры для таблицы product_variants
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_product_variants_notify ON product_variants;
        CREATE TRIGGER trigger_product_variants_notify
            AFTER INSERT OR UPDATE OR DELETE ON product_variants
            FOR EACH ROW
            EXECUTE FUNCTION notify_data_change();
    """)
    
    # Добавляем комментарии для документации
    op.execute("""
        COMMENT ON FUNCTION notify_data_change() IS 'Универсальная функция для отправки уведомлений о изменениях данных через PostgreSQL NOTIFY. Используется с триггерами для real-time обновлений.';
        COMMENT ON TRIGGER trigger_products_notify ON products IS 'Триггер для отправки уведомлений об изменениях в таблице products';
        COMMENT ON TRIGGER trigger_product_variants_notify ON product_variants IS 'Триггер для отправки уведомлений об изменениях в таблице product_variants';
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем триггеры
    op.execute("DROP TRIGGER IF EXISTS trigger_product_variants_notify ON product_variants;")
    op.execute("DROP TRIGGER IF EXISTS trigger_products_notify ON products;")
    
    # Удаляем функцию
    op.execute("DROP FUNCTION IF EXISTS notify_data_change();") 