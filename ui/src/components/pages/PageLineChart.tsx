
import { useQuery } from "@tanstack/react-query";

// import { Input } from "@/components/ui/input";
import { metricService } from "../../services/metric-service";

import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
import ExportData from 'highcharts/modules/export-data';
import Accessibility from 'highcharts/modules/accessibility';

Exporting(Highcharts);
ExportData(Highcharts);
Accessibility(Highcharts);

import { useEffect, useState } from 'react';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { chatbotService } from '../../services/chatbot-service';

import { Button } from "@/components/ui/button";
import { ChevronDown } from "lucide-react";

export function PageLineChart() {
  const [selectedChatbot, setSelectedChatbot] = useState(() => {
    return localStorage.getItem('selectedChatbot') || '';
  });

  useEffect(() => {
    if (selectedChatbot) {
      localStorage.setItem('selectedChatbot', selectedChatbot);
    }
  }, [selectedChatbot]);

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
              this.setTitle({
                text: selectedChatbot || 'No chatbot selected'
              });
            }
          }
        },
        xAxis: {
          type: 'datetime',
          minRange: minRange || 1000 * 60 * 60 * 24 * 3, // maximum zoom allowed: 2 days
          units: [
            ['minute', [1, 5, 15, 30]],
            ['hour', [1, 6, 12]],
            ['day', [1]]
          ],
          title: {
            text: 'Time'
          }
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
          <Button variant="outline">
            {selectedChatbot ? selectedChatbot : "Select Chatbot"} <ChevronDown className="ml-2 h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          {chatbots?.map((chatbot: any) => (
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
