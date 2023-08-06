# Soloway SDK (Unofficial)

Простейшая реализация SDK для https://dsp.soloway.ru/

### Реализованные методы
* ``/login``
* ``/whoami``
* ``/clients/{clientGuid}/placements``
* ``/placements_stat``
* ``/placements/{placementGuid}/stat``

## Установка
```bash    
    $ pip install soloway-unofficial
```

## Использование

```python
from soloway_unofficial import Client

client = Client("YOUR_LOGIN", "YOUR_PASSWORD")
```    

Получение статистики размещений по всем кампаниям.
* ``start_date — дата начала(включительно) периода в формате YYYY-MM-DD``
* ``stop_date — дата конца(включительно) периода, в формате YYYY-MM-DD``

```python
data = client.get_placements_stat_all("START_DATE", "STOP_DATE")
```    
Получение статистики размещений по выбранным кампаниям.
* ``start_date — дата начала(включительно) периода в формате YYYY-MM-DD``
* ``stop_date — дата конца(включительно) периода, в формате YYYY-MM-DD``

```python
data = client.get_placements_stat(list["PLACEMENT_ID"],"START_DATE", "STOP_DATE")
```    

Получение статистики по всем кампаниям по дням.
* ``start_date — дата начала(включительно) периода в формате YYYY-MM-DD``
* ``stop_date — дата конца(включительно) периода, в формате YYYY-MM-DD``

```python        
data = client.get_placements_stat_by_day("START_DATE", "STOP_DATE")
```

Получение статистики по выбранной кампании по дням.
* ``start_date — дата начала(включительно) периода в формате YYYY-MM-DD``
* ``stop_date — дата конца(включительно) периода, в формате YYYY-MM-DD``

```python        
data = client.get_placement_stat_by_day("PLACEMENT_ID", "START_DATE", "STOP_DATE")
```