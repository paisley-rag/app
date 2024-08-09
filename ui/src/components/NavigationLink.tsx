import { Link, useLocation } from "wouter";
import { ReactNode } from "react";

interface NavigationLinkProps {
  href: string;
  children: ReactNode;
  activePattern?: RegExp;
}

export function NavigationLink({
  href,
  children,
  activePattern,
}: NavigationLinkProps) {
  const [location] = useLocation();
  const isActive = activePattern
    ? activePattern.test(location)
    : location === href;

  return (
    <Link
      href={href}
      className={`flex items-center gap-2 px-2 py-2 rounded-md hover:bg-gray-100 ${
        isActive ? "bg-gray-100 text-blue-500" : "text-gray-700"
      }`}
    >
      {children}
    </Link>
  );
}
