import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/hooks/use-toast";
import { bacteriaService, PaginationParams } from "@/lib/api";
import { FilterFormData, SimilarBacteria } from "@/lib/types";
import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { BacteriaFilterForm } from "@/components/list/BacteriaFilterForm";
import { BacteriaTableDisplay } from "@/components/list/BacteriaTable";
import { BacteriaPaginationControls } from "@/components/list/PaginationControl";

const BacteriaDatabase = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [isLoading, setIsLoading] = useState(true);
  const [bacteria, setBacteria] = useState<SimilarBacteria[]>([]);

  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [uniquePhylums, setUniquePhylums] = useState<string[]>([]);
  const [filterData, setFilterData] = useState<FilterFormData>({
    name: "",
    gramStain: "",
    isPathogen: "",
    phylum: "",
  });
  const [error, setError] = useState<string | null>(null);

  const { register, handleSubmit, reset, setValue } = useForm<FilterFormData>({
    defaultValues: filterData,
  });

  const loadBacteria = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const isPathogen =
        filterData.isPathogen === "true"
          ? true
          : filterData.isPathogen === "false"
          ? false
          : undefined;

      const params: PaginationParams = {
        page: currentPage,
        page_size: pageSize,
        search: filterData.name || undefined,
        is_pathogen: isPathogen,
        gram_stain: filterData.gramStain || undefined,
        phylum: filterData.phylum || undefined,
      };
      const response = await bacteriaService.getBacteriaList(params);
      if (response.success && response.data) {
        setBacteria(response.data);
        setTotalItems(response.meta?.total_items || 0);
        setTotalPages(response.meta?.total_pages || 1);
      } else {
        setError(response.message || "Failed to load bacteria data");
        toast({
          variant: "destructive",
          title: "Error loading bacteria",
          description: response.message || "Failed to load bacteria data",
        });
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "An unknown error occurred";
      setError(errorMessage);
      toast({
        variant: "destructive",
        title: "Error loading bacteria",
        description: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  }, [
    currentPage,
    pageSize,
    filterData,
    setIsLoading,
    setError,
    setBacteria,
    setTotalItems,
    setTotalPages,
  ]);

  useEffect(() => {
    loadBacteria();
  }, [loadBacteria]);

  const onSubmitFilter = (data: FilterFormData) => {
    setFilterData(data);
    setCurrentPage(1);
  };

  const clearFilters = () => {
    const clearedFilters = {
      name: "",
      gramStain: "",
      isPathogen: "",
      phylum: "",
    };
    reset(clearedFilters);
    setFilterData(clearedFilters);
    setCurrentPage(1);
  };

  const handleSelectChange = (
    fieldName: keyof FilterFormData,
    value: string
  ) => {
    setValue(fieldName, value);
    setFilterData((prev) => ({ ...prev, [fieldName]: value }));
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const handlePageSizeChange = (size: number) => {
    setPageSize(size);
    setCurrentPage(1);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-primary to-blue-500 bg-clip-text text-transparent">
          Bacteria Database
        </h1>
        <p className="text-muted-foreground max-w-3xl">
          Browse our comprehensive collection of bacterial species and their
          characteristics. Use the filters below to refine your search.
        </p>
      </div>

      <BacteriaFilterForm
        isLoading={isLoading}
        uniquePhylums={uniquePhylums}
        onSubmit={handleSubmit(onSubmitFilter)}
        onClearFilters={clearFilters}
        register={register}
        filterData={filterData}
        handleSelectChange={handleSelectChange}
      />

      {error && (
        <Card className="bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
          <CardContent className="py-4">
            <p className="text-red-600 dark:text-red-400">{error}</p>
          </CardContent>
        </Card>
      )}

      <BacteriaTableDisplay
        isLoading={isLoading}
        bacteria={bacteria}
        totalItems={totalItems}
        pageSize={pageSize}
        onClearFilters={clearFilters}
      />

      <BacteriaPaginationControls
        currentPage={currentPage}
        totalPages={totalPages}
        pageSize={pageSize}
        bacteriaCount={bacteria.length}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};

export default BacteriaDatabase;
