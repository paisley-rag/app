import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
  SelectLabel,
  SelectSeparator,
  SelectGroup,
} from "@/components/ui/select";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";

import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction } from "react";
import { Overlay } from "./Overlay";
import {
  ClientKnowledgeBaseConfig,
  clientKnowledgeBaseConfigSchema,
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
import { zodResolver } from "@hookform/resolvers/zod";
import { RefreshCw } from "lucide-react";
import { useLocation } from "wouter";
import { ApiKeyContext } from '../providers/ApiKeyProvider.tsx';
import { useContext } from 'react';

interface ModalKnowledgeBaseProps {
  setModalVisible: Dispatch<SetStateAction<boolean>>;
}

export function ModalKnowledgeBase({
  setModalVisible,
}: ModalKnowledgeBaseProps) {
  const { apiKey } = useContext(ApiKeyContext);
  const form = useForm<ClientKnowledgeBaseConfig>({
    resolver: zodResolver(clientKnowledgeBaseConfigSchema),
    defaultValues: {
      kb_name: "",
    },
  });

  const [, setLocation] = useLocation();

  const { mutate, isPending } = useMutation({
    mutationFn: (data: ClientKnowledgeBaseConfig) =>
      knowledgeBaseService.createKnowledgeBase(data, apiKey),

    onSuccess: (data: ServerKnowledgeBaseConfig) => {
      setModalVisible(false);
      setLocation(`/knowledge-bases/${data.id}`);
    },
  });

  function handleCancelClick() {
    setModalVisible(false);
  }

  const handleSubmit = form.handleSubmit(
    (data) => {
      console.log(form.getValues());
      console.log(data);
      mutate(data);
    },
    (error) => {
      console.log(error);
    }
  );

  return (
    <>
      <Overlay setModalVisible={setModalVisible} />
      <Card className="min-w-0.5 max-w-2xl fixed top-1/2 -translate-x-1/2 -translate-y-1/2 left-1/2 z-20">
        <CardHeader>
          <CardTitle>Create new knowledge base</CardTitle>
          <CardDescription>
            Select the chunking strategies for the files that you'll upload into
            this knowledge base.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form className="space-y-6" onSubmit={handleSubmit}>
              <FormField
                name="kb_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Knowledge Base Name</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="Enter knowledge base name"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                name="ingest_method"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Ingestion Method</FormLabel>
                    <Select
                      onValueChange={(value: string) => {
                        field.onChange(value);
                        form.resetField("splitter");
                      }}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select ingestion method" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="LlamaParse">LlamaParse</SelectItem>
                        <SelectItem value="Simple">Simple</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                name="splitter"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Splitter</FormLabel>
                    <Select
                      onValueChange={(value: string) => {
                        field.onChange(value);
                        form.resetField("splitter_config");
                        if (value === "Markdown") {
                          form.setValue("splitter_config.num_workers", 8);
                        } else if (value === "Semantic") {
                          form.setValue("splitter_config.buffer_size", 100);
                          form.setValue(
                            "splitter_config.breakpoint_percentile_threshold",
                            95
                          );
                        } else {
                          form.setValue("splitter_config.chunk_size", 1024);
                          form.setValue("splitter_config.chunk_overlap", 200);
                        }
                      }}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select splitter" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {form.getValues("ingest_method") === "LlamaParse" ? (
                          <SelectItem value="Markdown">Markdown</SelectItem>
                        ) : (
                          <>
                            <SelectItem value="Sentence">Sentence</SelectItem>
                            <SelectItem value="Semantic">Semantic</SelectItem>
                          </>
                        )}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                name="splitter_config"
                render={() => {
                  const splitterValue = form.watch("splitter");

                  return (
                    <FormItem>
                      {splitterValue === "Markdown" ? (
                        <FormField
                          name="splitter_config.num_workers"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Number of Workers</FormLabel>
                              <FormControl>
                                <Input
                                  type="number"
                                  {...field}
                                  onChange={(e) =>
                                    field.onChange(Number(e.target.value))
                                  }
                                  placeholder="Enter number of workers"
                                />
                              </FormControl>
                            </FormItem>
                          )}
                        />
                      ) : (
                        <>
                          {splitterValue === "Semantic" && (
                            <>
                              <FormField
                                name="splitter_config.buffer_size"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Buffer Size</FormLabel>
                                    <FormControl>
                                      <Input
                                        type="number"
                                        {...field}
                                        onChange={(e) =>
                                          field.onChange(Number(e.target.value))
                                        }
                                      />
                                    </FormControl>
                                  </FormItem>
                                )}
                              />
                              <FormField
                                name="splitter_config.breakpoint_percentile_threshold"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>
                                      Breakpoint Percentile Threshold
                                    </FormLabel>
                                    <FormControl>
                                      <Input
                                        type="number"
                                        {...field}
                                        onChange={(e) =>
                                          field.onChange(Number(e.target.value))
                                        }
                                      />
                                    </FormControl>
                                  </FormItem>
                                )}
                              />
                            </>
                          )}
                          {splitterValue === "Sentence" && (
                            <>
                              <FormField
                                name="splitter_config.chunk_size"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Chunk Size</FormLabel>
                                    <FormControl>
                                      <Input
                                        type="number"
                                        {...field}
                                        onChange={(e) =>
                                          field.onChange(Number(e.target.value))
                                        }
                                      />
                                    </FormControl>
                                  </FormItem>
                                )}
                              />
                              <FormField
                                name="splitter_config.chunk_overlap"
                                render={({ field }) => (
                                  <FormItem>
                                    <FormLabel>Chunk Overlap</FormLabel>
                                    <FormControl>
                                      <Input
                                        type="number"
                                        {...field}
                                        onChange={(e) =>
                                          field.onChange(Number(e.target.value))
                                        }
                                      />
                                    </FormControl>
                                  </FormItem>
                                )}
                              />
                            </>
                          )}
                        </>
                      )}
                      <FormMessage />
                    </FormItem>
                  );
                }}
              />
              <FormField
                name="embed_config.embed_model"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Embed Model</FormLabel>
                    {/* temp, have to change this to use embed_model to somehow update embed_provider that's not dependent on the embed_model name */}
                    <Select
                      onValueChange={(value: string) => {
                        field.onChange(value);
                        const embedProvider = value.startsWith("text")
                          ? "OpenAI"
                          : "Cohere";
                        form.setValue(
                          "embed_config.embed_provider",
                          embedProvider
                        );
                      }}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select embed model" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectGroup>
                          <SelectLabel>OpenAI Models</SelectLabel>
                          <SelectItem value="text-embedding-3-small">
                            text-embedding-3-small
                          </SelectItem>
                          <SelectItem value="text-embedding-3-large">
                            text-embedding-3-large
                          </SelectItem>
                        </SelectGroup>
                        <SelectSeparator />
                        <SelectGroup>
                          <SelectLabel>Cohere Models</SelectLabel>
                          <SelectItem value="embed-english-light-v3.0">
                            embed-english-light-v3.0
                          </SelectItem>
                          <SelectItem value="embed-english-v3.0">
                            embed-english-v3.0
                          </SelectItem>
                          <SelectItem value="embed-multilingual-light-v3.0">
                            embed-multilingual-light-v3.0
                          </SelectItem>
                          <SelectItem value="embed-multilingual-v3.0">
                            embed-multilingual-v3.0
                          </SelectItem>
                        </SelectGroup>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              {form.watch("ingest_method") === "LlamaParse" && (
                <FormField
                  name="llm_config"
                  render={() => {
                    return (
                      <FormItem>
                        <FormField
                          name="llm_config.llm_model"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>LLM Model</FormLabel>
                              <Select
                                onValueChange={(value: string) => {
                                  field.onChange(value);
                                  form.setValue(
                                    "llm_config.llm_provider",
                                    value.startsWith("gpt")
                                      ? "OpenAI"
                                      : "Anthropic"
                                  );
                                }}
                                defaultValue={field.value}
                              >
                                <FormControl>
                                  <SelectTrigger>
                                    <SelectValue placeholder="Select LLM model" />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectGroup>
                                    <SelectLabel>OpenAI Models</SelectLabel>
                                    <SelectItem value="gpt-3.5-turbo">
                                      gpt-3.5-turbo
                                    </SelectItem>
                                    <SelectItem value="gpt-4-turbo">
                                      gpt-4-turbo
                                    </SelectItem>
                                    <SelectItem value="gpt-4o-mini">
                                      gpt-4o-mini
                                    </SelectItem>
                                    <SelectItem value="gpt-4o">
                                      gpt-4o
                                    </SelectItem>
                                  </SelectGroup>
                                  <SelectSeparator />
                                  <SelectGroup>
                                    <SelectLabel>Anthropic Models</SelectLabel>
                                    <SelectItem value="claude-4-haiku-20240307">
                                      claude-4-haiku-20240307
                                    </SelectItem>
                                    <SelectItem value="claude-3-sonnet-20240229">
                                      claude-3-sonnet-20240229
                                    </SelectItem>
                                    <SelectItem value="claude-3-5-sonnet-20240620">
                                      claude-3-5-sonnet-20240620
                                    </SelectItem>
                                  </SelectGroup>
                                </SelectContent>
                              </Select>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </FormItem>
                    );
                  }}
                />
              )}
              <div className="flex justify-end space-x-4">
                <Button variant="outline" onClick={handleCancelClick}>
                  Cancel
                </Button>
                {isPending ? (
                  <Button disabled>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Creating...
                  </Button>
                ) : (
                  <Button type="submit">Create</Button>
                )}
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </>
  );
}
