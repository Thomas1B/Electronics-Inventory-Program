'''
Script to handle the datasheets.

This script uses the pandas module to handle the data.
'''

import pandas as pd
import numpy as np
import os

labels = ['Digi-Key Part #', 'Manufacturer Part Number',
          'Description', 'Customer Reference', 'Unit Price', 'Quantity']


'''
creating dictionary of Category classes for the inventory.

Rememeber when adding new categories to add the nessecary conditions
in sort_order().

'''
dict_keys = [
    'Resistors',
    'Capacitors',
    'Inductors',
    'Transistors',
    'Diodes',
    'Regulator',
    'ICs',
    "Logic Gates",
    'Connectors',
    'Displays',
    'Buttons, Switches',
    'LEDs',
    'Audio',
    'Potentiometer',
    'Modules',
    'Fans',
    'ACDC Converters',
    'AC Transformer',
    'Resonators, Crystals',
    'Encoders',
    'Relay',
    'Other'
]


class Category:
    '''
    Catergory Class for electronic part.

    Attributes:
        category: what type of category. Ex: Resistors, Capacitors...
    '''

    def __init__(self, category: str) -> None:
        # dataframe to store the data.
        self.items = pd.DataFrame()
        # type of component, i.e: Resistors, Capacitors, etc.
        self.category = category

    def get_items(self) -> pd.DataFrame:
        '''
        Function to return dataframe of Category's items.
        '''
        return self.items

    def get_category(self) -> str:
        '''
        Function to return Category's type.
        '''
        return self.category

    def add_item(self, items: pd.DataFrame | list | pd.Series) -> None:
        '''
        Function to add items to category.
        'items' can be a dataframe, list of Series, or a single Serie of item(s).
        '''

        # checking if 'items' is a Series, list or a dataframe.
        if type(items) == pd.Series:
            self.items = pd.concat([
                self.items,
                pd.DataFrame(items).T
            ]).reset_index(drop=True)
        elif type(items) == list:
            self.items = pd.concat([
                self.items,
                pd.DataFrame(items)
            ]).reset_index(drop=True)
        elif type(items) == pd.DataFrame:
            self.items = pd.concat([
                self.items,
                items
            ]).reset_index(drop=True)

        # updating item some descriptions
        update_dict = {
            'RES': 'Resistor',
            'CAP': 'Capacitor',
            'IND': 'Inductor',
            'TRANS NPN': "TRANSISTOR NPN",
            'TRANS PNP': "TRANSISTOR PNP"
        }
        # for key, value in update_dict.items():
        #     self.items['Description'] = self.items['Description'].str.replace(
        #         key, value.upper(), case=False, n=1)

        # Changing the datatype of 'Quantity' and 'Unit Price'.
        # (Fixes bugs in later code)
        self.items['Quantity'] = self.get_items()[
            'Quantity'].astype(float)
        self.get_items()['Unit Price'] = self.get_items()[
            'Unit Price'].astype(float)

    def remove_duplicates(self, update_info=True) -> None:
        '''
        Function to remove duplicates (Part Number) and can update the quantities and unit prices of items.

        Parameters:
            update_quantity - bool, default True: if "False" doesn't update quantities and unit prices.

        Made using ChatGPT.
        '''
        self.get_items().sort_values(
            [labels[0], 'Unit Price'], ascending=[True, False], inplace=True)

        # whether to update the quantity and unit price, default - True.
        if update_info:
            self.get_items()['Quantity'] = self.get_items().groupby(
                labels[0])['Quantity'].transform('sum')
            self.get_items()['Unit Price'] = self.get_items().groupby(
                labels[0])['Unit Price'].transform('max')

        self.get_items().drop_duplicates(
            # Dropping duplicates based on DigiKey part #.
            subset=labels[0],
            keep='first',
            inplace=True)
        self.get_items().reset_index(inplace=True)
        self.get_items().sort_values('index', inplace=True)
        self.get_items().reset_index(drop=True, inplace=True)
        self.get_items().drop(columns=['index'], inplace=True)

    def save_toexcel(self, writer=None) -> None:
        '''
        Function to save the Category as a excel file, can be saved
        in a spreadsheet of multiple sheets.

        Parameters:
            writer - pd.ExcelWriter default none:
                     only pass 'writer' when saving in a group of other sheets.
        '''
        if writer:
            if self.items.empty:
                self.items = pd.DataFrame(columns=labels)
            self.items.to_excel(writer, sheet_name=self.category, index=False)
        else:
            with pd.ExcelWriter(f'Saved_Files/{self.category}.xlsx') as writer:
                self.items.to_excel(
                    writer,
                    sheet_name=self.category,
                    index=False
                )

    def save_tocsv(self, group=False) -> None:
        '''
        Function to save dataframe as a '.csv' file

        Parameters:
            group - bool, default False: combining with other dataframes.
        '''
        if group:
            return self.get_items()
        else:
            _ = self.get_items().to_csv(
                f'Saved Filed/{self.get_category()}.csv')

    def get_sorted_quantity(self, ascending=True) -> pd.DataFrame:
        '''
        Function to return the category sorted by quantity, by increasing or dreceasing quantities.

            Parameters:
                acsending: True - increaing quantity, False decreasing quantity.
        '''
        return self.items.sort_values('Quantity', ascending=ascending).reset_index(drop=True)

    def get_sorted_price(self, ascending=True) -> pd.DataFrame:
        '''
        Function to return the category sorted by unit price, by increasing or dreceasing unit prices.

            Parameters:
                acsending: True - increaing quantity, False decreasing quantity.
        '''
        return self.items.sort_values('Unit Price', ascending=ascending).reset_index(drop=True)

    def get_sorted_part_num(self) -> pd.DataFrame:
        '''
        Function to return the category items sorted by part number.
        '''
        return self.items.sort_values('Part Number').reset_index(drop=True)

    def get_sorted_man_num(self) -> pd.DataFrame:
        '''
        Function to return the category items sorted by manufacturer part number.
        '''
        return self.items.sort_values('Manufacturer Part Number').reset_index(drop=True)

    def drop_all_items(self) -> None:
        '''
        Function to drop all items in the dataframe.
        '''
        self.items.drop(self.items.index, inplace=True)

    def get_subtotal(self) -> float:
        '''
        Function to get the subtotal of all the items in the category.

            Returns:
                float
        '''
        subtotal = 0
        for i in range(self.items.shape[0]):
            subtotal += float(self.items.iloc[i]['Quantity']) * \
                float(self.items.iloc[i]['Unit Price'])
        return subtotal


