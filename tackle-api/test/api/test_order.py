import pytest
from unittest import TestCase


class TestOrder:
    # Tests retrieving a paginated list of orders
    def test_get_all_success(self, testapp):
        res = testapp.get('/api/v1/orders')
        data = res.json

        assert res.status_code == 200
        assert data is not None
        assert isinstance(data, dict)
        
        assert 'count' in data and data['count'] == 6
        assert 'total' in data and data['total'] == 6
        assert data['count'] == data['total']
        assert 'page' in data and data['page'] == 1
        assert 'page_size' in data and data['page_size'] == 20
        
        assert 'resource_type' in data and data['resource_type'] == "order"
        assert 'resources' in data and type(data['resources']) == list
        
        assert len(data['resources']) == data['count'] and len(data['resources']) == 6
        
        for resource in data['resources']:
            assert resource is not None
            assert isinstance(resource, dict)
            
            assert 'id' in resource and type(resource['id']) == int
            assert 'product_id' in resource and type(resource['id']) == int
            assert 'created_at' in resource and type(resource['created_at']) == str
            assert 'full_name' in resource and type(resource['full_name']) == str
            assert 'order_date' in resource and type(resource['order_date']) == str
            assert 'quantity' in resource and type(resource['quantity']) == int
            
    # Tests retrieving a paginated list of orders filter by product_id
    def test_get_all_product_id_filter_success(self, testapp):
        product_id = 2
        res = testapp.get('/api/v1/orders?product_id={}'.format(product_id))
        data = res.json

        assert res.status_code == 200
        assert data is not None
        assert isinstance(data, dict)
        
        assert 'count' in data and data['count'] == 2
        assert 'total' in data and data['total'] == 2
        assert data['count'] == data['total']
        assert 'page' in data and data['page'] == 1
        assert 'page_size' in data and data['page_size'] == 20
        
        assert 'resource_type' in data and data['resource_type'] == "order"
        assert 'resources' in data and type(data['resources']) == list
        
        assert len(data['resources']) == data['count'] and len(data['resources']) == 2
        
        for resource in data['resources']:
            assert resource is not None
            assert isinstance(resource, dict)
            
            assert 'id' in resource and type(resource['id']) == int
            assert 'product_id' in resource and type(resource['id']) == int
            assert 'created_at' in resource and type(resource['created_at']) == str
            assert 'full_name' in resource and type(resource['full_name']) == str
            assert 'order_date' in resource and type(resource['order_date']) == str
            assert 'quantity' in resource and type(resource['quantity']) == int
            
            assert resource['product_id'] == product_id
            
    # Tests creating a new order
    def test_create_success(self, testapp):
        request_body = {
            "product_id": 1,
            "full_name": "John Cena",
            "order_date": "2020-01-01",
            "quantity": 5,
        }
        res = testapp.post_json('/api/v1/orders', request_body)
        data = res.json

        assert res.status_int == 200
        assert isinstance(data, dict)
        
        assert data['product_id'] == request_body['product_id']
        assert data['full_name'] == request_body['full_name']
        assert data['order_date'] == request_body['order_date']
        assert data['quantity'] == request_body['quantity']
        
        assert 'id' in data and type(data['id']) == int
        assert 'created_at' in data and type(data['created_at']) == str
        
    # the POST will fail because there is no product with the given id in the pre-staged database
    def test_create_fail_fk_does_not_exist(self, testapp):
        request_body = {
            "product_id": 999,
            "full_name": "Evil Overlord",
            "order_date": "2020-01-01",
            "quantity": 1,
        }
                
        with pytest.raises(Exception) as e:
            testapp.post_json('/api/v1/orders', request_body)
        
        assert "FOREIGN KEY constraint failed" in str(e.value)
        assert '"resource_type":"order"' in str(e.value)
        assert '"status":500' in str(e.value)
        
    # the POST will fail because the order date is malformed
    def test_create_fail_invalid_date(self, testapp):
        request_body = {
            "product_id": 1,
            "full_name": "John Cena",
            "order_date": "2020-01-011",
            "quantity": 3,
        }
                
        with pytest.raises(Exception) as e:
            testapp.post_json('/api/v1/orders', request_body)
        
        assert '"resource_type":"order"' in str(e.value)
        assert '"status":405' in str(e.value)
        assert "ValueError" in str(e.value)
        
    # the POST will fail because the quantity is not an integer, as specified in openapi spec
    def test_create_fail_data_type_validation(self, testapp):
        request_body = {
            "product_id": 1,
            "full_name": "John Cena",
            "order_date": "2020-01-01",
            "quantity": "3",
        }
                
        with pytest.raises(Exception) as e:
            testapp.post_json('/api/v1/orders', request_body)
        
        assert '"status": 400' in str(e.value)
        
    # Tests successful fetch of a single order
    def test_get_by_id_success(self, testapp):
        order_id = 2
        res = testapp.get('/api/v1/orders/{}'.format(order_id))
        data = res.json

        assert res.status_code == 200
        assert data is not None
        assert isinstance(data, dict)
        
        assert 'id' in data and type(data['id']) == int
        assert 'product_id' in data and type(data['id']) == int
        assert 'created_at' in data and type(data['created_at']) == str
        assert 'full_name' in data and type(data['full_name']) == str
        assert 'order_date' in data and type(data['order_date']) == str
        assert 'quantity' in data and type(data['quantity']) == int
        
        assert data['id'] == order_id
        assert data['product_id'] == 1
        assert data['full_name'] == "Elon Musk"
        assert data['quantity'] == 2
        
    # Tests that we correctly return a 404 status code if the order_id does not exist
    def test_get_by_id_fail_no_data(self, testapp):
        order_id = 200

        with pytest.raises(Exception) as e:
            testapp.get('/api/v1/orders/{}'.format(order_id))
            
        assert '"resource_type":"order"' in str(e.value)
        assert '"status":404' in str(e.value)
        assert "not found" in str(e.value)
           
    # Tests successful update of a single order
    def test_update_success(self, testapp):
        order_id = 1
        request_body = {
            "full_name": "John Cena",
            "quantity": 5000,
        }
        res = testapp.put_json('/api/v1/orders/{}'.format(order_id), request_body)
        data = res.json

        assert res.status_int == 200
        assert isinstance(data, dict)
        
        assert data['product_id'] == 1
        assert data['id'] == order_id
        assert data['full_name'] == request_body['full_name']
        assert data['quantity'] == request_body['quantity']
        
        res = testapp.get('/api/v1/orders/{}'.format(order_id))
        db_data = res.json
        
        assert res.status_code == 200
        assert isinstance(db_data, dict)
        
        assert db_data['id'] == order_id and db_data['id'] == data['id']
        assert db_data['product_id'] == data['id']
        assert db_data['created_at'] == data['created_at']
        assert db_data['quantity'] == data['quantity']
        assert db_data['full_name'] == data['full_name']
        assert db_data['order_date'] == data['order_date']
        
    # PUT fails here because there is no order with the given id in the pre-staged database
    def test_update_fail_no_matching_data(self, testapp):
        order_id = 9001
        request_body = {
            "full_name": "John Cena",
            "quantity": 5000,
        }
        
        with pytest.raises(Exception) as e:
            testapp.put_json('/api/v1/orders/{}'.format(order_id), request_body)
            
        assert '"resource_type":"order"' in str(e.value)
        assert '"status":404' in str(e.value)
        assert "not found" in str(e.value)
        
    # Tests successful delete of a single order
    def test_delete_success(self, testapp):
        order_id = 1
        
        res = testapp.get('/api/v1/orders/{}'.format(order_id))
        data = res.json
        
        assert res.status_code == 200
        
        res = testapp.delete('/api/v1/orders/{}'.format(order_id))
        deleted_data = res.json

        assert res.status_code == 200
        
        TestCase().assertDictEqual(data, deleted_data)
        
    # DELETE fails here because there is no order with the given id in the pre-staged database
    def test_delete_fail_no_matching_data(self, testapp):
        order_id = 9001
        
        with pytest.raises(Exception) as e:
            testapp.delete('/api/v1/orders/{}'.format(order_id))

        assert '"resource_type":"order"' in str(e.value)
        assert '"status":404' in str(e.value)
        assert "not found" in str(e.value)