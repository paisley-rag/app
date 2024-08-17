import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useMutation } from "@tanstack/react-query";

import { zodResolver } from "@hookform/resolvers/zod";

import {
  clientPipelineConfigSchema,
  ServerPipelineConfig,
} from "../services/chatbot-service";
import { chatbotService } from "../services/chatbot-service";
import { ClientPipelineConfig } from "../services/chatbot-service";

import { Typography } from "./Typography";
import { Card } from "./ui/card";
import { Form } from "./ui/form";
import { Button } from "./ui/button";

import { KnowledgeBasesDropdownField } from "./form_fields/KnowledgeBasesDropdownField";
import { GenerativeModelField } from "./form_fields/GenerativeModelField";
import { SimilaritySearchField } from "./form_fields/SimilaritySearchField";
import { ColbertRerankField } from "./form_fields/ColbertRerankField";
import { LongContextReorderField } from "./form_fields/LongContextReorderField";
import { PromptField } from "./form_fields/PromptField";

import { ServerKnowledgeBaseConfig } from "../services/knowledge-base-service";
import { RotateCw } from "lucide-react";

interface ChatbotConfigurationProps {
  chatbot: ServerPipelineConfig;
  knowledgeBases: ServerKnowledgeBaseConfig[];
  onDeleteClick: (id: string) => void;
}

export function ChatbotConfiguration({
  chatbot,
  knowledgeBases,
  onDeleteClick,
}: ChatbotConfigurationProps) {
  const { mutate, isPending } = useMutation({
    mutationFn: (data: ClientPipelineConfig) =>
      chatbotService.updateChatbot(chatbot.id, data),
  });

  const form = useForm<ClientPipelineConfig>({
    resolver: zodResolver(clientPipelineConfigSchema),
  });

  useEffect(() => {
    if (chatbot) {
      form.reset(chatbot);
    }
  }, [chatbot, form]);

  const handleSubmit = form.handleSubmit((data) => {
    mutate(data);
  });

  return (
    <Card className="h-full flex flex-col px-6">
      <header className="flex justify-between items-baseline">
        <Typography variant="h4">Configuration</Typography>
        {isPending ? (
          <Button disabled>
            <RotateCw className="w-4 h-4 mr-2 animate-spin" />
            Saving...
          </Button>
        ) : (
          <Button
            type="submit"
            onClick={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
          >
            Save
          </Button>
        )}
      </header>
      <Form {...form}>
        <form className="space-y-8 mb-8">
          <KnowledgeBasesDropdownField
            control={form.control}
            knowledgeBases={knowledgeBases}
          />
          <GenerativeModelField control={form.control} />
          <SimilaritySearchField control={form.control} />
          <ColbertRerankField control={form.control} />
          <LongContextReorderField control={form.control} />
          <PromptField control={form.control} />
          <Button variant="destructive" onClick={() => onDeleteClick(chatbot.id)}>
            Delete Chatbot
          </Button>
        </form>
      </Form>
    </Card>
  );
}
