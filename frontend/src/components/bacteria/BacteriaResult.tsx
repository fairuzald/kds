import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { PredictionResult, SimilarBacteria } from "@/lib/types";
import { Activity, CircleCheck, CircleX } from "lucide-react";
import React from "react";

interface BacteriaPredictionResultProps {
  result: PredictionResult;
  onNewPrediction: () => void;
}

const SimilarBacteriaItem: React.FC<{ bacteria: SimilarBacteria }> = ({
  bacteria,
}) => {
  const getTaxonomyInfo = () => {
    const parts = [];
    if (bacteria.phylum) parts.push(`Phylum: ${bacteria.phylum}`);
    if (bacteria.class_name) parts.push(`Class: ${bacteria.class_name}`);
    if (bacteria.order) parts.push(`Order: ${bacteria.order}`);
    if (bacteria.family) parts.push(`Family: ${bacteria.family}`);

    if (parts.length === 0) {
      if (bacteria.gram_stain) parts.push(`Gram: ${bacteria.gram_stain}`);
      if (bacteria.shape) parts.push(`Shape: ${bacteria.shape}`);
    }

    if (parts.length === 0) {
      if (bacteria.oxygen_preference)
        parts.push(`Oxygen: ${bacteria.oxygen_preference}`);
      if (bacteria.habitat) parts.push(`Habitat: ${bacteria.habitat}`);
    }

    return parts.length > 0
      ? parts.join(" | ")
      : "No additional information available";
  };

  return (
    <div
      className={`p-4 rounded-lg border flex items-center justify-between ${
        bacteria.is_pathogen === true
          ? "bg-pathogen-100/40 border-pathogen-200"
          : "bg-non-pathogen-100/40 border-non-pathogen-200"
      }`}
    >
      <div className="flex items-center space-x-4">
        <div
          className={`h-8 w-8 rounded-full flex items-center justify-center ${
            bacteria.is_pathogen === true
              ? "bg-pathogen-500"
              : "bg-non-pathogen-500"
          }`}
        >
          {bacteria.is_pathogen === true ? (
            <CircleX className="h-5 w-5 text-white" />
          ) : (
            <CircleCheck className="h-5 w-5 text-white" />
          )}
        </div>
        <div>
          <h4 className="font-medium">
            {bacteria.name || "Unknown Bacterium"}
          </h4>
          <p className="text-sm text-muted-foreground">{getTaxonomyInfo()}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {bacteria.genus && bacteria.species
              ? `${bacteria.genus} ${bacteria.species}`
              : bacteria.genus || bacteria.species || ""}
            {bacteria.oxygen_preference && (bacteria.genus || bacteria.species)
              ? ` | ${bacteria.oxygen_preference}`
              : bacteria.oxygen_preference || ""}
          </p>
        </div>
      </div>
      <div className="text-right">
        <span className="text-sm font-semibold">
          {typeof bacteria.similarity_score === "number"
            ? (bacteria.similarity_score * 100).toFixed(2)
            : (parseFloat(String(bacteria.similarity_score)) * 100).toFixed(2)}
          % similarity
        </span>
      </div>
    </div>
  );
};

const BacteriaPredictionResult: React.FC<BacteriaPredictionResultProps> = ({
  result,
  onNewPrediction,
}) => {
  if (!result) {
    return (
      <Card className="p-6">
        <CardContent>
          <p className="text-center text-muted-foreground">
            No prediction data available
          </p>
        </CardContent>
      </Card>
    );
  }

  const pathogenProbability =
    typeof result.pathogen_probability === "number"
      ? result.pathogen_probability * 100
      : parseFloat(String(result.pathogen_probability)) * 100;

  const safePathogenProbability = isNaN(pathogenProbability)
    ? 0
    : pathogenProbability;

  return (
    <>
      <Card className="glass-card result-card border">
        <CardHeader>
          <CardTitle>Prediction Result</CardTitle>
          <CardDescription>
            Analysis results for{" "}
            {result.input_bacteria?.genus || "Unknown genus"}{" "}
            {result.input_bacteria?.species || "species"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex flex-col items-center space-y-4">
            {result.is_pathogen_prediction ? (
              <>
                <div className="h-24 w-24 rounded-full bg-pathogen-100 flex items-center justify-center">
                  <CircleX className="h-12 w-12 text-pathogen-500" />
                </div>
                <h3 className="text-xl font-semibold text-pathogen-500">
                  Likely Pathogenic
                </h3>
              </>
            ) : (
              <>
                <div className="h-24 w-24 rounded-full bg-non-pathogen-100 flex items-center justify-center">
                  <CircleCheck className="h-12 w-12 text-non-pathogen-500" />
                </div>
                <h3 className="text-xl font-semibold text-non-pathogen-500">
                  Likely Non-Pathogenic
                </h3>
              </>
            )}

            <div className="w-full max-w-md space-y-2">
              <div className="flex justify-between text-sm">
                <span>Pathogenicity Probability</span>
                <span className="font-semibold">
                  {safePathogenProbability.toFixed(1)}%
                </span>
              </div>
              <Progress
                value={safePathogenProbability}
                className={
                  result.is_pathogen_prediction
                    ? "bg-pathogen-100"
                    : "bg-non-pathogen-100"
                }
              />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Low Risk</span>
                <span>High Risk</span>
              </div>
            </div>
          </div>

          <Alert
            className={
              result.is_pathogen_prediction
                ? "border-pathogen-500"
                : "border-non-pathogen-500"
            }
          >
            <Activity
              className={`h-4 w-4 ${
                result.is_pathogen_prediction
                  ? "text-pathogen-500"
                  : "text-non-pathogen-500"
              }`}
            />
            <AlertTitle>
              {result.is_pathogen_prediction
                ? "Pathogenic Risk Detected"
                : "Low Pathogenic Risk"}
            </AlertTitle>
            <AlertDescription>
              {result.is_pathogen_prediction
                ? "This bacteria has characteristics commonly associated with pathogenic species. Further laboratory testing is recommended."
                : "This bacteria has characteristics that are not typically associated with pathogenic species."}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {Array.isArray(result.similar_bacteria) &&
      result.similar_bacteria.length > 0 ? (
        <Card
          className="glass-card result-card border"
          style={{ animationDelay: "0.4s" }}
        >
          <CardHeader>
            <CardTitle>Similar Bacteria</CardTitle>
            <CardDescription>
              Bacteria with similar characteristics from our database
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[400px]">
              <div className="space-y-4">
                {result.similar_bacteria.map((bacteria, index) => (
                  <SimilarBacteriaItem
                    key={bacteria.bacteria_id || `similar-${index}`}
                    bacteria={bacteria}
                  />
                ))}
              </div>
            </ScrollArea>
          </CardContent>
          <CardFooter className="border-t p-6">
            <Button
              variant="outline"
              onClick={onNewPrediction}
              className="w-full"
            >
              Make Another Prediction
            </Button>
          </CardFooter>
        </Card>
      ) : (
        <Card
          className="glass-card result-card border"
          style={{ animationDelay: "0.4s" }}
        >
          <CardHeader>
            <CardTitle>Similar Bacteria</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-center text-muted-foreground py-8">
              No similar bacteria found in the database.
            </p>
          </CardContent>
          <CardFooter className="border-t p-6">
            <Button
              variant="outline"
              onClick={onNewPrediction}
              className="w-full"
            >
              Make Another Prediction
            </Button>
          </CardFooter>
        </Card>
      )}
    </>
  );
};

export default BacteriaPredictionResult;
