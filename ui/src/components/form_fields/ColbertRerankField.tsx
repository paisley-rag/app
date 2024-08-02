import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
} from "../ui/form";
import { Switch } from "../ui/switch";
import { Input } from "../ui/input";
import { Control } from "react-hook-form";
import { ClientPipelineConfig } from "../../services/chatbot-service";

type ColbertRerankFieldProps = {
  control: Control<ClientPipelineConfig>;
  displayTopN: boolean;
  setDisplayTopN: (value: boolean) => void;
};

export function ColbertRerankField({
  control,
  displayTopN,
  setDisplayTopN,
}: ColbertRerankFieldProps) {
  return (
    <>
      <FormField
        control={control}
        name="colbert_rerank.on"
        render={({ field }) => (
          <FormItem className="flex flex-row items-center justify-between">
            <div className="space-y-0.5">
              <FormLabel>Colbert Rerank</FormLabel>
              <FormDescription>
                Enable Colbert reranking for improved context retrieval.
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
      {displayTopN && (
        <FormField
          control={control}
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
      )}
    </>
  );
}
