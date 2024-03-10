import pandas as pd

agg = pd.DataFrame(columns=['year', 'state', 'apple_sold', 'apple_stolen', 'pen_sold', 'pen_stolen'])

states = ['b1', 'b2', 'm1', 'm2', 's1', 's2', 's3', 's4']

rows = []
for state in states:

    df_sell = pd.read_csv(f'MS-{state}-sell.csv', parse_dates=['date'])
    df_supply = pd.read_csv(f'MS-{state}-supply.csv', parse_dates=['date'])
    df_inventory = pd.read_csv(f'MS-{state}-inventory.csv', parse_dates=['date'])


    for year in range(2006, 2016):

        vals = []  # sell, supply, inventory

        n_apples = df_sell[(df_sell['date'] >= pd.to_datetime(f'{year}-01-01')) \
            & (df_sell['date'] <= pd.to_datetime(f'{year}-12-31')) \
            & (df_sell['sku_num'].str.contains('-ap-'))].shape[0]
        n_pens = df_sell[(df_sell['date'] >= pd.to_datetime(f'{year}-01-01')) \
            & (df_sell['date'] <= pd.to_datetime(f'{year}-12-31')) \
            & (df_sell['sku_num'].str.contains('-pe-'))].shape[0]
        vals.append((n_apples, n_pens))

        n_apples = df_supply[(df_supply['date'] >= pd.to_datetime(f'{year}-01-01')) \
            & (df_supply['date'] <= pd.to_datetime(f'{year}-12-31'))]['apple'].sum()
        n_pens = df_supply[(df_supply['date'] >= pd.to_datetime(f'{year}-01-01')) \
            & (df_supply['date'] <= pd.to_datetime(f'{year}-12-31'))]['pen'].sum()
        vals.append((n_apples, n_pens))

        try:
            n_apples = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year}-12-31'))].iloc[-1]['apple'] \
                - df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year - 1}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year - 1}-12-31'))].iloc[-1]['apple']

            n_pens = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year}-12-31'))].iloc[-1]['pen'] \
                - df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year - 1}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year - 1}-12-31'))].iloc[-1]['pen']
        except:
            n_apples = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year}-12-31'))].iloc[-1]['apple']

            n_pens = df_inventory[(df_inventory['date'] >= pd.to_datetime(f'{year}-01-01')) \
                & (df_inventory['date'] <= pd.to_datetime(f'{year}-12-31'))].iloc[-1]['pen']

        vals.append((n_apples, n_pens))

        apples_stolen = vals[1][0] - vals[2][0] - vals[0][0]
        pens_stolen = vals[1][1] - vals[2][1] - vals[0][1]

        new_row = {'year': year, 'state': state, 'apple_sold': vals[0][0],
            'apple_stolen': apples_stolen, 'pen_sold': vals[0][1], 'pen_stolen': pens_stolen}
        rows.append(new_row)

agg = pd.concat([agg, pd.DataFrame(rows)], ignore_index=True)
agg.to_csv('aggregated_info.csv', index=False)
        