import Logo from "../assets/paisley-logo-icon.svg";
import { Link } from "wouter";
import { NavigationLink } from "./NavigationLink";

const PRIMARY_NAV_LINKS = [
  { href: "/dashboard", text: "Dashboard" },
  { href: "/knowledge-bases", text: "Knowledge Bases" },
  { href: "/chatbots", text: "Chatbots" },
  { href: "/evaluations", text: "Evaluations" },
];

const SECONDARY_NAV_LINKS = [
  { href: "/api-keys", text: "API Keys" },
  { href: "/settings", text: "Settings" },
];

export function Navigation() {
  return (
    <div className="flex flex-col justify-between fixed h-full w-72 bg-white z-10 px-12 py-8 border-r-2">
      <nav>
        <img src={Logo} alt="Paisley Logo" className="size-12" />
        {PRIMARY_NAV_LINKS.map((link) => (
          <Link key={link.href} href={link.href}>
            <NavigationLink>{link.text}</NavigationLink>
          </Link>
        ))}
      </nav>
      <nav>
        {SECONDARY_NAV_LINKS.map((link) => (
          <Link key={link.href} href={link.href}>
            <NavigationLink>{link.text}</NavigationLink>
          </Link>
        ))}
      </nav>
    </div>
  );
}
