import { Typography } from "../Typography";
import { Button } from "../ui/button";
import { Link } from "wouter";
import { useState } from "react";
import { ModalKnowledgeBase } from "../ModalKnowledgeBase";
import { useQuery } from "@tanstack/react-query";
import { knowledgeBaseService } from "@/services/knowledge-base-service";

export function PageKnowledgeBases() {
  const [modalVisible, setModalVisible] = useState(false);

  function handleNewKnowledgeBaseClick() {
    setModalVisible(true);
  }

  const { data, isLoading } = useQuery({
    queryKey: ["knowledge-bases"],
    queryFn: knowledgeBaseService.fetchKnowledgeBases,
  });

  if (isLoading) return <div>Loading...</div>;
  if (data)
    return (
      <>
        <div className="flex justify-between items-baseline mb-8">
          <Typography variant="h3">Knowledge Bases</Typography>
          <Button variant="default" onClick={handleNewKnowledgeBaseClick}>
            Create new knowledge base
          </Button>
        </div>
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <div className="grid grid-cols-3 gap-8">
            {data.map((knowledgeBase) => (
              <Link
                href={`/knowledge-bases/${knowledgeBase.id}`}
                key={knowledgeBase.id}
              >
                <div className="bg-gray-100 p-4 rounded-md">
                  {knowledgeBase.kb_name}
                </div>
              </Link>
            ))}
          </div>
        )}
        {modalVisible && (
          <ModalKnowledgeBase setModalVisible={setModalVisible} />
        )}
      </>
    );
}
