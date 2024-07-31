import { Typography } from "../Typography";
import { Chatbot } from "../Chatbot";
import { ChatbotConfiguration } from "../ChatbotConfiguration";

interface PageChatbotProps {
  id: number;
}

export function PageChatbot({ id }: PageChatbotProps) {
  return (
    <header>
      <Typography variant="h2" className="mb-4">
        Chatbot Name
      </Typography>
      <div className="grid grid-cols-2 gap-8">
        <div>
          <Chatbot id={id} />
        </div>
        <div>
          <ChatbotConfiguration id={id} />
        </div>
      </div>
    </header>
  );
}
