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
import { z } from "zod";
import { pipelineConfigSchema } from "../../service/service";

type KnowledgeBasesFieldProps = {
  control: Control<z.infer<typeof pipelineConfigSchema>>;
  knowledgeBases: z.infer<typeof pipelineConfigSchema>[];
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
                      checked={field.value?.includes(kb.name)}
                      onCheckedChange={(checked) => {
                        const updatedValue = checked
                          ? [...(field.value ?? []), kb.name]
                          : (field.value ?? []).filter(
                              (name) => name !== kb.name
                            );
                        field.onChange(updatedValue);
                      }}
                      onSelect={(e) => e.preventDefault()}
                    >
                      {kb.name}
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
