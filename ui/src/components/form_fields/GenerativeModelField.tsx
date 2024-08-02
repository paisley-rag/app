import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "../ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Control } from "react-hook-form";
import { z } from "zod";
import { pipelineConfigSchema } from "../../service/service";

type GenerativeModelFieldProps = {
  control: Control<z.infer<typeof pipelineConfigSchema>>;
};

export function GenerativeModelField({ control }: GenerativeModelFieldProps) {
  return (
    <FormField
      control={control}
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
                <SelectItem value="gpt-3.5-turbo">gpt-3.5-turbo</SelectItem>
                <SelectItem value="option-2">Option 2</SelectItem>
                <SelectItem value="option-3">Option 3</SelectItem>
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>
            The model that is provided context and generates the response.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
