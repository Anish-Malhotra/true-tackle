import { QueryClient, QueryClientProvider } from "react-query";
//import { ReactQueryDevtools } from "react-query-devtools";
import ProductsList from "./components/ProductsList";

const queryClient = new QueryClient({});

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
     

      <ProductsList />

    </QueryClientProvider>
  );
};

export default App;