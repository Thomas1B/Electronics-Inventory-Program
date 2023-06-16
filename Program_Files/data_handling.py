'''
Script to handle the datasheets.

This script uses the pandas module to handle the data.
'''

import pandas as pd
import numpy as np
import os

labels_drop = ['Index', 'Backorder', 'Extended Price']
labels = ['Part Number', 'Manufacturer Part Number',
          'Description', 'Customer Reference', 'Unit Price', 'Quantity']


class Category:
    '''
    Catergory Class for electronic part.
    '''

    def __init__(self, category):
        # dataframe to store the data.
        self.items = pd.DataFrame()
        # type of component, i.e: Resistors, Capacitors, etc.
        self.category = category

    def get_items(self):
        '''
        Function to return Category's data
        '''
        return self.items

    def get_category(self):
        '''
        Function to return Category's type
        '''
        return self.category

    def add_item(self, items):
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

        # Changing the datatype of 'Quantity' and 'Unit Price'.
        # (Fixes bugs in later code)
        self.get_items()['Quantity'] = self.get_items()[
            'Quantity'].astype(float)
        self.get_items()['Unit Price'] = self.get_items()[
            'Unit Price'].astype(float)

    def remove_duplicates(self, update_info=True):
        '''
        Function to remove duplicates and can update the quantities and unit prices of items.

        Parameters:
            update_quantity - bool, default True: if "False" doesn't update quantities and unit prices.

        Made using ChatGPT.
        '''
        self.get_items().sort_values(
            ['Part Number', 'Unit Price'], ascending=[True, False], inplace=True)

        # whether to update the quantity and unit price, default - True.
        if update_info:
            self.get_items()['Quantity'] = self.get_items().groupby(
                'Part Number')['Quantity'].transform('sum')
            self.get_items()['Unit Price'] = self.get_items().groupby(
                'Part Number')['Unit Price'].transform('max')

        self.get_items().drop_duplicates(subset='Part Number', keep='first', inplace=True)
        self.get_items().reset_index(inplace=True)
        self.get_items().sort_values('index', inplace=True)
        self.get_items().reset_index(drop=True, inplace=True)
        self.get_items().drop(columns=['index'], inplace=True)

    def save_toexcel(self, writer=None):
        '''
        Function to save the Category as a excel file, can be saved
        in a spreadsheet of multiple sheets.

        Parameters:
            writer - pd.ExcelWriter default none: 
                     only pass 'writer' when saving in a group of other sheets.
        '''
        if writer:
            self.items.to_excel(writer, sheet_name=self.category, index=False)
        else:
            with pd.ExcelWriter(f'Saved_Files/{self.category}.xlsx') as writer:
                self.items.to_excel(
                    writer,
                    sheet_name=self.category,
                    index=False
                )

    def save_tocsv(self, group=False):
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

    def get_sorted_quantity(self, ascending=True):
        '''
        Function to return the category sorted by quantity, by increasing or dreceasing quantities.

        Parameters: acsending - bool (default True): True - increaing quantity, False decreasing quantity.
        '''
        return self.items.sort_values('Quantity', ascending=ascending).reset_index(drop=True)

    def get_sorted_price(self, ascending=True):
        '''
        Function to return the category sorted by unit price, by increasing or dreceasing unit prices.

        Parameters: acsending - bool (default True): True - increasing price, False - decreasing price.
        '''
        return self.items.sort_values('Unit Price', ascending=ascending).reset_index(drop=True)

    def get_sorted_part_num(self):
        '''
        Function to return a dataframe sorted by part number.
        '''
        return self.items.sort_values('Part Number').reset_index(drop=True)

    def get_sorted_man_num(self):
        '''
        Function to return a dataframe sorted by manufacturer part number.
        '''
        return self.items.sort_values('Manufacturer Part Number').reset_index(drop=True)

    def drop_all_items(self):
        '''
        Function to drop all items in the dataframe.
        '''
        self.items.drop(self.items.index, inplace=True)

    def get_subtotal(self):
        '''
        Function to get the subtotal of all the items in the category.

        Returns float
        '''
        subtotal = 0
        for i in range(self.items.shape[0]):
            subtotal += self.items.iloc[i]['Quantity'].astype(
                float)*self.items.iloc[i]['Unit Price'].astype(float)
        return subtotal


# Dictionary of categories for the inventory.
Inventory = {
    'Resistors': Category("Resistors"),
    'Capacitors': Category("Capacitors"),
    'Inductors': Category("Inductors"),
    'Transistors': Category("Transistors"),
    'Diodes': Category('Diodes'),
    "ICs": Category('ICs'),
    "Connectors": Category('Connectors'),
    'Displays': Category('Displays'),
    "Buttons": Category('Buttons'),
    'LEDs': Category('LEDs'),
    'Modules': Category('Modules'),
    'Other': Category("Other"),
}


