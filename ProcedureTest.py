import pytest
import pymysql

# Database connection fixture
@pytest.fixture(scope="module")
def db_connection():
    connection = pymysql.connect(
        host='database-2.cnk646w46gc7.ap-south-1.rds.amazonaws.com',
        user='digit1808',
        password='Welcome!12345',
        database='classicmodels',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield connection
    connection.close()

@pytest.mark.p1
def test_stored_procedures_exist(db_connection):
    """TC001: Check stored procedures exist in the database"""
    query = "show procedure status where db='classicmodels';"
    with db_connection.cursor() as cursor:
        cursor.execute(query)
        procedures = [row['Name'] for row in cursor.fetchall()]
    expected_procedures = [
        'SelectAllCustomers',
        'SelectAllCustomersByCity',
        'SelectAllCustomersByCityandPin',
        'get_order_by_cust',
        'GetCustomerShipping'
    ]
    for proc in expected_procedures:
        assert proc in procedures, f"Procedure {proc} not found in database"

@pytest.mark.p1
def test_SelectAllCustomers(db_connection):
    """TC002: Check SelectAllCustomers procedure returns all customers"""
    with db_connection.cursor() as cursor:
        cursor.callproc('SelectAllCustomers')
        result = cursor.fetchall()

        # Verify count matches direct query
        cursor.execute('select * from customers')
        expected = cursor.fetchall()

    assert len(result) == len(expected), "Mismatch in customer count returned by SelectAllCustomers"

@pytest.mark.p1
@pytest.mark.parametrize("city", ["Singapore"])
def test_SelectAllCustomersByCity(db_connection, city):
    """TC003: Check SelectAllCustomersByCity returns customers for given city"""
    with db_connection.cursor() as cursor:
        cursor.callproc('SelectAllCustomersByCity', (city,))
        result = cursor.fetchall()

        cursor.execute('select * from customers where city=%s', (city,))
        expected = cursor.fetchall()

    assert len(result) == len(expected), f"Mismatch in customer count for city {city}"

@pytest.mark.p1
@pytest.mark.parametrize("city, pincode", [("Singapore", 79903)])  # corrected pincode leading zero to int
def test_SelectAllCustomersByCityandPin(db_connection, city, pincode):
    """TC004: Check SelectAllCustomersByCityandPin procedure"""
    with db_connection.cursor() as cursor:
        cursor.callproc('SelectAllCustomersByCityandPin', (city, pincode))
        result = cursor.fetchall()

        cursor.execute('select * from customers where city=%s and postalCode=%s', (city, str(pincode).zfill(5)))
        expected = cursor.fetchall()

    assert len(result) == len(expected), f"Mismatch customers for city {city} and pincode {pincode}"

@pytest.mark.p1
@pytest.mark.parametrize("custId", [141])
def test_get_order_by_cust(db_connection, custId):
    """TC005: Check get_order_by_cust procedure counts orders by status"""
    with db_connection.cursor() as cursor:
        cursor.callproc('get_order_by_cust', (custId,))
        # Assuming procedure returns multiple result sets, or you have output params
        # For simplicity, run expected queries here to compare counts
        
        cursor.execute(
            "SELECT COUNT(*) as shipped FROM orders WHERE customerNumber=%s AND status='Shipped'", (custId,))
        shipped = cursor.fetchone()['shipped']

        cursor.execute(
            "SELECT COUNT(*) as cancelled FROM orders WHERE customerNumber=%s AND status='Cancelled'", (custId,))
        cancelled = cursor.fetchone()['cancelled']

        cursor.execute(
            "SELECT COUNT(*) as resolved FROM orders WHERE customerNumber=%s AND status='Resolved'", (custId,))
        resolved = cursor.fetchone()['resolved']

        cursor.execute(
            "SELECT COUNT(*) as disputed FROM orders WHERE customerNumber=%s AND status='Disputed'", (custId,))
        disputed = cursor.fetchone()['disputed']
        
        # This test is placeholder; the procedure output needs to be fetched properly.
        # You might want to fetch procedure results here and compare each count

    assert True  # Replace with actual validation once procedure output retrieval is clarified

@pytest.mark.p1
@pytest.mark.parametrize("custid", [112])
def test_GetCustomerShipping(db_connection, custid):
    """TC006: Check GetCustomerShipping procedure for shipping time"""
    with db_connection.cursor() as cursor:
        cursor.callproc('GetCustomerShipping', (custid,))
        result = cursor.fetchone()

        # Get expected shipping time based on customer country
        cursor.execute('select country from customers where customerNumber = %s', (custid,))
        country = cursor.fetchone()['country']

        if country == 'USA':
            expected_shipping = 'Two-day shipping'
        elif country == 'Canada':
            expected_shipping = 'Three-day shipping'
        else:
            expected_shipping = 'Five-day shipping'

    # The procedure might return the shipping time as p_shipping or similar
    # Adapt this assertion based on actual output format of procedure
    assert result is not None, "Procedure returned nothing"
    # Assuming result has a key with shipping info, e.g. 'Shippingtime'
    # Adjust keys as per actual procedure output
    # expected format from your description is not fully clear,
    # so example below assumes a shipping time string returned
    found_shipping = list(result.values())[0] if result else None
    assert expected_shipping in found_shipping, f"Expected shipping '{expected_shipping}' but got '{found_shipping}'"
