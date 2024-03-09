import pandas as pd
import random
import uuid

random.seed(24)

agg = pd.read_csv('agregate.csv')
states = ['b1', 'b2', 's1', 's2', 's3', 's4', 'm1', 'm2']
'''
for state in states:

    epsilon = 10

    dfd = pd.read_csv(f'MS-{state}-daily.csv')
    dfd_diffs = dfd.copy()

    apple_diffs = dfd_diffs.iloc[1:].reset_index().iloc[:, 2] - dfd_diffs.iloc[:-1, 1]
    pen_diffs = dfd_diffs.iloc[1:].reset_index().iloc[:, 3] - dfd_diffs.iloc[:-1, 2]

    dfd_diffs = dfd_diffs.iloc[1:, :].reset_index().iloc[:, 1:4]

    dfd_diffs['apple'] = apple_diffs
    dfd_diffs['pen'] = pen_diffs



    start_date = pd.to_datetime('2006-01-01')
    end_date = pd.to_datetime('2006-12-31')

    dfd_diffs['date'] = pd.to_datetime(dfd_diffs['date'])

    dfd_diffs.loc[dfd_diffs['apple'] >= 0, 'apple'] = 0

    total_sold = agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['apple_sold'].iloc[0]
    difference = total_sold + dfd_diffs[(dfd_diffs['date'] >= start_date) \
        & (dfd_diffs['date'] <= end_date)]['apple'].sum() \
        - agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['apple_stolen'].iloc[0]

    maxif = dfd_diffs.loc[(dfd_diffs['apple'] < 0), 'apple'].max()
    minif = dfd_diffs.loc[(dfd_diffs['apple'] < 0), 'apple'].min()
    window = maxif - minif

    nums = []
    while abs(sum(nums) + difference) >= epsilon:
        nums.clear()
        for i in range(24):
            nums.append(random.randint(minif, maxif))
        if nums[23] - (sum(nums) + difference) >= 0:
                nums.clear()

    nums[23] -= sum(nums) + difference

    new_row = {'date': start_date, 'apple': 0, 'pen': 0}

    insert_position = 0
    #dfd_diffs.loc[insert_position + 1:] = dfd_diffs.loc[insert_position:].shift(1)
    #dfd_diffs.loc[insert_position] = new_row
    
    dfd_diffs = pd.concat([pd.DataFrame([new_row]), dfd_diffs], ignore_index=True)

    indexer = dfd_diffs[(dfd_diffs['apple'] == 0) & (dfd_diffs['date'] >= start_date)
        & (dfd_diffs['date'] <= end_date)].index


    dfd_diffs.loc[(dfd_diffs['apple'] == 0) & (dfd_diffs['date'] >= start_date)
        & (dfd_diffs['date'] <= end_date), 'apple'] = pd.Series(nums, index = indexer)

    ##############################
    start_date = pd.to_datetime('2007-01-01')
    end_date = pd.to_datetime('2007-12-31')

    print(state)
    while end_date != pd.to_datetime('2016-12-31'):
        total_sold = agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['apple_sold'].iloc[0]
        difference = total_sold + dfd_diffs[(dfd_diffs['date'] >= start_date) \
            & (dfd_diffs['date'] <= end_date)]['apple'].sum() \
            - agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['apple_stolen'].iloc[0]

        maxif = dfd_diffs.loc[(dfd_diffs['apple'] < 0), 'apple'].max()
        minif = dfd_diffs.loc[(dfd_diffs['apple'] < 0), 'apple'].min()

        nums = []
        while abs(sum(nums) + difference) >= epsilon:
            nums.clear()
            for i in range(24):
                nums.append(random.randint(minif, maxif))
            if nums[23] - (sum(nums) + difference) >= 0:
                nums.clear()

        nums[23] -= sum(nums) + difference

        indexer = dfd_diffs[(dfd_diffs['apple'] == 0) & (dfd_diffs['date'] >= start_date)
            & (dfd_diffs['date'] <= end_date)].index


        dfd_diffs.loc[(dfd_diffs['apple'] == 0) & (dfd_diffs['date'] >= start_date)
            & (dfd_diffs['date'] <= end_date), 'apple'] = pd.Series(nums, index = indexer)

        start_date += pd.offsets.DateOffset(years=1)
        end_date += pd.offsets.DateOffset(years=1)       


    start_date = pd.to_datetime('2006-01-01')
    end_date = pd.to_datetime('2006-12-31')

    dfd_diffs.loc[dfd_diffs['pen'] >= 0, 'pen'] = 0

    print(state)
    while end_date != pd.to_datetime('2016-12-31'):
        total_sold = agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['pen_sold'].iloc[0]
        difference = total_sold + dfd_diffs[(dfd_diffs['date'] >= start_date) \
            & (dfd_diffs['date'] <= end_date)]['pen'].sum() \
            - agg.loc[(agg['state'] == state) & (agg['year'] == start_date.year)]['pen_stolen'].iloc[0]
            

        maxif = dfd_diffs.loc[(dfd_diffs['pen'] < 0), 'pen'].max()
        minif = dfd_diffs.loc[(dfd_diffs['pen'] < 0), 'pen'].min()

        nums = []
        while abs(sum(nums) + difference) >= epsilon:
            nums.clear()
            for i in range(24):
                nums.append(random.randint(minif, maxif))
            if nums[23] - (sum(nums) + difference) >= 0:
                nums.clear()

        nums[23] -= sum(nums) + difference

        indexer = dfd_diffs[(dfd_diffs['pen'] == 0) & (dfd_diffs['date'] >= start_date)
            & (dfd_diffs['date'] <= end_date)].index


        dfd_diffs.loc[(dfd_diffs['pen'] == 0) & (dfd_diffs['date'] >= start_date)
            & (dfd_diffs['date'] <= end_date), 'pen'] = pd.Series(nums, index = indexer)

        start_date += pd.offsets.DateOffset(years=1)
        end_date += pd.offsets.DateOffset(years=1)       
        dfd_diffs.to_csv(f'test_{state}.csv')
    print(state)

'''

