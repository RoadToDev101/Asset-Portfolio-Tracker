/* eslint-disable @typescript-eslint/no-explicit-any */
import { Button } from "@/components/ui/button";
import {
  CardTitle,
  CardHeader,
  CardContent,
  Card,
  CardDescription,
} from "@/components/ui/card";
import { ResponsiveLine } from "@nivo/line";
import { ResponsivePie } from "@nivo/pie";
import { FileEditIcon, TrashIcon } from "lucide-react";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axiosInstance from "@/api/axiosInstance";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import RenderAssetsTable from "./AssetsTable";

interface PortfolioDetailProps {
  id: string;
  name: string;
  description: string;
  user_id: string;
  asset_type: string;
  created_at: string;
  updated_at: string;
}

// interface Transaction {
//   id: string;
//   description: string;
//   transaction_type: string;
//   asset_type: string;
//   user_id: string;
//   portfolio_id: string;
//   ticker_symbol: string;
//   amount: number;
//   currency: string;
//   unit_price: number;
//   transaction_fee: number;
//   created_at: string;
//   updated_at: string;
//   deleted_at: string;
// }

const PortfolioDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [portfolio, setPortfolio] = useState<PortfolioDetailProps>();
  // const [transactions, setTransactions] = useState<Transaction[]>([]);
  // const [currentTransactionsTablePage, setCurrentTransactionsTablePage] =
  //   useState(1);
  // const [currentAssetsTablePage, setCurrentAssetsTablePage] = useState(1);
  // const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const response = await axiosInstance.get(`/v1/portfolios/${id}`);
        if (response.data && response.data.success) {
          setPortfolio(response.data.data);
        }
      } catch (error) {
        console.error("Error fetching portfolio:", error);
      }
    };
    fetchPortfolio();
  }, [id]);

  // useEffect(() => {
  //   const fetchTransactions = async () => {
  //     try {
  //       const response = await axiosInstance.get(
  //         `/v1/transactions/portfolio/${id}?page=1&page_size=10`
  //       );
  //       if (response.data && response.data.success) {
  //         setTransactions(response.data.data);
  //       }
  //     } catch (error) {
  //       console.error("Error fetching transactions:", error);
  //     }
  //   };
  //   fetchTransactions();
  // }, [id]);

  if (!portfolio) {
    return (
      <div className="flex flex-col items-center justify-center flex-1">
        <Alert variant="destructive" className="w-80">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>Portfolio not found.</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <main className="flex min-h-[calc(100vh-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
          <div className="flex flex-col space-y-1">
            <CardTitle className="text-lg font-medium">
              {portfolio.name.toUpperCase()}
            </CardTitle>
            <CardDescription className="text-sm text-gray-500">
              {portfolio.description}
              <br />
              Asset Type: {portfolio.asset_type}
            </CardDescription>
          </div>
          <div className="flex items-center gap-2">
            <Button size="icon" variant="ghost">
              <FileEditIcon className="w-4 h-4 text-blue-500" />
            </Button>
            <Button size="icon" variant="ghost">
              <TrashIcon className="w-4 h-4 text-red-500" />
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">$45,231.89</div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            +20.1% from last month
          </p>
          <div className="grid grid-cols-3 gap-4">
            <div className="col-span-2">
              <CurvedlineChart className="w-full aspect-[3/1]" />
            </div>
            <div className="col-span-1">
              <PieChart className="w-full aspect-[3/2]" />
            </div>
          </div>
        </CardContent>
      </Card>
      <RenderAssetsTable />
      <div className="flex justify-between mt-8">
        <h2 className="text-lg font-medium">Transactions</h2>
        <Button>Add New Transaction</Button>
      </div>
      <div className="mt-4">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Date
              </th>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Type
              </th>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Amount
              </th>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="hover:bg-gray-100">
              <td className="py-4 px-6 border-b border-gray-200">2024-01-01</td>
              <td className="py-4 px-6 border-b border-gray-200">Buy</td>
              <td className="py-4 px-6 border-b border-gray-200">$1,000.00</td>
              <td className="py-4 px-6 border-b border-gray-200">
                <div className="flex items-center gap-2">
                  <Button size="icon" variant="ghost">
                    <FileEditIcon className="w-4 h-4 text-blue-500" />
                  </Button>
                  <Button size="icon" variant="ghost">
                    <TrashIcon className="w-4 h-4 text-red-500" />
                  </Button>
                </div>
              </td>
            </tr>
            <tr className="hover:bg-gray-100">
              <td className="py-4 px-6 border-b border-gray-200">2024-01-02</td>
              <td className="py-4 px-6 border-b border-gray-200">Sell</td>
              <td className="py-4 px-6 border-b border-gray-200">$500.00</td>
              <td className="py-4 px-6 border-b border-gray-200">
                <div className="flex items-center gap-2">
                  <Button size="icon" variant="ghost">
                    <FileEditIcon className="w-4 h-4 text-blue-500" />
                  </Button>
                  <Button size="icon" variant="ghost">
                    <TrashIcon className="w-4 h-4 text-red-500" />
                  </Button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  );
};