def dict_to_dataframe(dictionary):
    '''
    Function to convert a dictionary into a dataframe.

    '''
    items = pd.concat([dictionary[cat].get_items()
                      for cat in dictionary]).reset_index(drop=True)
    return items


def dataframe_to_dict(dataframes=[]):
    '''
    Function to convert a list of dataframes into a dictionary, the keys 
    are the type of category.

    Returns dictionary of categories.
    '''

    new_dict = {}
    keys = get_category_types()
    for dataframe, key in zip(dataframes, keys):
        new_dict[key] = dataframe
    return new_dict


def get_category_types():
    '''
    Function return a list of keys from the Iventory class.


    '''
    return Inventory.keys()


def load_Inventory():
    '''
    Function to check if inventory exists, if it does then load the Inventory dictionary data.
    '''
    if not os.path.exists("Saved_Lists/Inventory.xlsx"):
        return 'Inventory missing...'
    else:
        # loading the Inventory dictionary data
        _ = get_inventory(check_load=False)


def get_inventory(check_load=True):
    '''
    Function to get current inventory from the inventory.xlsx (excel) file.

    Returns:
        Dictionary of class for each sheet in the excel file.

    Parameters:
        check_load: DO NOT CHANGE, NEEDS FOR SET UP.
    '''
    if check_load == False:  # only runs one for set up
        inventory = pd.read_excel(
            'Saved_Lists/Inventory.xlsx', sheet_name=None)
        for section in inventory.keys():
            Inventory[section].add_item(inventory[section])
        check_load = True

    return Inventory


def sort_order(order):
    '''
    Function to sort an order (or any dataframe) into categories based on the item description.
    (i.e: Resistors, Capacitors, etc...)

    Parameter
        order: dataframe.

    Return list of dataframe for each category.
    '''

    ics_conds = ['ics', 'ic']
    diodes_conds = ['diode']
    modules_conds = ['modules', 'module']
    connectors_conds = ['conn', 'term']
    capacitors_conds = ['cap']
    resistors_conds = ['res']
    leds_conds = ['leds', 'led', 'light']
    transistors_conds = ['transistors', 'transistor', 'NPN', "PNP"]
    inductors_conds = ['inductors', 'inductor', 'ind']
    displays_conds = ['display', 'screen']
    buttons_conds = ['button', 'switch', 'tact']

    # empty lists for parts to be added.
    # if adding new sections, dont forget to add
    resistors, capacitors, inductors = [], [], []
    transistors, diodes, ics = [], [], []
    leds, connectors, buttons = [], [], []
    displays, modules, other = [], [], []

    # THIS NEEDS TO BE IN THE SAME ORDER AS THE CATEGORY CLASS!
    # Otherwise when showing a category it will display an unintended one.
    sections = [resistors, capacitors, inductors, transistors, diodes,
                ics, connectors, displays, buttons, leds, modules, other]

    # sorting the order into categories by checking if any words from
    # the conditions are in the item description.
    for i, line in enumerate(order['Description']):
        line = line.lower().split()

        if any(word.lower() in line for word in ics_conds):
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
        elif any(word.lower() in line for word in transistors_conds):
            transistors.append(order.iloc[i])
        elif any(word.lower() in line for word in inductors_conds):
            inductors.append(order.iloc[i])
        elif any(word.lower() in line for word in displays_conds):
            displays.append(order.iloc[i])
        elif any(word.lower() in line for word in buttons_conds):
            buttons.append(order.iloc[i])
        else:
            other.append(order.iloc[i])

    # returning list of dataframe for each category.
    return [pd.DataFrame(section) for section in sections]


def get_ordersheet(filepath):
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

        order = ''
        if filetype == 'csv':
            order = pd.read_csv(filepath)
            if str(order.iloc[-1]["Unit Price"]).lower() == 'subtotal':
                # if subtotal line exists drop it.
                order = order.drop(order.index[-1], axis=0)

        elif filetype == 'xlsx':
            # subtotal line needs to be removed from the xlsx manual.
            # Need to fix this...
            order = pd.read_excel(filepath)
        else:
            pass

        # condition for when getting a order that has this labels dropped already.
        if all(col in order.columns for col in labels_drop):
            # dropping unwanted labels
            order.drop(labels_drop, axis=1, inplace=True)
        # reindexing dataframe
        order[labels].reset_index(drop=True, inplace=True)
        # dropping unnamed columns
        unnamed_cols = [
            col for col in order.columns if 'unnamed' in col.lower()
        ]
        order.drop(columns=unnamed_cols, inplace=True)
        # sorting the order into categories of product types.
        order = sort_order(order)
        return order


def add_order_to_Inventory(filename):
    '''
    Function to add a new order to the inventory
    '''

    orders = get_ordersheet(filename)

    for order, section in zip(orders, Inventory.keys()):
        if len(order) > 0:
            Inventory[section].add_item(order)
            Inventory[section].remove_duplicates()


if __name__ == "__main__":
    print('Running check inventory file...')
    result = load_Inventory()
    if not result:
        print("Inventory file exists.")
