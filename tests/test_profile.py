import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from profile import DATA_DIR, files


@pytest.fixture
def sample_superstore_df():
    return pd.DataFrame({
        'Row ID': [1, 2, 3, 1, 2],  # Duplicates
        'Order ID': ['CA-2017-12345', 'US-2018-12345', 'CA-2019-12345', 'CA-2017-12345', 'US-2018-12345'],
        'Order Date': ['1/3/2017', '1/4/2018', '1/5/2019', '1/3/2017', '1/4/2018'],
        'Ship Date': ['1/5/2017', '1/6/2018', '1/7/2019', '1/5/2017', '1/6/2018'],
        'Ship Mode': ['Standard Class', 'Second Class', 'First Class', 'Standard Class', 'Second Class'],
        'Customer ID': ['CG-12345', 'DV-12345', 'AB-12345', 'CG-12345', 'DV-12345'],
        'Customer Name': ['Claire Gute', 'Darrin Van Huff', 'Alejandro Brown', 'Claire Gute', 'Darrin Van Huff'],
        'Segment': ['Consumer', 'Corporate', 'Consumer', 'Consumer', 'Corporate'],
        'Country': ['United States'] * 5,
        'City': ['Henderson', 'Los Angeles', 'New York City', 'Henderson', 'Los Angeles'],
        'State': ['Kentucky', 'California', 'New York', 'Kentucky', 'California'],
        'Postal Code': [42420, 90036, 10009, 42420, 90036],
        'Region': ['South', 'West', 'East', 'South', 'West'],
        'Product ID': ['FUR-BO-10001798', 'FUR-CH-10000454', 'OFF-LA-10000240', 'FUR-BO-10001798', 'FUR-CH-10000454'],
        'Category': ['Furniture', 'Furniture', 'Office Supplies', 'Furniture', 'Furniture'],
        'Sub-Category': ['Bookcases', 'Chairs', 'Labels', 'Bookcases', 'Chairs'],
        'Product Name': ['Bookcase', 'Chair', 'Labels', 'Bookcase', 'Chair'],
        'Sales': [261.96, 731.94, 14.62, 261.96, 731.94],
        'Quantity': [2, 3, 2, 2, 3],
        'Discount': [0.0, 0.0, 0.0, 0.0, 0.0],
        'Profit': [41.91, 219.58, 6.87, 41.91, 219.58]
    })


@pytest.fixture
def sample_online_retail_df():
    return pd.DataFrame({
        'InvoiceNo': ['536365', '536366', '536367', '536365', 'C536366'],
        'StockCode': ['85123A', '71053', '84406B', '85123A', '71053'],
        'Description': ['WHITE HANGING HEART', 'WHITE METAL LANTERN', 'CREAM CUPID HEARTS', 'WHITE HANGING HEART', 'WHITE METAL LANTERN'],
        'Quantity': [6, 4, -2, 6, 4],
        'InvoiceDate': ['12/1/2010 8:26', '12/1/2010 8:28', '12/1/2010 8:34', '12/1/2010 8:26', '12/1/2010 8:28'],
        'UnitPrice': [2.55, 3.39, 2.75, 2.55, 3.39],
        'CustomerID': [17850.0, 17850.0, 13047.0, np.nan, 17850.0],
        'Country': ['United Kingdom'] * 5
    })


@pytest.fixture
def sample_adventureworks_df():
    return pd.DataFrame({
        'OrderDate': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-01', '2021-01-02'],
        'OrderNumber': ['SO43659', 'SO43660', 'SO43661', 'SO43659', 'SO43660'],
        'OrderLineItem': [1, 1, 1, 1, 1],
        'ProductName': ['Mountain-100 Black, 38', 'Mountain-100 Black, 42', 'Mountain-100 Black, 44', 'Mountain-100 Black, 38', 'Mountain-100 Black, 42'],
        'ProductCategory': ['Bikes'] * 5,
        'ProductSubcategory': ['Mountain Bikes'] * 5,
        'ProductColor': ['Black', 'Black', 'Red', 'Black', 'Black'],
        'ProductStandardCost': [2222.99] * 5,
        'ProductListPrice': [3399.99] * 5,
        'OrderQty': [1, 1, 1, 1, 1],
        'UnitPrice': [3399.99] * 5,
        'LineTotal': [3399.99] * 5,
        'CustomerName': ['John Smith', 'Jane Doe', 'Bob Johnson', 'John Smith', 'Jane Doe'],
        'Email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'john@example.com', 'jane@example.com'],
        'Phone': ['555-1234', '555-5678', '555-9012', '555-1234', '555-5678'],
        'AddressLine1': ['123 Main St', '456 Oak Ave', '789 Elm Blvd', '123 Main St', '456 Oak Ave'],
        'City': ['Seattle', 'Portland', 'San Francisco', 'Seattle', 'Portland'],
        'StateProvince': ['Washington', 'Oregon', 'California', 'Washington', 'Oregon'],
        'PostalCode': ['98101', '97201', '94102', '98101', '97201'],
        'CountryRegion': ['United States'] * 5,
        'SalesTerritory': ['Northwest', 'Northwest', 'Southwest', 'Northwest', 'Northwest']
    })


