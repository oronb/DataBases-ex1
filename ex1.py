from enum import Enum

# Declare Constants
CUSTOMERS_TABLE_NAME = "Customers"
ORDERS_TABLE_NAME = "Orders"

NAME_COL_NAME = "Name"
AGE_COL_NAME = "Age"
PRICE_COL_NAME = "Price"
CUSTOMER_NAME_COL_NAME = "CustomerName"
PRODUCT_COL_NAME = "Product"


class Tables(Enum):
    CUSTOMERS = 1
    ORDERS = 2
    ALL = 3


def str_contain_only_spaces(string):
    string = string.replace(" ", "")
    if len(string) == 0:
        return True
    else:
        return False


def check_columns(string, name_of_table):
    if string.find("*") >= 0:
        if (len(string.strip())) > 1:
            return False
        else:
            return True
    comma_ind = string.find(",")
    if comma_ind < 0:
        return check_valid_column_from_table(string, name_of_table)
    else:
        left_string = string[:comma_ind]
        right_string = string[comma_ind + 1:]
        valid_left_part = check_valid_column_from_table(left_string, name_of_table)
        if not valid_left_part:
            return False
        return check_columns(right_string, name_of_table)


def check_valid_column_from_table(string, name_of_table):
    separator = "."
    string = string.replace(" ", "")
    place_of_dot = string.find(separator)
    if place_of_dot == -1:
        return False
    table = get_table_from_attribute(string)
    col = get_col_from_attribute(string)
    if name_of_table == Tables.ORDERS or name_of_table == Tables.ALL:
        if check_if_col_in_orders_col(col) and table == ORDERS_TABLE_NAME:
            return True
    if name_of_table == Tables.CUSTOMERS or name_of_table == Tables.ALL:
        if check_if_col_in_customers_col(col) and table == CUSTOMERS_TABLE_NAME:
            return True
    return False


def get_table_from_attribute(string):
    string_after_split = string.split(sep=".", maxsplit=2)
    return string_after_split[0]


def check_if_col_in_customers_col(col):
    return col == NAME_COL_NAME or col == AGE_COL_NAME


def check_if_col_in_orders_col(col):
    return col == CUSTOMER_NAME_COL_NAME or col == PRODUCT_COL_NAME or col == PRICE_COL_NAME


def get_col_from_attribute(string):
    string_after_split = string.split(sep=".", maxsplit=2)
    return string_after_split[1]


def check_tables(string):
    comma_ind = string.find(",")
    if comma_ind < 0:
        return check_valid_table(string)
    else:
        left_string = string[:comma_ind]
        right_string = string[comma_ind + 1:]
        valid_left_part = check_valid_table(left_string)
        if not valid_left_part:
            return False
        return check_tables(right_string)


def check_valid_table(string):
    string = string.replace(" ", "")
    if string == CUSTOMERS_TABLE_NAME or string == ORDERS_TABLE_NAME:
        return True
    else:
        return False


def check_cond(string):
    string = string.strip()
    if cond_has_outer_parenthesis(string):
        stripped_string = string[1:-1]  # strip the outer parenthesis and re-check the trimmed string
        if check_cond(stripped_string):  # perform the condition without outer parenthesis
            return True
    # WHILE loop that goes over all the operators:
    location_to_look_from = 0
    last_ind = len(string) - 1
    while location_to_look_from <= last_ind:
        operator_ind = find_operator_ind(string, location_to_look_from)
        if operator_ind < 0:  # no operator found from given location
            if location_to_look_from == 0:  # no AND or OR operators at all in string
                return check_simple_cond(string)
            else:  # string does have some AND or OR operator
                return False
        else:  # found an operator
            ind_after_operator = find_ind_after_operator(string, operator_ind)
            string_left_of_operator = string[:operator_ind]
            string_right_of_operator = string[ind_after_operator:]
            if check_cond(string_left_of_operator) and check_cond(string_right_of_operator):
                return True
            else:
                location_to_look_from = ind_after_operator


def check_simple_cond(string):
    ind_of_rel_op = find_rel_op_ind(string)
    if ind_of_rel_op < 1 or ind_of_rel_op >= len(string) - 1:
        return False
    ind_after_rel_op = find_ind_after_rel_op(string, ind_of_rel_op)
    if ind_after_rel_op >= len(string):
        return False
    string_left_of_rel_op = string[:ind_of_rel_op]
    string_right_of_rel_op = string[ind_after_rel_op:]
    return is_constant(string_left_of_rel_op, string_right_of_rel_op)


def find_rel_op_ind(string):
    ind_small = string.find('<')
    if ind_small >= 0:
        return ind_small
    ind_big = string.find('>')
    if ind_big >= 0:
        return ind_big
    ind_eq = string.find('=')
    if ind_eq >= 0:
        return ind_eq
    return -1


def find_ind_after_rel_op(string, ind_of_rel_op):
    ind_after_rel_op = ind_of_rel_op + 1
    if string[ind_of_rel_op] == '<':
        if string[ind_after_rel_op] == '=':
            ind_after_rel_op += 1
        if string[ind_after_rel_op] == '>':
            ind_after_rel_op += 1
    if string[ind_of_rel_op] == '>':
        if string[ind_after_rel_op] == '=':
            ind_after_rel_op += 1
    return ind_after_rel_op


def check_if_const_is_str(string):
    return (string.startswith("'") and string.endswith("'")) or (string.startswith("\"") and string.endswith("\""))


