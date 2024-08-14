
import { useQuery } from "@tanstack/react-query";

// import { Input } from "@/components/ui/input";
import { metricService } from "../../services/metric-service";

import { useEffect } from 'react';
import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
import ExportData from 'highcharts/modules/export-data';
import Accessibility from 'highcharts/modules/accessibility';

Exporting(Highcharts);
ExportData(Highcharts);
Accessibility(Highcharts);


export function PageLineChart() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ["metrics"],
    queryFn: () => metricService.fetchChatbotMetrics(),
    // staleTime: 5 * 60 * 1000, // 5 minutes
    // refetchOnWindowFocus: false, // Disable refetch on window focus
  });

  useEffect(() => {
    if (!isLoading && metrics) {
      Highcharts.chart('container', {
        chart: {
          zooming: {
            type: 'x'
          },
          events: {
            render: function () {
              const info = this.xAxis[0]?.tickPositions?.info;

              if (info) {
                this.setTitle({
                  text: 'chatbot-123'
                });
              }
            }
          }
        },
        xAxis: {
          type: 'datetime',
          minRange: 1000 * 60 * 60 * 24 * 2, // maximum zoom allowed: 2 days
          units: [
            ['day', [1, 4]],
            ['month', [1]]
          ]
        },
        series: metrics
      });
    }
  }, [isLoading, metrics]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div id="container"></div>
  );
}