export default PortfolioDetail;

function CurvedlineChart(props: any) {
  return (
    <div {...props}>
      <ResponsiveLine
        data={[
          {
            id: "B",
            data: [
              { x: "2018-01-01", y: 7 },
              { x: "2018-01-02", y: 5 },
              { x: "2018-01-03", y: 11 },
              { x: "2018-01-04", y: 9 },
              { x: "2018-01-05", y: 12 },
              { x: "2018-01-06", y: 16 },
              { x: "2018-01-07", y: 13 },
              { x: "2018-01-08", y: 13 },
            ],
          },
          {
            id: "A",
            data: [
              { x: "2018-01-01", y: 9 },
              { x: "2018-01-02", y: 8 },
              { x: "2018-01-03", y: 13 },
              { x: "2018-01-04", y: 6 },
              { x: "2018-01-05", y: 8 },
              { x: "2018-01-06", y: 14 },
              { x: "2018-01-07", y: 11 },
              { x: "2018-01-08", y: 12 },
            ],
          },
        ]}
        enableCrosshair={false}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{
          type: "time",
          format: "%Y-%m-%d",
          useUTC: false,
          precision: "day",
        }}
        xFormat="time:%Y-%m-%d"
        yScale={{
          type: "linear",
          min: 0,
          max: "auto",
        }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "X",
          legendOffset: 45,
          legendPosition: "middle",
          format: "%b %d",
          tickValues: "every 1 day",
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Y",
          legendOffset: -45,
          legendPosition: "middle",
        }}
        colors={{ scheme: "paired" }}
        pointSize={5}
        pointColor={{
          from: "color",
          modifiers: [["darker", 0.2]],
        }}
        pointBorderWidth={2}
        pointBorderColor={{
          from: "color",
          modifiers: [["darker", 0.2]],
        }}
        pointLabelYOffset={-12}
        useMesh={true}
        curve="monotoneX"
        legends={[
          {
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 100,
            translateY: 0,
            itemsSpacing: 0,
            itemDirection: "left-to-right",
            itemWidth: 80,
            itemHeight: 20,
            symbolSize: 14,
            symbolShape: "circle",
          },
        ]}
        theme={{
          tooltip: {
            container: {
              fontSize: "12px",
            },
          },
        }}
        role="application"
      />
    </div>
  );
}

function PieChart(props: any) {
  return (
    <div {...props}>
      <ResponsivePie
        data={[
          {
            id: "A",
            value: 634,
          },
          {
            id: "B",
            value: 456,
          },
          {
            id: "C",
            value: 150,
          },
          {
            id: "D",
            value: 258,
          },
          {
            id: "E",
            value: 511,
          },
        ]}
        sortByValue
        margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
        cornerRadius={0}
        activeOuterRadiusOffset={2}
        borderWidth={1}
        borderColor={{
          from: "color",
          modifiers: [["darker", 0.2]],
        }}
        arcLabel="id"
        arcLabelsRadiusOffset={0.6}
        arcLabelsTextColor={{
          from: "color",
          modifiers: [["darker", 2]],
        }}
        enableArcLinkLabels={false}
        colors={{ scheme: "paired" }}
        legends={[
          {
            anchor: "bottom",
            direction: "row",
            justify: false,
            translateX: 0,
            translateY: 56,
            itemsSpacing: 0,
            itemWidth: 50,
            itemHeight: 18,
            itemDirection: "left-to-right",
            symbolSize: 18,
            symbolShape: "circle",
          },
        ]}
        theme={{
          tooltip: {
            container: {
              fontSize: "12px",
            },
          },
        }}
        role="application"
      />
    </div>
  );
}
