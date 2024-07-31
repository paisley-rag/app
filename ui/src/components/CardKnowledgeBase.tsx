import { Link } from "wouter";

export function CardKnowledgeBase({ card }) {
  return (
    <Link href={`/knowledge-bases/${card.id}`} key={card.id}>
      <div className="bg-gray-100 p-4 rounded-md">{card.name}</div>
    </Link>
  );
}
