import service from "../../service/service";
import { useQuery } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { Typography } from "../Typography";
import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { ModalFileUpload } from "../ModalFileUpload";

export function PageKnowledgeBase({ id }: { id: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["knowledge-base", id],
    queryFn: () => service.fetchFilesByKnolwedgeBaseId(id),
  });
  const [, setLocation] = useLocation();
  const [modalVisible, setModalVisible] = useState(false);

  function handleBackClick(e: React.SyntheticEvent) {
    e.preventDefault();
    setLocation("/knowledge-bases/");
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error loading knowledge base</div>;
  }

  return (
    <>
      <div className="mb-8">
        <Button variant="ghost" onClick={handleBackClick}>
          Back
        </Button>
        <Typography variant="h2">Knowledge Base Details</Typography>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Typography variant="h4">Ingest Method:</Typography>
            <Typography variant="p">{data[0].ingest_method}</Typography>
          </div>
          <div>
            <Typography variant="h4">Splitter:</Typography>
            <Typography variant="p">{data[0].splitter}</Typography>
          </div>
          <div>
            <Typography variant="h4">Embed Model:</Typography>
            <Typography variant="p">{data[0].embed_model}</Typography>
          </div>
          <div>
            <Typography variant="h4">Chunk Size:</Typography>
            <Typography variant="p">{data[0].chunk_size}</Typography>
          </div>
          <div>
            <Typography variant="h4">Chunk Overlap:</Typography>
            <Typography variant="p">{data[0].chunk_overlap}</Typography>
          </div>
          <div>
            <Typography variant="h4">Separator:</Typography>
            <Typography variant="p">{data[0].separator}</Typography>
          </div>
          <div>
            <Typography variant="h4">LLM:</Typography>
            <Typography variant="p">{data[0].llm || "N/A"}</Typography>
          </div>
        </div>
      </div>

      <header className="flex items-center justify-between">
        <Typography variant="h3">Files</Typography>
        <Button onClick={() => setModalVisible(true)}>Upload File</Button>
      </header>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>File Name</TableHead>
            <TableHead>File Type</TableHead>
            <TableHead>Source</TableHead>
            <TableHead>Date</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data[0].files.map((file) => (
            <TableRow key={file.id}>
              <TableCell>{file.name}</TableCell>
              <TableCell>{file.file_type}</TableCell>
              <TableCell>{file.source}</TableCell>
              <TableCell>{file.date}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {modalVisible && <ModalFileUpload setModalVisible={setModalVisible} />}
    </>
  );
}
