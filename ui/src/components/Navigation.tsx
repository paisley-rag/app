import Logo from "../assets/paisley-logo-icon.svg";
import { NavigationLink } from "./NavigationLink";
import { Typography } from "./Typography";
import {
  // LayoutDashboard,
  BookOpenText,
  BotMessageSquare,
  ScrollText,
  // KeyRound,
  // Settings,
  ChartLine,
} from "lucide-react";


export function Navigation() {
  return (
    <div className="flex flex-col justify-start gap-8 fixed h-full w-60 bg-white z-10 p-6 border-r">
      <div className="flex items-center gap-3 pb-5 border-b">
        <img src={Logo} alt="Paisley Logo" className="size-8" />
        <Typography className="text-xl font-semibold font-inter">
          Paisley
        </Typography>
      </div>
      <nav className="flex flex-col gap-2">
        <Typography variant="muted" className="px-2">
          Menu
        </Typography>
        {/* <NavigationLink href="/dashboard">
          <LayoutDashboard />
          <p className="text-base">Dashboard</p>
        </NavigationLink> */}
        <NavigationLink
          href="/knowledge-bases"
          activePattern={/\/knowledge-bases/}
        >
          <BookOpenText />
          <p className="text-base">Knowledge Bases</p>
        </NavigationLink>
        <NavigationLink href="/chatbots" activePattern={/\/chatbots/}>
          <BotMessageSquare />
          <p className="text-base">Chatbots</p>
        </NavigationLink>
        <NavigationLink href="/history">
          <ScrollText />
          <p className="text-base">History</p>
        </NavigationLink>
        <NavigationLink href="/metrics">
          <ChartLine />
          <p className="text-base">Metrics</p>
        </NavigationLink>
      </nav>
      {/* <nav className="flex flex-col gap-2">
        <Typography variant="muted" className="px-2">
          Account
        </Typography>
        <NavigationLink href="/api-keys">
          <KeyRound />
          <p className="text-base">API Keys</p>
        </NavigationLink>
        <NavigationLink href="/settings">
          <Settings />
          <p className="text-base">Settings</p>
        </NavigationLink>
      </nav> */}
    </div>
  );
}
