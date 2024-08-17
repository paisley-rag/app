import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction, useState } from "react";
import { Overlay } from "./Overlay";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { useMutation } from "@tanstack/react-query";
import { knowledgeBaseService } from "@/services/knowledge-base-service";

interface ModalFileUploadProps {
  setModalVisible: Dispatch<SetStateAction<boolean>>;
  id: string;
}

const formSchema = z.object({
  file: z.instanceof(File).refine((file) => file.size <= 25000000, {
    message: "File size must be less than 25MB.",
  }),
});

export function ModalFileUpload({ setModalVisible, id }: ModalFileUploadProps) {
  const [loadingStatus, setLoadingStatus] = useState<string | null>(null);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });

  function handleCancelClick() {
    setModalVisible(false);
  }

  function onSubmit(values: z.infer<typeof formSchema>) {
    setLoadingStatus("File loading, please wait...");
    uploadMutation.mutate(values.file);
  }

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      return await knowledgeBaseService.uploadFile(id, file);
    },
    onSuccess: async () => {
      await new Promise((resolve) => setTimeout(resolve, 0)); // Ensures synchronous execution
      setModalVisible(false);
    },
    onError: (error) => {
      setLoadingStatus("Error uploading file");
      console.error("Error uploading file:", error);
    },
  });

  return (
    <>
      <Overlay setModalVisible={setModalVisible} />
      <Card className="min-w-0.5 max-w-2xl fixed top-1/2 -translate-x-1/2 -translate-y-1/2 left-1/2 z-20">
        <CardHeader>
          <CardTitle>Upload a file</CardTitle>
          <CardDescription>
            Upload a file to the knowledge base for your chatbot to reference.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <FormField
                control={form.control}
                name="file"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>File</FormLabel>
                    <FormControl>
                      <Input
                        type="file"
                        onChange={(e) => field.onChange(e.target.files?.[0])}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="flex justify-between">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={handleCancelClick}
                >
                  Cancel
                </Button>
                <Button type="submit">Upload</Button>
              </div>
              {loadingStatus && <p>{loadingStatus}</p>}
            </form>
          </Form>
        </CardContent>
      </Card>
    </>
  );
}
