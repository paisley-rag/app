import { useEffect, useState } from "react";
import { Typography } from "./Typography";
import { Card } from "./ui/card";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "./ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";

import { DropdownMenuCheckboxItemProps } from "@radix-ui/react-dropdown-menu";

import { Button } from "./ui/button";
import { pipelineConfigSchema } from "../service/service";
import service from "../service/service";

interface ChatbotConfigurationProps {
  id: number;
}

type Checked = DropdownMenuCheckboxItemProps["checked"];

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
          <div className="mt-4">
            <FormField
              control={form.control}
              name="knowledge_bases"
              render={() => (
                <FormItem>
                  <FormLabel>Knowledge Bases</FormLabel>
                  <FormControl>
                    <div>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="outline">
                            {(form.getValues("knowledge_bases") ?? []).length}{" "}
                            knowledge base(s) selected
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-56">
                          <DropdownMenuLabel>Knowledge Bases</DropdownMenuLabel>
                          <DropdownMenuSeparator />
                          {knowledgeBases.map(
                            (kb: z.infer<typeof pipelineConfigSchema>) => (
                              <DropdownMenuCheckboxItem
                                key={kb.id}
                                checked={(
                                  form.getValues("knowledge_bases") ?? []
                                ).includes(kb.name)}
                                onCheckedChange={(checked: Checked) => {
                                  const currentKbs =
                                    form.getValues("knowledge_bases") ?? [];
                                  if (checked) {
                                    form.setValue("knowledge_bases", [
                                      ...currentKbs,
                                      kb.name,
                                    ]);
                                  } else {
                                    form.setValue(
                                      "knowledge_bases",
                                      currentKbs.filter(
                                        (name: string) => name !== kb.name
                                      )
                                    );
                                  }
                                }}
                                onSelect={(e) => e.preventDefault()}
                              >
                                {kb.name}
                              </DropdownMenuCheckboxItem>
                            )
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </FormControl>
                  <FormDescription>
                    The knowledge base(s) that the chatbot will reference to
                    generate responses.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
          <div>
            <FormField
              control={form.control}
              name="generative_model"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Generative Model</FormLabel>
                  <FormControl>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <SelectTrigger>
                        <SelectValue placeholder="Generative Model" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gpt-3.5-turbo">
                          gpt-3.5-turbo
                        </SelectItem>
                        <SelectItem value="option-2">Option 2</SelectItem>
                        <SelectItem value="option-3">Option 3</SelectItem>
                      </SelectContent>
                    </Select>
                  </FormControl>
                  <FormDescription>
                    The model that is provided context and generates the
                    response.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
          <div>
            <FormField
              control={form.control}
              name="similarity.on"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between">
                  <div className="space-y-0.5">
                    <FormLabel>Similarity Search</FormLabel>
                    <FormDescription>
                      Enable similarity search for context retrieval.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={(checked) => {
                        field.onChange(checked);
                        setDisplayCutoff(checked);
                      }}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>
          {displayCutoff && (
            <div>
              <FormField
                control={form.control}
                name="similarity.cutoff"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Similarity Cutoff</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        max={1}
                        step={0.01}
                        value={field.value ?? 0}
                        onChange={(e) => field.onChange(e.target.value)}
                      />
                    </FormControl>
                    <FormDescription>
                      Set the similarity cutoff threshold.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          )}
          <div>
            <FormField
              control={form.control}
              name="colbert_rerank.on"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between">
                  <div className="space-y-0.5">
                    <FormLabel>ColBERT Rerank</FormLabel>
                    <FormDescription>
                      Enable ColBERT reranking for improved context retrieval.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={(checked) => {
                        field.onChange(checked);
                        setDisplayTopN(checked);
                      }}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>
          {displayTopN && (
            <div>
              <FormField
                control={form.control}
                name="colbert_rerank.top_n"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Top N</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        value={field.value ?? 0}
                        onChange={(e) => field.onChange(e.target.value)}
                      />
                    </FormControl>
                    <FormDescription>
                      Set the number of top results to rerank.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          )}
          <div>
            <FormField
              control={form.control}
              name="long_context_reorder.on"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between">
                  <div className="space-y-0.5">
                    <FormLabel>Long Context Reorder</FormLabel>
                    <FormDescription>
                      Enable long context reordering for improved context
                      handling.
                    </FormDescription>
                  </div>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
          </div>
        </form>
      </Form>
    </Card>
  );
}