'''
dictionary used a temporary holder for opening files.
'''
# Inventory = {key: Category(key) for key in dict_keys}
# Items = {key: Category(key) for key in Inventory.keys()}


class Data:
    def __init__(self, sections: list):
        '''
            Parameters:
                sections: list of category names.
        '''
        self.sections = sections
        self.data = {section: Category(section) for section in sections}

    def get_sections(self) -> list:
        '''
        Function to get the avaliable category.

            Returns:
                list of cateogory names.
        '''
        return self.sections

    def get_data(self, section='all') -> pd.DataFrame:
        '''
        Function to get the data

            Parameters:
                section: category name to get items from.
        '''
        if section == 'all':
            return self.to_dataframe()
        else:
            return self.data[section].get_items()

    def add_item(self, items: pd.DataFrame | list | pd.Series, section: str) -> None:
        '''
        Function to add items to the data dictionary.

            Parameters:
                key: what category to add items to.
                items: Dataframe, list of Series, or single Serie of items.
        '''
        self.data[section].add_item(items)

    def remove_duplicates(self, section='all', update_info=True) -> None:
        '''
        Function to remove duplicates (Part Number) and can update the quantities and unit prices of items.

        Parameters:
            section: what section to remove duplicates from, (default all).
            update_info - bool, default True: if "False" doesn't update quantities and unit prices.
        '''

        if section == 'all':
            for section in self.sections:
                self.data[section].remove_duplicates(update_info)
        else:
            self.data[section].remove_duplicates(update_info)

    def drop_all_items(self) -> None:
        '''
        Function to drop all items from each category in the data dictionary.
        '''

        for section in self.sections:
            self.data[section].drop_all_items()

    def check_if_empty(self) -> bool:
        '''
        Function to check if a dictionary has any items.

            Returns:
                True if dictionary has any items.
        '''
        for key in self.sections:
            if self.data[key].get_items().empty:
                return True
        return False

    def to_dataframe(self) -> pd.DataFrame:
        '''
        Function to convert the data dictionary into a single dataframe.

            Returns:
                single dataframe of entire data dictionary.
        '''

        items = pd.concat([self.data[cat].get_items()
                           for cat in self.sections]).reset_index(drop=True)
        return items

    def get_subtotal(self) -> float:
        '''
        Function to get the subtotal of the data dictionary.

            Returns:
                float
        '''
        subtotal = 0
        for section in self.sections:
            subtotal += self.data[section].get_subtotal()
        return subtotal

    def get_item_category(self, item: pd.DataFrame) -> str:
        '''
        Function to get the category an item belongs to.

            Parameters:
                item: DataFrame of item.
        '''
        category = None
        for i, df in enumerate(sort_order(item)):
            if not df.empty:
                category = list(self.sections)[i]
                break

        return category

    def update_item(self, item: pd.DataFrame, delete=False) -> None:
        '''
        Function to update an item.
        Triggered when item is editted (see get_editted() in project_window.py).

            Parameter:
                item - DataFrame: dataframe of the item.
                delete - bool: drop item (default false).
        '''

        # getting item category
        category = self.get_item_category(item)

        # updating the item in the dictionary
        category_items = self.data[category].get_items()
        for i in range(category_items.shape[0]):
            # checking if item's description matches any in each category.
            if category_items.iloc[i]['Description'] == item["Description"].iloc[0]:
                self.editted_save = False
                if delete:
                    self.data[category].get_items().drop(
                        index=i, inplace=True)
                else:
                    self.data[category].get_items().iloc[i] = item.iloc[0]
                break


