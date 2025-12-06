import { Link } from "react-router-dom";
import { BookOpen, ArrowRight, Feather, Clock, Heart } from "lucide-react";
import { cn } from "@/lib/utils";

const features = [
  {
    icon: Feather,
    title: "Simple Conversations",
    description: "Answer questions at your own pace. No complicated technology — just a friendly conversation.",
  },
  {
    icon: Clock,
    title: "Your Life, Your Time",
    description: "Start from your earliest memories and journey forward. Take breaks whenever you need.",
  },
  {
    icon: Heart,
    title: "A Gift for Family",
    description: "Create something meaningful that your children and grandchildren will treasure forever.",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-card">
        <div className="max-w-4xl mx-auto px-6 h-20 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <BookOpen className="w-7 h-7 text-primary" />
            <span className="text-xl font-semibold text-foreground font-story">Life Story</span>
          </Link>
          <div className="flex items-center gap-6">
            <Link
              to="/auth"
              className="text-lg text-muted-foreground hover:text-foreground transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/auth"
              className={cn(
                "px-6 py-3 rounded-lg text-lg font-medium transition-colors",
                "bg-primary text-primary-foreground hover:bg-primary/90"
              )}
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-story font-semibold text-foreground leading-tight mb-8">
            Your Story Matters.
            <br />
            <span className="text-primary">Let's Write It Together.</span>
          </h1>

          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-12 leading-relaxed">
            A gentle guide to help you capture your life's memories, 
            one conversation at a time. Simple, meaningful, and made for you.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/auth"
              className={cn(
                "px-8 py-4 rounded-lg font-medium text-xl transition-colors",
                "bg-primary text-primary-foreground hover:bg-primary/90",
                "flex items-center gap-3"
              )}
            >
              Begin Your Story
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Divider */}
      <div className="max-w-xl mx-auto px-6">
        <hr className="border-border" />
      </div>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-story font-semibold text-foreground text-center mb-4">
            How It Works
          </h2>
          <p className="text-lg text-muted-foreground text-center mb-16 max-w-xl mx-auto">
            We ask the questions. You share your memories. It's that simple.
          </p>

          <div className="grid md:grid-cols-3 gap-10">
            {features.map((feature, index) => (
              <div key={feature.title} className="text-center">
                <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mx-auto mb-6">
                  <feature.icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonial Section */}
      <section className="py-16 px-6 bg-secondary/50">
        <div className="max-w-2xl mx-auto text-center">
          <blockquote className="text-2xl font-story italic text-foreground mb-6 leading-relaxed">
            "This helped me remember stories I thought I'd forgotten. 
            My grandchildren now know where they come from."
          </blockquote>
          <p className="text-lg text-muted-foreground">
            — Margaret, age 72
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-story font-semibold text-foreground mb-6">
            Ready to Begin?
          </h2>
          <p className="text-lg text-muted-foreground mb-10">
            Every life has stories worth preserving. Start yours today — it's free.
          </p>
          <Link
            to="/auth"
            className={cn(
              "inline-flex items-center gap-3 px-8 py-4 rounded-lg font-medium text-xl transition-colors",
              "bg-primary text-primary-foreground hover:bg-primary/90"
            )}
          >
            Create Your Account
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-10 px-6 border-t border-border">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <BookOpen className="w-5 h-5 text-primary" />
            <span className="text-muted-foreground">
              © 2024 Life Story
            </span>
          </div>
          <div className="flex items-center gap-8 text-muted-foreground">
            <a href="#" className="hover:text-foreground transition-colors">Privacy</a>
            <a href="#" className="hover:text-foreground transition-colors">Terms</a>
            <a href="#" className="hover:text-foreground transition-colors">Help</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
