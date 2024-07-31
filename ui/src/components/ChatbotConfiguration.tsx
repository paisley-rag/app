import { useEffect, useState } from "react";
import { Typography } from "./Typography";
import { Card } from "./ui/card";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Form } from "./ui/form";

import { Button } from "./ui/button";
import { pipelineConfigSchema } from "../service/service";
import service from "../service/service";

import { KnowledgeBasesField } from "./form_fields/KnowledgeBasesField";
import { GenerativeModelField } from "./form_fields/GenerativeModelField";
import { SimilaritySearchField } from "./form_fields/SimilaritySearchField";
import { ColbertRerankField } from "./form_fields/ColbertRerankField";
import { LongContextReorderField } from "./form_fields/LongContextReorderField";

interface ChatbotConfigurationProps {
  id: string;
}

export function ChatbotConfiguration({ id }: ChatbotConfigurationProps) {
  const mutation = useMutation({
    mutationFn: (data: z.infer<typeof pipelineConfigSchema>) =>
      service.updateChatbot(id, data),
  });

  const { data: knowledgeBases, isLoading: isKnowledgeBasesLoading } = useQuery(
    {
      queryKey: ["knowledgeBases"],
      queryFn: service.fetchKnowledgeBases,
    }
  );

  const { data: chatbot, isLoading: isChatbotLoading } = useQuery({
    queryKey: ["chatbot", id],
    queryFn: () => service.fetchChatbotById(id),
  });

  const [displayCutoff, setDisplayCutoff] = useState(false);
  const [displayTopN, setDisplayTopN] = useState(false);

  const form = useForm<z.infer<typeof pipelineConfigSchema>>({
    resolver: zodResolver(pipelineConfigSchema),
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
      console.log("Form submitted successfully with data:", data);
      mutation.mutate(data);
    },
    (errors) => {
      console.error("Form submission failed. Errors:", errors);
    }
  );

  if (isKnowledgeBasesLoading || isChatbotLoading) return <div>Loading...</div>;

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
        </form>
      </Form>
    </Card>
  );
}
