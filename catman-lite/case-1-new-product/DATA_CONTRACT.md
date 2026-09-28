# Контракт данных и источников

## Реальные публичные наблюдения
`catalog_observations.csv`: `source_id,retailer,store_or_channel,region,observed_at,url,source_product_id,ean_or_gtin,title,brand,category,attributes_json,pack_size,pack_unit,listed_price,currency,availability,source_terms_checked`. Одна строка — наблюдение, не продажа. Для заявления «появился недавно» нужны хотя бы два датированных среза либо проверяемая дата запуска. Отсутствие на странице не означает отсутствие в магазине.
`product_matches.csv`: `candidate_id,reference_id,match_type,matching_attributes,evidence_url,confidence,review_status`. `match_type`: exact / similar / unknown. Цена, объём и форма упаковки не смешиваются без нормализации.

## Демо-данные условной сети
`demo_stores.csv`: `store_id,cluster_id,region,format,shelf_capacity,capacity_unit`. `demo_matrix.csv`: `store_id,sku,from_date,to_date,facings,source_observation_id`. `demo_economics.csv`: `store_id,sku,period,units,net_sales,net_cogs,var_fulfillment,promo_spend,supplier_funding,on_hand,source_type`. Для всех внутренних строк `source_type=synthetic_demo`, фиксированные `snapshot_date` и `demo_seed`; никакие строки не выдавать за фактический P&L выбранного ритейлера. Если недоступна история продаж, покупательская лояльность или закупка, не изображать их извлечёнными из сайтов.

## Решение и проверка
`scenario_results`: `scenario_id,store_or_cluster,candidate_sku,removed_sku_or_facings,assumptions,demand_range,contribution_profit_range,capacity_check,baseline,limitations`. Финансовый контракт демо: `contribution_profit = net_sales - net_cogs - var_fulfillment - promo_spend + supplier_funding`; funding ровно один раз. Для альтернативы «ничего не менять» — та же формула и тот же горизонт. Неизвестная себестоимость = неизвестный результат, а не 0.
`pilot_plan`: `decision,owner,test_stores,control_stores,period,primary_metric,guardrails,success_rule`. Пример метрик без целевых цифр: вклад в прибыль категории, OOS, продажи аналогов, покрытие потребности. До теста все изменения — модельные гипотезы.

## Гейты перед показом
- Публичные URL доступны и сохранены с датой/географией; правила использования проверены, персональные данные и закрытые источники исключены.
- Товар кандидата не признан «новым на рынке» лишь потому, что его нет в нашем снимке.
- Продажи конкурентов отсутствуют, если нет отдельного допустимого источника; не выводить их из цены, отзывов или рейтинга.
- Синтетические таблицы согласованы по SKU/store/time и дают как выгодный, так и невыгодный сценарий; формулы воспроизводимы.
- Если нет доступного источника или доказательства потребности, результат `unknown/collect_evidence` допустим и предпочтительнее выдумки.

Это спецификация поиска и будущего набора, а не утверждение, что файлы CSV уже собраны.