'''
states = ['b1', 'b2', 's1', 's2', 's3', 's4', 'm1', 'm2']
for state in states:
    df_old = pd.read_csv(f'test_{state}.csv')

    df = pd.DataFrame(columns=['date', 'sku_num'])
    df.to_csv(f'MS-{state}-sell.csv', index=False, mode='a')

    to_concat = []
    counter = 0
    for row_n in df_old.index:
        counter += 1
        if (counter % 250 == 0):
            pd.DataFrame(to_concat).to_csv(f'MS-{state}-sell.csv', mode='a', index=False, header=False)  # Sparing RAM
            to_concat.clear()

        n_apples = abs(df_old.loc[row_n]['apple'])
        n_pens = abs(df_old.loc[row_n]['pen'])
        
        obj_type = [0 for i in range(n_apples)]
        obj_type += [1 for i in range(n_pens)]
        random.shuffle(obj_type)

        for i in range(n_apples + n_pens):
            uuid_val = uuid.uuid4()
            uuid_str = f"{uuid_val.hex[:8]}-{uuid_val.hex[8:12]}-{uuid_val.hex[12:16]}-{uuid_val.hex[16:20]}-{uuid_val.hex[20:]}"
            
            new_row = {'date': df_old.loc[row_n].loc['date'], 'sku_num': f'MS-{state}-{"pe" if obj_type[i] else "ap"}-' + uuid_str}
            to_concat.append(new_row)
        print(row_n)
    pd.DataFrame(to_concat).to_csv(f'MS-{state}-sell.csv', mode='a', index=False, header=False)

'''

'''
states = ['b1', 'b2', 's1', 's2', 's3', 's4', 'm1', 'm2']
for state in states:

    dfd = pd.read_csv(f'MS-{state}-daily.csv')
    df_old = pd.read_csv(f'test_{state}.csv')


    dfd = pd.read_csv(f'MS-{state}-daily.csv')
    dfd_diffs = dfd.copy()

    apple_diffs = dfd_diffs.iloc[1:].reset_index().iloc[:, 2] - dfd_diffs.iloc[:-1, 1]
    pen_diffs = dfd_diffs.iloc[1:].reset_index().iloc[:, 3] - dfd_diffs.iloc[:-1, 2]

    dfd_diffs = dfd_diffs.iloc[1:, :].reset_index().iloc[:, 1:4]

    dfd_diffs['apple'] = apple_diffs
    dfd_diffs['pen'] = pen_diffs

    new_row = dfd.loc[0]
    dfd_diffs = pd.concat([pd.DataFrame([new_row]), dfd_diffs], ignore_index=True)

    indexer = dfd_diffs['apple'] >= 0


    supply_df = df_old[indexer].iloc[:, 1:4].copy()

    supply_df.loc[0, 'apple'] = dfd.loc[0, 'apple'] - supply_df.loc[0, 'apple']
    supply_df.loc[0, 'pen'] = dfd.loc[0, 'pen'] - supply_df.loc[0, 'pen']

    supply_df.loc[1:, 'apple'] = dfd_diffs[indexer].loc[1:, 'apple'] - supply_df.loc[1:, 'apple']
    supply_df.loc[1:, 'pen'] = dfd_diffs[indexer].loc[1:, 'pen'] - supply_df.loc[1:, 'pen']

    supply_df.to_csv(f'MS-{state}-supply.csv', index=False)
'''


states = ['b1', 'b2', 's1', 's2', 's3', 's4', 'm1', 'm2']
for state in states:

    df_supply = pd.read_csv(f'MS-{state}-supply.csv')
    df_test = pd.read_csv(f'test_{state}.csv')
    df_steal = pd.read_csv(f'MS-{state}-steal.csv')

    df_test['date'] = pd.to_datetime(df_test['date'])
    df_supply['date'] = pd.to_datetime(df_supply['date'])

    inventory_log_apple = []
    inventory_log_pen = []
    dates = []
    for year in range(2006, 2016):
        for month in range(1, 13):
            total_apples = df_test.loc[(df_test['date'].dt.year == year) & (df_test['date'].dt.month == month), 'apple'].sum() \
                + df_supply.loc[(df_supply['date'].dt.year == year) & (df_supply['date'].dt.month == month), 'apple'].sum()
            inventory_log_apple.append(total_apples)

            total_pens = df_test.loc[(df_test['date'].dt.year == year) & (df_test['date'].dt.month == month), 'pen'].sum() \
                + df_supply.loc[(df_supply['date'].dt.year == year) & (df_supply['date'].dt.month == month), 'pen'].sum()
            inventory_log_pen.append(total_pens)

            dates.append(pd.to_datetime(f'{year}-{month}-01') + pd.offsets.MonthEnd(0))

    for i in range(1, len(inventory_log_apple)):
        inventory_log_apple[i] += inventory_log_apple[i - 1]
        inventory_log_pen[i] += inventory_log_pen[i - 1]

    df = pd.DataFrame(columns=['date', 'apple', 'pen'])
    df['apple'] = pd.Series(inventory_log_apple)
    df['pen'] = pd.Series(inventory_log_pen)
    df['date'] = pd.Series(dates)

    df.to_csv(f'MS-{state}-inventory.csv')

