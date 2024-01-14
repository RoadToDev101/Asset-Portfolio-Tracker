import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@ui/table";

type Asset = {
  name: string;
  quantity: number;
  totalValue: number;
  averagePrice: number;
  currentValue: number;
};

const assets: Asset[] = [
  {
    name: "BTC",
    quantity: 2,
    totalValue: 20000,
    averagePrice: 10000,
    currentValue: 30000,
  },
  {
    name: "ETH",
    quantity: 10,
    totalValue: 25231.89,
    averagePrice: 2523.189,
    currentValue: 25231.89,
  },
];

const columns: ColumnDef<Asset>[] = [
  {
    header: "Asset",
    accessorKey: "name",
  },
  {
    header: "Quantity",
    accessorKey: "quantity",
  },
  {
    header: "Value",
    accessorKey: "totalValue",
  },
  {
    header: "Average Price",
    accessorKey: "averagePrice",
  },
  {
    header: "Current Value",
    accessorKey: "currentValue",
  },
];

interface AssetsTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

function AssetsTable<TData, TValue>({
  columns,
  data,
}: AssetsTableProps<TData, TValue>) {
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
  });
  return (
    <Table>
      <TableHeader>
        {table.getHeaderGroups().map((headerGroup) => (
          <TableRow key={headerGroup.id}>
            {headerGroup.headers.map((header) => {
              return (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              );
            })}
          </TableRow>
        ))}
      </TableHeader>
      <TableBody>
        {table.getRowModel().rows?.length ? (
          table.getRowModel().rows.map((row) => (
            <TableRow
              key={row.id}
              data-state={row.getIsSelected() && "selected"}
            >
              {row.getVisibleCells().map((cell) => (
                <TableCell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={columns.length} className="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}

const RenderAssetsTable = () => {
  const data = assets;

  return (
    <div className="container mx-auto py-10">
      <AssetsTable columns={columns} data={data} />
    </div>
  );
};

export default RenderAssetsTable;
