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

type KnowledgeBasesFieldProps = {
  control: Control<ClientPipelineConfig>;
  knowledgeBases: ServerKnowledgeBaseConfig[];
};

export function KnowledgeBasesField({
  control,
  knowledgeBases,
}: KnowledgeBasesFieldProps) {
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
                      checked={field.value?.includes(kb.kb_name)}
                      onCheckedChange={(checked) => {
                        const updatedValue = checked
                          ? [...(field.value ?? []), kb.kb_name]
                          : (field.value ?? []).filter(
                              (name) => name !== kb.kb_name
                            );
                        field.onChange(updatedValue);
                      }}
                      onSelect={(e) => e.preventDefault()}
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
