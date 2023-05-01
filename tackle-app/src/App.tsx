import { QueryClient, QueryClientProvider } from "react-query";
//import { ReactQueryDevtools } from "react-query-devtools";
import ProductsList from "./components/ProductsList";
import { Grid } from "@mui/material";
import Header from "./components/Header";

const queryClient = new QueryClient({});

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
        <Grid container
            spacing={0}
            direction="column"
            alignItems="center"
        >
            <Header />
            <ProductsList />
        </Grid>
    </QueryClientProvider>
  );
};

export default App;