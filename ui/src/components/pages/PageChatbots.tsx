import { useQuery } from "@tanstack/react-query";
import { useLocation } from "wouter";

import { Typography } from "../Typography";
import { Button } from "@/components/ui/button";
import { CardChatbot } from "../CardChatbot";

import {
  chatbotService,
  ClientPipelineConfig,
} from "../../services/chatbot-service";

export function PageChatbots() {
  const { data: chatbots, isLoading } = useQuery({
    queryKey: ["chatbots"],
    queryFn: () => chatbotService.fetchChatbots(),
  });
  const [, setLocation] = useLocation();

  const handleClick = () => {
    setLocation("/chatbots/create");
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (chatbots)
    return (
      <>
        <header className="flex justify-between items-baseline mb-8">
          <Typography variant="h3">Chatbots</Typography>
          <Button variant="default" onClick={handleClick}>
            Create new chatbot
          </Button>
        </header>
        {chatbots ? (
          <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {chatbots.map((chatbot: ClientPipelineConfig) => (
              <CardChatbot key={chatbot.id} chatbot={chatbot} />
            ))}
          </ul>
        ) : (
          <p>No chatbots found</p>
        )}
      </>
    );
}
