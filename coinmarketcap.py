from bs4 import BeautifulSoup
import requests
import pandas as pd
import copy


def main():
    data_frame = get_data_market()
    view_stat(data_frame)


def get_data_market():
    url = 'https://coinmarketcap.com/'
    page = requests.get(url)
    return soup_work(page)


def soup_work(page):
    soup = BeautifulSoup(page.text, "html.parser")
    soup_result = {
        'Name': [],
        'Market Cap': [],
        'Price': [],
        'Volume(24h)': [],
        'Circulating Supply': [],
        'Change (24h)': []
    }
    result_parse = soup.find_all("tr", {"class": "cmc-table-row"})
    for i in result_parse:
        soup_result['Name'].append(i.contents[1].text)
        soup_result['Market Cap'].append(i.contents[2].text)
        soup_result['Price'].append(i.contents[3].text)
        soup_result['Volume(24h)'].append(i.contents[4].text)
        soup_result['Circulating Supply'].append(i.contents[5].text)
        soup_result['Change (24h)'].append(i.contents[6].text)
    data_frame = pandas_func(soup_result)
    return data_frame


def pandas_func(data):
    data_frame = pd.DataFrame(data=data, index=list(range(1, len(data['Name']) + 1)))
    return data_frame


def top_5_first_and_top_5_last(data_frame):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print('First TOP 5 coins in TOP 100',
              data_frame.loc[1:5, ['Name', 'Market Cap', 'Price', 'Volume(24h)', 'Circulating Supply', 'Change (24h)']],
              sep='\n')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print('Last 5 coins in TOP 100',
              data_frame.loc[95:100,
              ['Name', 'Market Cap', 'Price', 'Volume(24h)', 'Circulating Supply', 'Change (24h)']],
              sep='\n')


def view_stat_any_coin(data_frame):
    short_coins_names = [i.split(' ')[1] for i in data_frame['Circulating Supply']]
    full_coins_names = data_frame["Name"].tolist()
    val = input('Input coin name: ')
    if val.upper() in short_coins_names:
        num_coin = short_coins_names.index(val.upper())
        print(data_frame.loc[num_coin + 1])
    elif val in full_coins_names:
        num_coin = full_coins_names.index(val)
        print(data_frame.loc[num_coin + 1])
    else:
        try:
            tmp_v = [(i + 1, e) for i, e in enumerate(full_coins_names) if e.lower().startswith(val.lower()[0:3])]
            if len(tmp_v) > 1:
                try:
                    wrong_val = input(f'You input \'{val}\', did you mean something from this list:\n{tmp_v}\nIf name '
                                      f'of coin in list, just input number your coin: ')
                    print(data_frame.iloc[int(wrong_val) - 1])
                except IndexError:
                    print(f'Wrong number or coin {val} not in TOP 100')
            else:
                try:
                    print('\n' + str(data_frame.loc[tmp_v[0][0]]))
                except IndexError:
                    print(f'Wrong name or coin {val} not in TOP 100')
        except ValueError:
            print(f'Wrong name or coin {val} not in TOP 100')


def top_5_price_and_top_5_low_price(data_frame):
    data_frame_copy = copy.deepcopy(data_frame)
    data_frame_copy['Price'] = data_frame_copy['Price'].str.strip('$')
    data_frame_copy['Price'] = data_frame_copy['Price'].str.replace(",", "").astype(float)
    biggest_prices = data_frame_copy.nlargest(5, ['Price'])
    lowest_prices = data_frame_copy.nsmallest(5, ['Price'])
    print('Top 5 biggest price\n' + str(data_frame.loc[list(biggest_prices.index), ['Name', 'Price']]),
          '\nTop 5 lowest price\n' + str(data_frame.loc[list(lowest_prices.index), ['Name', 'Price']]), sep='\n')


MENU = {
    '1': top_5_first_and_top_5_last,
    '2': view_stat_any_coin,
    '3': top_5_price_and_top_5_low_price,

}


def view_stat(data_frame):
    input_var = input(
        '1: Top 5 first and Top 5 last coins\n2: View full info of any coin\n3: Top 5 price and Top 5 low '
        'price\nChoose menu: ')
    try:
        func = MENU[input_var]
        func(data_frame)
    except KeyError:
        print("Wrong menu number.")


if __name__ == "__main__":
    main()
