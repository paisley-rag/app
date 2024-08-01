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

type SimilaritySearchFieldProps = {
  control: Control<ClientPipelineConfig>;
  displayCutoff: boolean;
  setDisplayCutoff: (value: boolean) => void;
};

export function SimilaritySearchField({
  control,
  displayCutoff,
  setDisplayCutoff,
}: SimilaritySearchFieldProps) {
  return (
    <>
      <FormField
        control={control}
        name="similarity.on"
        render={({ field }) => (
          <FormItem className="flex flex-row items-center justify-between">
            <div className="space-y-0.5">
              <FormLabel>Similarity Search</FormLabel>
              <FormDescription>
                Enable similarity search for context retrieval.
              </FormDescription>
            </div>
            <FormControl>
              <Switch
                checked={field.value}
                onCheckedChange={(checked) => {
                  field.onChange(checked);
                  setDisplayCutoff(checked);
                }}
              />
            </FormControl>
          </FormItem>
        )}
      />
      {displayCutoff && (
        <FormField
          control={control}
          name="similarity.cutoff"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Similarity Cutoff</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min={0}
                  max={1}
                  step={0.01}
                  value={field.value ?? 0}
                  onChange={(e) => field.onChange(e.target.value)}
                />
              </FormControl>
              <FormDescription>
                Set the similarity cutoff threshold.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
      )}
    </>
  );
}
