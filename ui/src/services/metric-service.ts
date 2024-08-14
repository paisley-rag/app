import axios from "axios";
import { SeriesOptionsType } from 'highcharts';
const baseUrl = import.meta.env.VITE_BASE_URL;

type SeriesData = SeriesOptionsType & {
  type: string;
  name: string;
  data: number[][];
};


function seriesFromData(test_data: any[]): SeriesData[] {
  let series: SeriesData[] = [
    {
      type: 'line',
      name: 'faithfulness',
      data: [],
    },
    {
      type: 'line',
      name: 'answer_relevancy',
      data: []
    }
  ];
  
  test_data.forEach((entry: any) => {
    let time_ms = new Date(entry.time).getTime();
    series[0].data.push([time_ms, entry.faithfulness]);
    series[1].data.push([time_ms, entry.answer_relevancy]);
  });

  return series;
}

async function fetchChatbotMetrics() {
  
  let chatbot = 'chatbot-123'
  // let chatbot = 'test1'
  // let chatbot = 'lpbot1'
  // let chatbot = 'lpbot'

  const response = await axios.get(`${baseUrl}/api/history`);
  let data = response.data

  data = data.filter((entry: any) => entry.chatbot_id === chatbot);

  return seriesFromData(data);
}

export const metricService = {
  fetchChatbotMetrics,
};
