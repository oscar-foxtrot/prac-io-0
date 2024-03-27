import pandas as pd
import calendar
from dateutil.relativedelta import relativedelta

agg = pd.DataFrame(columns=['date', 'apple', 'pen'])

states = ['b1', 'b2', 'm1', 'm2', 's1', 's2', 's3', 's4']


for state in states:
    rows = []
    df_sell = pd.read_csv(f'MS-{state}-sell.csv', parse_dates=['date'])
    df_supply = pd.read_csv(f'MS-{state}-supply.csv', parse_dates=['date'])
    df_inventory = pd.read_csv(f'MS-{state}-inventory.csv', parse_dates=['date'])


    for year in range(2006, 2016):
        for month in range(1, 13):

            vals = []  # sell, supply, inventory

            n_apples = df_sell[(df_sell['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                & (df_sell['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}')) \
                & (df_sell['sku_num'].str.contains('-ap-'))].shape[0]
            n_pens = df_sell[(df_sell['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                & (df_sell['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}')) \
                & (df_sell['sku_num'].str.contains('-pe-'))].shape[0]
            vals.append((n_apples, n_pens))

            n_apples = df_supply[(df_supply['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                & (df_supply['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}'))]['apple'].sum()
            n_pens = df_supply[(df_supply['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                & (df_supply['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}'))]['pen'].sum()
            vals.append((n_apples, n_pens))

            try:
                prevdate = [0, 0]
                if month > 1:
                    prevdate[0], prevdate[1] = \
                        pd.to_datetime(f'{year}-{month - 1}-01'), pd.to_datetime(f'{year}-{month - 1}-{calendar.monthrange(year, month - 1)[1]}')
                else:
                    prevdate[0], prevdate[1] = pd.to_datetime(f'{year - 1}-12-01'), pd.to_datetime(f'{year - 1}-12-31')

                n_apples = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                    & (df_inventory['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}'))].iloc[-1]['apple'] \
                    - df_inventory[(df_inventory['date'] >= prevdate[0]) \
                    & (df_inventory['date'] <= prevdate[1])].iloc[-1]['apple']

                n_pens = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-{month}-01')) \
                    & (df_inventory['date'] <= pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}'))].iloc[-1]['pen'] \
                    - df_inventory[(df_inventory['date'] >= prevdate[0]) \
                    & (df_inventory['date'] <= prevdate[1])].iloc[-1]['pen']
            
            # The very first month case
            except IndexError:
                n_apples = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                    & (df_inventory['date'] <= pd.to_datetime(f'{year}-01-31'))].iloc[-1]['apple']

                n_pens = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                    & (df_inventory['date'] <= pd.to_datetime(f'{year}-01-31'))].iloc[-1]['pen']

            vals.append((n_apples, n_pens))

            apples_stolen = vals[1][0] - vals[2][0] - vals[0][0]
            pens_stolen = vals[1][1] - vals[2][1] - vals[0][1]

            new_row = {'date': pd.to_datetime(f'{year}-{month}-{calendar.monthrange(year, month)[1]}'), 'apple': apples_stolen, 'pen': pens_stolen}
            rows.append(new_row)

    agg = pd.concat([agg, pd.DataFrame(rows)], ignore_index=True)
    agg.to_csv(f'MS-{state}-steal.csv', index=False)
        