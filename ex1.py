# test hi oron

def check_columns(string):
    if string.find("*") >= 0:
        if (len(string.strip())) > 1:
            return False
        else:
            return True

    # TODO check optional distinct
    # TODO if both are fine, send the following code to recursion (make it different function)
    comma_ind = string.find(",")
    if comma_ind < 0:
        return check_valid_column(string)
    else:
        left_string = string[:comma_ind]
        right_string = string[comma_ind + 1:]
        valid_left_part = check_valid_column(left_string)
        if not valid_left_part:
            return False
        return check_columns(right_string)


def check_valid_column(string):
    valid_c_bool = True
    # perform all kinds of checks
    return valid_c_bool


def check_from(string):
    comma_ind = string.find(",")
    if comma_ind < 0:
        return check_valid_column(string)
    else:
        left_string = string[:comma_ind]
        right_string = string[comma_ind + 1:]
        valid_left_part = check_valid_table(left_string)
        if not valid_left_part:
            return False
        return check_from(right_string)


def check_valid_table(string):
    valid_t_bool = True
    # perform all kinds of checks
    return valid_t_bool


# ((X AND Y) AND (X AND Y))
# (X AND Y) AND (X AND Y)

# first_par = 0
# last_par =  [end of string]


def check_cond(string):
    string = string.strip()
    if cond_has_outer_parenthesis(string):
        string = string[1:-1]  # strip the outer parenthesis and re-check the trimmed string
        return check_cond(string)
    else:
        if check_valid_parenthesis(string):
            ind_of_main_operator = find_main_operator_ind(string)
            if ind_of_main_operator < 0:  # no logical operator AND or OR
                return check_simple_cond(string)
            else:
                ind_after_main_operator = find_ind_after_operator(string, ind_of_main_operator)
                left_string = string[:ind_of_main_operator]
                right_string = string[ind_after_main_operator:]
                return check_cond(left_string) and check_cond(right_string)
        else:
            return False


def cond_has_outer_parenthesis(string):
    stripped_string = string.strip()
    if stripped_string[0] != '(' or stripped_string[-1] != ')':
        return False
    else:
        string_without_side_parenthesis = stripped_string[1:-1]
        return check_valid_parenthesis(string_without_side_parenthesis)


def find_main_operator_ind(string):
    last_ind = len(string) - 1
    location_to_look_from = 0
    while location_to_look_from <= last_ind:
        operator_ind = find_operator_ind(string, location_to_look_from)
        if operator_ind < 0:  # no operator found from given location
            return -1
        else:
            ind_after_operator = find_ind_after_operator(string, operator_ind)
            string_left_of_operator = string[:operator_ind]
            string_right_of_operator = string[ind_after_operator:]
            if check_valid_parenthesis(string_left_of_operator) and check_valid_parenthesis(string_right_of_operator):
                return operator_ind
            else:
                location_to_look_from = ind_after_operator


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
                ind_after_operator = and_ind + 3
            else:
                first_operator_ind = or_ind
                ind_after_operator = or_ind + 2
        else:
            if or_ind >= 0:
                first_operator_ind = or_ind
                ind_after_operator = or_ind + 2
            else:
                first_operator_ind = and_ind
                ind_after_operator = and_ind + 3
        return first_operator_ind


def find_ind_after_operator(string, operator_ind):
    if string[operator_ind] == 'A':
        ind_after_operator = operator_ind + 3
    else:  # operator is OR
        ind_after_operator = operator_ind + 2
    return ind_after_operator


def check_valid_parenthesis(string):
    stack = []
    for i in string:
        if i == '(':
            stack.append(i)
        elif i == ')':
            if len(stack) > 0:
                stack.pop()
            else:
                return False
            """
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                    (open_list[pos] == stack[len(stack) - 1])):
                stack.pop()
            else:
                return "Unbalanced"
            """
    if len(stack) == 0:
        return True
    else:
        return False


