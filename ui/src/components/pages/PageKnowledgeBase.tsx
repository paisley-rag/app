import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
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

interface PageKnowledgeBaseProps {
  id: string;
}

export function PageKnowledgeBase({ id }: PageKnowledgeBaseProps) {
  const { data, isLoading, error } = useQuery<ServerKnowledgeBaseConfig>({
    queryKey: ["knowledge-base", id],
    queryFn: () => knowledgeBaseService.fetchKnowledgeBaseById(id),
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

  if (data)
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
              <Typography variant="p">{data.ingestion_method}</Typography>
            </div>
            <div>
              <Typography variant="h4">Splitter:</Typography>
              <Typography variant="p">{data.splitter}</Typography>
            </div>
            <div>
              <Typography variant="h4">Embed Model:</Typography>
              <Typography variant="p">
                {data.embed_config.embed_model}
              </Typography>
            </div>
            {/* TODO: Add more fields, conditional on ingestion method */}
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
            {data.files.map((file) => (
              <TableRow key={file.file_name}>
                <TableCell>{file.file_name}</TableCell>
                <TableCell>{file.content_type}</TableCell>
                <TableCell>{file.date_uploaded}</TableCell>
                <TableCell>{file.time_uploaded}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {modalVisible && <ModalFileUpload setModalVisible={setModalVisible} />}
      </>
    );
}
