import { Button } from "../ui/button";
import { Form } from "../ui/form";
import { KnowledgeBasesDropdownField } from "../form_fields/KnowledgeBasesDropdownField";
import { GenerativeModelField } from "../form_fields/GenerativeModelField";
import { SimilaritySearchField } from "../form_fields/SimilaritySearchField";
import { ColbertRerankField } from "../form_fields/ColbertRerankField";
import { LongContextReorderField } from "../form_fields/LongContextReorderField";
import { PromptField } from "../form_fields/PromptField";
import { ChatbotNameField } from "../form_fields/ChatbotNameField";
import { ErrorMessageWithReload } from "../ErrorMessageWithReload";
import { chatbotService } from "../../services/chatbot-service";
import { useMutation } from "@tanstack/react-query";

import { ArrowLeftIcon } from "lucide-react";
import { useLocation } from "wouter";

import { useQuery } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { knowledgeBaseService } from "../../services/knowledge-base-service";
import { Typography } from "../Typography";
import { clientPipelineConfigSchema } from "@/services/chatbot-service";
import { Skeleton } from "../ui/skeleton";

export function PageCreateChatbot() {
  const form = useForm<z.infer<typeof clientPipelineConfigSchema>>({
    resolver: zodResolver(clientPipelineConfigSchema),
    defaultValues: {
      name: "",
      knowledge_bases: [],
      generative_model: "",
      similarity: {
        on: false,
      },
      colbert_rerank: {
        on: false,
      },
      long_context_reorder: {
        on: false,
      },
      prompt: "",
    },
  });
  const [, navigate] = useLocation();

  const {
    data: knowledgeBases,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["knowledgeBases"],
    queryFn: knowledgeBaseService.fetchKnowledgeBases,
  });

  const mutation = useMutation({
    mutationFn: (data: z.infer<typeof clientPipelineConfigSchema>) =>
      chatbotService.createChatbot(data),
    onMutate: () => {},
    onSuccess: (data) => {
      navigate(`/chatbots/${data.id}`);
    },
    onError: (error) => {
      console.error("Error creating chatbot:", error);
    },
  });

  function handleFormSubmit(
    values: z.infer<typeof clientPipelineConfigSchema>
  ) {
    mutation.mutate(values);
  }

  function handleBackClick() {
    navigate("/chatbots");
  }

  if (isLoading) {
    return (
      <>
        <header className="mb-8 flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={handleBackClick}>
            <ArrowLeftIcon className="h-5 w-5" />
          </Button>
          <Typography variant="h3">Create a new chatbot</Typography>
        </header>
        <Skeleton className="h-12 w-1/2 mb-4" />
        <Skeleton className="h-12 w-1/3 mb-4" />
        <Skeleton className="h-12 w-2/3 mb-4" />
        <Skeleton className="h-12 w-1/4 mb-4" />
        <Skeleton className="h-12 w-3/4 mb-4" />
        <Skeleton className="h-12 w-1/2 mb-4" />
      </>
    );
  }

  if (error) {
    return (
      <>
        <header className="mb-8 flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={handleBackClick}>
            <ArrowLeftIcon className="h-5 w-5" />
          </Button>
          <Typography variant="h3">Create a new chatbot</Typography>
        </header>
        <ErrorMessageWithReload />
      </>
    );
  }

  if (knowledgeBases)
    return (
      <>
        <header className="mb-8 flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={handleBackClick}>
            <ArrowLeftIcon className="h-5 w-5" />
          </Button>
          <Typography variant="h3">Create a new chatbot</Typography>
        </header>
        <Form {...form}>
          <form className="space-y-8 mb-8">
            <ChatbotNameField control={form.control} />
            <KnowledgeBasesDropdownField
              control={form.control}
              knowledgeBases={knowledgeBases}
            />
            <GenerativeModelField control={form.control} />
            <SimilaritySearchField control={form.control} />
            <ColbertRerankField control={form.control} />
            <LongContextReorderField control={form.control} />
            <PromptField control={form.control} />
            <div className="flex justify-end">
              <Button
                type="submit"
                onClick={(e) => {
                  e.preventDefault();
                  form.handleSubmit(handleFormSubmit)();
                }}
              >
                Create
              </Button>
            </div>
          </form>
        </Form>
      </>
    );
}
