import { useState, useRef, useEffect } from "react";
import { PhaseTimeline } from "./PhaseTimeline";
import { ChatMessage } from "./ChatMessage";
import { AgeSelectionCards } from "./AgeSelectionCards";
import { InputBar } from "./InputBar";

interface Message {
  id: string;
  type: "ai" | "user";
  content: string;
  showAgeCards?: boolean;
}

const initialPhases = [
  { id: "greeting", label: "Greeting", status: "complete" as const },
  { id: "age", label: "Age", status: "complete" as const },
  { id: "childhood", label: "Childhood", status: "active" as const },
  { id: "adolescence", label: "Adolescence", status: "inactive" as const },
  { id: "adulthood", label: "Adulthood", status: "inactive" as const },
  { id: "synthesis", label: "Synthesis", status: "inactive" as const },
];

const initialMessages: Message[] = [
  {
    id: "1",
    type: "ai",
    content: "Welcome! I'm here to help you tell your life story chronologically. This will be a journey through your memories, capturing the moments that shaped who you are. Ready to begin?",
  },
  {
    id: "2",
    type: "user",
    content: "Yes, I am.",
  },
  {
    id: "3",
    type: "ai",
    content: "Great! To customize the interview and tailor our conversation to your life experiences, please select your age range:",
    showAgeCards: true,
  },
  {
    id: "4",
    type: "user",
    content: "31-45",
  },
  {
    id: "5",
    type: "ai",
    content: "Perfect. Let's start with your childhood — those formative years that often hold our most vivid memories. What is your earliest memory of home? It could be a place, a feeling, or even a specific moment.",
  },
];

interface ChatAreaProps {
  sendMessage: any;
  storyId: number | undefined;
}

export function ChatArea({ sendMessage, storyId }: ChatAreaProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [selectedAge, setSelectedAge] = useState<string>("31-45");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, sendMessage.isPending]);

  const handleSendMessage = async (content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content,
    };
    setMessages((prev) => [...prev, newMessage]);

    try {
      const response = await sendMessage.mutateAsync({ message: content });
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: response.response,
      };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (error) {
      console.error("Failed to send message:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: "Sorry, I couldn't process your message. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleAgeSelect = (age: string) => {
    setSelectedAge(age);
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-background">
      <PhaseTimeline phases={initialPhases} currentStep={2} totalSteps={5} />

      <div className="flex-1 overflow-y-auto px-6 py-6 scrollbar-thin">
        <div className="max-w-3xl mx-auto flex flex-col gap-4">
          {messages.map((message) => (
            <div key={message.id} className="flex flex-col gap-3">
              <ChatMessage type={message.type} content={message.content} />
              {message.showAgeCards && (
                <AgeSelectionCards onSelect={handleAgeSelect} selectedAge={selectedAge} />
              )}
            </div>
          ))}
          {sendMessage.isPending && <ChatMessage type="ai" content="" isTyping />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <InputBar onSend={handleSendMessage} disabled={sendMessage.isPending} />
    </div>
  );
}
