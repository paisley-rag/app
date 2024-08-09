import { Typography } from "../Typography";
import { Chatbot } from "../Chatbot";
import { ChatbotConfiguration } from "../ChatbotConfiguration";
import { chatbotService } from "@/services/chatbot-service";
import { useQuery } from "@tanstack/react-query";
import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorMessageWithReload } from "../ErrorMessageWithReload";

interface PageChatbotProps {
  id: string;
}

export function PageChatbot({ id }: PageChatbotProps) {
  const {
    data: chatbot,
    isLoading: isChatbotLoading,
    error: chatbotError,
  } = useQuery({
    queryKey: ["chatbot", id],
    queryFn: () => chatbotService.fetchChatbotById(id),
  });

  const {
    data: knowledgeBases,
    isLoading: isKnowledgeBasesLoading,
    error: knowledgeBasesError,
  } = useQuery<ServerKnowledgeBaseConfig[]>({
    queryKey: ["knowledgeBases"],
    queryFn: knowledgeBaseService.fetchKnowledgeBases,
  });

  if (isChatbotLoading || isKnowledgeBasesLoading) {
    return (
      <>
        <header>
          <Skeleton className="h-10 mb-4" />
        </header>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Skeleton className="h-10 mb-4" />
            <Skeleton className="h-6 mb-2" />
            <Skeleton className="h-6 mb-2" />
            <Skeleton className="h-6 mb-2" />
          </div>
          <div>
            <Skeleton className="h-10 mb-4" />
            <Skeleton className="h-6 mb-2" />
            <Skeleton className="h-6 mb-2" />
            <Skeleton className="h-6 mb-2" />
          </div>
        </div>
      </>
    );
  }

  if (chatbotError || knowledgeBasesError) {
    return (
      <>
        <ErrorMessageWithReload />
      </>
    );
  }

  if (chatbot && knowledgeBases)
    return (
      <>
        <header>
          <Typography variant="h3" className="mb-5">
            {chatbot.name}
          </Typography>
        </header>
        <div className="grid grid-cols-2 gap-4">
          <Chatbot id={id} />
          <ChatbotConfiguration
            chatbot={chatbot}
            knowledgeBases={knowledgeBases}
          />
        </div>
      </>
    );
}
