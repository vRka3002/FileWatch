import time
import csv
import sys
import constants as C
from globals import Global

class Products:
    """
        Class to save lowest and highest pricing products and handling the calls for getting the same
    """

    def __init__(
                self, price, vendor='', productname='',
                productcode=0, unit='', weight=0,
                id=0):
        self.id = id
        self.vendor = vendor
        self.productName = productname
        self.productCode = productcode
        self.unit = unit
        self.weight = weight
        self.price = price

    @staticmethod
    def create_product_holder(csvpath):
        """
            Function to create a container to hold the value of cheapest
            and most expensive vendor data for a product

        :type globals.productDict: dictionary to hold min/max value against a product code
        :param csvpath: path of the csv file containing info of the products

        """

        with open(csvpath, 'r') as productsfile:
            reader = csv.reader(productsfile, delimiter=',')
            next(reader)        # Have to start reading from second line as first contains column name
            for row in reader:
                    # If product is already present in current tracker dictionary
                    if row[C.I_CODE] in Global.productDict:
                        # Store product info in temporary variable
                        temp = Global.productDict[row[C.I_CODE]]
                        # Check if product is present and is intended to be removed
                        if row[C.I_PRICE] == C.PRICE_ON_REMOVAL:
                            if temp[C.MIN_VAL_INDEX].vendor == row[C.I_VENDOR]:
                                Global.productDict[row[C.I_CODE]][C.MIN_VAL_INDEX] = Products(C.INVALID_MIN_PRICE)
                            elif temp[C.MAX_VAL_INDEX].vendor == row[C.I_VENDOR]:
                                Global.productDict[row[C.I_CODE]][C.MAX_VAL_INDEX] = Products(C.INVALID_MAX_PRICE)
                        else:
                            # Check if current entry from csv is already present in product dictionary
                            if((temp[C.MIN_VAL_INDEX].vendor == row[C.I_VENDOR] and
                                    float(temp[C.MIN_VAL_INDEX].price) == float(row[C.I_PRICE])) or
                                    (temp[C.MAX_VAL_INDEX].vendor == row[C.I_VENDOR] and
                                    float(temp[C.MAX_VAL_INDEX].price) == float(row[C.I_PRICE]))):
                                pass
                            # else this is a new entry, proceed
                            else:
                                # Replace min index value if current vendor offers less price
                                if float(temp[C.MIN_VAL_INDEX].price) > float(row[C.I_PRICE]) or \
                                            temp[C.MIN_VAL_INDEX].vendor == row[C.I_VENDOR] or \
                                            temp[C.MIN_VAL_INDEX].price == C.INVALID_MAX_PRICE:
                                    Global.productDict[row[C.I_CODE]][C.MIN_VAL_INDEX] = Products(
                                        row[C.I_PRICE], row[C.I_VENDOR], row[C.I_CODE],
                                        row[C.I_UNIT], row[C.I_UNIT], row[C.I_WEIGHT],
                                        row[C.I_ID]
                                    )
                                # Replace max index value if current vendor offer greater price
                                if float(temp[C.MAX_VAL_INDEX].price) < float(row[C.I_PRICE]) or \
                                                temp[C.MAX_VAL_INDEX].vendor == row[C.I_VENDOR] or \
                                                temp[C.MAX_VAL_INDEX].price == C.INVALID_MIN_PRICE:
                                    Global.productDict[row[C.I_CODE]][C.MAX_VAL_INDEX] = Products(
                                        row[C.I_PRICE], row[C.I_VENDOR], row[C.I_CODE],
                                        row[C.I_UNIT], row[C.I_UNIT], row[C.I_WEIGHT],
                                        row[C.I_ID]
                                    )
                    # Else product will be inserted for the first time
                    else:
                        # Form object with details new product
                        newvalue = Products(
                                            row[C.I_PRICE], row[C.I_VENDOR], row[C.I_CODE],
                                            row[C.I_UNIT], row[C.I_UNIT], row[C.I_WEIGHT],
                                            row[C.I_ID]
                                            )
                        # Initialize to store min and max data for this product id
                        Global.productDict[row[C.I_CODE]] = [newvalue, newvalue]

    @staticmethod
    def fetch_min_values():
        """
            Function to return products along with there minimum price value details
        :return: Products with miminum price details
        """
        details = []
        # Iterate product holder dictionary
        for key, value in Global.productDict.iteritems():
            details.append(value[C.MIN_VAL_INDEX])

        # Return the extracted data
        return details

    @staticmethod
    def fetch_max_values():
        """
            Function to return products along with there maximum price value details
        :return: Products with maximum price details
        """
        details = []
        # Iterate product holder dictionary
        for key, value in Global.productDict.iteritems():
            details.append(value[C.MAX_VAL_INDEX])
        # Return the list to callee
        return details

    @staticmethod
    def print_data(data):
        """
            Function to display data to user
        :param data: Data to be displayed
        :return: None
        """
        print "####################"
        print "DESIRED DATA SET -- "
        for value in data:
            info = [value.id, value.vendor, value.productName, value.productCode, value.unit, value.weight, value.price]
            print(','.join(str(x) for x in info))
        print "####################"


    @staticmethod
    def get_specific_min_price(code_list):
        """
            Function to return data of products with associated minimum price
        :param code_list: List containing codes of products
        :return: Data for desired products
        """
        details = []
        for code in code_list:
            details.append(Global.productDict[code][C.MIN_VAL_INDEX])

        # Return data
        return details
