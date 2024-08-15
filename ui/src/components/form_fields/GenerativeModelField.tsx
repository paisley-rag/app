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
import { ClientPipelineConfig } from "@/services/chatbot-service";

type GenerativeModelFieldProps = {
  control: Control<ClientPipelineConfig>;
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
              <SelectItem value="gpt-4-turbo">gpt-4-turbo</SelectItem>
                <SelectItem value="gpt-4o-mini">gpt-4o-mini</SelectItem>
                <SelectItem value="gpt-4o">gpt-4o</SelectItem>
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
