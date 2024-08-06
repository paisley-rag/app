import { Typography } from "../Typography";
import { Chatbot } from "../Chatbot";
import { ChatbotConfiguration } from "../ChatbotConfiguration";

interface PageChatbotProps {
  id: string;
}

export function PageChatbot({ id }: PageChatbotProps) {
  return (
    <header>
      <Typography variant="h2" className="mb-4">
        Chatbot Name
      </Typography>
      <div className="grid grid-cols-2 gap-4">
        <Chatbot id={id} />
        <ChatbotConfiguration id={id} />
      </div>
    </header>
  );
}