def check_if_str_is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_constant(string1, string2):
    stripped_string1 = string1.strip()
    stripped_string2 = string2.strip()
    string1_is_col = check_valid_column_from_table(stripped_string1, Tables.ALL)
    string2_is_col = check_valid_column_from_table(stripped_string2, Tables.ALL)
    if check_if_str_is_int(stripped_string1) and check_if_str_is_int(stripped_string2):
        return True
    if string1_is_col and string2_is_col:
        col1 = get_col_from_attribute(stripped_string1)
        col2 = get_col_from_attribute(stripped_string2)
        if check_same_attribute_type(col1, col2):
            return True
    if string1_is_col:
        col = get_col_from_attribute(stripped_string1)
        if check_if_const_type_valid(col, stripped_string2):
            return True
    if string2_is_col:
        col = get_col_from_attribute(stripped_string2)
        if check_if_const_type_valid(col, stripped_string1):
            return True


def check_if_const_type_valid(col_to_compare, const):
    if check_if_attribute_is_string_type(col_to_compare):
        return check_if_const_is_str(const)
    elif check_if_attribute_is_int_type(col_to_compare):
        return check_if_str_is_int(const)
    else:
        return False


def check_if_attribute_is_string_type(col):
    return col == NAME_COL_NAME or \
            col == CUSTOMER_NAME_COL_NAME or col == PRODUCT_COL_NAME


def check_if_attribute_is_int_type(col):
    col == AGE_COL_NAME or col == PRICE_COL_NAME


def check_same_attribute_type(col1, col2):
    if check_if_attribute_is_string_type(col1) and check_if_attribute_is_string_type(col2):
        return True
    elif check_if_attribute_is_int_type(col1) and check_if_attribute_is_int_type(col2):
        return True
    else:
        return False


def cond_has_outer_parenthesis(string):
    stripped_string = string.strip()
    return stripped_string[0] == '(' and stripped_string[-1] == ')'


def find_operator_ind(string, location_to_look_from):
    and_ind = string.find("AND", location_to_look_from)
    or_ind = string.find("OR", location_to_look_from)
    if and_ind < 0 and or_ind < 0:  # no AND or OR operators in string from given index
        return -1
    else:
        # find first of the two operators:
        if and_ind < or_ind:
            if and_ind >= 0:
                first_operator_ind = and_ind
            else:
                first_operator_ind = or_ind
        else:
            if or_ind >= 0:
                first_operator_ind = or_ind
            else:
                first_operator_ind = and_ind
        return first_operator_ind


def find_ind_after_operator(string, operator_ind):
    if string[operator_ind] == 'A':
        ind_after_operator = operator_ind + 3
    else:  # operator is OR
        ind_after_operator = operator_ind + 2
    return ind_after_operator


def get_table_name(string):
    if CUSTOMERS_TABLE_NAME in string and ORDERS_TABLE_NAME in string:
        return Tables.ALL
    elif CUSTOMERS_TABLE_NAME in string:
        return Tables.CUSTOMERS
    elif ORDERS_TABLE_NAME in string:
        return Tables.ORDERS


def check_dist_in_location(location_of_select, location_of_distinct, location_after_from):
    return location_of_select < location_of_distinct < location_after_from


def check_distinct(string, location_of_select, location_of_distinct, location_after_from):
    str_between_select_and_distinct = string[location_after_SELECT:location_of_DISTINCT]
    location_exists = location_of_DISTINCT != -1
    dist_in_location = check_dist_in_location(location_of_select, location_of_distinct, location_after_from)
    only_spaces_between_select_and_distinct = str_contain_only_spaces(str_between_select_and_distinct)
    return location_exists and dist_in_location and only_spaces_between_select_and_distinct


# CONDITION CHECKS:
# query = "\"SELECT Customers.Name FROM Customers WHERE  Customers.Age>5 OR 'Mike'<=Customers.Name AND Customers.Name=\"x\""  # VALID
# query = "SELECT DISTINCT Customers.Name  FROM Customers  WHERE  ( (Customers.Age>5)   OR ( ('Mike'<=Customers.Name) ));" # VALID
# query = "SELECT Customers.Name FROM Customers WHERE Customers.Age=25;"  # VALID
# query = "SELECT Customers.Name FROM Customers WHERE Customers.Name='Mike';"
# query = "SELECT  Customers.Name FROM  Customers WHERE DISTINCT Customer.Age=25;"
query = "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName;"
# query = "SELECT Customers.CustomerName,Orders.Price FROM Customers,Orders WHERE Customer.Name=Orders.CustomerName AND Orders.Price>1000;"
# query = "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customer.Name=Orders.CustomerName) AND Orders.Price>1000;"
# query = "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customer.Name=Orders.CustomerName) OR (Orders.Price>59);"

# query = input("Enter a query: ")
print(query)

query = query.strip()
if query.endswith(";"):
    query = query[:-1]

location_of_SELECT = query.find("SELECT")
location_after_SELECT = location_of_SELECT + 6
location_of_DISTINCT = query.find("DISTINCT")
location_of_FROM = query.find("FROM")
location_after_FROM = location_of_FROM + 4
location_of_WHERE = query.find("WHERE")
location_after_WHERE = location_of_WHERE + 5

if check_distinct(query, location_of_SELECT, location_of_DISTINCT, location_of_FROM):
    location_after_SELECT = location_of_DISTINCT + 8

string_after_select = query[location_after_SELECT:location_of_FROM]
string_after_from = query[location_after_FROM:location_of_WHERE]
string_after_where = query[location_after_WHERE:]

if check_tables(string_after_from):
    table_name = get_table_name(string_after_from)
    if check_columns(string_after_select, table_name):
        if check_cond(
                string_after_where):  # TODO decide if we need to check if the conditions apply to the specific table
            print("Valid")
        else:
            print("Invalid")
            print("Parsing <condition> failed")
    else:
        print("Invalid")
        print("Parsing <attribute_list> failed")
else:
    print("Invalid")
    print("Parsing <table_list> failed")
