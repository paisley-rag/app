import { Link } from "wouter";

interface NavigationLinkProps {
  href: string;
  children: React.ReactNode;
}

export function NavigationLink({ href, children }: NavigationLinkProps) {
  return (
    <Link
      className="flex items-center gap-2 px-2 py-2 rounded-md hover:bg-gray-100"
      href={href}
    >
      {children}
    </Link>
  );
}
