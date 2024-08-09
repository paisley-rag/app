import { Skeleton } from "@/components/ui/skeleton";

export function SkeletonPageChatbots() {
  return (
    <>
      <header className="mb-8 flex items-center gap-2">
        <Skeleton className="h-8 w-48" />
      </header>
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[...Array(6)].map((_, index) => (
          <li key={index}>
            <Skeleton className="h-48 w-full" />
          </li>
        ))}
      </ul>
    </>
  );
}
