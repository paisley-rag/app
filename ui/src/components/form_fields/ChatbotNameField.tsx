import { Control } from "react-hook-form";
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "../ui/form";
import { Input } from "../ui/input";
import { ClientPipelineConfig } from "@/services/chatbot-service";

interface ChatbotNameFieldProps {
  control: Control<ClientPipelineConfig>;
}

export function ChatbotNameField({ control }: ChatbotNameFieldProps) {
  return (
    <FormField
      control={control}
      name="name"
      render={({ field }) => (
        <FormItem className="w-1/2">
          <FormLabel>Chatbot Name</FormLabel>
          <FormControl>
            <Input
              type="text"
              placeholder="Enter chatbot name"
              {...field}
              className="input"
            />
          </FormControl>
          <FormDescription>The name of your chatbot.</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
