export function NavigationLink({ children }: { children: React.ReactNode }) {
  return (
    <div className="my-4">
      <p className="px-4 py-2 border rounded-lg">{children}</p>
    </div>
  );
}
