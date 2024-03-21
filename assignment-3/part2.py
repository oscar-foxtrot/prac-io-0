import pandas as pd 

states = ['b1', 'b2', 'm1', 'm2', 's1', 's2', 's3', 's4']

def daily_inventory(state):
    supply = pd.read_csv(f'MS-{state}-supply.csv', parse_dates=['date'])
    sell = pd.read_csv(f'MS-{state}-sell.csv', parse_dates=['date'])

    supply.index = pd.to_datetime(supply['date'])
    supply.drop('date', axis=1, inplace=True)

    sell['sku_num'] = sell['sku_num'].apply(lambda x: -1 if x.find('ap') == 6 else 1)
    sell['num'] = sell['sku_num']
    sell['sku_num'] = sell['sku_num'].apply(lambda x: 0 if x > 0 else -x)
    sell['num'] = sell['num'].apply(lambda x: 0 if x < 0 else x)
    sell = sell.rename(columns={"sku_num": "apple", "num": "pen"})
    sell = sell.groupby(['date']).sum()
    sell.index = pd.to_datetime(sell.index)

    daily_inventory = pd.DataFrame(columns=['apple', 'pen'], index = sell.index)
    daily_inventory['apple'] = -sell['apple']
    daily_inventory['pen'] = -sell['pen']
    daily_inventory = pd.concat([daily_inventory, supply])
    daily_inventory = daily_inventory.groupby(['date']).sum()
    daily_inventory['apple'] = daily_inventory['apple'].cumsum()
    daily_inventory['pen'] = daily_inventory['pen'].cumsum()
    daily_inventory.to_csv(f'{state}_daily_inventory.csv', index=True)

for state in states:
    daily_inventory(state)