import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FilterFormData } from "@/lib/types";
import { Filter, Search } from "lucide-react";
import React from "react";
import { UseFormRegister } from "react-hook-form";

interface BacteriaFilterFormProps {
  isLoading: boolean;
  uniquePhylums: string[];
  onSubmit: (e?: React.BaseSyntheticEvent) => Promise<void>;
  onClearFilters: () => void;
  register: UseFormRegister<FilterFormData>;
  filterData: FilterFormData;
  handleSelectChange: (fieldName: keyof FilterFormData, value: string) => void;
}

export const BacteriaFilterForm: React.FC<BacteriaFilterFormProps> = ({
  isLoading,
  uniquePhylums,
  onSubmit,
  onClearFilters,
  register,
  filterData,
  handleSelectChange,
}) => {
  return (
    <Card className="glass-card shadow-lg border-primary/20">
      <CardHeader className="bg-gradient-to-r from-primary/10 to-blue-500/5 rounded-t-lg">
        <CardTitle className="flex items-center gap-2 text-xl">
          <Filter className="h-5 w-5 text-primary" />
          Filter Bacteria
        </CardTitle>
        <CardDescription>
          Refine the results using the filters below.
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="name">
                Name or Species
              </label>
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  id="name"
                  placeholder="Search bacteria..."
                  className="pl-8 border-primary/20 focus-visible:ring-primary"
                  {...register("name")}
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="gramStain">
                Gram Stain
              </label>
              <Select
                onValueChange={(value) =>
                  handleSelectChange("gramStain", value)
                }
                value={filterData.gramStain}
              >
                <SelectTrigger
                  id="gramStain"
                  className="border-primary/20 focus:ring-primary"
                >
                  <SelectValue placeholder="All gram stains" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Positive">Positive</SelectItem>
                  <SelectItem value="Negative">Negative</SelectItem>
                  <SelectItem value="Variable">Variable</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="isPathogen">
                Pathogen Status
              </label>
              <Select
                onValueChange={(value) =>
                  handleSelectChange("isPathogen", value)
                }
                value={filterData.isPathogen}
              >
                <SelectTrigger
                  id="isPathogen"
                  className="border-primary/20 focus:ring-primary"
                >
                  <SelectValue placeholder="All bacteria" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="true">Pathogenic</SelectItem>
                  <SelectItem value="false">Non-pathogenic</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="phylum">
                Phylum
              </label>
              <Select
                onValueChange={(value) => handleSelectChange("phylum", value)}
                value={filterData.phylum}
              >
                <SelectTrigger
                  id="phylum"
                  className="border-primary/20 focus:ring-primary"
                >
                  <SelectValue placeholder="All phylums" />
                </SelectTrigger>
                <SelectContent>
                  {uniquePhylums.map((phylum) => (
                    <SelectItem key={phylum} value={phylum}>
                      {phylum}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-between pt-2 gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={onClearFilters}
              className="border-primary/20 hover:bg-primary/5 w-full sm:w-auto"
            >
              Clear Filters
            </Button>
            <Button
              type="submit"
              disabled={isLoading}
              className="bg-gradient-to-r from-primary to-blue-500 hover:from-primary/90 hover:to-blue-500/90 text-white w-full sm:w-auto"
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Filtering...
                </>
              ) : (
                <>Apply Filters</>
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};
