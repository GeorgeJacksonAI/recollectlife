import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface Phase {
  id: string;
  label: string;
  status: "complete" | "active" | "inactive";
}

interface PhaseTimelineProps {
  phases: Phase[];
  currentStep: number;
  totalSteps: number;
}

export function PhaseTimeline({ phases, currentStep, totalSteps }: PhaseTimelineProps) {
  return (
    <div className="px-6 py-5 border-b border-border bg-card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-medium text-foreground">Chapter 1: Childhood</h2>
        <span className="text-base text-muted-foreground">
          Step {currentStep} of {totalSteps}
        </span>
      </div>
      
      <div className="flex items-center gap-2">
        {phases.map((phase, index) => (
          <div key={phase.id} className="flex items-center flex-1">
            <div className="flex flex-col items-center flex-1">
              <div
                className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all",
                  phase.status === "complete" && "bg-timeline-complete text-primary-foreground",
                  phase.status === "active" && "bg-timeline-active text-primary-foreground ring-4 ring-primary/20",
                  phase.status === "inactive" && "bg-timeline-inactive text-muted-foreground"
                )}
              >
                {phase.status === "complete" ? (
                  <Check className="w-5 h-5" />
                ) : (
                  index + 1
                )}
              </div>
              <span
                className={cn(
                  "text-sm mt-2 text-center",
                  phase.status === "active" ? "text-foreground font-medium" : "text-muted-foreground"
                )}
              >
                {phase.label}
              </span>
            </div>
            
            {index < phases.length - 1 && (
              <div
                className={cn(
                  "h-1 flex-1 mx-2 rounded-full transition-colors",
                  phase.status === "complete" ? "bg-timeline-complete" : "bg-timeline-inactive"
                )}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
