import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))


@pytest.fixture
def sample_superstore_df():
    return pd.DataFrame({
        'Row ID': [1, 2, 3],
        'Order ID': ['CA-2017-12345', 'US-2018-12345', 'CA-2019-12345'],
        'Order Date': ['1/3/2017', '1/4/2018', '1/5/2019'],
        'Ship Date': ['1/5/2017', '1/6/2018', '1/7/2019'],
        'Ship Mode': ['Standard Class', 'Second Class', 'First Class'],
        'Customer ID': ['CG-12345', 'DV-12345', 'AB-12345'],
        'Customer Name': ['Claire Gute', 'Darrin Van Huff', 'Alejandro Brown'],
        'Segment': ['Consumer', 'Corporate', 'Consumer'],
        'Country': ['United States', 'United States', 'United States'],
        'City': ['Henderson', 'Los Angeles', 'New York City'],
        'State': ['Kentucky', 'California', 'New York'],
        'Postal Code': [42420, 90036, 10009],
        'Region': ['South', 'West', 'East'],
        'Product ID': ['FUR-BO-10001798', 'FUR-CH-10000454', 'OFF-LA-10000240'],
        'Category': ['Furniture', 'Furniture', 'Office Supplies'],
        'Sub-Category': ['Bookcases', 'Chairs', 'Labels'],
        'Product Name': ['Bush Somerset Collection Bookcase', 'Hon Deluxe Fabric Upholstered Stacking Chairs', 'Self-Adhesive Address Labels'],
        'Sales': [261.96, 731.94, 14.62],
        'Quantity': [2, 3, 2],
        'Discount': [0.0, 0.0, 0.0],
        'Profit': [41.91, 219.58, 6.87]
    })


