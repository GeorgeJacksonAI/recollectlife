import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, BookOpen, Feather } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatArea } from "@/components/chat/ChatArea";
import { ChapterSummaryDrawer } from "@/components/chat/ChapterSummaryDrawer";

// Mock story snippets
const mockSnippets = [
  {
    id: "1",
    chapter: "Childhood",
    content:
      "I grew up in a small farmhouse on the outskirts of town. The mornings were always filled with the sound of roosters and the smell of my mother's fresh bread baking in the wood-fired oven.",
    timestamp: "Just now",
  },
  {
    id: "2",
    chapter: "Childhood",
    content:
      "My father was a carpenter. I remember watching him work in his workshop for hours, the sawdust floating in the afternoon light like tiny golden specks.",
    timestamp: "2 min ago",
  },
  {
    id: "3",
    chapter: "Childhood",
    content:
      "We had a big oak tree in the backyard where my siblings and I would climb and pretend we were explorers discovering new lands.",
    timestamp: "5 min ago",
  },
];

export default function StoryInterview() {
  const navigate = useNavigate();
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  return (
    <div className="flex flex-col h-screen w-full overflow-hidden bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-4 flex items-center gap-4">
        <Button
          variant="ghost"
          onClick={() => navigate("/dashboard")}
          className="h-11 px-4 text-base"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Stories
        </Button>

        <div className="flex items-center gap-3 ml-auto">
          <Button
            variant="outline"
            onClick={() => setIsDrawerOpen(true)}
            className="h-11 px-4 text-base"
          >
            <Feather className="w-5 h-5 mr-2" />
            View Story
          </Button>
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-primary" />
            <span className="font-story text-lg text-foreground">New Story</span>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden">
        <ChatArea />
      </div>

      {/* Chapter Summary Drawer */}
      <ChapterSummaryDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        snippets={mockSnippets}
      />
    </div>
  );
}
