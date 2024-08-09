import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "../ui/form";
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuCheckboxItem,
} from "../ui/dropdown-menu";
import { Control } from "react-hook-form";
import { ClientPipelineConfig } from "../../services/chatbot-service";
import { ServerKnowledgeBaseConfig } from "../../services/knowledge-base-service";
import React from "react";

type KnowledgeBasesDropdownFieldProps = {
  control: Control<ClientPipelineConfig>;
  knowledgeBases: ServerKnowledgeBaseConfig[];
};

export function KnowledgeBasesDropdownField({
  control,
  knowledgeBases,
}: KnowledgeBasesDropdownFieldProps) {
  return (
    <FormField
      control={control}
      name="knowledge_bases"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Knowledge Bases</FormLabel>
          <FormControl>
            <div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline">
                    {field.value?.length ?? 0} knowledge base(s) selected
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56">
                  <DropdownMenuLabel>Knowledge Bases</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  {knowledgeBases.map((kb) => (
                    <DropdownMenuCheckboxItem
                      key={kb.id}
                      checked={field.value?.includes(kb.id)}
                      onCheckedChange={(checked: boolean) => {
                        const updatedValue = checked
                          ? [...(field.value ?? []), kb.id]
                          : (field.value ?? []).filter((id) => id !== kb.id);
                        field.onChange(updatedValue);
                      }}
                      onSelect={(e: React.SyntheticEvent) => e.preventDefault()}
                    >
                      {kb.kb_name}
                    </DropdownMenuCheckboxItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </FormControl>
          <FormDescription>
            The knowledge base(s) that the chatbot will reference to generate
            responses.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
