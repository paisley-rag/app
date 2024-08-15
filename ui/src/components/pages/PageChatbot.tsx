import { Typography } from "../Typography";
import { Chatbot } from "../Chatbot";
import { ChatbotConfiguration } from "../ChatbotConfiguration";
import { chatbotService } from "@/services/chatbot-service";
import { useQuery } from "@tanstack/react-query";
import { useLocation } from "wouter";
import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { ArrowLeftIcon } from "lucide-react";
import { ErrorMessageWithReload } from "../ErrorMessageWithReload";
import axios from "axios";

import { useMutation } from "@tanstack/react-query";
const baseUrl = import.meta.env.VITE_BASE_URL;

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

  const [, navigate] = useLocation();

  function handleBackClick() {
    navigate("/chatbots");
  }

  const deleteMutation = useMutation({
    mutationFn: (id: string) => axios.delete(`${baseUrl}/api/chatbots/${id}/delete`),
    onSuccess: () => {
      navigate('/chatbots'); // doesn't work for some reason
    },
    onError: (error) => {
      console.error("Error deleting chatbot:", error);
    },
  });

  function handleDeleteClick(id: string) {
    if (window.confirm("Are you sure you want to delete this chatbot?")) {
      deleteMutation.mutate(id);
    }
  }

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
          <Typography variant="h3" className="mb-5 flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={handleBackClick}>
              <ArrowLeftIcon className="h-5 w-5" />
            </Button>
            {chatbot.name}
          </Typography>
          
        </header>
        <div className="grid grid-cols-2 gap-4">
          <Chatbot id={id} />
          <ChatbotConfiguration
            chatbot={chatbot}
            knowledgeBases={knowledgeBases}
            onDeleteClick={(id: string) => handleDeleteClick(id)}
          />
        </div>
      </>
    );
}
