import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "../ui/form";
import { Textarea } from "../ui/textarea";
import { Control } from "react-hook-form";
import { z } from "zod";
import { pipelineConfigSchema } from "../../service/service";

type PromptFieldProps = {
  control: Control<z.infer<typeof pipelineConfigSchema>>;
};

export function PromptField({ control }: PromptFieldProps) {
  return (
    <FormField
      control={control}
      name="prompt"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Prompt</FormLabel>
          <FormControl>
            <Textarea
              placeholder="Enter your prompt here..."
              className="resize-vertical"
              {...field}
            />
          </FormControl>
          <FormDescription>
            The prompt to be used for generating responses.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