Inventory = Data(dict_keys)
Items = Data(dict_keys)


def sort_order(order: pd.DataFrame) -> list:
    '''
    Function to sort an order (or any dataframe) into categories based on the item description.
    (i.e: Resistors, Capacitors, etc...)

        Parameter
            order - DataFrame: dataframe of items.

        Returns:
            list of dataframe for each category.
    '''

    # list of key description words to sorting items
    ac_transformer_conds = ['AC/AC', 'AC Transformer', 'AC Trans']
    pot_conds = ['potentiometer', 'pot']
    acdc_conds = ['AC/DC', 'AC/DC Converter', 'ACDC']
    fan_conds = ['fan', 'fans']
    audio_conds = ['speaker', 'audio', 'mp3']
    ics_conds = ['ics', 'ic']
    diodes_conds = ['diode']
    modules_conds = ['modules', 'module']
    connectors_conds = ['conn', 'term', 'socket', 'receptacle']
    capacitors_conds = ['cap', 'capacitor', 'capacitors']
    resistors_conds = ['res', 'resistor', 'resistors']
    leds_conds = ['leds', 'led', 'light']
    transistors_conds = ['transistors', 'transistor', 'NPN', "PNP"]
    inductors_conds = ['inductors', 'inductor', 'ind']
    displays_conds = ['display', 'screen']
    buttons_conds = ['button', 'switch', 'tact']
    regulator_conds = ['reg', 'regulator']
    resonator_conds = ['crystal', 'resonator']
    encoder_conds = ['encoder']
    relay_conds = ['relay']

    # empty lists for parts to be added.
    # if adding new sections, dont forget to add
    ac_transformer, potentiometer = [], []
    acdc, audio, fans = [], [], []
    resistors, capacitors, inductors = [], [], []
    transistors, diodes, ics = [], [], []
    leds, connectors, buttons = [], [], []
    displays, modules, other = [], [], []
    regulator, logic_gates, resonators = [], [], []
    encoders, relay = [], []

    # THIS NEEDS TO BE IN THE SAME ORDER AS THE INVENTORY DICTIONARY!
    # Otherwise when showing a category it will display an unintended one.
    sections = [
        resistors, capacitors, inductors, transistors,
        diodes, regulator, ics, logic_gates, connectors, displays, buttons, leds,
        audio, potentiometer, modules, fans, acdc, ac_transformer, resonators, encoders,
        relay,
        other
    ]

    # sorting the order into categories by checking if any words from
    # the conditions are in the item description.
    for i, descrip in enumerate(order['Description']):
        line = descrip.lower().split()

        if any(word.lower() in line for word in ac_transformer_conds):
            ac_transformer.append(order.iloc[i])

        elif any(word.lower() in line for word in regulator_conds):
            regulator.append(order.iloc[i])

        elif any(word.lower() in line for word in pot_conds):
            potentiometer.append(order.iloc[i])

        elif any(word.lower() in line for word in acdc_conds):
            acdc.append(order.iloc[i])

        elif any(word.lower() in line for word in fan_conds):
            fans.append(order.iloc[i])

        elif (
            any(word.lower() in line for word in audio_conds) or
            all(word.lower() in line for word in ['board', 'max9744'])
        ):
            audio.append(order.iloc[i])

        elif any(word.lower() in line for word in ics_conds):
            if any(word.lower() in line for word in ['gate']):
                logic_gates.append(order.iloc[i])
            else:
                ics.append(order.iloc[i])

        elif any(word.lower() in line for word in diodes_conds):
            diodes.append(order.iloc[i])

        elif any(word.lower() in line for word in modules_conds):
            modules.append(order.iloc[i])

        elif any(word.lower() in line for word in connectors_conds):
            connectors.append(order.iloc[i])

        elif any(word.lower() in line for word in capacitors_conds):
            capacitors.append(order.iloc[i])

        elif any(word.lower() in line for word in resistors_conds):
            resistors.append(order.iloc[i])

        elif any(word.lower() in line for word in leds_conds):
            leds.append(order.iloc[i])

        elif any(word.lower() in line for word in transistors_conds) and any('trans' in word for word in line):
            transistors.append(order.iloc[i])

        elif any(word.lower() in line for word in inductors_conds):
            inductors.append(order.iloc[i])

        elif any(word.lower() in line for word in displays_conds):
            displays.append(order.iloc[i])

        elif any(word.lower() in line for word in buttons_conds):
            buttons.append(order.iloc[i])

        elif any(word.lower() in line for word in resonator_conds):
            resonators.append(order.iloc[i])

        elif any(word.lower() in line for word in encoder_conds):
            encoders.append(order.iloc[i])
            
        elif any(word.lower() in line for word in relay_conds):
            relay.append(order.iloc[i])

        else:  # left over
            other.append(order.iloc[i])

    # returning list of dataframe for each category.
    return [pd.DataFrame(section) for section in sections]


