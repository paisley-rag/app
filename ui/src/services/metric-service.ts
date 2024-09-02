import axios from "axios";
import { SeriesOptionsType } from 'highcharts';
import { axiosHeader, baseUrl } from '../lib/utils.ts';

import { chatbotService } from './chatbot-service';


export type SeriesData = SeriesOptionsType & {
  type: string;
  name: string;
  data: number[][];
};


async function seriesFromData(test_data: any[] = [], apiKey: string): Promise<any> {
  const scoreNames = await fetchScoreNames(apiKey);
    
  let series: SeriesData[] = scoreNames.map((name: string) => ({
    type: 'line',
    name: name,
    data: []
  }));
  
  if (!test_data) {
    return series;
  }

  test_data.forEach((entry: any) => {
    let time_ms = new Date(entry.time).getTime();
    scoreNames.forEach((name: string, index: number) => {
      series[index].data.push([time_ms, entry[name]]);
    });
  });
  return series;
}

async function fetchChatbotMetrics(chatbotName: string | null, apiKey: string) {
  
  let chatbots = await chatbotService.fetchChatbots(apiKey);

  const chatbot = chatbots.find((chatbot: any) => chatbot.name === chatbotName); // change any later
  if (!chatbot) {
    return seriesFromData([], apiKey);
  }

  const response = await axios.get(`${baseUrl}/api/history`, axiosHeader(apiKey));
  let data = response.data

  data = data.filter((entry: any) => entry.chatbot_id === chatbot.id);

  return seriesFromData(data, apiKey);
}

async function fetchScoreNames(apiKey: string) {
  const response = await axios.get(`${baseUrl}/api/scores`, axiosHeader(apiKey));
  console.log('SCORE NAMES ARE:', response.data)
  return response.data;
}

export const metricService = {
  fetchChatbotMetrics,
  fetchScoreNames
};
