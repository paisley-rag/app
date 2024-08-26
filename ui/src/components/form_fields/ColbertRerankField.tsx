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
import { Control, useWatch } from "react-hook-form";
import { ClientPipelineConfig } from "../../services/chatbot-service";

type ColbertRerankFieldProps = {
  control: Control<ClientPipelineConfig>;
};

export function ColbertRerankField({ control }: ColbertRerankFieldProps) {
  const colbertRerankOn = useWatch({
    control,
    name: "colbert_rerank.on",
  });

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
                onCheckedChange={(checked: boolean) => {
                  field.onChange(checked);
                }}
              />
            </FormControl>
          </FormItem>
        )}
      />
      {colbertRerankOn && (
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
                Set the number of top results return after rerank.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
      )}
    </>
  );
}
