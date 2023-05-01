import React from 'react';
import { Box, Button, Card, List } from '@mui/material';

import { useGetProductsList } from "../api/hooks";
import ProductCard from './ProductCard';

const ProductsList = () => {
    const {
      data: products,
      isLoading,
      fetchNextPage,
      hasNextPage,
      isFetchingNextPage,
    } = useGetProductsList();

    if (!isLoading) {
      console.log(products)
      // @ts-ignore
      //console.log(hasNextPage)
    }
   
    return (
        <>
            {!isLoading && (
              <List>
                {products!.pages.map((page) => (
                  <React.Fragment key={page.next_id || 0}>
                    // @ts-ignore
                    {page.data.map((product) => (
                      <ProductCard
                        key={product.id}
                        listing_type={product.listing_type}
                        title={product.title}
                        price={product.price}
                        vendor_id={product.vendor_id}
                        created_at={product.created_at}
                      />
                    ))}
                  </React.Fragment>
                ))}
              </List>
            )}
            {hasNextPage && (
                <Box mt={2}>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => {
                        fetchNextPage();
                    }}
                    disabled={isFetchingNextPage}
                >
                    {isFetchingNextPage ? 'Loading more...' : 'Load more products'}
                </Button>
                </Box>
            )}
        </>
    );
};

export default ProductsList;