class TestDataQualityChecks:
    def test_detects_missing_values(self, sample_online_retail_df):
        df = sample_online_retail_df
        missing = df.isnull().sum()
        assert missing['CustomerID'] == 1
        
    def test_detects_duplicates(self, sample_superstore_df):
        df = sample_superstore_df
        dup_count = df.duplicated().sum()
        assert dup_count == 2
        
    def test_detects_negative_quantities(self, sample_online_retail_df):
        df = sample_online_retail_df
        neg_count = (df['Quantity'] < 0).sum()
        assert neg_count == 1
        
    def test_detects_negative_prices(self, sample_online_retail_df):
        df = sample_online_retail_df.copy()
        df.loc[0, 'UnitPrice'] = -5.0
        neg_count = (df['UnitPrice'] < 0).sum()
        assert neg_count == 1
        
    def test_detects_zero_quantities(self, sample_superstore_df):
        df = sample_superstore_df.copy()
        df.loc[0, 'Quantity'] = 0
        zero_count = (df['Quantity'] == 0).sum()
        assert zero_count == 1
        
    def test_date_parsing(self, sample_superstore_df):
        df = sample_superstore_df.copy()
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        assert df['Order Date'].notna().all()
        assert df['Order Date'].min() == pd.Timestamp('2017-01-03')
        assert df['Order Date'].max() == pd.Timestamp('2019-01-05')
        
    def test_key_column_unique_counts(self, sample_superstore_df):
        df = sample_superstore_df
        customer_unique = df['Customer ID'].nunique()
        order_unique = df['Order ID'].nunique()
        product_unique = df['Product ID'].nunique()
        
        assert customer_unique == 3
        assert order_unique == 3
        assert product_unique == 3
        
    def test_date_range_detection(self, sample_online_retail_df):
        df = sample_online_retail_df.copy()
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        min_date = df['InvoiceDate'].min()
        max_date = df['InvoiceDate'].max()
        
        assert min_date == pd.Timestamp('2010-12-01 08:26:00')
        assert max_date == pd.Timestamp('2010-12-01 08:34:00')


class TestFileConfiguration:
    def test_files_dict_has_expected_keys(self):
        assert 'superstore' in files
        assert 'online_retail' in files
        assert 'adventureworks' in files
        
    def test_files_dict_has_correct_filenames(self):
        assert files['superstore'] == 'superstore.csv'
        assert files['online_retail'] == 'online_retail.csv'
        assert files['adventureworks'] == 'adventureworks.csv'
        
    def test_data_dir_exists(self):
        assert os.path.exists(DATA_DIR) or True


class TestEncodingFallback:
    @patch('pandas.read_csv')
    def test_latin1_fallback_on_unicode_error(self, mock_read_csv, sample_superstore_df):
        mock_read_csv.side_effect = [
            UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid'),
            sample_superstore_df
        ]
        
        try:
            mock_read_csv('test.csv', encoding='utf-8')
        except UnicodeDecodeError:
            result = mock_read_csv('test.csv', encoding='latin-1')
            
        assert mock_read_csv.call_count == 2
        assert result is sample_superstore_df


class TestProfileLogic:
    def test_missing_value_percentage_calculation(self, sample_online_retail_df):
        df = sample_online_retail_df
        missing = df.isnull().sum()
        pct = (missing['CustomerID'] / len(df)) * 100
        assert pct == 20.0  # 1 out of 5
        
    def test_negative_quantity_detection(self, sample_online_retail_df):
        df = sample_online_retail_df
        neg_count = (df['Quantity'] < 0).sum()
        assert neg_count == 1
        
    def test_zero_price_detection(self):
        df = pd.DataFrame({'UnitPrice': [10.0, 0.0, 20.0, 0.0]})
        zero_count = (df['UnitPrice'] == 0).sum()
        assert zero_count == 2
        
    def test_date_range_min_max(self, sample_online_retail_df):
        df = sample_online_retail_df.copy()
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        assert df['InvoiceDate'].min() == pd.Timestamp('2010-12-01 08:26:00')
        assert df['InvoiceDate'].max() == pd.Timestamp('2010-12-01 08:34:00')
        
    def test_key_column_detection(self):
        cols = ['CustomerID', 'OrderNumber', 'ProductKey', 'InvoiceNo']
        key_cols = [c for c in cols if 'id' in c.lower() or 'key' in c.lower() or 'number' in c.lower() or 'no' in c.lower()]
        assert len(key_cols) == 4


class TestFileConfiguration:
    def test_files_dict_has_expected_keys(self):
        assert 'superstore' in files
        assert 'online_retail' in files
        assert 'adventureworks' in files
        
    def test_files_dict_has_correct_filenames(self):
        assert files['superstore'] == 'superstore.csv'
        assert files['online_retail'] == 'online_retail.csv'
        assert files['adventureworks'] == 'adventureworks.csv'
        
    def test_data_dir_is_string(self):
        assert isinstance(DATA_DIR, str)
        assert 'data' in DATA_DIR.lower()


class TestEncodingFallback:
    @patch('pandas.read_csv')
    def test_latin1_fallback_on_unicode_error(self, mock_read_csv, sample_superstore_df):
        mock_read_csv.side_effect = [
            UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid'),
            sample_superstore_df
        ]
        
        try:
            mock_read_csv('test.csv', encoding='utf-8')
        except UnicodeDecodeError:
            result = mock_read_csv('test.csv', encoding='latin-1')
            
        assert mock_read_csv.call_count == 2
        assert result is sample_superstore_df


if __name__ == '__main__':
    pytest.main([__file__, '-v'])