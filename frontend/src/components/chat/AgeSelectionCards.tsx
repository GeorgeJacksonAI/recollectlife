import { cn } from "@/lib/utils";

interface AgeSelectionCardsProps {
  onSelect: (age: string) => void;
  selectedAge?: string;
}

const ageRanges = [
  { id: "under-18", label: "Under 18" },
  { id: "18-30", label: "18 – 30" },
  { id: "31-45", label: "31 – 45" },
  { id: "46-60", label: "46 – 60" },
  { id: "61+", label: "61 and over" },
];

export function AgeSelectionCards({ onSelect, selectedAge }: AgeSelectionCardsProps) {
  return (
    <div className="self-start max-w-full message-appear">
      <div className="flex flex-wrap gap-3 p-5 bg-bubble-ai rounded-2xl rounded-tl-md">
        <p className="w-full text-lg text-foreground mb-2">Please select your age range:</p>
        {ageRanges.map((age) => (
          <button
            key={age.id}
            onClick={() => onSelect(age.label)}
            className={cn(
              "px-6 py-4 rounded-xl border-2 text-lg font-medium transition-all",
              "hover:border-primary hover:bg-primary/5",
              "focus:outline-none focus:ring-2 focus:ring-primary/30",
              selectedAge === age.label
                ? "border-primary bg-primary/10 text-foreground"
                : "border-border bg-card text-foreground"
            )}
          >
            {age.label}
          </button>
        ))}
      </div>
    </div>
  );
}
