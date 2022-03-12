# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

# %%
import requests
import pandas as pd
import numpy as np
import time
import itertools
import os

def expenses_cong(id_dep, years, page):

    years_lst = list(years)

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('ano', years_lst),
        ('pagina', page),
        ('itens', '100'),
        ('ordem', 'ASC'),
        ('ordenarPor', 'ano'),
    )

    response = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados/' + id_dep + '/despesas',
                            headers=headers,
                            params=params)

    return response.json()


congs_df = pd.read_excel('congress_men.xls')

ids_lst = np.array(congs_df['id'])

names_lst = np.array(congs_df['nome'])

parties_lst= np.array(congs_df['siglaPartido'])

ufs_lst = np.array(congs_df['siglaUf'])

print('Requests loop initialized')
ti = time.time()

df1_lst = []

for (i, j, k, l) in zip(ids_lst, names_lst, parties_lst, ufs_lst):
    print(i, j)
    df2_lst = []
    for num in range(1, 13, 1):  # iterates thru all the pages of expense results (each page has 100 results).

        expense = expenses_cong(id_dep=str(i), years=['2019', '2020', '2021'], page=str(num))  # calls the function on a congressman.

        data = expense['dados']  # key for the data of an expense.

        df = pd.DataFrame(data)  # transforms the dict into a data frame.

        df2_lst.append(df)  # appends each page df to a list of data frames


    
    result_spending = pd.concat(df2_lst, ignore_index=True)  # concatenates the data frames(pages) into 1 df.

    result_spending['id'] = np.array([i] * len(result_spending))

    result_spending['name'] = np.array([j] * len(result_spending))

    result_spending['party'] = np.array([k] * len(result_spending))

    result_spending['state'] = np.array([l] * len(result_spending))

    df1_lst.append(result_spending)
        
all_in_one = pd.concat(df1_lst)

tf = time.time()
print('Ruquests loop finalized in',tf-ti, 'seconds')

all_in_one.to_csv(path_or_buf='/home/jovyan/work/indiv_expense/all_congs_expenses.csv')


# %%
all_in_one.head()


# %%
all_in_one.info()


# %%
all_in_one.to_excel('all_congs_expenses.xlsx')


