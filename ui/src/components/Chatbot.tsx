import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Typography } from "./Typography";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { queryService } from "../services/query-service";

interface ChatbotProps {
  id: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function Chatbot({ id }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello, how can I help you?" },
  ]);
  const [input, setInput] = useState("");

  const mutation = useMutation({
    mutationFn: (message: string) => queryService.sendMessage(id, message),
    onSuccess: (data) => {
      const assistantMessage: Message = {
        role: "assistant",
        content: data.body,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    },
    onError: (error) => {
      console.error("Error sending message:", error);
    },
  });

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const newMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    mutation.mutate(input);
  };

  return (
    <div className="flex flex-col h-[75vh]">
      <div className="flex-grow mb-4 overflow-hidden">
        <Card className="h-full flex flex-col">
          <ScrollArea className="flex-grow">
            <div className="p-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`mb-4 flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[75%] ${
                      message.role === "user" ? "ml-auto" : ""
                    }`}
                  >
                    <Card
                      className={`py-2 px-4 ${
                        message.role === "user" ? "bg-blue-100" : "bg-gray-100"
                      }`}
                    >
                      <Typography variant="p" className="text-left">
                        {message.content}
                      </Typography>
                    </Card>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </Card>
      </div>
      <div className="flex space-x-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message here..."
          className="flex-grow"
        />
        <Button onClick={sendMessage}>Send</Button>
      </div>
    </div>
  );
}
