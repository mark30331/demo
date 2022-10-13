
from ast import AsyncFunctionDef
import pytest # Required for testing - Kept out of testing functions
#import pandas as pd # Will be added into the required testing functions
from urllib import request
from app import*


# ========================== Functions ========================
# -------------------------- Package Tests ------------------------------
def package_confirm():
    import sys
    missing_packages = [] # List for Missing Packages
    if ('boto3' in sys.modules):
        print("boto3  - Confirmed")
    else:
        missing_packages.append('boto3')
    if ('flask' in sys.modules):
        print("flask  - Confirmed")
    else:
        missing_packages.append('flask')
    if ('pandas' in sys.modules):
        print("pandas  - Confirmed")
    else:
        missing_packages.append('pandas')
    if ('plotly' in sys.modules):
        print("plotly  - Confirmed")
    else:
        missing_packages.append('plotly')
    if ('json' in sys.modules):
        print("json  - Confirmed")
    else:
        missing_packages.append('json')
    return missing_packages

def connection():
    import AWS_connector
    return AWS_connector.boto_dynamo_connect()

def tables():
    import AWS_connector
    conn = connection()
    return AWS_connector.get_all_tables(conn)

def table_data():
    import AWS_connector
    conn = connection()
    return AWS_connector.get_all_items(conn)

def dataframe():
    import AWS_connector
    data = table_data()
    return AWS_connector.clean_items(data)


#--------------------------- Test Answers --------------------
# -------------- Setup and connections tests
def test_package_confirm():
    assert package_confirm() == []

def test_connection():
    assert str(type(connection())) == "<class 'boto3.resources.factory.dynamodb.ServiceResource'>"

def test_tables():
    assert type(tables()) == type([])

def test_table_contents():
    assert type(table_data()) == type([])

def test_table_contents_1lv_down():
    data = table_data()
    assert type(data[1]) == type({})

# -------------- Dataframe tests
def test_is_dataframe():
    pass

def test_temp_threshhold():
    pass



# --------------- Web pages tests
def test_index():
    pass
    

def test_html_table():
    # content = app.app_context()
    # assert content.push()
    pass
    
def test_t_graph():
    pass

def test_h_graph():
    # result = h_graph()
    # html = result.read()
    # return html
    pass


def test_press_graph():
    pass

pytest.main(["test_app.py"])
