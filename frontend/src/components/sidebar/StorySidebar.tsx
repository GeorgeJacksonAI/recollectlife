import { useState } from "react";
import { Plus, Settings, BookOpen, ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

interface Story {
  id: string;
  title: string;
  date: string;
  status: "in-progress" | "completed";
}

const mockStories: Story[] = [
  { id: "1", title: "My Life Story", date: "Dec 2, 2024", status: "in-progress" },
  { id: "2", title: "Dad's Memories", date: "Nov 28, 2024", status: "completed" },
  { id: "3", title: "Grandma's Early Years", date: "Nov 15, 2024", status: "completed" },
];

interface StorySidebarProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

export function StorySidebar({ isCollapsed, onToggle }: StorySidebarProps) {
  const [activeStory, setActiveStory] = useState("1");

  return (
    <aside
      className={cn(
        "h-full bg-sidebar border-r border-sidebar-border flex flex-col shrink-0 transition-all duration-300",
        isCollapsed ? "w-20" : "w-72"
      )}
    >
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <Link to="/" className="flex items-center gap-3">
              <BookOpen className="w-6 h-6 text-primary" />
              <span className="text-lg font-semibold text-sidebar-foreground font-story">Life Story</span>
            </Link>
          )}
          <button
            onClick={onToggle}
            className="p-3 rounded-lg hover:bg-sidebar-accent transition-colors text-sidebar-foreground"
          >
            {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          </button>
        </div>

        <button
          className={cn(
            "mt-4 flex items-center justify-center gap-2 rounded-lg transition-colors",
            "bg-primary text-primary-foreground hover:bg-primary/90",
            isCollapsed ? "w-full p-3" : "w-full px-4 py-3 text-lg font-medium"
          )}
        >
          <Plus className="w-5 h-5" />
          {!isCollapsed && "New Story"}
        </button>
      </div>

      {/* Stories List */}
      <div className="flex-1 overflow-y-auto p-3 scrollbar-thin">
        {!isCollapsed && (
          <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider px-3 mb-3">
            My Stories
          </p>
        )}

        <div className="space-y-1">
          {mockStories.map((story) => (
            <button
              key={story.id}
              onClick={() => setActiveStory(story.id)}
              className={cn(
                "w-full flex items-center gap-3 p-3 rounded-lg transition-colors",
                activeStory === story.id
                  ? "bg-sidebar-accent text-sidebar-foreground"
                  : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
              )}
            >
              <BookOpen className="w-5 h-5 shrink-0" />
              {!isCollapsed && (
                <div className="flex-1 text-left min-w-0">
                  <p className="text-base font-medium truncate">{story.title}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-sm text-muted-foreground">{story.date}</span>
                    <span
                      className={cn(
                        "text-xs px-2 py-0.5 rounded-full font-medium",
                        story.status === "completed"
                          ? "bg-timeline-complete/20 text-timeline-complete"
                          : "bg-primary/20 text-primary"
                      )}
                    >
                      {story.status === "completed" ? "Done" : "In Progress"}
                    </span>
                  </div>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium text-lg">
            M
          </div>
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-base font-medium text-sidebar-foreground truncate">Margaret</p>
              <p className="text-sm text-muted-foreground">Free Plan</p>
            </div>
          )}
          <button className="p-2 rounded-lg hover:bg-sidebar-accent transition-colors text-muted-foreground hover:text-sidebar-foreground">
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </div>
    </aside>
  );
}
