import React from "react";
import { cn } from "@/lib/utils";

interface TypographyProps {
  variant?:
    | "h1"
    | "h2"
    | "h3"
    | "h4"
    | "p"
    | "blockquote"
    | "lead"
    | "large"
    | "small"
    | "muted";
  children: React.ReactNode;
  className?: string;
}

export function Typography({ variant, children, className }: TypographyProps) {
  const baseStyles = "text-foreground";

  const variantStyles = {
    h1: "scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl",
    h2: "scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0",
    h3: "scroll-m-20 text-2xl font-semibold tracking-tight",
    h4: "scroll-m-20 text-xl font-semibold tracking-tight first:mt-6",
    p: "leading-7 [&:not(:first-child)]:mt-6",
    blockquote: "mt-6 border-l-2 pl-6 italic",
    lead: "text-xl text-muted-foreground",
    large: "text-lg font-semibold",
    small: "text-sm font-medium leading-none",
    muted: "text-sm text-muted-foreground",
  };

  let Component: keyof React.JSX.IntrinsicElements;

  if (variant === "p") {
    Component = "p";
  } else if (variant?.startsWith("h")) {
    Component = variant as keyof React.JSX.IntrinsicElements;
  } else {
    Component = "div";
  }

  if (variant) {
    return (
      <Component className={cn(baseStyles, variantStyles[variant], className)}>
        {children}
      </Component>
    );
  }

  return (
    <Component className={cn(baseStyles, className)}>{children}</Component>
  );
}
