import { Typography } from "../Typography";
import { Chatbot } from "../Chatbot";
import { ChatbotConfiguration } from "../ChatbotConfiguration";
import { chatbotService } from "@/services/chatbot-service";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import { useLocation, useParams } from "wouter";
import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { ArrowLeftIcon } from "lucide-react";
import { ErrorMessageWithReload } from "../ErrorMessageWithReload";

export function PageChatbot() {
  const { id } = useParams();

  if (!id || id === 'create') return null;

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

  const queryClient = useQueryClient();

  const [, navigate] = useLocation();


  function handleBackClick() {
    navigate("/chatbots");
  }

  const deleteMutation = useMutation({
    mutationFn: async () => {
      // Note: Note sure WHY this works, but it seems critical:
      // - mutationFn defined as 'async'
      // - having the return statement on a separate line from service call
      chatbotService.deleteChatbotById(id);
      return
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["chatbot", id] });
      navigate('/chatbots');
    },
    onError: (error) => {
      console.error("Error deleting chatbot:", error);
    },
  });

  function handleDeleteClick() {
    if (window.confirm("Are you sure you want to delete this chatbot?")) {
      deleteMutation.mutate();
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
            onDeleteClick={() => handleDeleteClick()}
          />
        </div>
      </>
    );
}
