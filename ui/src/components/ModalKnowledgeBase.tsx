import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction } from "react";
import { Overlay } from "./Overlay";

interface ModalKnowledgeBaseProps {
  setModalVisible: Dispatch<SetStateAction<boolean>>;
}

export function ModalKnowledgeBase({
  setModalVisible,
}: ModalKnowledgeBaseProps) {
  function handleOverlayClick(e: React.SyntheticEvent) {
    e.stopPropagation();
    setModalVisible(false);
  }

  function handleCancelClick() {
    setModalVisible(false);
  }

  async function handleFormSubmit(e: React.SyntheticEvent) {
    // needs to send formdata to KnowledgeBase api
    e.preventDefault();
    console.log(e.target);
  }

  return (
    <>
      <Overlay handleOverlayClick={handleOverlayClick} />
      <Card className="min-w-0.5 max-w-2xl fixed top-1/2 -translate-x-1/2 -translate-y-1/2 left-1/2 z-20">
        <CardHeader>
          <CardTitle>Create new knowledge base</CardTitle>
          <CardDescription>
            Select the chunking strategies for the files that you'll upload into
            this knowledge base.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleFormSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="name">Name</Label>
                <Input id="name" placeholder="Name of your knowledge base" />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="embed_model">Embedding Model</Label>
                <Select>
                  <SelectTrigger id="embed_model">
                    <SelectValue placeholder="Select" />
                  </SelectTrigger>
                  <SelectContent position="popper">
                    <SelectItem value="text-embedding-ada-002">
                      text-embedding-ada-002
                    </SelectItem>
                    <SelectItem value="option-2">Option 2</SelectItem>
                    <SelectItem value="option-3">Option 3</SelectItem>
                    <SelectItem value="option-4">Option 4</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex flex-row grow gap-4">
                <div className="flex flex-col space-y-1.5 basis-1/2">
                  <Label htmlFor="chunk_size">Chunk Size</Label>
                  <Input id="chunk_size" placeholder="256" type="number" />
                </div>
                <div className="flex flex-col space-y-1.5 basis-1/2">
                  <Label htmlFor="chunk_overlap">Chunk Overlap</Label>
                  <Input id="chunk_overlap" placeholder="32" type="number" />
                </div>
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="separator">Separator</Label>
                <Input id="separator" type="text" />
              </div>
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
