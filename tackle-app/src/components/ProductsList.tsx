import React from 'react';
import { Box, Button, List, ListItem, Divider, Grid, Typography } from '@mui/material';

import { useGetProductsList } from "../api/hooks";
import ProductCard from './ProductCard';

import _ from 'lodash';
import { PaginationInterface } from '../interfaces';
import { Product } from '../interfaces/interfaces';

const ProductsList = () => {
    const {
      data: products,
      isLoading,
      fetchNextPage,
      hasNextPage,
      isFetchingNextPage,
    } = useGetProductsList();
   
    return (
        <>
            {!isLoading && (
                <Box display="flex" flexWrap="wrap" justifyContent="center" m={1} p={1}>
                    <Grid container
                        spacing={0}
                        direction="column"
                        alignItems="center"
                    >
                        <List>
                            {products!.pages.map((page) => (
                                <ListItem>
                                    <React.Fragment key={page.next_id || 0}>
                                        {page.data.map((product) => (
                                                <ProductCard
                                                    key={product.id}
                                                    product_id={product.id}
                                                    listing_type={product.listing_type}
                                                    title={product.title}
                                                    price={product.price}
                                                    vendor_id={product.vendor_id}
                                                    created_at={product.created_at}
                                                />
                                        ))}
                                    </React.Fragment>
                                </ListItem>
                            ))}
                            <Divider />
                        </List>
                    </Grid>
                </Box>
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
            {!isLoading && products && (
                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                    Loaded {_.sumBy(products!.pages, (page: PaginationInterface<Product[]>) => page.data.length)} out of {products!.pages[0].count} products.
                </Typography>
            )}
        </>
    );
}

export default ProductsList;