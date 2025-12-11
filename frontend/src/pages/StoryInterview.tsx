import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, BookOpen, Feather } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatArea } from "@/components/chat/ChatArea";
import { ChapterSummaryDrawer } from "@/components/chat/ChapterSummaryDrawer";
import { useStory, useCreateStory } from "@/hooks/useStories";
import { useSendMessage } from "@/hooks/useChat";

export default function StoryInterview() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isCreatingStory, setIsCreatingStory] = useState(false);

  const { data: story, isLoading } = useStory(id ? parseInt(id) : undefined);
  const sendMessage = useSendMessage(id ? parseInt(id) : undefined);
  const createStory = useCreateStory();

  // Auto-create story when id === "new"
  useEffect(() => {
    if (id === "new" && !isCreatingStory && !createStory.isPending) {
      setIsCreatingStory(true);
      createStory.mutateAsync({
        title: "My Life Story",
      }).then((newStory) => {
        // Navigate to the newly created story
        navigate(`/story/${newStory.id}`, { replace: true });
      }).catch((error) => {
        console.error("Failed to create story:", error);
        setIsCreatingStory(false);
      });
    }
  }, [id, isCreatingStory, createStory, navigate]);

  if (isLoading || (id === "new" && (isCreatingStory || createStory.isPending))) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-lg text-muted-foreground">
          {id === "new" ? "Creating your story..." : "Loading story..."}
        </p>
      </div>
    );
  }

  if (!story && id !== "new") {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-lg text-destructive">Story not found</p>
      </div>
    );
  }

  const mockSnippets: any[] = [];

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
            <span className="font-story text-lg text-foreground">
              {story?.title || "New Story"}
            </span>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden">
        <ChatArea sendMessage={sendMessage} storyId={id ? parseInt(id) : undefined} />
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