"""
def check_cond(string):
    stripped_string = string.strip()
    if stripped_string[0] == ')':
        return False
    if stripped_string[-1] == '(':
        return False
    if stripped_string[0] == '(':
        # one recursion without removing ending parenthesis # GOOD FOR: (x and y) or z
        if cond_rec_operator_break(stripped_string):
            return True
        # one recursion with removing, good for (x and y)
        if stripped_string[-1] == ')':
            string_without_parenthesis = stripped_string[1:-1]
            if cond_rec_operator_break(string_without_parenthesis):
                return True
        return False
    else:
        return cond_rec_operator_break(stripped_string)


# ((X AND Y) AND (X AND Y)
def cond_rec_operator_break(string):
    last_ind = len(string) - 1
    location_to_look_from = 0
    while location_to_look_from <= last_ind:
        and_ind = string.find("AND", location_to_look_from)
        or_ind = string.find("OR", location_to_look_from)
        if and_ind < 0 and or_ind < 0:  # no AND or OR operators in string
            stripped_string = string.strip()
            if stripped_string[0] == ')':
                return False
            if stripped_string[-1] == '(':
                return False
            if stripped_string[0] == '(':
                if stripped_string[-1] == ')':
                    string_without_parenthesis = stripped_string[1:-1]
                    if check_cond(string_without_parenthesis):
                        return True
                    else:
                        location_to_look_from = last_ind;
                else:
                    return False
            else:
                return check_simple_cond(stripped_string)
        else:
            # find first of the two operators:
            if and_ind < or_ind:
                if and_ind >= 0:
                    first_operator_ind = and_ind
                    ind_after_operator = and_ind + 3
                else:
                    first_operator_ind = or_ind
                    ind_after_operator = or_ind + 2
            else:
                if or_ind >= 0:
                    first_operator_ind = or_ind
                    ind_after_operator = or_ind + 2
                else:
                    first_operator_ind = and_ind
                    ind_after_operator = and_ind + 3
            string_left_of_operator = string[:first_operator_ind]
            string_right_of_operator = string[ind_after_operator:]
            left_res = check_cond(string_left_of_operator)
            if left_res: # check right only if left is good - no point checking right otherwise
                right_res = check_cond(string_right_of_operator)
            if left_res and right_res:
                return True
            else:
                location_to_look_from = ind_after_operator
    return False
"""


def check_simple_cond(string):
    valid_cond = True
    # perform checks
    return valid_cond


# query = input("Enter a query: ")
# print(query)

# CONDITION CHECKS:
# query = "SELECT something  FROM somewhere  WHERE  y OR x "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  y  OR (x )  "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  y  OR ( (x ) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  (y )  OR ( (x ) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  (y   OR ( (x ) ) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  ( (y)   OR ( (x ) ) )  "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  ( (x AND y) OR ((w AND z )) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  ( (x AND y) OR ((w AND z )) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  y OR ((w AND z )) ) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  y OR (w AND z )) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  ( ((y)) OR x )"  # VALID
query = "SELECT something  FROM somewhere  WHERE  (X) and ((Y)) or (Z)"  # VALID?

# query = "SELECT something  FROM somewhere  WHERE ((((Customers.Name=Orders.CustomerName) and ((Orders.Price > 59)) or (Customers.Age=25))))"
print(query)

location_of_SELECT = query.find("SELECT")
location_after_SELECT = location_of_SELECT + 6
location_of_FROM = query.find("FROM")
location_after_FROM = location_of_FROM + 4
location_of_WHERE = query.find("WHERE")
location_after_WHERE = location_of_WHERE + 5

string_after_select = query[location_after_SELECT:location_of_FROM]
string_after_from = query[location_after_FROM:location_of_WHERE]
string_after_where = query[location_after_WHERE:]

# code just to check the condition code
if check_cond(string_after_where):
    print("condition is valid :D")
else:
    print("condition is invalid :(")

"""
if check_columns(string_after_select):
    if check_from(string_after_from):
        if check_cond(string_after_where):
            print("Valid query :D")
        else:
            print("Parsing <condition> failed")
    else:
        print("Parsing <table_list> failed")
else:
    print("Parsing <attribute_list> failed")
    # TODO do we need to insert something into <attribute_list> or print as is?
"""

# SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customer.Name=Orders.CustomerName;

# " Customers.Name,Orders.Price, Orders.Price2 "
"""
example_string = "SELECT SELECT A B FROM customers WHERE A.B = \"2\""

print(example_string)

select_count = example_string.count("SELECT")

if select_count == 1:
    print("SELECT appears once")
else:
    if select_count == 0:
        print("SELECT does not appear")
    else:
        print("SELECT appears more than once")
"""

""" 
EXAMPLES TO TRY
    SELECT Customers.Name FROM Customers WHERE Customer.Age=25;
    SELECT Customers.Name FROM Customers WHERE Customer.Name=’Mike’;
    SELECT DISTINCT Customers.Name FROM Customers WHERE Customer.Age=25;
    SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customer.Name=Orders.CustomerName;
    SELECT Customers.CustomerName,Orders.Price FROM Customers,Orders WHERE Customer.Name=Orders.CustomerName AND Orders.Price>1000;
    SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customer.Name=Orders.CustomerName) AND Orders.Price>1000;
    SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customer.Name=Orders.CustomerName) OR (Orders.Price>59);
"""
