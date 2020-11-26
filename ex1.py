
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
        else: # found an operator
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
    return is_constant(string_left_of_rel_op) and is_constant(string_right_of_rel_op)


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
    # TODO ? check validity, e.g. ind in range
    # TODO change this to CASE
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


def is_constant(string):
    stripped_string = string.strip()
    # TODO add the actual checks
    return stripped_string == 'x' or stripped_string == 'y' or stripped_string == 'z'


def cond_has_outer_parenthesis(string):
    stripped_string = string.strip()
    return stripped_string[0] == '(' and stripped_string[-1] == ')'


def find_operator_ind(string, location_to_look_from):
    # TODO can find be not case sensitive? That's good for us
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


# query = input("Enter a query: ")
# print(query)

# CONDITION CHECKS:
query = "SELECT something  FROM somewhere  WHERE  y>x OR x<=y AND x=x "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  y>>x OR x<y "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  y=x  OR (x<>y )  "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  y<=y  OR ( (x<x ) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  (y>x )  OR ( (x=y ) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  (y<=x   OR ( (x>y ) ) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  ( (y>x)   OR ( (x<y ) ) )  "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  ( (y>x)   OR ( (x<<y ) ) )  "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  ( (x>>y AND y==x) OR ((y><x AND z>y )) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  ( (x>y AND y<=x) OR ((y>=x AND z>y )) ) "  # VALID
# query = "SELECT something  FROM somewhere  WHERE  ( (x=y AND y<x) OR ((y>x AND z<=x )) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  y=y OR ((y>x AND z<x )) ) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  y=x OR (y=y AND z<x )) "  # INVALID
# query = "SELECT something  FROM somewhere  WHERE  ( ((y=x)) OR x=y )"  # VALID
# query = "SELECT something  FROM somewhere  WHERE  (x=y) AND ((y<=x)) OR (z<>y)"  # VALIDv
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
