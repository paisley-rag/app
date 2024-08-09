import Logo from "../assets/paisley-logo-icon.svg";
import { NavigationLink } from "./NavigationLink";
import { Typography } from "./Typography";
import {
  LayoutDashboard,
  BookOpenText,
  BotMessageSquare,
  ChartCandlestick,
  KeyRound,
  Settings,
} from "lucide-react";

export function Navigation() {
  return (
    <div className="flex flex-col justify-start gap-8 fixed h-full w-60 bg-white z-10 p-6 border-r">
      <div className="flex items-center gap-3 pb-4 border-b">
        <img src={Logo} alt="Paisley Logo" className="size-8" />
        <Typography className="text-xl font-semibold font-inter">
          Paisley
        </Typography>
      </div>
      <nav className="flex flex-col gap-2">
        <Typography variant="muted" className="px-2">
          Main Menu
        </Typography>
        <NavigationLink href="/dashboard">
          <LayoutDashboard />
          <Typography className="text-base">Dashboard</Typography>
        </NavigationLink>
        <NavigationLink href="/knowledge-bases">
          <BookOpenText />
          <Typography className="text-base">Knowledge Bases</Typography>
        </NavigationLink>
        <NavigationLink href="/chatbots">
          <BotMessageSquare />
          <Typography className="text-base">Chatbots</Typography>
        </NavigationLink>
        <NavigationLink href="/evaluations">
          <ChartCandlestick />
          <Typography className="text-base">Evaluations</Typography>
        </NavigationLink>
      </nav>
      <nav className="flex flex-col gap-2">
        <Typography variant="muted" className="px-2">
          Account
        </Typography>
        <NavigationLink href="/api-keys">
          <KeyRound />
          <Typography className="text-base">API Keys</Typography>
        </NavigationLink>
        <NavigationLink href="/settings">
          <Settings />
          <Typography className="text-base">Settings</Typography>
        </NavigationLink>
      </nav>
    </div>
  );
}
