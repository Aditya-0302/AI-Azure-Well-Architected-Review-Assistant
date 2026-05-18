"use client";

import { useState } from "react";
import { Bot, Send, UserRound } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { chatMessages } from "@/data/platform";

export function ChatConsole() {
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState(chatMessages);

  function sendMessage() {
    if (!draft.trim()) return;
    setMessages((current) => [
      ...current,
      { role: "user", content: draft.trim(), citation: null },
      {
        role: "assistant",
        content: "I would ground that answer against the current review evidence, tenant policy, and Azure WAF guidance before issuing a recommendation.",
        citation: "Pending retrieval"
      }
    ]);
    setDraft("");
  }

  return (
    <div className="grid min-h-[calc(100vh-8rem)] gap-6 xl:grid-cols-[1fr_320px]">
      <Card className="flex min-h-[640px] flex-col">
        <CardContent className="flex min-h-0 flex-1 flex-col p-0">
          <div className="flex items-center justify-between border-b p-4">
            <div>
              <p className="text-sm font-semibold">Architecture Consulting Session</p>
              <p className="text-xs text-muted-foreground">Enterprise Claims Platform</p>
            </div>
            <Badge variant="success">Grounded</Badge>
          </div>
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.map((message, index) => {
                const assistant = message.role === "assistant";
                return (
                  <div key={`${message.role}-${index}`} className="flex gap-3">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback>{assistant ? <Bot className="h-4 w-4" /> : <UserRound className="h-4 w-4" />}</AvatarFallback>
                    </Avatar>
                    <div className="min-w-0 flex-1 rounded-lg border bg-card p-3">
                      <p className="text-sm leading-6">{message.content}</p>
                      {message.citation && (
                        <p className="mt-2 text-xs text-muted-foreground">Citation: {message.citation}</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>
          <div className="border-t p-4">
            <div className="flex gap-3">
              <Textarea
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                placeholder="Ask about Azure architecture risk, remediation, service choices, or tradeoffs"
                className="min-h-12"
              />
              <Button size="icon" className="h-12 w-12 shrink-0" onClick={sendMessage} aria-label="Send message">
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <aside className="space-y-4">
        {["Security evidence", "Reliability review", "Tenant policy", "Azure WAF guidance"].map((item, index) => (
          <div key={item} className="rounded-lg border bg-card p-4">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-semibold">{item}</p>
              <Badge variant={index < 2 ? "success" : "secondary"}>{index < 2 ? "Active" : "Ready"}</Badge>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">{12 + index * 7} citations available</p>
          </div>
        ))}
      </aside>
    </div>
  );
}

