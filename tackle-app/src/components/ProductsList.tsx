import { useGetProductsList } from "../api/hooks";

const ProductsList = () => {
    const {
      data: list,
      isLoading,
      fetchNextPage,
      hasNextPage,
      isFetchingNextPage,
    } = useGetProductsList();

    if (!isLoading) {
      console.log(list)
    }
   
    return (
      <></>
      );
};

export default ProductsList;