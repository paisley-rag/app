import { Typography } from "../Typography";
import { Button } from "../ui/button";
import { CardKnowledgeBase } from "../CardKnowledgeBase";
import service from "../../service/service";
import { useState } from "react";
import { ModalKnowledgeBase } from "../ModalKnowledgeBase";
import { useQuery } from "@tanstack/react-query";

export function PageKnowledgeBases() {
  const [modalVisible, setModalVisible] = useState(false);

  function handleNewKnowledgeBaseClick() {
    setModalVisible(true);
  }

  const { data, isLoading } = useQuery({
    queryKey: ["knowledge-bases"],
    queryFn: service.fetchKnowledgeBases,
  });

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
          {data.map((card) => (
            <CardKnowledgeBase key={card.id} card={card} />
          ))}
        </div>
      )}
      {modalVisible && <ModalKnowledgeBase setModalVisible={setModalVisible} />}
    </>
  );
}
