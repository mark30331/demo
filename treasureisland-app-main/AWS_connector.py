import boto3
import json
import AWS_config
import pandas
import datetime as dt
import plotly
import plotly.graph_objects as go
import plotly.express as px

def main():
    dynamo_resource = boto_dynamo_connect()

def values():
    dynamo_resource = boto_dynamo_connect()
    table_data = get_all_items(dynamo_resource)
    x = clean_items(table_data)    
    temperature_value = x['temperature'].values[-1]
    humidity_value = x['humidity'].values[-1]
    return [temperature_value,humidity_value]
    

# ------------------------------------------> Connection < ---------------------------------------
# Dynamodb connection - Client is disabled for now.
def boto_dynamo_connect():  # Active
    '''
    client = boto3.client('dynamodb',
        aws_access_key_id=AWS_config.access_key,
        aws_secret_access_key=AWS_config.secret_key,
        region_name=AWS_config.AWS_REGION)
    '''
    dynamodb_resource = boto3.resource('dynamodb', region_name = AWS_config.AWS_REGION)
    #print(dynamodb_resource)
    return dynamodb_resource

# ------------------------------------------> Client Methods < ---------------------------------------
def table_scan(client):
    return client.scan(
        TableName='wx_data'
    )

def describe_table(client):
    return client.describe_table(
        TableName='Test_table'
    )

# ------------------------------------------> Resource Methods < ---------------------------------------
def get_all_tables(dynamo_resource):
    tables = list(dynamo_resource.tables.all())
    return tables

def get_all_items(dynamo_resource): # Active
    dynamo_resource = boto3.resource('dynamodb', region_name = AWS_config.AWS_REGION)
    table = dynamo_resource.Table('ti_table') # Table Name will need to be manually changed
    response = table.scan()
    table_data = response['Items']

    while 'LastEvaluatedkey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        table_data.extend(response['Items'])

    if(len(table_data) <1):
        print("No Items in table")

    return table_data

def display_items(table_data): # for testing data contents
    print("Start of Recieved Data ---->")
    print()
    for item in table_data:
        print(item)
        print()
    print("<----- End of Revieved Data")

# ------------------------------------------> Cleaning < ---------------------------------------
def clean_items(table_data): # Active
    df = pandas.DataFrame(table_data)
    df["sample_time"] = pandas.to_numeric(df["sample_time"]) # Converts str milliseconds to float
    df["sample_time"] = pandas.to_datetime(df["sample_time"], unit = 'ms') \
        .dt.tz_localize('UTC' ).dt.tz_convert('America/New_York')# Converts float to datetime with EST as timezone

    df = df.sort_values(by='sample_time')
    df = df[df.device_data != {}] # Removed items with empty 'device_data'm

    df2 = list(df.device_data)
    df2 = pandas.DataFrame.from_records(data=df2)
    df = df.drop(columns=['device_data'])
    df = df.reset_index()
    df = df.drop(columns=['index'])
    new_df = pandas.concat([df, df2], axis=1)
    # ------------------Sensor Data------------------
    new_df["gas_red"] = pandas.to_numeric(new_df['gas_red'], downcast="float")
    new_df["gas_amm"] = pandas.to_numeric(new_df['gas_amm'], downcast="float")
    new_df["gas_oxi"] = pandas.to_numeric(new_df['gas_oxi'], downcast="float")
    new_df["temperature"] = pandas.to_numeric(new_df['temperature'], downcast="float")
    new_df["humidity"] = pandas.to_numeric(new_df['humidity'], downcast="float")
    new_df["pressure"] = pandas.to_numeric(new_df['pressure'], downcast="float")
    new_df["particulate"] = pandas.to_numeric(new_df['particulate'], downcast="float")
    #---------------> Extent of current Data <-------------------

    new_df = new_df.drop(columns=['device_id',"error", "gas_red", "gas_amm", "gas_oxi" , "sample_time"])
    new_df=new_df.dropna().reset_index(drop=True)
    new_df.loc[:, "temperature"] = new_df["temperature"].apply(lambda x: x - 15)
    #       New Values / Sensors Here
    new_df.style.apply(new_df, axis=None)
    return new_df

# ------------------------------------------> Testing / App.py Calls < ---------------------------------------
def test_scan():
    dynamo_resource = boto_dynamo_connect()
    table_data = get_all_items(dynamo_resource)
    df = clean_items(table_data)
    jdf = df.to_json()
    parsed = json.loads(jdf)

    return parsed

def get_table_view(): # TODO reformat to JSON format?
    dynamo_resource = boto_dynamo_connect()
    table_data = get_all_items(dynamo_resource)
    df = clean_items(table_data)
    return df

# ------------------------------------------> Graphing < ---------------------------------------
def simple_graph():
    dynamo_resource = boto_dynamo_connect()
    table_data = get_all_items(dynamo_resource)
    df = clean_items(table_data)
    df_tail = df.tail(120) # will need to adjust for all boards - last hour for all 3 boards is 180 values

    # -- px --
    #Temperature
    temp_g = px.line(df_tail, x = 'sample_time', y= 'temperature', color = 'device_id', symbol= 'device_id', markers=True)
    temp_g.update_layout(title_text='Sample Collection time and Temperature (last hour) - Plotly Express')
    #Humidity
    hum_g = px.line(df_tail, x = 'sample_time', y= 'humidity', color = 'device_id', symbol= 'device_id', markers=True)
    hum_g.update_layout(title_text='Sample Collection time and Humidity (last hour) - Plotly Express')
    #Pressure
    pres_g = px.line(df_tail, x = 'sample_time', y= 'pressure', color = 'device_id', symbol= 'device_id', markers=True)
    pres_g.update_layout(title_text='Sample Collection time and Pressure (last hour) - Plotly Express')
    #Particulate
    part_g = px.line(df_tail, x = 'sample_time', y= 'particulate', color = 'device_id', symbol= 'device_id', markers=True)
    part_g.update_layout(title_text='Sample Collection time and Particulate (last hour) - Plotly Express')

    return temp_g, hum_g, pres_g, part_g

def grab_graph(sensor_type = 'temperature'): # sensor_type is a valid entry in device data|Default of "temperature"
    dynamo_resource = boto_dynamo_connect()
    table_data = get_all_items(dynamo_resource)
    df = clean_items(table_data)
    #df_tail = df.tail(120) # will need to adjust for all boards - last hour for all 3 boards is 180 values
    df_tail = get_tail(df)
    graph = px.line(df_tail, x = df_tail.index, y= [sensor_type], color = 'deviceID', symbol= 'deviceID', markers=True)
    graph.update_layout(title_text='Sample Collection time and '+ str(sensor_type) +' (last hour) - Plotly Express')

    graphjson = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphjson

def get_tail(df):
    #dynamo_resource = boto_dynamo_connect()
    #table_data = get_all_items(dynamo_resource)
    #df = clean_items(table_data)
    #df_tail = df.tail(120) # will need to adjust for all boards - last hour for all 3 boards is 180 values
    df["datetime"] = pandas.to_datetime(df["datetime"])
    ndf = df.set_index('datetime')
    df_tail = ndf.last('1h')
    #print(ndf.columns)
    #print(df.dtypes)
    #print(df_tail)
    return df_tail

main()
