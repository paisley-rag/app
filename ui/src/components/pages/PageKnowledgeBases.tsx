import { Typography } from "../Typography";
import { Button } from "../ui/button";
import { Link } from "wouter";
import { useState } from "react";
import { SkeletonPageKnowledgeBase } from "../skeletons/SkeletonPageKnowledgeBases";
import { ModalKnowledgeBase } from "../ModalKnowledgeBase";
import { useQuery } from "@tanstack/react-query";
import {
  knowledgeBaseService,
  ServerKnowledgeBaseConfig,
} from "@/services/knowledge-base-service";
import { ErrorMessageWithReload } from "../ErrorMessageWithReload";

export function PageKnowledgeBases() {
  const [modalVisible, setModalVisible] = useState(false);

  function handleNewKnowledgeBaseClick() {
    setModalVisible(true);
  }

  const { data, isLoading, isError } = useQuery({
    queryKey: ["knowledge-bases"],
    queryFn: knowledgeBaseService.fetchKnowledgeBases,
  });

  if (isLoading) return <SkeletonPageKnowledgeBase />;

  if (isError) {
    return <ErrorMessageWithReload />;
  }

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
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.map((knowledgeBase: ServerKnowledgeBaseConfig) => (
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
