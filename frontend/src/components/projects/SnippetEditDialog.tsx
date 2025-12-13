import { useState, useEffect } from "react";
import { Loader2, Pencil, Check } from "lucide-react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import type { Snippet, UpdateSnippetDto } from "@/hooks/useProjects";

const MAX_CONTENT_LENGTH = 300;
const MAX_TITLE_LENGTH = 200;

/**
 * Theme options with display names and gradient previews
 */
const themeOptions = [
    { value: "family", label: "Family", gradient: "from-orange-400 via-rose-400 to-red-400" },
    { value: "growth", label: "Growth", gradient: "from-emerald-400 via-teal-400 to-cyan-400" },
    { value: "challenge", label: "Challenge", gradient: "from-violet-400 via-purple-400 to-indigo-400" },
    { value: "adventure", label: "Adventure", gradient: "from-amber-400 via-orange-400 to-yellow-400" },
    { value: "love", label: "Love", gradient: "from-pink-400 via-rose-400 to-red-300" },
    { value: "legacy", label: "Legacy", gradient: "from-amber-500 via-yellow-400 to-orange-400" },
    { value: "identity", label: "Identity", gradient: "from-indigo-400 via-violet-400 to-purple-400" },
    { value: "friendship", label: "Friendship", gradient: "from-sky-400 via-blue-400 to-indigo-400" },
];

/**
 * Phase options with display names
 */
const phaseOptions = [
    { value: "FAMILY_HISTORY", label: "Family History" },
    { value: "CHILDHOOD", label: "Childhood" },
    { value: "ADOLESCENCE", label: "Adolescence" },
    { value: "EARLY_ADULTHOOD", label: "Early Adulthood" },
    { value: "MIDLIFE", label: "Midlife" },
    { value: "PRESENT", label: "Present Day" },
];

interface SnippetEditDialogProps {
    snippet: Snippet | null;
    isOpen: boolean;
    onClose: () => void;
    onSave: (data: UpdateSnippetDto) => void;
    isSaving?: boolean;
}

/**
 * Dialog for editing snippet card details.
 * 
 * Features:
 * - Edit title and content with character limits
 * - Theme selector with gradient color preview
 * - Phase selector
 * - Live character counter with warning state
 * - Real-time preview of card appearance
 */
export function SnippetEditDialog({
    snippet,
    isOpen,
    onClose,
    onSave,
    isSaving = false,
}: SnippetEditDialogProps) {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [theme, setTheme] = useState("");
    const [phase, setPhase] = useState("");

    // Reset form when snippet changes
    useEffect(() => {
        if (snippet) {
            setTitle(snippet.title || "");
            setContent(snippet.content || "");
            setTheme(snippet.theme || "growth");
            setPhase(snippet.phase || "PRESENT");
        }
    }, [snippet]);

    const handleSave = () => {
        const updates: UpdateSnippetDto = {};

        if (title !== snippet?.title) updates.title = title;
        if (content !== snippet?.content) updates.content = content;
        if (theme !== snippet?.theme) updates.theme = theme;
        if (phase !== snippet?.phase) updates.phase = phase;

        // Only save if there are actual changes
        if (Object.keys(updates).length > 0) {
            onSave(updates);
        } else {
            onClose();
        }
    };

    const contentLength = content.length;
    const isOverLimit = contentLength > MAX_CONTENT_LENGTH;
    const isNearLimit = contentLength > MAX_CONTENT_LENGTH * 0.9;

    const selectedTheme = themeOptions.find(t => t.value === theme);

    if (!snippet) return null;

    return (
        <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="sm:max-w-[600px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Pencil className="w-5 h-5 text-primary" />
                        Edit Card
                    </DialogTitle>
                    <DialogDescription>
                        Customize your story card's content and appearance.
                    </DialogDescription>
                </DialogHeader>

                <div className="grid gap-6 py-4">
                    {/* Title Field */}
                    <div className="space-y-2">
                        <Label htmlFor="title">Title</Label>
                        <Input
                            id="title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value.slice(0, MAX_TITLE_LENGTH))}
                            placeholder="Enter a catchy title..."
                            className="font-medium"
                        />
                        <p className="text-xs text-muted-foreground text-right">
                            {title.length}/{MAX_TITLE_LENGTH}
                        </p>
                    </div>

                    {/* Content Field */}
                    <div className="space-y-2">
                        <Label htmlFor="content">Content</Label>
                        <Textarea
                            id="content"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            placeholder="Write the snippet text (max 300 characters)..."
                            className="min-h-[120px] resize-none"
                            rows={4}
                        />
                        <p className={cn(
                            "text-xs text-right transition-colors",
                            isOverLimit ? "text-destructive font-medium" :
                                isNearLimit ? "text-amber-500" :
                                    "text-muted-foreground"
                        )}>
                            {contentLength}/{MAX_CONTENT_LENGTH}
                            {isOverLimit && " — Content will be trimmed"}
                        </p>
                    </div>

                    {/* Theme and Phase Row */}
                    <div className="grid grid-cols-2 gap-4">
                        {/* Theme Selector */}
                        <div className="space-y-2">
                            <Label>Theme</Label>
                            <Select value={theme} onValueChange={setTheme}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select theme" />
                                </SelectTrigger>
                                <SelectContent>
                                    {themeOptions.map((opt) => (
                                        <SelectItem key={opt.value} value={opt.value}>
                                            <div className="flex items-center gap-2">
                                                <div className={cn(
                                                    "w-4 h-4 rounded-full bg-gradient-to-r",
                                                    opt.gradient
                                                )} />
                                                {opt.label}
                                            </div>
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Phase Selector */}
                        <div className="space-y-2">
                            <Label>Life Phase</Label>
                            <Select value={phase} onValueChange={setPhase}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select phase" />
                                </SelectTrigger>
                                <SelectContent>
                                    {phaseOptions.map((opt) => (
                                        <SelectItem key={opt.value} value={opt.value}>
                                            {opt.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    {/* Live Preview Card */}
                    <div className="space-y-2">
                        <Label className="text-muted-foreground">Preview</Label>
                        <div className={cn(
                            "relative overflow-hidden rounded-xl p-4",
                            "bg-gradient-to-br min-h-[100px]",
                            selectedTheme?.gradient || "from-slate-400 to-gray-400"
                        )}>
                            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                            <div className="relative z-10 flex flex-col justify-end h-full min-h-[80px]">
                                <h3 className="text-base font-bold text-white leading-tight mb-1">
                                    {title || "Card Title"}
                                </h3>
                                <p className="text-sm text-white/90 line-clamp-2">
                                    {content || "Card content will appear here..."}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <DialogFooter className="gap-2">
                    <Button
                        variant="outline"
                        onClick={onClose}
                        disabled={isSaving}
                    >
                        Cancel
                    </Button>
                    <Button
                        onClick={handleSave}
                        disabled={isSaving || isOverLimit || !title.trim() || !content.trim()}
                    >
                        {isSaving ? (
                            <>
                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                Saving...
                            </>
                        ) : (
                            <>
                                <Check className="w-4 h-4 mr-2" />
                                Save Changes
                            </>
                        )}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