def sort_by(self, index: int, data: pd.DataFrame) -> pd.DataFrame:
    '''
    Function to sort a dataframe by a column header.

        Parameters:
            index: index of column.
            data: Dataframe to sort.

        Returns:
            sorted DataFrame.
    '''
    header = labels[index]  # column header name

    # condition to fix datatype sorting issues with strings.
    if header == 'Quantity':
        data['Quantity'] = data['Quantity'].astype(int)
    elif header == 'Unit Price':
        data['Unit Price'] = data['Unit Price'].astype(float)

    if self.sort_by[header]:
        self.sort_by[header] = False
        data = data.sort_values(by=header).reset_index(drop=True)
    else:
        self.sort_by[header] = True
        data = data.sort_values(
            by=header, ascending=False).reset_index(drop=True)

    return data


def dict_to_dataframe(dictionary: dict) -> pd.DataFrame:
    '''
    Function to convert a category dictionary into a dataframe.

        Parameters:
            dictionary: dict of Category classes.

        Returns:
            single dataframe of entire dictionary.
    '''

    items = pd.concat([dictionary[cat].get_items()
                      for cat in dictionary]).reset_index(drop=True)
    return items


def dataframe_to_dict(dataframes=[]) -> dict:
    '''
    Function to convert a list of dataframes into a category dictionary.

            Parameter:
                dataframes: list of dataframes

            Returns:
                dictionary of categories.
    '''

    new_dict = {}
    keys = Inventory.get_sections()
    for dataframe, key in zip(dataframes, keys):
        new_dict[key] = dataframe
    return new_dict


