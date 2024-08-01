import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useMutation, useQuery } from "@tanstack/react-query";

import { zodResolver } from "@hookform/resolvers/zod";

import { clientPipelineConfigSchema } from "../services/chatbot-service";
import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "../services/knowledge-base-service";
import { chatbotService } from "../services/chatbot-service";
import { ClientPipelineConfig } from "../services/chatbot-service";

import { Typography } from "./Typography";
import { Card } from "./ui/card";
import { Form } from "./ui/form";
import { Button } from "./ui/button";

import { KnowledgeBasesField } from "./form_fields/KnowledgeBasesField";
import { GenerativeModelField } from "./form_fields/GenerativeModelField";
import { SimilaritySearchField } from "./form_fields/SimilaritySearchField";
import { ColbertRerankField } from "./form_fields/ColbertRerankField";
import { LongContextReorderField } from "./form_fields/LongContextReorderField";
import { PromptField } from "./form_fields/PromptField";

interface ChatbotConfigurationProps {
  id: string;
}

export function ChatbotConfiguration({ id }: ChatbotConfigurationProps) {
  const mutation = useMutation({
    mutationFn: (data: ClientPipelineConfig) =>
      chatbotService.updateChatbot(id, data),
  });

  const {
    data: knowledgeBases,
    isLoading: isKnowledgeBasesLoading,
    error: knowledgeBasesError,
  } = useQuery<ServerKnowledgeBaseConfig[]>({
    queryKey: ["knowledgeBases"],
    queryFn: knowledgeBaseService.fetchKnowledgeBases,
  });

  const {
    data: chatbot,
    isLoading: isChatbotLoading,
    error: chatbotError,
  } = useQuery({
    queryKey: ["chatbot", id],
    queryFn: () => chatbotService.fetchChatbotById(id),
  });

  const [displayCutoff, setDisplayCutoff] = useState(false);
  const [displayTopN, setDisplayTopN] = useState(false);

  const form = useForm<ClientPipelineConfig>({
    resolver: zodResolver(clientPipelineConfigSchema),
  });

  useEffect(() => {
    if (chatbot && !isChatbotLoading) {
      form.reset(chatbot);
      setDisplayCutoff(chatbot.similarity.on);
      setDisplayTopN(chatbot.colbert_rerank.on);
    }
  }, [chatbot, isChatbotLoading, form]);

  const handleSubmit = form.handleSubmit(
    (data) => {
      mutation.mutate(data);
    },
    (errors) => {
      console.error("Form submission failed. Errors:", errors);
    }
  );

  if (isKnowledgeBasesLoading || isChatbotLoading) return <div>Loading...</div>;
  if (knowledgeBasesError) return <div>Error loading knowledge bases</div>;
  if (chatbotError) return <div>Error loading chatbot</div>;

  if (knowledgeBases && chatbot)
    return (
      <Card className="h-full flex flex-col px-6">
        <header className="flex justify-between items-baseline">
          <Typography variant="h4">Configuration</Typography>
          <Button
            type="submit"
            onClick={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
          >
            Save
          </Button>
        </header>
        <Form {...form}>
          <form className="space-y-8 mb-8">
            <KnowledgeBasesField
              control={form.control}
              knowledgeBases={knowledgeBases}
            />
            <GenerativeModelField control={form.control} />
            <SimilaritySearchField
              control={form.control}
              displayCutoff={displayCutoff}
              setDisplayCutoff={setDisplayCutoff}
            />
            <ColbertRerankField
              control={form.control}
              displayTopN={displayTopN}
              setDisplayTopN={setDisplayTopN}
            />
            <LongContextReorderField control={form.control} />
            <PromptField control={form.control} />
          </form>
        </Form>
      </Card>
    );
}
