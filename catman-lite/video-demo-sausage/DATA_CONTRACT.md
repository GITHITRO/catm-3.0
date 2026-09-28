# Контракт данных v0 (для последующей реализации)

Все записи: `dataset_version`, `snapshot_date`, `provenance` (`synthetic` или документированный `observed_card`). Даты — ISO 8601, деньги — RUB, количество — штуки. Никаких персональных данных покупателей.

Таблицы: `products(sku_id, name, sausage_type, brand, pack_g, shelf_life_days, regular_price_rub, unit_cost_rub, provenance)`; `stores(store_id, city_context, format, cluster_id, provenance)`; `assortment(store_id, sku_id, valid_from, valid_to, listed_flag)`; `daily_sales(date, store_id, sku_id, units, net_sales_rub, promo_flag, oos_flag, provenance)`; `batches(batch_id, store_id, sku_id, received_at, expires_at, received_units, provenance)`; `inventory_daily(date, batch_id, opening_units, received_units, sold_units, written_off_units, closing_units)`; `scenario_events(event_id, case_id, date, store_id, sku_id, event_type, notes)`. Стабильные ID используются во всех сценах.

Инварианты: внешние ключи и уникальные составные ключи; неотрицательные количества; `opening + received - sold - written_off = closing` на уровне партия-день; сумма проданных единиц по партиям равна `daily_sales.units` на уровне дата-магазин-SKU; продажи возможны только в активной матрице и при запасе; истёкшие партии не продаются; FEFO либо строго соблюдается, либо исключение явно зафиксировано; зафиксирован seed генератора. Ноль продаж вне матрицы или при OOS нельзя трактовать как ноль спроса.

В видео и в API отдельно показывать исторический факт внутри синтетического мира, прогноз и what-if. Финансовые сценарии обязаны включать вариант «ничего не менять» и хотя бы один отрицательный результат. Показатели не объявлять фактическим эффектом реальной сети.
