import { useState } from "react";
import { Send, Mic } from "lucide-react";
import { cn } from "@/lib/utils";

interface InputBarProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function InputBar({ onSend, disabled }: InputBarProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  return (
    <div className="p-5 border-t border-border bg-card">
      <form onSubmit={handleSubmit} className="flex items-end gap-4">
        <div className="flex-1">
          <div
            className={cn(
              "flex items-end bg-background rounded-xl border border-border transition-all",
              "input-glow focus-within:border-primary"
            )}
          >
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your response here..."
              disabled={disabled}
              rows={1}
              className={cn(
                "flex-1 bg-transparent px-5 py-4 text-lg text-foreground placeholder:text-muted-foreground",
                "resize-none focus:outline-none max-h-40 scrollbar-thin",
                "disabled:opacity-50 disabled:cursor-not-allowed"
              )}
              style={{ minHeight: "56px" }}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="button"
              className="p-4 text-muted-foreground hover:text-foreground transition-colors"
              title="Voice input (coming soon)"
            >
              <Mic className="w-6 h-6" />
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={!message.trim() || disabled}
          className={cn(
            "w-14 h-14 rounded-xl flex items-center justify-center transition-all",
            "bg-primary text-primary-foreground",
            "hover:bg-primary/90",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
        >
          <Send className="w-6 h-6" />
        </button>
      </form>

      <p className="text-sm text-muted-foreground text-center mt-4">
        Take your time. There's no rush.
      </p>
    </div>
  );
}
