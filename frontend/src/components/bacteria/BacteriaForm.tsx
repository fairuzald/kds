import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { BacteriaPredictionInput, bacteriaPredictionSchema } from "@/lib/types";
import { zodResolver } from "@hookform/resolvers/zod";
import React from "react";
import { useForm } from "react-hook-form";

interface BacteriaPredictionFormProps {
  onSubmit: (data: BacteriaPredictionInput) => void;
  isLoading: boolean;
}

const BacteriaPredictionForm: React.FC<BacteriaPredictionFormProps> = ({
  onSubmit,
  isLoading,
}) => {
  const form = useForm<BacteriaPredictionInput>({
    resolver: zodResolver(bacteriaPredictionSchema),
    defaultValues: {
      genus: "",
      species: "",
      gram_stain: "",
      shape: "",
      mobility: "",
      oxygen_preference: "",
      habitat: "",
    },
  });

  const handleFormSubmit = (data: BacteriaPredictionInput) => {
    onSubmit(data);
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(handleFormSubmit)}
        className="space-y-8"
      >
        <Card className="glass-card form-section border">
          <CardHeader>
            <CardTitle>Essential Information</CardTitle>
            <CardDescription>
              Information about the bacteria for prediction.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-6">
              <FormField
                control={form.control}
                name="genus"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Genus</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g. Escherichia"
                        {...field}
                        value={field.value || ""}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="species"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Species</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g. coli"
                        {...field}
                        value={field.value || ""}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="gram_stain"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Gram Stain</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Gram stain" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Positive">Positive</SelectItem>
                        <SelectItem value="Negative">Negative</SelectItem>
                        <SelectItem value="Variable">Variable</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="shape"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Shape</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select shape" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Rod">Rod</SelectItem>
                        <SelectItem value="Cocci">Cocci</SelectItem>
                        <SelectItem value="Spiral">Spiral</SelectItem>
                        <SelectItem value="Vibrio">Vibrio</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </CardContent>
        </Card>

        <Card
          className="glass-card form-section border"
          style={{ animationDelay: "0.3s" }}
        >
          <CardHeader>
            <CardTitle>Additional Characteristics</CardTitle>
            <CardDescription>
              Optional but helpful for more accurate predictions.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-6">
              <FormField
                control={form.control}
                name="oxygen_preference"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Oxygen Preference</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select oxygen preference" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Aerobe">Aerobic</SelectItem>
                        <SelectItem value="Anaerobe">Anaerobic</SelectItem>
                        <SelectItem value="Facultative anaerobe">
                          Facultative
                        </SelectItem>
                        <SelectItem value="Microaerophilic">
                          Microaerophilic
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="mobility"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Mobility</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select mobility" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Yes">Motile</SelectItem>
                        <SelectItem value="No">Non-motile</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="habitat"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Habitat</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select habitat" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Soil">Soil</SelectItem>
                        <SelectItem value="Water">Water</SelectItem>
                        <SelectItem value="HostAssociated">
                          Host-associated
                        </SelectItem>
                        <SelectItem value="Multiple">Multiple</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="optimal_temperature"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Optimal Temperature (°C)</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="e.g. 37"
                        {...field}
                        value={field.value || ""}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <FormField
                control={form.control}
                name="phylum"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Phylum</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select phylum" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Proteobacteria">
                          Proteobacteria
                        </SelectItem>
                        <SelectItem value="Firmicutes">Firmicutes</SelectItem>
                        <SelectItem value="Actinobacteria">
                          Actinobacteria
                        </SelectItem>
                        <SelectItem value="Bacteroidetes">
                          Bacteroidetes
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="flagellar_presence"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Flagellar Presence</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value || ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select flagellar presence" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </CardContent>
          <CardFooter className="border-t p-6">
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Predicting..." : "Predict Pathogenicity"}
            </Button>
          </CardFooter>
        </Card>
      </form>
    </Form>
  );
};

export default BacteriaPredictionForm;
