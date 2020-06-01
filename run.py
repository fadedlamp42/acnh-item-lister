#!/bin/python3.7
from selenium.webdriver import Firefox, FirefoxOptions
from time import sleep
from pandas import DataFrame
opt = FirefoxOptions()
opt.headless = True
driver = Firefox(options=opt)

# adjust this number for slower connections
wait = 1

print("getting page")
driver.get("https://www.animalcrossingitemlist.com/list/all-items/")
print(f"waiting {wait} seconds...")
sleep(wait)

# this will overwrite items.csv with a more up to date version
frame = DataFrame(columns=['Name', 'Sell Price', 'Buy Price'])
has_more = True
while has_more:
    buttons = driver.find_elements_by_class_name("v-btn__content")
    table = driver.find_element_by_tag_name("tbody")
    for tr in table.find_elements_by_tag_name("tr"):
        tds = tr.find_elements_by_tag_name("td")

        name = tds[1].text
        sell = tds[2].text
        if sell not in ['Cannot', '???']:
            sell = int(sell.replace(',',''))

        buy = tds[3].text
        if buy not in ['Cannot', '???']:
            buy = int(buy.replace(',',''))

        print(f'name: "{name}"')
        print(f'sell: "{sell}"')
        print(f'buy: "{buy}"\n')
        frame = frame.append({
            'Name': name,
            'Sell Price': sell,
            'Buy Price': buy
        }, ignore_index=True)

    if len(buttons) > 0:
        next_button = buttons[-1]
        if next_button.text != "NEXT":
            has_more = False
        else:
            print("found next button, click!")
            next_button.click()

    print(f"waiting {wait} seconds...")
    sleep(wait)

print("Done! writing to file...")
frame.to_csv("items.csv", index=False)
