import { useQuery } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { Typography } from "../Typography";
import { Button } from "@/components/ui/button";
import { CardChatbot } from "../CardChatbot";
import { SkeletonPageChatbots } from "../skeletons/SkeletonPageChatbots";
import { ApiKeyContext } from '../../providers/ApiKeyProvider.tsx';
import { useContext } from 'react';

import {
  chatbotService,
  ClientPipelineConfig,
} from "../../services/chatbot-service";

export function PageChatbots() {
  const { apiKey } = useContext(ApiKeyContext);
  const { data: chatbots, isLoading } = useQuery({
    queryKey: ["chatbots"],
    queryFn: () => chatbotService.fetchChatbots(apiKey),
  });
  const [, setLocation] = useLocation();

  const handleClick = () => {
    setLocation("/chatbots/create");
  };

  if (isLoading) {
    return <SkeletonPageChatbots />;
  }

  if (chatbots)
    return (
      <div className="mx-auto">
        <header className="flex flex-col md:flex-row justify-between items-baseline mb-8">
          <Typography variant="h3" className="mb-4 md:mb-0">
            Chatbots
          </Typography>
          <Button variant="default" onClick={handleClick}>
            Create new chatbot
          </Button>
        </header>
        {chatbots ? (
          <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {chatbots.map((chatbot: ClientPipelineConfig) => (
              <CardChatbot key={chatbot.id} chatbot={chatbot} />
            ))}
          </ul>
        ) : (
          <p>No chatbots found</p>
        )}
      </div>
    );
}
