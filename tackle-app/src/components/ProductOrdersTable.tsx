import * as React from 'react';
import { DataGrid, GridRowId, GridPaginationModel, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { DEFAULT_PAGE_SIZE } from '../routes';
import { useGetOrdersList } from '../api/hooks';

import _ from 'lodash';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'order_date', headerName: 'Order Date', width: 130 },
  {
      field: 'full_name',
      headerName: 'Full Name',
      sortable: false,
      width: 160,
  },
  {
    field: 'quantity',
    headerName: 'Quantity',
    type: 'number',
    width: 90,
  },
  { field: 'created_at', headerName: 'Created At', width: 130 },
];

//@ts-ignore
const ProductOrderTable = (props) => {
    const mapPageToNextCursor = React.useRef<{ [page: number]: GridRowId }>({});
  
    const [paginationModel, setPaginationModel] = React.useState({
      page: 1,
      pageSize: DEFAULT_PAGE_SIZE,
    });
  
    const queryOptions = React.useMemo(
      () => ({
        product_id: props.product_id,
        cursor: mapPageToNextCursor.current[paginationModel.page - 1],
        page: paginationModel.pageSize,
      }),
      [paginationModel, props.product_id],
    );

    const {
        data: orders,
        isLoading,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage
    } = useGetOrdersList(queryOptions.product_id, DEFAULT_PAGE_SIZE)
  
    const handlePaginationModelChange = (newPaginationModel: GridPaginationModel) => {
      // We have the cursor, we can allow the page transition.
      if (
        newPaginationModel.page === 0 ||
        mapPageToNextCursor.current[newPaginationModel.page - 1]
      ) {
        setPaginationModel(newPaginationModel);
        fetchNextPage();
      }
    };
  
    React.useEffect(() => {
      if (!isLoading && hasNextPage) {
        // We add nextCursor when available
        //@ts-ignore
        mapPageToNextCursor.current[paginationModel.page] = orders?.pages.length + 1;
      }
    }, [paginationModel.page, isLoading, orders?.pages]);
  
    // Some API clients return undefined while loading
    // Following lines are here to prevent `rowCountState` from being undefined during the loading
    const [rowCountState, setRowCountState] = React.useState(
      orders?.pages[0].count || 0,
    );
    React.useEffect(() => {
      // @ts-ignore
      setRowCountState((prevRowCountState) =>
        orders?.pages[0].count !== undefined
          ? orders?.pages[0].count
          : prevRowCountState,
      );
    }, [orders?.pages[0].count, setRowCountState]);

    const data_rows = React.useMemo(
        () => _.flatten(_.map(orders?.pages, (page) => page.data)),
        [orders],
    );

    // This is pretty bad and should probably be handled by a sum in a SQL query
    // or enriching orders with product price or similar
    const total_revenue = React.useMemo(() =>
        props.price * _.sumBy(data_rows, (row) => row.quantity),
        [data_rows, props.price]
    );
  
    return (
      <>

      { !(isLoading || isFetchingNextPage) && (
        <h4>Total revenue: ${total_revenue}</h4>
      )}
      { !(isLoading || isFetchingNextPage) && (
        <div style={{ height: 400, width: '100%' }}>
            <DataGrid
            // @ts-ignore
            rows={data_rows}
            columns={columns}
            pageSizeOptions={[DEFAULT_PAGE_SIZE]}
            rowCount={rowCountState}
            getRowId={(row) => row.id}
            paginationMode="server"
            onPaginationModelChange={handlePaginationModelChange}
            paginationModel={paginationModel}
            loading={isLoading || isFetchingNextPage}
            autoHeight
            />
        </div>
      )}
      </>
    );
};

export default ProductOrderTable;