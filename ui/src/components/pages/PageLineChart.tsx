
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

import { useState } from 'react';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { chatbotService } from '../../services/chatbot-service';

export function PageLineChart() {
  const [selectedChatbot, setSelectedChatbot] = useState(null);
  const { data: chatbots } = useQuery({
    queryKey: ["chatbots"],
    queryFn: () => chatbotService.fetchChatbots(),
  });

  const { data: metrics, isLoading } = useQuery({
    queryKey: ["metrics", selectedChatbot],
    queryFn: () => metricService.fetchChatbotMetrics(selectedChatbot),
    enabled: !!selectedChatbot,
  });

  useEffect(() => {
    if (!isLoading && metrics) {
      const minRange = metrics.reduce((min, series) => {
        const seriesMin = Math.min(...series.data.map(point => point[0]));
        const seriesMax = Math.max(...series.data.map(point => point[0]));
        return Math.min(min, seriesMax - seriesMin);
      }, Infinity);

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
                  text: selectedChatbot || 'No chatbot selected'
                });
              }
            }
          }
        },
        xAxis: {
          type: 'datetime',
          minRange: minRange || 1000 * 60 * 60 * 24 * 3, // maximum zoom allowed: 2 days
          units: [
            ['day', [1, 4]],
            ['month', [1]]
          ]
        },
        yAxis: {
          min: 0, // Set your desired minimum value
          max: 1.00 // Set your desired maximum value
        },
        series: metrics
      });
    }
  }, [isLoading, metrics, selectedChatbot]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger>
          <button>Select Chatbot</button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          {chatbots?.map((chatbot) => (
            <DropdownMenuItem key={chatbot.id} onSelect={() => setSelectedChatbot(chatbot.name)}>
              {chatbot.name}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
      <div id="container"></div>
    </div>
  );
}

// export function PageLineChart() {
//   const { data: metrics, isLoading } = useQuery({
//     queryKey: ["metrics"],
//     queryFn: () => metricService.fetchChatbotMetrics(),
//     // staleTime: 5 * 60 * 1000, // 5 minutes
//     // refetchOnWindowFocus: false, // Disable refetch on window focus
//   });

//   useEffect(() => {
//     if (!isLoading && metrics) {
//       Highcharts.chart('container', {
//         chart: {
//           zooming: {
//             type: 'x'
//           },
//           events: {
//             render: function () {
//               const info = this.xAxis[0]?.tickPositions?.info;

//               if (info) {
//                 this.setTitle({
//                   text: 'chatbot-123'
//                 });
//               }
//             }
//           }
//         },
//         xAxis: {
//           type: 'datetime',
//           minRange: 1000 * 60 * 60 * 24 * 2, // maximum zoom allowed: 2 days
//           units: [
//             ['day', [1, 4]],
//             ['month', [1]]
//           ]
//         },
//         series: metrics
//       });
//     }
//   }, [isLoading, metrics]);

//   if (isLoading) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div id="container"></div>
//   );
// }