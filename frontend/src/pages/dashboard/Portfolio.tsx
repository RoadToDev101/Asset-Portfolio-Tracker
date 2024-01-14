import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  CardTitle,
  CardHeader,
  CardContent,
  Card,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { EyeIcon } from "lucide-react";
import axiosInstance from "@/api/axiosInstance";
import PortfolioCreateDialog from "./PortfolioCreateDialog";
import { Link } from "react-router-dom";
import CustomPagination from "@/components/shared/CustomPagination";

interface Portfolio {
  id: string;
  name: string;
  asset_type: string;
  current_value: number;
  description: string;
  created_at: string;
  updated_at: string;
}

const Portfolio = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const fetchPortfolios = async () => {
      try {
        const response = await axiosInstance.get(
          `/v1/portfolios?page=${currentPage}&page_size=10`
        );
        if (response.data && response.data.success) {
          setPortfolios(response.data.data.data);
          setTotalPages(response.data.data.pagination.total_pages);
        }
      } catch (error) {
        console.error("Error fetching portfolios:", error);
        // Handle error here, e.g., set an error state, show a notification, etc.
      }
    };

    fetchPortfolios();
  }, [currentPage, refreshKey]);

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleDialogSuccess = () => {
    setCurrentPage(1); // Reset current page to 1
    setRefreshKey((oldKey) => oldKey + 1); // Increment refreshKey
  };

  return (
    <main className="flex min-h-[calc(100vh-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10">
      <PortfolioCreateDialog onSuccess={handleDialogSuccess} />
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {portfolios.map((portfolio: Portfolio) => (
          <Card key={portfolio.id}>
            <CardHeader className="flex justify-between items-center pb-2">
              <CardTitle className="text-sm font-medium">
                {portfolio.name.toUpperCase()}
              </CardTitle>
              <CardDescription className="text-xs text-gray-500 dark:text-gray-400">
                {portfolio.asset_type.toUpperCase()}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col justify-between">
              {/* Placeholder for actual content like portfolio value and performance */}
              <div className="text-2xl font-bold mt-2 text-center">
                $ {portfolio.current_value.toLocaleString()}
              </div>
              <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-1">
                0.00%
              </p>
            </CardContent>
            <CardFooter className="flex justify-center space-x-2">
              <Button asChild size="icon" variant="ghost">
                <Link to={`/dashboard/portfolio/${portfolio.id}`}>
                  <EyeIcon className="w-4 h-4 text-blue-500" />
                </Link>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
      <div className="flex justify-center my-4">
        <CustomPagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      </div>
    </main>
  );
};

export default Portfolio;
