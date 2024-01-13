/* eslint-disable @typescript-eslint/no-explicit-any */
import { Button } from "@/components/ui/button";
import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { ResponsiveLine } from "@nivo/line";
import { ResponsivePie } from "@nivo/pie";

const PortfolioDetail = () => {
  return (
    <main className="flex min-h-[calc(100vh-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle className="text-lg font-medium">Portfolio 1</CardTitle>
          <div className="flex items-center gap-2">
            <Button size="icon" variant="ghost">
              <FileEditIcon className="w-4 h-4 text-blue-500" />
            </Button>
            <Button size="icon" variant="ghost">
              <DeleteIcon className="w-4 h-4 text-red-500" />
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
      <div className="flex justify-between mt-8">
        <h2 className="text-lg font-medium">Assets</h2>
      </div>
      <div className="mt-4">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Asset
              </th>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Quantity
              </th>
              <th className="py-4 px-6 bg-gray-100 font-bold uppercase text-sm text-gray-500 border-b border-gray-200">
                Value
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="hover:bg-gray-100">
              <td className="py-4 px-6 border-b border-gray-200">BTC</td>
              <td className="py-4 px-6 border-b border-gray-200">2</td>
              <td className="py-4 px-6 border-b border-gray-200">$20,000.00</td>
            </tr>
            <tr className="hover:bg-gray-100">
              <td className="py-4 px-6 border-b border-gray-200">ETH</td>
              <td className="py-4 px-6 border-b border-gray-200">10</td>
              <td className="py-4 px-6 border-b border-gray-200">$25,231.89</td>
            </tr>
          </tbody>
        </table>
      </div>
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
                    <DeleteIcon className="w-4 h-4 text-red-500" />
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
                    <DeleteIcon className="w-4 h-4 text-red-500" />
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

function DeleteIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M20 5H9l-7 7 7 7h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Z" />
      <line x1="18" x2="12" y1="9" y2="15" />
      <line x1="12" x2="18" y1="9" y2="15" />
    </svg>
  );
}

function FileEditIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 13.5V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2h-5.5" />
      <polyline points="14 2 14 8 20 8" />
      <path d="M10.42 12.61a2.1 2.1 0 1 1 2.97 2.97L7.95 21 4 22l.99-3.95 5.43-5.44Z" />
    </svg>
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
