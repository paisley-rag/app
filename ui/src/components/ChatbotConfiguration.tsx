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

interface ChatbotConfigurationProps {
  chatbot: ServerPipelineConfig;
  knowledgeBases: ServerKnowledgeBaseConfig[];
}

export function ChatbotConfiguration({
  chatbot,
  knowledgeBases,
}: ChatbotConfigurationProps) {
  const mutation = useMutation({
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

  const handleSubmit = form.handleSubmit(
    (data) => {
      mutation.mutate(data);
    },
    (errors) => {
      console.error("Form submission failed. Errors:", errors);
    }
  );

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
          <KnowledgeBasesDropdownField
            control={form.control}
            knowledgeBases={knowledgeBases}
          />
          <GenerativeModelField control={form.control} />
          <SimilaritySearchField control={form.control} />
          <ColbertRerankField control={form.control} />
          <LongContextReorderField control={form.control} />
          <PromptField control={form.control} />
        </form>
      </Form>
    </Card>
  );
}
