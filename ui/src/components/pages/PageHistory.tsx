"use client";

import { useEffect, useState } from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { 
  ArrowUpDown, 
  ChevronDown, 
  // MoreHorizontal 
} from "lucide-react";

import { Button } from "@/components/ui/button";
// import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  // DropdownMenuLabel,
  // DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
// import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { useQuery } from "@tanstack/react-query";

import { chatbotService } from "../../services/chatbot-service";
import { historyService } from "../../services/history-service";
import { metricService } from "../../services/metric-service";

export function PageHistory() {
  const [selectedChatbot, setSelectedChatbot] = useState(() => {
    return localStorage.getItem('selectedChatbot') || '';
  });

  const { data: chatHistory, isLoading } = useQuery({
    queryKey: ["chatHistory"],
    queryFn: () => historyService.fetchChatbotHistory(),
  });

  
  
  
  // Name/id cache for chatbots
  const [chatbotNames, setChatbotNames] = useState<{ [key: string]: string }>({});
  
  useEffect(() => {
    const fetchChatbotNames = async () => {
      if (chatHistory) {
        const chatbots = await chatbotService.fetchChatbots();
        const namesMap = Object.fromEntries(
          chatbots.map((chatbot: any) => [chatbot.id, chatbot.name])
        );
        setChatbotNames(namesMap);
      }
    };
    fetchChatbotNames();
  }, [chatHistory]);



  useEffect(() => {
    if (selectedChatbot) {
      localStorage.setItem('selectedChatbot', selectedChatbot);
      const chatbotId = Object.keys(chatbotNames).find(key => chatbotNames[key] === selectedChatbot);
      table.getColumn("chatbot_id")?.setFilterValue(chatbotId);
    }
  }, [selectedChatbot, chatbotNames]);

  const handleChatbotSelection = (name: string) => {
    setSelectedChatbot(name);
    
  };
 

  // Shadcn table stuff
  const [sorting, setSorting] = useState<SortingState>([
    { id: "time", desc: true }
  ]);

  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(
    []
  );

  const [columnVisibility, setColumnVisibility] =
    useState<VisibilityState>({});

  const [rowSelection, setRowSelection] = useState({});

  const [scoreNames, setScoreNames] = useState<string[]>([]);

  useEffect(() => {
    const fetchScoreNames = async () => {
      const scores = await metricService.fetchScoreNames();
      setScoreNames(scores);
    };
    fetchScoreNames();
  }, []);

  const columns: ColumnDef<any>[] = [
    {
      accessorKey: "chatbot_id",
      header: "Chatbot",
      cell: ({ row }) => {
        const id = row.getValue("chatbot_id") as string;
        const name = chatbotNames[id] || "Loading...";
        return <div>{name}</div>;
      },
    },
    {
      accessorKey: "time",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Time
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        );
      },
      cell: ({ row }) => (
        <div className="lowercase">
          {new Date(row.getValue("time")).toLocaleString()}
        </div>
      ),
    },
    {
      accessorKey: "input",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Input
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        );
      },
      cell: ({ row }) => <div className="lowercase">{row.getValue("input")}</div>,
    },
    {
      accessorKey: "output",
      header: "Output",
      cell: ({ row }) => {
        const output = row.getValue("output") as string;
        return (
          <div className="text-left font-medium">
            {output.slice(0, 150) + (output.length > 150 ? "..." : "")}
          </div>
        );
      },
    },
    {
      accessorKey: "context",
      header: () => <div className="text-left">Context</div>,
      cell: ({ row }) => {
        const context = row.getValue("context") as string | string[];
        const cellStyle = { width: '250px', maxHeight: '100px', overflowY: 'auto' }; // Added styles

        if (Array.isArray(context)) {
          return (
            <div className="text-left font-small" style={cellStyle}>
              {context.map((entry, index) => (
                <div key={index}>
                  {`CONTEXT ${index + 1}: ${entry.slice(0, 150) + (entry.length > 150 ? "..." : "")}`}
                </div>
              ))}
            </div>
          );
        } else {
          return (
            <div className="text-left font-small" style={cellStyle}>
              {context.slice(0, 150) + (context.length > 150 ? "..." : "")}
            </div>
          );
        }
      },
    },
    ...scoreNames.map((scoreName) => ({
      accessorKey: scoreName,
      header: () => <div className="text-right capitalize">{scoreName.replace(/_/g, ' ')}</div>,
      cell: ({ row }: any) => {
        const score = parseFloat(row.getValue(scoreName));
        return <div className="text-right font-medium">{score.toFixed(2)}</div>;
      },
    })),
  ];

  const table = useReactTable({
    data: chatHistory || [],
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full">
      <div className="flex items-center py-4">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">
              {selectedChatbot || "Select Chatbot"} <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start">
            {Object.entries(chatbotNames).map(([id, name]) => (
              <DropdownMenuItem
                key={id}
                onClick={() => handleChatbotSelection(name)}
              >
                {name}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                );
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="rounded-md border">
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
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
