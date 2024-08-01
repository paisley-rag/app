import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
} from "../ui/form";
import { Switch } from "../ui/switch";
import { Control } from "react-hook-form";
import { z } from "zod";
import { pipelineConfigSchema } from "../../service/service";

type LongContextReorderFieldProps = {
  control: Control<z.infer<typeof pipelineConfigSchema>>;
};

export function LongContextReorderField({
  control,
}: LongContextReorderFieldProps) {
  return (
    <FormField
      control={control}
      name="long_context_reorder.on"
      render={({ field }) => (
        <FormItem className="flex flex-row items-center justify-between">
          <div className="space-y-0.5">
            <FormLabel>Long Context Reorder</FormLabel>
            <FormDescription>
              Enable long context reordering for improved context handling.
            </FormDescription>
          </div>
          <FormControl>
            <Switch checked={field.value} onCheckedChange={field.onChange} />
          </FormControl>
        </FormItem>
      )}
    />
  );
}
