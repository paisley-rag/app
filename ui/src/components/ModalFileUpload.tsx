import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction } from "react";
import { Overlay } from "./Overlay";

interface ModalFileUploadProps {
  setModalVisible: Dispatch<SetStateAction<boolean>>;
}

export function ModalFileUpload({ setModalVisible }: ModalFileUploadProps) {
  function handleCancelClick() {
    setModalVisible(false);
  }

  async function handleFormSubmit(e: React.SyntheticEvent) {
    // needs to send formdata to FileUpload api
    e.preventDefault();
    console.log(e.target);
  }

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
          {
            // need to update all forms with shadcn-ui forms for upload functionality
          }
          <form onSubmit={handleFormSubmit}>
            <div className="grid w-full items-center gap-4">
              <Label htmlFor="file">File</Label>
              <Input id="file" type="file" />
            </div>
            <div className="mt-4 flex justify-between">
              <Button variant="secondary" onClick={handleCancelClick}>
                Cancel
              </Button>
              <Button>Create</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </>
  );
}
