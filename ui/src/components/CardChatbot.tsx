import { Link } from "wouter";
import { ClientPipelineConfig } from "../services/chatbot-service";

interface CardChatbotProps {
  chatbot: ClientPipelineConfig;
}

export function CardChatbot({ chatbot }: CardChatbotProps) {
  return (
    <li key={chatbot.id}>
      <Link href={`/chatbots/${chatbot.id}`}>
        <div className="card p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow">
          {chatbot.name}
        </div>
      </Link>
    </li>
  );
}
