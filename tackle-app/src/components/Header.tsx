import { useGetOrderRevenue } from "../api/hooks";

const Header = () => {
    const { data, isLoading } = useGetOrderRevenue();

    return (
        <div className="header">
            <h1>Welcome to the tackle.io sales dashboard!</h1>
            <h4>Total Revenue: {!isLoading && (`\$${data?.amount}`)}</h4>
        </div>
    )
};

export default Header;