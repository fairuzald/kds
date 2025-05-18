import * as z from "zod";

export const bacteriaFormSchema = z.object({
  genus: z.string().min(1, { message: "Genus is required" }),
  species: z.string().min(1, { message: "Species is required" }),
  gram_stain: z.string().min(1, { message: "Gram stain is required" }),
  shape: z.string().min(1, { message: "Shape is required" }),

  name: z.string().optional(),
  strain: z.string().optional(),
  superkingdom: z.string().optional(),
  kingdom: z.string().optional(),
  phylum: z.string().optional(),
  class_name: z.string().optional(),
  order: z.string().optional(),
  family: z.string().optional(),
  mobility: z.string().optional().nullable(),
  flagellar_presence: z.string().optional().nullable(),
  number_of_membranes: z.string().optional().nullable(),
  oxygen_preference: z.string().optional().nullable(),
  optimal_temperature: z.string().optional().nullable(),
  temperature_range: z.string().optional().nullable(),
  habitat: z.string().optional().nullable(),
  biotic_relationship: z.string().optional().nullable(),
  cell_arrangement: z.string().optional().nullable(),
  sporulation: z.string().optional().nullable(),
  metabolism: z.string().optional().nullable(),
  energy_source: z.string().optional().nullable(),
});

export type BacteriaFormValues = z.infer<typeof bacteriaFormSchema>;

export const convertFormValuesToBacteriaInput = (
  values: BacteriaFormValues
) => {
  return {
    ...values,
    mobility:
      values.mobility === "Motile"
        ? true
        : values.mobility === "Non-motile"
        ? false
        : null,
    flagellar_presence:
      values.flagellar_presence === "Yes"
        ? true
        : values.flagellar_presence === "No"
        ? false
        : null,
    sporulation:
      values.sporulation === "Yes"
        ? true
        : values.sporulation === "No"
        ? false
        : null,
    optimal_temperature: values.optimal_temperature
      ? parseFloat(values.optimal_temperature)
      : null,
    number_of_membranes: values.number_of_membranes
      ? parseInt(values.number_of_membranes)
      : null,
  };
};
