import BacteriaPredictionForm from "@/components/bacteria/BacteriaForm";
import BacteriaPredictionResult from "@/components/bacteria/BacteriaResult";
import { Loading } from "@/components/loading";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "@/hooks/use-toast";
import { bacteriaService } from "@/lib/api";
import { BacteriaPredictionInput, PredictionResult } from "@/lib/types";
import { sanitizeBacteriaPredictionInput } from "@/lib/utils";
import { useState } from "react";

const PredictBacteria: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [predictionResult, setPredictionResult] =
    useState<PredictionResult | null>(null);
  const [activeTab, setActiveTab] = useState("form");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: BacteriaPredictionInput) => {
    try {
      setIsLoading(true);
      setError(null);

      const sanitizedData = sanitizeBacteriaPredictionInput({
        ...data,
        bacteria_id: data.bacteria_id || `TEMP-${Date.now()}`,
      }) as BacteriaPredictionInput;

      const result = await bacteriaService.predictPathogenicity(sanitizedData);
      setPredictionResult(result);
      setActiveTab("result");
      toast({
        title: "Prediction complete",
        description: "Your bacteria has been analyzed successfully.",
      });
    } catch (error) {
      console.error("Error in handleSubmit:", error);
      setError(
        error instanceof Error ? error.message : "Unknown error occurred"
      );
      toast({
        variant: "destructive",
        title: "Prediction failed",
        description:
          error instanceof Error
            ? error.message
            : "There was an error processing your request. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewPrediction = () => {
    setActiveTab("form");
  };

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">
          Bacteria Pathogenicity Prediction
        </h1>
        <p className="text-muted-foreground">
          Enter bacteria characteristics to predict its pathogenicity.
        </p>
      </div>

      {error && (
        <Card className="border-red-500 bg-red-50 dark:bg-red-950/20">
          <CardContent className="pt-6">
            <p className="text-red-600 dark:text-red-400">{error}</p>
          </CardContent>
        </Card>
      )}

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="form">Input Form</TabsTrigger>
          <TabsTrigger value="result" disabled={!predictionResult}>
            Results
          </TabsTrigger>
        </TabsList>

        <TabsContent value="form" className="space-y-4 pt-4">
          {isLoading ? (
            <div className="flex justify-center py-12">
              <Loading size="lg" withText text="Processing your request..." />
            </div>
          ) : (
            <BacteriaPredictionForm
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
          )}
        </TabsContent>

        <TabsContent value="result" className="space-y-4 pt-4">
          {isLoading ? (
            <div className="flex justify-center py-12">
              <Loading size="lg" withText text="Processing your request..." />
            </div>
          ) : predictionResult ? (
            <BacteriaPredictionResult
              result={predictionResult}
              onNewPrediction={handleNewPrediction}
            />
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              No prediction results available. Please submit the form first.
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default PredictBacteria;
