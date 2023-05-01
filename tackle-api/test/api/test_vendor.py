import pytest
from unittest import TestCase

# This test class is stubbed, see the tests in the test_orders.py file for implementation details
class TestVendor:
    # Tests retrieving a paginated list of orders
    def test_get_all_success(self, testapp):
        pass
            
    # Tests creating a new order
    def test_create_success(self, testapp):
        pass
        
    # the POST will fail because there is no product with the given id in the pre-staged database
    def test_create_fail_fk_does_not_exist(self, testapp):
        pass
        
    # the POST will fail because the order date is malformed
    def test_create_fail_invalid_date(self, testapp):
        pass
        
    # the POST will fail because the quantity is not an integer, as specified in openapi spec
    def test_create_fail_data_type_validation(self, testapp):
        pass
        
    # Tests successful fetch of a single order
    def test_get_by_id_success(self, testapp):
        pass
        
    # Tests that we correctly return a 404 status code if the order_id does not exist
    def test_get_by_id_fail_no_data(self, testapp):
        pass
           
    # Tests successful update of a single order
    def test_update_success(self, testapp):
        pass
        
    # PUT fails here because there is no order with the given id in the pre-staged database
    def test_update_fail_no_matching_data(self, testapp):
        pass
        
    # Tests successful delete of a single order
    def test_delete_success(self, testapp):
        pass
        
    # DELETE fails here because there is no order with the given id in the pre-staged database
    def test_delete_fail_no_matching_data(self, testapp):
        pass