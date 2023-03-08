from collections import Counter
import pandas as pd
import re

# abbv = pd.read_html('https://www.onemap.gov.sg/abbreviations/index.html')[0]
# abbv.columns = ['abbreviated', 'full_text']
# abbv.to_csv('abbreviations.csv', index=False)
abbv = pd.read_csv('data/abbreviations.csv')
abbv = abbv.loc[abbv['abbreviated'].str.len() > 1]
mapper = pd.Series(abbv['full_text'].values, abbv['abbreviated'].values).to_dict()


df = pd.read_csv('data/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
# ll stands for lat-long data
ll = pd.read_csv('./research/sg_zipcode_mapper.csv', encoding='ISO-8859-1')
ll = ll.rename(columns={'road_name': 'street_name', 'blk_no': 'block'})
ll = ll.drop(['searchval', 'postal.1'], axis=1, errors='ignore')

# df['street_num_part'] = df['street_name'].str.extract('([^ ]+ \d{1,3})')
# df['admin_abbr'] = df['street_name'].str.extract('([^ ]+) \d{1,3}')
# df['street_num'] = df['street_name'].str.extract('(\d{1,3})')
# df['street_excl_num'] = df['street_name'].str.extract('(.*) [^ ]+ \d{1,3}')


# c = Counter()
# all_tokens = df['street_name'].str.split().tolist() 
# for row in all_tokens:
#     c.update(row)
# {k: v for k, v in sorted(c.items(), key=lambda item: -item[1])}

changes = {}

df['key'] = df['street_name']
df['key'] = df['street_name'].str.replace('ST.', 'SAINT', regex=False)
for k, v in mapper.items():
    
    df['temp'] = df['key'].str.replace(fr'\b{k}\b', v, regex=True)
    num_changes = sum((df['temp'] != df['key']) * 1)
    changes[k] = num_changes

    df['key'] = df['temp']

df = df.drop('temp', axis=1, errors='ignore')

# sorted_changes = {k: v for k, v in sorted(changes.items(), key=lambda item: -item[1])}
# sorted_changes
# relevant_changes = {k: v for k, v in changes.items() if v > 0}
# relevant_changes
df.sample(5).T
ll.sample(5).T

da = df.merge(ll,
    how='left',
    left_on=['key', 'block'],
    right_on=['street_name', 'block'])


da['postal'].isnull().mean()
da[da['postal'].isnull()].sample(5).T

(da[da['postal'].isnull()]['town'].value_counts() / df['town'].value_counts()).sort_values(ascending=False)

da.sample(5).T

da['latitude'].isnull().mean()

da.to_csv('data/processed/cleaned_data.csv', index=False)
