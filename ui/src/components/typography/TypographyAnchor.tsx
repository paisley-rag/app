export function TypographyAnchor({ children }: { children: React.ReactNode }) {
  return (
    <a
      href="#"
      className="font-medium text-primary underline underline-offset-4"
    >
      {children}
    </a>
  );
}
