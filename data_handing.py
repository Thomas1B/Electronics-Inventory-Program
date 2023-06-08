'''
Class and Functions to handle the datasheets.

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

    def add_item(self, item):
        '''
        Function to add_item to category.
        'item' can be a dataframe, list of series, or a single series of item(s).
        '''

        if type(item) == pd.Series:
            self.items = pd.concat(
                [self.items, pd.DataFrame(item).T]).reset_index(drop=True)
        elif type(item) == list:
            self.items = pd.concat(
                [self.items, pd.DataFrame(item)]).reset_index(drop=True)
        elif type(item) == pd.DataFrame:
            self.items = pd.concat([self.items, item]).reset_index(drop=True)

        self.get_items()['Quantity'] = self.get_items()[
            'Quantity'].astype(float)
        self.get_items()['Unit Price'] = self.get_items()[
            'Unit Price'].astype(float)

    def remove_duplicates(self, update_info=True):
        '''
        Function to remove duplicates and updates the quantity.

        Parameters:
            update_quantity - bool, default true: if "False" doesn't update quantity.

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
        Function to save the Category as a excel file.

        only pass 'writer' when saving in a group of other sheets.
        '''
        if writer:
            self.items.to_excel(writer, sheet_name=self.category, index=False)
        else:
            with pd.ExcelWriter(f'Saved_Files{self.category}.xlsx') as writer:
                self.items.to_excel(
                    writer, sheet_name=self.category, index=False)

    def save_tocsv(self, group=False):
        '''
        Function to save dataframe as a '.csv' file

        Parameters:
            group - bool, default False: combining with other dataframes.
        '''
        if group:
            return self.get_items()
        else:
            csv = self.get_items().to_csv(
                f'Saved Filed/{self.get_category()}.csv')

    def get_sorted_quantity(self, ascending=True):
        '''
        Function to return a dataframe sorted by quantity, by increasing or dreceasing.

        Parameters: acsending - bool (default true)
        '''
        return self.items.sort_values('Quantity', ascending=ascending).reset_index(drop=True)

    def get_sorted_price(self, ascending=True):
        '''
        Function to return a dataframe sorted by unit price, by increasing or dreceasing.

        Parameters: acsending - bool (default true)
        '''
        return self.items.sort_values('Unit Price', ascending=ascending).reset_index(drop=True)

    def get_sorted_part_num(self):
        '''
        Function to return a dataframe sorted by part number, by increasing or dreceasing.

        Parameters: acsending - bool (default true)
        '''
        return self.items.sort_values('Part Number').reset_index(drop=True)

    def get_sorted_man_num(self):
        '''
        Function to return a dataframe sorted by manufacturer part number, by increasing or dreceasing.

        Parameters: acsending - bool (default true)
        '''
        return self.items.sort_values('Manufacturer Part Number').reset_index(drop=True)


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
    'Other': Category("Other"),
    'Modules': Category('Modules'),
}


def load_Inventory():
    '''
    Function to check if inventory exists, if it does then load the Inventory dictionary data.

    '''
    if not os.path.exists("Inventory.xlsx"):
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
        inventory = pd.read_excel('Inventory.xlsx', sheet_name=None)
        for section in inventory:
            Inventory[section].add_item(inventory[section])
        check_load = True

    return Inventory


def sort_order(order):
    '''
    Function to sort a given order.

    Parameter
        order: dataframe.

    Return list of dataframe for each category.
    '''

    '''
    Conditions for each catergory:

        Some strings in the condition are redudant, they may be change later...
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
    resistors = []
    capacitors = []
    inductors = []
    transistors = []
    diodes = []
    ics = []
    connectors = []
    displays = []
    buttons = []
    leds = []
    other = []
    modules = []

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

    sections = [resistors, capacitors, inductors, transistors, diodes,
                ics, connectors, displays, buttons, leds, modules, other]

    return [pd.DataFrame(section) for section in sections]


def get_new_ordersheet(filename):
    '''
    Function to read in a NEW order sheet (csv) and sorts it into categories.

    Returns list of dataframe for each category.


    *** Need to add part for reading excel
    '''
    if os.path.isfile(filename):
        filetype = filename.split(".")[-1]

        order = ''
        if filetype == 'csv':
            order = pd.read_csv(filename)
            order = order.drop(labels_drop, axis=1)  # dropping unwanted labels
            order = order.drop(len(order)-1, axis=0)  # dropping subtotal line

        elif filetype == 'xlsx':
            order = pd.read_excel(filename)
            order = order.drop(labels_drop, axis=1)  # dropping unwanted labels
        else:
            return
        order = order[labels].reset_index(drop=True)  # reindexing dataframe
        order = sort_order(order)
        return order


def inventory_to_dataframe(inv=Inventory):
    '''
    Function to convert the inventory into a dataframe.
    '''
    items = pd.concat([inv[cat].get_items()
                      for cat in inv]).reset_index(drop=True)
    return items


def add_order_to_Inventory(filename, get_user=False):
    '''
    Function to add a new order to the inventory
    '''

    orders = get_new_ordersheet(filename)

    for order, section in zip(orders, Inventory):
        Inventory[section].add_item(order)
        Inventory[section].remove_duplicates()


if __name__ == "__main__":
    print('Running check inventory file...')
    result = load_Inventory()
    if not result:
        print("Inventory file exists.")