def load_Inventory() -> None:
    '''
    Function to check if inventory exists, if it does then load the Inventory dictionary data.
    '''
    if not os.path.exists("Saved_Lists/Inventory.xlsx"):
        return 'Inventory missing...'
    else:
        # loading the Inventory dictionary data
        _ = get_inventory(check_load=False)


def get_inventory(check_load=True) -> dict:
    '''
    Function to get current inventory from the inventory.xlsx (excel) file.

        Parameters:
            check_load: DO NOT CHANGE, NEEDS FOR SET UP.

        Returns:
            Dictionary of class for each sheet in the excel file.
    '''
    if check_load == False:  # only runs one for set up
        inventory = pd.read_excel(
            'Saved_Lists/Inventory.xlsx', sheet_name=None)
        for section in inventory.keys():
            Inventory.data[section].add_item(inventory[section])
        check_load = True

    return Inventory.data


def get_ordersheet(filepath: str) -> list:
    '''
    Function to read in an ordersheet using pandas.

    Drops columns: 'Index', 'Backorder', 'Extended Price' from the dataframes
    and the subtotal line ONLY from the csv file.

        Parameters:
            filepath - str: filepath to the othersheet.

        Returns:
            a list of dataframes for each category, (see sort_order()).
    '''
    if os.path.isfile(filepath):
        filetype = filepath.split(".")[-1]

        order = None
        if filetype == 'csv':
            order = pd.read_csv(filepath)
            if str(order.iloc[-1]["Unit Price"]).lower() == 'subtotal':
                # if subtotal line exists drop it.
                order = order.drop(order.index[-1], axis=0)

        elif filetype == 'xlsx':
            # subtotal line needs to be removed from the xlsx manual.
            # Need to fix this...
            order = pd.read_excel(filepath)

        # condition for when getting a order that has this labels dropped already.
        order = order[labels]
        order[labels].reset_index(drop=True, inplace=True)  # reindexing
        if order['Unit Price'].dtype != float:
            order['Unit Price'] = order['Unit Price'].str.strip(to_strip='$')

        # retyping some item descriptions, i.e RES -> Resistor
        update_dict = {
            'RES': 'Resistor',
            'CAP': 'Capacitor',
            'IND': 'Inductor',
        }
        for key, value in update_dict.items():
            if key in order['Description']:
                order['Description'] = order['Description'].str.replace(
                    key, value.upper(), case=False, n=1)

        order = sort_order(order)  # sorting the order
        return order


def add_order_to_Inventory(order) -> None:
    '''
    Function to add a new order to the inventory

        Parameter:
            order: dict of categories or single dataframe.
    '''

    if type(order) == dict:
        for section in Inventory.get_sections():
            # checking if pass 'order' is empty
            if not order[section].get_items().empty:
                Inventory.data[section].add_item(order[section].get_items())
                Inventory.data[section].remove_duplicates()
    else:
        for items, section in zip(order, Inventory.get_sections()):
            if not items.empty:
                Inventory.data[section].add_item(items)
                Inventory.data[section].remove_duplicates()


def load_Items(self, order: list) -> None:
    '''
    Function to load items into the Item dictionary.

        Parameters:
            order: list of items to load into the the dictionary
    '''
    self.Items.drop_all_items()
    for items, section in zip(order, Items.get_sections()):
        if len(order) > 0:
            if not items.empty:
                self.Items.add_item(items=items, section=section)
                self.Items.remove_duplicates(section=section)


if __name__ == "__main__":
    print('Running check inventory file...')
    result = load_Inventory()
    if not result:
        print("Inventory file exists.")
    else:
        print("Inventory file does not exists.")
