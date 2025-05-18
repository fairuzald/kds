import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Activity, Database, Filter } from "lucide-react";
import { Link } from "react-router-dom";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer } from "recharts";

const Index = () => {
  const data = [
    { name: "Pathogenic", value: 64, color: "#ef5350" },
    { name: "Non-Pathogenic", value: 2110, color: "#66bb6a" },
  ];

  const features = [
    {
      icon: <Activity className="h-12 w-12 text-primary" />,
      title: "Bacteria Prediction",
      description:
        "Predict if a bacteria is pathogenic based on its characteristics using our advanced machine learning model.",
      link: "/predict",
      linkText: "Make a Prediction",
    },
    {
      icon: <Database className="h-12 w-12 text-primary" />,
      title: "Bacteria Database",
      description:
        "Browse our comprehensive database of bacteria with detailed information and pathogenicity status.",
      link: "/database",
      linkText: "Explore Database",
    },
    {
      icon: <Filter className="h-12 w-12 text-primary" />,
      title: "Similar Bacteria",
      description:
        "Find bacteria with similar characteristics to your input and compare their pathogenicity.",
      link: "/predict",
      linkText: "Find Similar Bacteria",
    },
  ];

  return (
    <div className="space-y-12">
      <section className="text-center space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">
          Bacteria Pathogenicity Prediction
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          An advanced machine learning system to predict whether a bacteria is
          pathogenic based on its characteristics.
        </p>
        <div className="flex justify-center gap-4 pt-4">
          <Button asChild size="lg">
            <Link to="/predict">Make a Prediction</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link to="/database">Explore Database</Link>
          </Button>
        </div>
      </section>

      <section className="grid lg:grid-cols-3 gap-6 pt-8">
        {features.map((feature, index) => (
          <Card
            key={index}
            className="glass-card form-section"
            style={{ animationDelay: `${index * 0.1 + 0.3}s` }}
          >
            <CardHeader className="space-y-1">
              <div className="mb-3">{feature.icon}</div>
              <CardTitle>{feature.title}</CardTitle>
              <CardDescription>{feature.description}</CardDescription>
            </CardHeader>
            <CardFooter>
              <Button asChild className="w-full">
                <Link to={feature.link}>{feature.linkText}</Link>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </section>

      <section className="pt-8">
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Bacteria Statistics</CardTitle>
            <CardDescription>
              Distribution of pathogenic and non-pathogenic bacteria in our
              database
            </CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center">
            <div className="w-full max-w-md h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name}: ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Legend verticalAlign="bottom" height={36} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
};

export default Index;