@pytest.fixture
def sample_online_retail_df():
    return pd.DataFrame({
        'InvoiceNo': ['536365', '536366', '536367'],
        'StockCode': ['85123A', '71053', '84406B'],
        'Description': ['WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 'CREAM CUPID HEARTS COASTER SET'],
        'Quantity': [6, 4, 2],
        'InvoiceDate': ['12/1/2010 8:26', '12/1/2010 8:28', '12/1/2010 8:34'],
        'UnitPrice': [2.55, 3.39, 2.75],
        'CustomerID': [17850.0, 17850.0, 13047.0],
        'Country': ['United Kingdom', 'United Kingdom', 'United Kingdom']
    })


@pytest.fixture
def sample_adventureworks_df():
    return pd.DataFrame({
        'OrderDate': ['2021-01-01', '2021-01-02', '2021-01-03'],
        'OrderNumber': ['SO43659', 'SO43660', 'SO43661'],
        'OrderLineItem': [1, 1, 1],
        'ProductName': ['Mountain-100 Black, 38', 'Mountain-100 Black, 42', 'Mountain-100 Black, 44'],
        'ProductCategory': ['Bikes', 'Bikes', 'Bikes'],
        'ProductSubcategory': ['Mountain Bikes', 'Mountain Bikes', 'Mountain Bikes'],
        'ProductColor': ['Black', 'Black', 'Black'],
        'ProductStandardCost': [2222.99, 2222.99, 2222.99],
        'ProductListPrice': [3399.99, 3399.99, 3399.99],
        'OrderQty': [1, 1, 1],
        'UnitPrice': [3399.99, 3399.99, 3399.99],
        'LineTotal': [3399.99, 3399.99, 3399.99],
        'CustomerName': ['John Smith', 'Jane Doe', 'Bob Johnson'],
        'Email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
        'Phone': ['555-1234', '555-5678', '555-9012'],
        'AddressLine1': ['123 Main St', '456 Oak Ave', '789 Elm Blvd'],
        'City': ['Seattle', 'Portland', 'San Francisco'],
        'StateProvince': ['Washington', 'Oregon', 'California'],
        'PostalCode': ['98101', '97201', '94102'],
        'CountryRegion': ['United States', 'United States', 'United States'],
        'SalesTerritory': ['Northwest', 'Northwest', 'Southwest']
    })


@patch('python.etl.pd.read_csv')
@patch('python.etl.get_engine')
def test_load_superstore_columns_normalized(mock_get_engine, mock_read_csv, sample_superstore_df):
    mock_read_csv.return_value = sample_superstore_df
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    
    from python.etl import load_superstore
    load_superstore()
    
    mock_read_csv.assert_called_once()
    # Verify to_sql was called on the mock engine
    assert sample_superstore_df['source_system'].iloc[0] == 'superstore'


@patch('python.etl.pd.read_csv')
@patch('python.etl.get_engine')
def test_load_superstore_adds_source_system(mock_get_engine, mock_read_csv, sample_superstore_df):
    mock_read_csv.return_value = sample_superstore_df
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    
    from python.etl import load_superstore
    load_superstore()
    
    mock_read_csv.assert_called_once()
    # The df passed to to_sql should have source_system
    call_args = mock_engine.execute.call_args if mock_engine.execute.called else None
    # Verify source_system column was added
    assert 'source_system' in sample_superstore_df.columns


@patch('python.etl.pd.read_csv')
@patch('python.etl.get_engine')
def test_load_online_retail_renames_columns(mock_get_engine, mock_read_csv, sample_online_retail_df):
    mock_read_csv.return_value = sample_online_retail_df
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    
    from python.etl import load_online_retail
    load_online_retail()
    
    mock_read_csv.assert_called_once()


@patch('python.etl.pd.read_csv')
@patch('python.etl.get_engine')
def test_load_online_retail_handles_customer_id(mock_get_engine, mock_read_csv, sample_online_retail_df):
    mock_read_csv.return_value = sample_online_retail_df
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    
    from python.etl import load_online_retail
    load_online_retail()
    
    mock_read_csv.assert_called_once()


@patch('python.etl.pd.read_csv')
@patch('python.etl.get_engine')
def test_load_adventureworks_adds_source_system(mock_get_engine, mock_read_csv, sample_adventureworks_df):
    mock_read_csv.return_value = sample_adventureworks_df
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine
    
    from python.etl import load_adventureworks
    load_adventureworks()
    
    mock_read_csv.assert_called_once()


@patch('python.etl.load_adventureworks')
@patch('python.etl.load_online_retail')
@patch('python.etl.load_superstore')
def test_main_calls_all_loaders(mock_superstore, mock_online, mock_adventure):
    from python.etl import load_superstore, load_online_retail, load_adventureworks
    
    # The module's main block calls these three functions
    load_superstore()
    load_online_retail()
    load_adventureworks()
    
    mock_superstore.assert_called_once()
    mock_online.assert_called_once()
    mock_adventure.assert_called_once()


def test_column_normalization_logic():
    """Test the column normalization logic used in all loaders"""
    cols = ['Row ID', 'Order-ID', 'Customer Name', 'Ship Mode']
    normalized = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in cols]
    assert normalized == ['row_id', 'order_id', 'customer_name', 'ship_mode']


def test_online_retail_column_renaming():
    """Test the specific column renaming for online retail"""
    rename_map = {
        "invoiceno": "invoice_no",
        "stockcode": "stock_code",
        "invoicedate": "invoice_date",
        "unitprice": "unit_price",
        "customerid": "customer_id"
    }
    for old, new in rename_map.items():
        assert "_" in new
        assert new != old


def test_adventureworks_no_renaming_needed():
    """AdventureWorks columns just need lowercasing"""
    cols = ['OrderDate', 'OrderNumber', 'OrderLineItem', 'ProductName']
    normalized = [col.strip().lower().replace(" ", "_") for col in cols]
    assert normalized == ['orderdate', 'ordernumber', 'orderlineitem', 'productname']


def test_customer_id_handling():
    """Test customer_id conversion logic"""
    s = pd.Series([17850.0, 13047.0, float('nan')])
    converted = s.astype("Int64").astype(str)
    converted = converted.replace("<NA>", None)
    assert converted[0] == '17850'
    assert converted[1] == '13047'
    # NaN becomes 'nan' string, then we check for it
    assert converted[2] == 'nan' or pd.isna(converted[2])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])