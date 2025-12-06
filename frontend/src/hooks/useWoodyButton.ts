import { useCallback } from 'react';

/**
 * Hook to add woody forest button effects with leaf animations
 */
export const useWoodyButton = () => {
    const handleWoodyClick = useCallback((event: React.MouseEvent<HTMLElement>) => {
        const button = event.currentTarget;
        const rect = button.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Create 5-8 leaves that float upward
        const leafCount = Math.floor(Math.random() * 4) + 5;

        for (let i = 0; i < leafCount; i++) {
            const leaf = document.createElement('div');
            leaf.className = 'leaf';

            // Random horizontal spread
            const xOffset = (Math.random() - 0.5) * 80;
            leaf.style.setProperty('--leaf-x', `${xOffset}px`);

            // Position at click location
            leaf.style.left = `${x}px`;
            leaf.style.top = `${y}px`;

            // Slight delay for each leaf
            leaf.style.animationDelay = `${i * 0.05}s`;

            button.appendChild(leaf);

            // Trigger animation
            setTimeout(() => {
                leaf.classList.add('animate');
            }, 10);

            // Remove after animation
            setTimeout(() => {
                leaf.remove();
            }, 1300);
        }
    }, []);

    return { handleWoodyClick };
};
