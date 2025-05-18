import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { SimilarBacteria } from "@/lib/types";
import { CircleCheck, CircleX, Database } from "lucide-react";

interface BacteriaTableDisplayProps {
  isLoading: boolean;
  bacteria: SimilarBacteria[];
  totalItems: number;
  pageSize: number;
  onClearFilters: () => void;
}

export const BacteriaTableDisplay: React.FC<BacteriaTableDisplayProps> = ({
  isLoading,
  bacteria,
  totalItems,
  pageSize,
  onClearFilters,
}) => {
  return (
    <Card className="glass-card shadow-lg overflow-hidden border-primary/20">
      <CardHeader className="bg-gradient-to-r from-primary/10 to-blue-500/5 rounded-t-lg">
        <CardTitle className="flex items-center gap-2 text-xl">
          <Database className="h-5 w-5 text-primary" />
          Bacteria List
        </CardTitle>
        <CardDescription>
          Showing {isLoading ? "..." : bacteria.length} of{" "}
          {isLoading ? "..." : totalItems} bacteria
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border border-primary/20 overflow-hidden">
          <Table>
            <TableHeader className="bg-muted/50">
              <TableRow>
                <TableHead className="w-[100px]">ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Gram Stain</TableHead>
                <TableHead>Shape</TableHead>
                <TableHead>Phylum</TableHead>
                <TableHead>Pathogenic</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                Array(pageSize)
                  .fill(0)
                  .map((_, index) => (
                    <TableRow
                      key={`skeleton-${index}`}
                      className="animate-pulse"
                    >
                      {Array(6)
                        .fill(0)
                        .map((_, cellIndex) => (
                          <TableCell key={`skeleton-cell-${cellIndex}`}>
                            <Skeleton className="h-5 w-full" />
                          </TableCell>
                        ))}
                    </TableRow>
                  ))
              ) : bacteria.length > 0 ? (
                bacteria.map((bact) => (
                  <TableRow
                    key={bact.id}
                    className="hover:bg-primary/5 transition-colors"
                  >
                    <TableCell className="font-mono text-xs">
                      {bact.bacteria_id}
                    </TableCell>
                    <TableCell className="font-medium">
                      {bact.name || "Unknown"}
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          bact.gram_stain === "Positive"
                            ? "outline"
                            : "secondary"
                        }
                        className={
                          bact.gram_stain === "Positive"
                            ? "border-violet-500/50 text-violet-700 bg-violet-50 dark:bg-violet-950/30 dark:text-violet-300"
                            : bact.gram_stain === "Negative"
                            ? "border-blue-500/50 text-blue-700 bg-blue-50 dark:bg-blue-950/30 dark:text-blue-300"
                            : "border-gray-500/50 text-gray-700 bg-gray-50 dark:bg-gray-950/30 dark:text-gray-300"
                        }
                      >
                        {bact.gram_stain || "Unknown"}
                      </Badge>
                    </TableCell>
                    <TableCell>{bact.shape || "Unknown"}</TableCell>
                    <TableCell>
                      {bact.phylum ? (
                        <Badge
                          variant="outline"
                          className="border-primary/50 text-primary bg-primary/10"
                        >
                          {bact.phylum}
                        </Badge>
                      ) : (
                        "Unknown"
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        {bact.is_pathogen === true ? (
                          <Badge
                            variant="destructive"
                            className="flex items-center gap-1 bg-red-100 text-red-700 dark:bg-red-950/30 dark:text-red-300 border-red-300"
                          >
                            <CircleX className="h-3 w-3" />
                            Yes
                          </Badge>
                        ) : bact.is_pathogen === false ? (
                          <Badge
                            variant="outline"
                            className="flex items-center gap-1 border-green-300 text-green-700 bg-green-50 dark:bg-green-950/30 dark:text-green-300"
                          >
                            <CircleCheck className="h-3 w-3" />
                            No
                          </Badge>
                        ) : (
                          <Badge
                            variant="outline"
                            className="border-gray-300 text-gray-700 bg-gray-50"
                          >
                            No
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} className="text-center h-24">
                    <div className="flex flex-col items-center justify-center space-y-2 text-muted-foreground">
                      <Database className="h-10 w-10 opacity-40" />
                      <p>No bacteria found matching your filters.</p>
                      <Button
                        variant="outline"
                        onClick={onClearFilters}
                        className="mt-2"
                      >
                        Clear filters
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};
